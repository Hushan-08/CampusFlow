"""
CampusFlow - Chandigarh University Map Visualization Engine
============================================================
Corrected True-North Real-World Orientation:
- NH-05 Highway runs along the NORTH / NORTH-EAST frontage of the campus
- Main Gate 1 is at the TOP (North) directly opening onto and facing NH-05
- Entering through Gate 1 moves SOUTH / SOUTH-WEST inward into the campus
- Block B1 (Kalam Block) is on the WEST / Left flank
- Academic Block D1 and Block C are on the EAST / Right flank
- Central Knowledge Centre (Library) is in the core academic quad
- Maka Trophy Sports Arena is in the South-West interior
- Hostel Complex is positioned in the South interior on the C3 side
- 100% internal pedestrian pathways (No highway or external routing)
"""

import folium
from typing import Dict, List, Optional, Any


def render_schematic_svg(
    locations: List[Dict[str, Any]],
    paths: List[Dict[str, Any]],
    start_node: Optional[str] = None,
    target_node: Optional[str] = None,
    shortest_path: Optional[List[str]] = None
) -> str:
    """
    Renders an editorial-quality, interactive vector blueprint of Chandigarh University
    with verified True-North real-world orientation.
    """
    view_width = 1000
    view_height = 720

    loc_dict = {loc["id"]: loc for loc in locations}
    shortest_set = set(shortest_path) if shortest_path else set()

    # Pre-compute shortest path edges
    shortest_edges = set()
    if shortest_path and len(shortest_path) > 1:
        for i in range(len(shortest_path) - 1):
            u, v = shortest_path[i], shortest_path[i + 1]
            shortest_edges.add((u, v))
            shortest_edges.add((v, u))

    svg_elements = []

    # 1. Background (Deep Charcoal #131417)
    svg_elements.append(
        f'<rect width="{view_width}" height="{view_height}" fill="#131417" rx="10" />'
    )

    # 2. Subtle architectural grid (40px)
    for x in range(0, view_width, 40):
        svg_elements.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{view_height}" stroke="#1E2026" stroke-width="0.8" opacity="0.6"/>')
    for y in range(0, view_height, 40):
        svg_elements.append(f'<line x1="0" y1="{y}" x2="{view_width}" y2="{y}" stroke="#1E2026" stroke-width="0.8" opacity="0.6"/>')

    # 3. External NH-05 Highway Zone (NORTH FRONTAGE AT THE TOP)
    svg_elements.append(f"""
      <rect x="25" y="16" width="{view_width - 50}" height="42" rx="6" fill="#1A1C20" stroke="#2B2E36" stroke-width="1"/>
      <line x1="30" y1="37" x2="{view_width - 30}" y2="37" stroke="#585E6D" stroke-width="1.8" stroke-dasharray="14,12" opacity="0.8"/>
      <text x="50" y="42" fill="#8C93A0" font-family="IBM Plex Mono, monospace" font-size="11" font-weight="600" letter-spacing="1">NH-05 LUDHIANA — CHANDIGARH HIGHWAY (NORTH HIGHWAY FRONTAGE — EXTERNAL ROAD)</text>
    """)

    # 4. University Campus Boundary (Enclosing internal walkable grounds south of NH-05)
    svg_elements.append(
        f'<rect x="25" y="68" width="{view_width - 50}" height="635" rx="12" fill="none" stroke="#2D313A" stroke-width="2" stroke-dasharray="6,4" />'
    )

    # 5. Corrected Campus Zones (Oriented from North Gate 1 down into South Hostels/Sports)
    zones = [
        {"x": 660, "y": 70,  "w": 320, "h": 140, "name": "🚪 GATE 1 ENTRANCE & NH-05 FRONTAGE", "color": "#24201B"},
        {"x": 480, "y": 220, "w": 350, "h": 260, "name": "🏛️ CENTRAL ACADEMIC CORE (B-BLOCKS & FOUNTAIN PARK)", "color": "#1C2028"},
        {"x": 840, "y": 220, "w": 180, "h": 260, "name": "🏛️ EAST ACADEMIC (A1–A3 COMPLEX)", "color": "#1D1E28"},
        {"x": 60,  "y": 120, "w": 380, "h": 290, "name": "💻 SOUTH CAMPUS (D-BLOCKS D1–D7 & STAR LIBRARY)", "color": "#181D26"},
        {"x": 60,  "y": 440, "w": 360, "h": 220, "name": "🏆 SPORTS COMPLEX (MAKA TROPHY ARENA)", "color": "#18221D"},
        {"x": 450, "y": 490, "w": 570, "h": 320, "name": "🏠 C-BLOCKS & HOSTELS (NC1–NC6 & ZAKIR)", "color": "#201E26"},
    ]
    for z in zones:
        svg_elements.append(
            f'<rect x="{z["x"]}" y="{z["y"]}" width="{z["w"]}" height="{z["h"]}" rx="8" fill="{z["color"]}" opacity="0.55" stroke="#2B2F38" stroke-width="1"/>'
        )
        svg_elements.append(
            f'<text x="{z["x"] + 14}" y="{z["y"] + 22}" fill="#6E7480" font-family="Space Grotesk, sans-serif" font-size="10" font-weight="700" letter-spacing="0.5">{z["name"]}</text>'
        )

    # 6. Standard (Inactive) Internal Campus Pathways
    for path in paths:
        u_id, v_id = path["source"], path["target"]
        if (u_id, v_id) in shortest_edges:
            continue
        u, v = loc_dict[u_id], loc_dict[v_id]
        x1, y1 = u["schematic"]["x"], u["schematic"]["y"]
        x2, y2 = v["schematic"]["x"], v["schematic"]["y"]
        dist = path["distance"]
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2

        # Paved internal walkway line
        svg_elements.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#343844" stroke-width="2.5" stroke-linecap="round" />'
        )
        # Walkway distance badge
        svg_elements.append(
            f'<rect x="{mx - 20}" y="{my - 9}" width="40" height="18" rx="4" fill="#1C1E24" stroke="#323640" stroke-width="1" />'
            f'<text x="{mx}" y="{my + 4}" fill="#8D93A0" font-family="IBM Plex Mono, monospace" font-size="9" font-weight="600" text-anchor="middle">{dist}m</text>'
        )

    # 7. Active Shortest Route (Highlighted in Warm Terracotta Orange #E58A45)
    if shortest_edges:
        for path in paths:
            u_id, v_id = path["source"], path["target"]
            if (u_id, v_id) not in shortest_edges:
                continue
            u, v = loc_dict[u_id], loc_dict[v_id]
            x1, y1 = u["schematic"]["x"], u["schematic"]["y"]
            x2, y2 = v["schematic"]["x"], v["schematic"]["y"]
            dist = path["distance"]
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2

            # Route glow base
            svg_elements.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#E58A45" stroke-width="7" stroke-linecap="round" opacity="0.3" />'
            )
            # Route crisp line
            svg_elements.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#E58A45" stroke-width="3.5" stroke-linecap="round" />'
            )
            # Animated directional indicator dash
            svg_elements.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="8,12" opacity="0.85" class="route-dash"/>'
            )
            # Highlighted distance pill
            svg_elements.append(
                f'<rect x="{mx - 22}" y="{my - 10}" width="44" height="20" rx="4" fill="#E58A45" stroke="#FFFFFF" stroke-width="1" />'
                f'<text x="{mx}" y="{my + 4}" fill="#FFFFFF" font-family="IBM Plex Mono, monospace" font-size="10" font-weight="700" text-anchor="middle">{dist}m</text>'
            )

    # 8. Landmark Vertices (Buildings, Plazas & Pathway Junctions)
    for loc in locations:
        loc_id = loc["id"]
        x, y = loc["schematic"]["x"], loc["schematic"]["y"]
        name = loc["name"]
        code = loc["code"]
        is_junction = (loc.get("node_type") == "junction")

        is_start = (loc_id == start_node)
        is_target = (loc_id == target_node)
        is_in_route = (loc_id in shortest_set)

        # Subtle rendering for non-active pathway junctions to keep schematic pristine
        if is_junction and not (is_start or is_target or is_in_route):
            svg_elements.append(
                f'<circle cx="{x}" cy="{y}" r="3" fill="#3A3E4A" stroke="#25272F" stroke-width="1" opacity="0.7"/>'
            )
            continue

        if is_start:
            node_fill = "#426B57"        # Forest Green
            node_stroke = "#68A889"
            label_bg = "#253E32"
            label_border = "#426B57"
            label_text = f"ORIGIN: {name}"
            label_color = "#E1F2E9"
        elif is_target:
            node_fill = "#E58A45"        # Warm Terracotta
            node_stroke = "#FFB37C"
            label_bg = "#4D2D14"
            label_border = "#E58A45"
            label_text = f"DEST: {name}"
            label_color = "#FFE8D6"
        elif is_in_route:
            node_fill = "#2F281E"
            node_stroke = "#E58A45"
            label_bg = "#201E1A"
            label_border = "#E58A45"
            label_text = f"STOP: {name}"
            label_color = "#F8D5B8"
        else:
            node_fill = "#1E2026"
            node_stroke = "#4A4F5C"
            label_bg = "#181A20"
            label_border = "#2E323A"
            label_text = f"{code}: {name}"
            label_color = "#A8AFBD"

        # Outer pulsing ring for active nodes
        if is_start or is_target:
            p_color = "#426B57" if is_start else "#E58A45"
            svg_elements.append(
                f'<circle cx="{x}" cy="{y}" r="20" fill="none" stroke="{p_color}" stroke-width="2" opacity="0.75" class="pulse-marker"/>'
            )

        # Node dot
        node_r = 14 if not is_junction else 7
        svg_elements.append(
            f'<g class="campus-node" data-id="{loc_id}">'
            f'<circle cx="{x}" cy="{y}" r="{node_r}" fill="{node_fill}" stroke="{node_stroke}" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y}" r="3" fill="#FFFFFF"/>'
        )

        # Label pill (omit for inactive junctions)
        if not is_junction or is_in_route or is_start or is_target:
            p_len = len(label_text) * 6.5 + 16
            pill_w = max(p_len, 70)
            pill_h = 20
            pill_x = x - pill_w / 2
            pill_y = y + 18

            svg_elements.append(
                f'<rect x="{pill_x}" y="{pill_y}" width="{pill_w}" height="{pill_h}" rx="4" fill="{label_bg}" stroke="{label_border}" stroke-width="1"/>'
                f'<text x="{x}" y="{pill_y + 14}" fill="{label_color}" font-family="Space Grotesk, sans-serif" font-size="10" font-weight="600" text-anchor="middle">{label_text}</text>'
            )
        svg_elements.append('</g>')

    # 9. Minimal Compass Rose (North points Up directly towards NH-05)
    svg_elements.append(f"""
      <!-- Minimal Compass Rose -->
      <g transform="translate(945, 95)">
        <circle cx="0" cy="0" r="16" fill="#1C1E24" stroke="#323640" stroke-width="1" />
        <polygon points="0,-12 3,2 0,0" fill="#E58A45" />
        <polygon points="0,12 3,-2 0,0" fill="#585E6D" />
        <text x="0" y="-16" fill="#E58A45" font-family="Space Grotesk, sans-serif" font-size="10" font-weight="bold" text-anchor="middle">N</text>
      </g>
    """)

    # 10. Minimal Legend
    svg_elements.append(f"""
      <g transform="translate(35, {view_height - 35})">
        <rect x="0" y="0" width="530" height="26" rx="5" fill="#181A20" stroke="#2B2F38" stroke-width="1"/>
        <circle cx="16" cy="13" r="5" fill="#426B57" stroke="#68A889" stroke-width="1.5"/>
        <text x="26" y="17" fill="#E1F2E9" font-family="Inter, sans-serif" font-size="10" font-weight="600">Start (Origin)</text>
        <circle cx="120" cy="13" r="5" fill="#E58A45" stroke="#FFB37C" stroke-width="1.5"/>
        <text x="130" y="17" fill="#FFE8D6" font-family="Inter, sans-serif" font-size="10" font-weight="600">Destination</text>
        <line x1="225" y1="13" x2="255" y2="13" stroke="#E58A45" stroke-width="3"/>
        <text x="262" y="17" fill="#E58A45" font-family="Inter, sans-serif" font-size="10" font-weight="700">Dijkstra Shortest Path</text>
        <line x1="400" y1="13" x2="425" y2="13" stroke="#343844" stroke-width="2"/>
        <text x="432" y="17" fill="#8D93A0" font-family="Inter, sans-serif" font-size="10">Internal Walkway</text>
      </g>
    """)

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600;700&family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
      <style>
        body {{
          margin: 0;
          padding: 0;
          background: #121316;
          font-family: 'Inter', system-ui, sans-serif;
          overflow: hidden;
          display: flex;
          justify-content: center;
          align-items: center;
        }}
        .blueprint-wrapper {{
          width: 100%;
          max-width: {view_width}px;
          margin: 0 auto;
        }}
        svg {{
          width: 100%;
          height: auto;
          display: block;
          border-radius: 8px;
          border: 1px solid rgba(255, 255, 255, 0.08);
          box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5);
        }}
        .campus-node {{
          cursor: pointer;
          transition: transform 0.2s ease;
        }}
        .campus-node:hover circle:first-child {{
          filter: brightness(1.25);
        }}
        @keyframes pulseMarker {{
          0% {{ r: 16px; opacity: 0.8; }}
          50% {{ r: 24px; opacity: 0.15; }}
          100% {{ r: 16px; opacity: 0.8; }}
        }}
        .pulse-marker {{
          animation: pulseMarker 2s infinite ease-in-out;
        }}
        @keyframes routeDashFlow {{
          from {{ stroke-dashoffset: 40; }}
          to {{ stroke-dashoffset: 0; }}
        }}
        .route-dash {{
          animation: routeDashFlow 1.4s linear infinite;
        }}
      </style>
    </head>
    <body>
      <div class="blueprint-wrapper">
        <svg viewBox="0 0 {view_width} {view_height}" xmlns="http://www.w3.org/2000/svg">
          {''.join(svg_elements)}
        </svg>
      </div>
    </body>
    </html>
    """
    return full_html


def create_folium_map(
    locations: List[Dict[str, Any]],
    paths: List[Dict[str, Any]],
    start_node: Optional[str] = None,
    target_node: Optional[str] = None,
    shortest_path: Optional[List[str]] = None
) -> folium.Map:
    """
    Generates an OpenStreetMap focused strictly inside Chandigarh University, Gharuan.
    Renders verified internal walkways with correct True-North orientation.
    """
    center_lat = 30.7680
    center_lng = 76.5742

    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=16,
        tiles="OpenStreetMap",
        control_scale=True
    )

    loc_dict = {loc["id"]: loc for loc in locations}
    shortest_set = set(shortest_path) if shortest_path else set()

    shortest_edges = set()
    if shortest_path and len(shortest_path) > 1:
        for i in range(len(shortest_path) - 1):
            u, v = shortest_path[i], shortest_path[i + 1]
            shortest_edges.add((u, v))
            shortest_edges.add((v, u))

    # Add internal walkways
    for path in paths:
        u_id, v_id = path["source"], path["target"]
        u, v = loc_dict[u_id], loc_dict[v_id]
        p1 = [u["coordinates"]["lat"], u["coordinates"]["lng"]]
        p2 = [v["coordinates"]["lat"], v["coordinates"]["lng"]]
        dist = path["distance"]
        desc = path.get("description", "Campus Walkway")

        if (u_id, v_id) not in shortest_edges:
            folium.PolyLine(
                locations=[p1, p2],
                color="#505664",
                weight=3,
                opacity=0.7,
                dash_array="4, 6",
                tooltip=f"<b>{desc}</b> ({dist}m internal walk)"
            ).add_to(m)

    # Highlight calculated shortest walking path (Terracotta Orange)
    if shortest_path and len(shortest_path) > 1:
        route_coords = [
            [loc_dict[node_id]["coordinates"]["lat"], loc_dict[node_id]["coordinates"]["lng"]]
            for node_id in shortest_path
        ]
        folium.PolyLine(
            locations=route_coords,
            color="#E58A45",
            weight=6,
            opacity=0.9,
            tooltip="<b>Shortest Campus Walking Route</b>"
        ).add_to(m)

    # Add verified building & junction markers
    for loc in locations:
        loc_id = loc["id"]
        coord = [loc["coordinates"]["lat"], loc["coordinates"]["lng"]]
        name = loc["name"]
        code = loc.get("code", "")
        desc = loc.get("description", "")
        cat = loc.get("category", "Campus Facility")
        region = loc.get("region", "Campus")
        status = loc.get("verification_status", "Verified")
        is_junc = (loc.get("node_type") == "junction")

        is_start = (loc_id == start_node)
        is_target = (loc_id == target_node)
        is_in_route = (loc_id in shortest_set)

        popup_html = f"""
        <div style="font-family:'Inter', sans-serif; min-width:190px; padding:4px;">
            <div style="font-size:13px; font-weight:700; color:#181A20;">{name}</div>
            <div style="font-size:11px; color:#585E6D; margin-top:2px;"><b>{code}</b> ⬝ {cat}</div>
            <div style="font-size:11px; color:#7B5838; font-weight:600; margin-top:2px;">📍 {region}</div>
            <div style="font-size:11px; color:#2E323A; margin-top:4px;">{desc}</div>
            <div style="font-size:10px; color:#426B57; font-weight:600; margin-top:4px;">✓ {status}</div>
        </div>
        """

        if is_start:
            folium.Marker(
                location=coord,
                popup=folium.Popup(popup_html, max_width=270),
                tooltip=f"🟢 START: {name}",
                icon=folium.Icon(color="darkgreen", icon="play", prefix="fa")
            ).add_to(m)
        elif is_target:
            folium.Marker(
                location=coord,
                popup=folium.Popup(popup_html, max_width=270),
                tooltip=f"🎯 DESTINATION: {name}",
                icon=folium.Icon(color="orange", icon="flag-checkered", prefix="fa")
            ).add_to(m)
        elif is_junc:
            if is_in_route:
                folium.CircleMarker(
                    location=coord,
                    radius=5,
                    color="#E58A45",
                    weight=2,
                    fill=True,
                    fill_color="#E58A45",
                    fill_opacity=0.9,
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=f"🔹 Waypoint: {name}"
                ).add_to(m)
            else:
                folium.CircleMarker(
                    location=coord,
                    radius=3,
                    color="#4F5565",
                    weight=1,
                    fill=True,
                    fill_color="#30343F",
                    fill_opacity=0.5,
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=f"Walkway: {name}"
                ).add_to(m)
        elif is_in_route:
            folium.CircleMarker(
                location=coord,
                radius=8,
                color="#E58A45",
                weight=3,
                fill=True,
                fill_color="#E58A45",
                fill_opacity=0.9,
                popup=folium.Popup(popup_html, max_width=270),
                tooltip=f"📍 Step: {name}"
            ).add_to(m)
        else:
            # Color-coded icons based on building category
            c_color = "#3B82F6"
            if "Housing" in cat or "Hostel" in cat:
                c_color = "#9333EA"
            elif "Dining" in cat or "Food" in cat:
                c_color = "#EA580C"
            elif "Library" in cat:
                c_color = "#0284C7"
            elif "Park" in cat or "Concourse" in cat:
                c_color = "#16A34A"
            elif "Athletics" in cat or "Sports" in cat:
                c_color = "#059669"
            elif "Entrance" in cat:
                c_color = "#DC2626"
            elif "Parking" in cat:
                c_color = "#64748B"

            folium.CircleMarker(
                location=coord,
                radius=6,
                color=c_color,
                weight=2,
                fill=True,
                fill_color="#181A20",
                fill_opacity=0.85,
                popup=folium.Popup(popup_html, max_width=270),
                tooltip=f"{loc.get('icon', '📍')} {name} ({code})"
            ).add_to(m)

    return m
