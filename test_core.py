"""
CampusFlow - Comprehensive Unit & Algorithm Verification Suite
==============================================================
Validates:
1. Binary Min-Heap ordering invariants.
2. Complete Chandigarh University Graph Topology (60 nodes, 67 edges).
3. All 8 User Required Navigation Scenarios via Dijkstra's Algorithm.
4. Full Graph Reachability & Traversal (BFS & DFS visit all 60 nodes).
5. All-Pairs Shortest Path Symmetry.
6. Automated Data Validation (0 issues, 0 highway violations).
"""

import os
import sys
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from graph import load_campus_graph_from_json, Graph
from algorithms import dijkstra_shortest_path, bfs_traversal, dfs_traversal, MinHeap
from validator import validate_campus_data

def test_min_heap():
    print("[1/6] Testing MinHeap Invariants...")
    h = MinHeap()
    assert h.is_empty() is True
    assert h.size() == 0

    elements = [(45, "Node_45"), (10, "Node_10"), (30, "Node_30"), (5, "Node_5"), (70, "Node_70")]
    for p, val in elements:
        h.push(p, val)

    assert h.size() == 5
    assert h.is_empty() is False
    assert h.peek() == (5, "Node_5")

    extracted = []
    while not h.is_empty():
        extracted.append(h.pop())

    expected = [(5, "Node_5"), (10, "Node_10"), (30, "Node_30"), (45, "Node_45"), (70, "Node_70")]
    assert extracted == expected, f"Expected {expected}, got {extracted}"
    print("   [OK] MinHeap passed all ordering, sift-up, and sift-down invariants.")

def test_graph_loading():
    print("[2/6] Testing Graph Data Loading (Chandigarh University)...")
    json_path = os.path.join(BASE_DIR, "campus_data.json")
    graph, info = load_campus_graph_from_json(json_path)
    v_count = graph.get_vertex_count()
    e_count = graph.get_edge_count()
    print(f"   [OK] Graph initialized with {v_count} vertices and {e_count} edges.")
    assert v_count == 60, f"Expected 60 vertices, got {v_count}"
    assert e_count == 67, f"Expected 67 edges, got {e_count}"

    # Check bidirectional edges
    mg_to_jp = graph.get_edge_weight("main_gate", "j_gate_plaza")
    jp_to_mg = graph.get_edge_weight("j_gate_plaza", "main_gate")
    assert mg_to_jp == jp_to_mg
    assert mg_to_jp is not None

    b1_to_kp = graph.get_edge_weight("b1_kalam", "j_kalam_plaza")
    kp_to_b1 = graph.get_edge_weight("j_kalam_plaza", "b1_kalam")
    assert b1_to_kp == kp_to_b1
    assert b1_to_kp is not None
    print("   [OK] Bidirectional internal walkway weights verified.")
    return graph

def test_dijkstra_user_scenarios(graph: Graph):
    print("[3/6] Testing Dijkstra's Algorithm across 8 Required Scenarios...")
    scenarios = [
        ("Scenario 1: Main Gate to Central Passage", "main_gate", "central_passage", 520),
        ("Scenario 2: Main Gate to B1 (Kalam Block)", "main_gate", "b1_kalam", 590),
        ("Scenario 3: B1 to D6 Star Library", "b1_kalam", "d6_star_library", 840),
        ("Scenario 4: South Campus to Central Academic Area (D1 to B1)", "d1", "b1_kalam", 770),
        ("Scenario 5: Central Academic Area to C1", "b1_kalam", "c1", 430),
        ("Scenario 6: Central Academic Area to C3", "b1_kalam", "c3", 520),
        ("Scenario 7: B1 to NC3 Boys Hostel", "b1_kalam", "nc3_hostel", 840),
        ("Scenario 8: D Block to Sports Complex", "d1", "sports_complex", 395)
    ]

    for label, s, t, expected_dist in scenarios:
        res = dijkstra_shortest_path(graph, s, t)
        assert res["success"] is True, f"Failed route {label}"
        assert res["path"][0] == s, f"Route must start at {s}"
        assert res["path"][-1] == t, f"Route must end at {t}"
        assert res["total_distance"] == expected_dist, f"Expected {expected_dist}m for {label}, got {res['total_distance']}m"
        print(f"   [OK] {label}: {res['total_distance']}m ({len(res['path'])} waypoints)")

    # Edge Case: Same Start and Destination
    same = dijkstra_shortest_path(graph, "central_passage", "central_passage")
    assert same["success"] is True
    assert same["total_distance"] == 0
    assert same["path"] == ["central_passage"]
    print("   [OK] Same source and destination handled correctly (0 m).")

    # Edge Case: Invalid node ID handling
    invalid_res = dijkstra_shortest_path(graph, "non_existent_node", "main_gate")
    assert invalid_res["success"] is False
    print("   [OK] Invalid node IDs caught gracefully.")

def test_bfs_dfs(graph: Graph):
    print("[4/6] Testing BFS and DFS Graph Traversals (100% Reachability)...")
    bfs_res = bfs_traversal(graph, "main_gate")
    assert bfs_res["success"] is True
    assert bfs_res["total_visited"] == 60, f"BFS expected 60 visited, got {bfs_res['total_visited']}"
    assert bfs_res["traversal_order"][0] == "main_gate"
    print(f"   [OK] BFS successfully reached all 60 vertices from Main Gate.")

    dfs_res = dfs_traversal(graph, "main_gate")
    assert dfs_res["success"] is True
    assert dfs_res["total_visited"] == 60, f"DFS expected 60 visited, got {dfs_res['total_visited']}"
    assert dfs_res["traversal_order"][0] == "main_gate"
    print(f"   [OK] DFS successfully reached all 60 vertices from Main Gate.")

def test_all_pairs_symmetry(graph: Graph):
    print("[5/6] Testing Shortest Path Symmetry across Key Destinations...")
    test_nodes = [
        "main_gate", "d1", "d6_star_library", "shivalik_hostel",
        "b1_kalam", "fountain_park", "central_passage",
        "c1", "c3", "nc3_hostel", "zakir_a_hostel", "sports_complex"
    ]
    pairs_tested = 0
    for u in test_nodes:
        for v in test_nodes:
            res_uv = dijkstra_shortest_path(graph, u, v)
            res_vu = dijkstra_shortest_path(graph, v, u)
            assert res_uv["success"] is True
            assert res_vu["success"] is True
            assert res_uv["total_distance"] == res_vu["total_distance"]
            pairs_tested += 1
    print(f"   [OK] Verified symmetric distance equality across all {pairs_tested} destination pairs.")

def test_automated_validation(graph: Graph):
    print("[6/6] Testing Automated Validation Suite (validator.py)...")
    json_path = os.path.join(BASE_DIR, "campus_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    report = validate_campus_data(data, graph)
    assert report["is_valid"] is True, f"Validation failed with issues: {report['issues']}"
    assert len(report["issues"]) == 0
    assert len(report["warnings"]) == 0
    assert report["total_locations"] == 60
    assert report["total_paths"] == 67
    assert len(report["disconnected_nodes"]) == 0
    print(f"   [OK] Automated validation passed with 0 issues and 0 warnings.")

if __name__ == "__main__":
    test_min_heap()
    g = test_graph_loading()
    test_dijkstra_user_scenarios(g)
    test_bfs_dfs(g)
    test_all_pairs_symmetry(g)
    test_automated_validation(g)
    print("\nALL 6/6 UNIT & ALGORITHM VERIFICATION SUITES PASSED! 🚀")
