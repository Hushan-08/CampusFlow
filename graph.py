"""
CampusFlow - Graph Data Structure Module
=========================================
College ADSA Lab Project: Custom Undirected Weighted Graph representation
using an Adjacency List.

Viva Concept:
- A Graph G = (V, E) consists of a set of Vertices V (campus locations)
  and Edges E (walking pathways between locations).
- This is an Undirected Weighted Graph because a student can walk both ways
  along a path, and each path has a weight corresponding to walking distance in meters.
- Representation: Adjacency List using a Python dictionary:
    adj_list[u] = [(v1, weight1), (v2, weight2), ...]
"""

import json
from typing import Dict, List, Tuple, Optional, Any


class Graph:
    """
    Custom Graph class representing the campus map as an adjacency list.
    Designed for clarity, correctness, and viva demonstration.
    """

    def __init__(self):
        # adj_list stores: { vertex_id: [ (neighbor_id, weight, path_info), ... ] }
        self.adj_list: Dict[str, List[Tuple[str, int, Dict[str, Any]]]] = {}
        # metadata stores vertex-specific details (name, category, coords, icon)
        self.vertices_metadata: Dict[str, Dict[str, Any]] = {}

    def add_vertex(self, vertex_id: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Adds a new vertex (location) to the graph if it doesn't already exist.
        Time Complexity: O(1)
        """
        if vertex_id not in self.adj_list:
            self.adj_list[vertex_id] = []
            self.vertices_metadata[vertex_id] = metadata or {
                "name": vertex_id,
                "category": "General",
                "icon": "📍"
            }

    def add_edge(
        self,
        u: str,
        v: str,
        weight: int,
        path_type: str = "Paved Walkway",
        description: str = "",
        bidirectional: bool = True
    ) -> None:
        """
        Adds a weighted edge between vertex u and vertex v.
        Since campus walking paths are bidirectional, an edge is added in both directions.
        Time Complexity: O(1)
        """
        # Ensure both endpoints exist in the graph
        self.add_vertex(u)
        self.add_vertex(v)

        edge_metadata = {
            "path_type": path_type,
            "description": description
        }

        # Add u -> v
        self.adj_list[u].append((v, weight, edge_metadata))

        # If bidirectional (walking paths), add v -> u
        if bidirectional:
            self.adj_list[v].append((u, weight, edge_metadata))

    def get_neighbors(self, u: str) -> List[Tuple[str, int, Dict[str, Any]]]:
        """
        Returns list of (neighbor_id, distance, metadata) for vertex u.
        Time Complexity: O(deg(u))
        """
        return self.adj_list.get(u, [])

    def get_edge_weight(self, u: str, v: str) -> Optional[int]:
        """
        Returns the weight (distance in meters) of edge (u, v) if it exists, else None.
        """
        for neighbor, weight, _ in self.adj_list.get(u, []):
            if neighbor == v:
                return weight
        return None

    def get_vertices(self) -> List[str]:
        """Returns a list of all vertex IDs in the graph."""
        return list(self.adj_list.keys())

    def get_vertex_count(self) -> int:
        """Returns total number of vertices |V|."""
        return len(self.adj_list)

    def get_edge_count(self) -> int:
        """
        Returns total number of unique undirected edges |E|.
        In an undirected graph, sum of degrees = 2 * |E|.
        """
        total_directed_edges = sum(len(neighbors) for neighbors in self.adj_list.values())
        return total_directed_edges // 2

    def get_vertex_name(self, vertex_id: str) -> str:
        """Helper to get friendly name of a vertex."""
        return self.vertices_metadata.get(vertex_id, {}).get("name", vertex_id)

    def get_vertex_metadata(self, vertex_id: str) -> Dict[str, Any]:
        """Helper to get full metadata dictionary of a vertex."""
        return self.vertices_metadata.get(vertex_id, {})

    def to_readable_adjacency_list(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Formats adjacency list into human-readable dictionary
        for viva demonstration and frontend tables.
        """
        readable = {}
        for u, neighbors in self.adj_list.items():
            u_name = self.get_vertex_name(u)
            readable[u_name] = [
                {
                    "neighbor_id": v,
                    "neighbor_name": self.get_vertex_name(v),
                    "distance_meters": weight,
                    "path_type": meta.get("path_type", "Standard"),
                    "description": meta.get("description", "")
                }
                for v, weight, meta in neighbors
            ]
        return readable


def load_campus_graph_from_json(json_path: str) -> Tuple[Graph, Dict[str, Any]]:
    """
    Factory function to initialize and populate the Graph object
    from campus_data.json.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = Graph()

    # 1. Add all locations (vertices)
    for loc in data.get("locations", []):
        graph.add_vertex(loc["id"], metadata=loc)

    # 2. Add all walking paths (edges)
    for path in data.get("paths", []):
        graph.add_edge(
            u=path["source"],
            v=path["target"],
            weight=int(path["distance"]),
            path_type=path.get("path_type", "Paved Walkway"),
            description=path.get("description", ""),
            bidirectional=True
        )

    return graph, data.get("campus_info", {})
