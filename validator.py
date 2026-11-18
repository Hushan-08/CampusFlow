"""
CampusFlow - Automated Data & Graph Validation Engine
====================================================
Validates all campus landmarks, coordinates, boundaries, graph connectivity,
and ensures zero-highway routing policy for Chandigarh University.
"""

import math
from typing import Dict, Any, List

def haversine_m(c1, c2):
    R = 6371000
    phi1, phi2 = math.radians(c1[0]), math.radians(c2[0])
    dphi = math.radians(c2[0] - c1[0])
    dlam = math.radians(c2[1] - c1[1])
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def validate_campus_data(data: Dict[str, Any], graph=None) -> Dict[str, Any]:
    """
    Runs automated validation across locations, edges, coordinates, and graph integrity.
    Returns a comprehensive validation report dictionary.
    """
    locations = data.get("locations", [])
    paths = data.get("paths", [])
    
    issues = []
    warnings = []
    
    # 1. Check Duplicate Location IDs and Missing Coordinates
    seen_ids = set()
    loc_by_id = {}
    verified_count = 0
    approx_count = 0
    unverified_count = 0
    
    # Campus bounding box: lat 30.762 to 30.774, lng 76.567 to 76.582
    CAMPUS_BOUNDS = {
        "min_lat": 30.7620,
        "max_lat": 30.7740,
        "min_lng": 76.5670,
        "max_lng": 76.5820
    }
    
    for loc in locations:
        loc_id = loc.get("id", "")
        if not loc_id:
            issues.append("Found location with missing or empty ID.")
            continue
        if loc_id in seen_ids:
            issues.append(f"Duplicate location ID detected: '{loc_id}'")
        seen_ids.add(loc_id)
        loc_by_id[loc_id] = loc
        
        coords = loc.get("coordinates", {})
        lat = coords.get("lat")
        lng = coords.get("lng")
        
        if lat is None or lng is None:
            issues.append(f"Location '{loc_id}' ({loc.get('name')}) is missing latitude/longitude coordinates.")
        else:
            # Boundary check
            if not (CAMPUS_BOUNDS["min_lat"] <= lat <= CAMPUS_BOUNDS["max_lat"] and 
                    CAMPUS_BOUNDS["min_lng"] <= lng <= CAMPUS_BOUNDS["max_lng"]):
                issues.append(f"Location '{loc_id}' coordinates ({lat}, {lng}) fall outside valid campus boundary.")
        
        # Verification categorization
        status = loc.get("verification_status", "").lower()
        if "verified" in status:
            verified_count += 1
        elif "approx" in status:
            approx_count += 1
        else:
            unverified_count += 1

    # 2. Duplicate Coordinate Check (detect accidental copy-paste overlaps < 8m apart)
    loc_list = list(loc_by_id.values())
    for i in range(len(loc_list)):
        for j in range(i + 1, len(loc_list)):
            u, v = loc_list[i], loc_list[j]
            c1 = (u["coordinates"]["lat"], u["coordinates"]["lng"])
            c2 = (v["coordinates"]["lat"], v["coordinates"]["lng"])
            dist = haversine_m(c1, c2)
            if dist < 8.0:
                warnings.append(
                    f"Locations '{u['id']}' and '{v['id']}' are only {dist:.1f}m apart (potential coordinate overlap)."
                )

    # 3. Path Validation
    seen_edges = set()
    edge_count = 0
    for p in paths:
        edge_count += 1
        s = p.get("source")
        t = p.get("target")
        dist = p.get("distance", 0)
        
        if s not in loc_by_id:
            issues.append(f"Path references non-existent source location ID: '{s}'")
        if t not in loc_by_id:
            issues.append(f"Path references non-existent target location ID: '{t}'")
            
        edge_key = tuple(sorted([s, t]))
        if edge_key in seen_edges:
            warnings.append(f"Duplicate edge detected between '{s}' and '{t}'.")
        seen_edges.add(edge_key)
        
        # Unrealistic distance check
        if dist < 5:
            issues.append(f"Unrealistic path distance ({dist}m) between '{s}' and '{t}' (too short).")
        elif dist > 1500:
            warnings.append(f"Long internal path distance ({dist}m) between '{s}' and '{t}'.")
            
        # Check NH-5 crossing violation
        # NH-5 highway is situated at lat > 30.7730. If both nodes are near highway and not Gate 1, flag.
        if s in loc_by_id and t in loc_by_id:
            lat_s = loc_by_id[s]["coordinates"]["lat"]
            lat_t = loc_by_id[t]["coordinates"]["lat"]
            if lat_s > 30.7735 and lat_t > 30.7735:
                issues.append(f"Policy violation: Connection between '{s}' and '{t}' traverses external NH-05 highway.")

    # 4. Graph Connectivity Validation
    disconnected_nodes = []
    if graph is not None:
        from algorithms import bfs_traversal
        bfs = bfs_traversal(graph, "main_gate")
        visited_set = set(bfs["traversal_order"])
        for loc_id in loc_by_id:
            if loc_id not in visited_set:
                disconnected_nodes.append(loc_id)
                issues.append(f"Graph node '{loc_id}' ({loc_by_id[loc_id].get('name')}) is disconnected from main campus network.")

    dest_count = sum(1 for loc in locations if loc.get("node_type") != "junction")
    junc_count = sum(1 for loc in locations if loc.get("node_type") == "junction")

    is_valid = len(issues) == 0
    return {
        "is_valid": is_valid,
        "total_locations": len(locations),
        "destination_count": dest_count,
        "junction_count": junc_count,
        "total_paths": len(paths),
        "verified_locations": verified_count,
        "approximate_locations": approx_count,
        "unverified_locations": unverified_count,
        "issues": issues,
        "warnings": warnings,
        "disconnected_nodes": disconnected_nodes
    }
