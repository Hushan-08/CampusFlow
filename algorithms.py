"""
CampusFlow - Algorithms Module
==============================
College ADSA Lab Project: Custom implementations of core algorithms.

Included Implementations (NO third-party graph/algorithm libraries used):
1. MinHeap / PriorityQueue (Binary Min-Heap from scratch)
2. Dijkstra's Shortest Path Algorithm
3. Breadth-First Search (BFS) Traversal
4. Depth-First Search (DFS) Traversal

Time and Space Complexities for Viva:
- Min Heap Operations:
    * Insert (push): O(log V)
    * Extract Min (pop): O(log V)
    * Peek / Size: O(1)
- Dijkstra's Algorithm:
    * Time Complexity: O((V + E) log V) with Adjacency List + Min Heap
    * Space Complexity: O(V) for distances, previous, and heap
- BFS:
    * Time Complexity: O(V + E)
    * Space Complexity: O(V)
- DFS:
    * Time Complexity: O(V + E)
    * Space Complexity: O(V)
"""

from typing import Dict, List, Tuple, Optional, Any, Set
from graph import Graph


class MinHeap:
    """
    A manual 0-indexed Binary Min Heap implementation.
    Stores tuples of (priority, counter, item) where:
    - priority: numeric key to order by (e.g., shortest distance)
    - counter: tiebreaker integer to maintain stability and prevent object comparison
    - item: the stored data (e.g., vertex ID)

    Array math:
    - Parent of index i:      (i - 1) // 2
    - Left child of index i:   2 * i + 1
    - Right child of index i:  2 * i + 2
    """

    def __init__(self):
        self.heap: List[Tuple[float, int, Any]] = []
        self._counter: int = 0  # Tiebreaker counter

    def is_empty(self) -> bool:
        """Checks if the heap has no elements. O(1)"""
        return len(self.heap) == 0

    def size(self) -> int:
        """Returns the number of elements in the heap. O(1)"""
        return len(self.heap)

    def peek(self) -> Optional[Tuple[float, Any]]:
        """Returns the minimum element without removing it. O(1)"""
        if self.is_empty():
            return None
        priority, _, item = self.heap[0]
        return priority, item

    def push(self, priority: float, item: Any) -> None:
        """
        Inserts a new element into the min heap and maintains the heap property.
        Time Complexity: O(log N)
        """
        self._counter += 1
        entry = (priority, self._counter, item)
        self.heap.append(entry)
        self._heapify_up(len(self.heap) - 1)

    def pop(self) -> Optional[Tuple[float, Any]]:
        """
        Extracts and returns the element with the minimum priority.
        Time Complexity: O(log N)
        """
        if self.is_empty():
            return None

        # Base case: only 1 element
        if len(self.heap) == 1:
            priority, _, item = self.heap.pop()
            return priority, item

        # Swap root with the last leaf
        root_priority, _, root_item = self.heap[0]
        last_element = self.heap.pop()
        self.heap[0] = last_element

        # Restore min-heap property from root downwards
        self._heapify_down(0)

        return root_priority, root_item

    def _heapify_up(self, index: int) -> None:
        """
        Restores min-heap invariant by moving an element up towards the root.
        """
        while index > 0:
            parent_index = (index - 1) // 2
            # Compare priorities: self.heap[index][0] vs self.heap[parent_index][0]
            if self.heap[index] < self.heap[parent_index]:
                # Swap child with parent
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def _heapify_down(self, index: int) -> None:
        """
        Restores min-heap invariant by sinking an element down towards the leaves.
        """
        n = len(self.heap)
        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            # Check if left child exists and is smaller than current
            if left_child < n and self.heap[left_child] < self.heap[smallest]:
                smallest = left_child

            # Check if right child exists and is smaller than smallest so far
            if right_child < n and self.heap[right_child] < self.heap[smallest]:
                smallest = right_child

            # If the current element is smaller than both children, heap is restored
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break


def dijkstra_shortest_path(
    graph: Graph,
    start_vertex: str,
    target_vertex: str
) -> Dict[str, Any]:
    """
    Computes the shortest path from start_vertex to target_vertex
    using Dijkstra's Algorithm with a custom Binary Min Heap.

    Algorithm Steps:
    1. Initialize distances to all vertices as infinity (inf), except start_vertex = 0.
    2. Maintain a predecessor map (previous) to reconstruct the path.
    3. Push (0, start_vertex) into the custom Min Heap.
    4. While min heap is not empty:
       a. Extract vertex u with smallest current distance.
       b. If u was already visited with a shorter distance, continue.
       c. Mark u as visited.
       d. If u is target_vertex, early exit can be performed (or full search).
       e. For each neighbor v with edge weight w:
          If distance[u] + w < distance[v]:
             distance[v] = distance[u] + w
             previous[v] = u
             Push (distance[v], v) to min heap.
    5. Reconstruct the shortest path by backtracking from target_vertex to start_vertex.

    Returns a rich dictionary containing:
    - success (bool)
    - path (List[str] IDs)
    - path_names (List[str] friendly names)
    - total_distance (int meters)
    - visited_count (int)
    - visited_order (List[str])
    - distances (Dict[str, float])
    - trace_log (List[str])
    - message (str)
    """
    vertices = graph.get_vertices()

    # Edge Case: Invalid vertex selection
    if start_vertex not in graph.adj_list or target_vertex not in graph.adj_list:
        return {
            "success": False,
            "path": [],
            "path_names": [],
            "total_distance": 0,
            "visited_count": 0,
            "visited_order": [],
            "distances": {},
            "trace_log": ["Error: One or both selected locations do not exist in the graph."],
            "message": "Invalid starting or destination location selected."
        }

    # Edge Case: Start and Destination are the exact same location
    if start_vertex == target_vertex:
        return {
            "success": True,
            "path": [start_vertex],
            "path_names": [graph.get_vertex_name(start_vertex)],
            "total_distance": 0,
            "visited_count": 1,
            "visited_order": [start_vertex],
            "distances": {v: (0 if v == start_vertex else float("inf")) for v in vertices},
            "trace_log": [
                f"Starting location '{graph.get_vertex_name(start_vertex)}' is identical to destination. Distance is 0 meters."
            ],
            "message": "You are already at your destination!"
        }

    # Step 1: Initialization
    distances: Dict[str, float] = {v: float("inf") for v in vertices}
    previous: Dict[str, Optional[str]] = {v: None for v in vertices}
    distances[start_vertex] = 0

    min_heap = MinHeap()
    min_heap.push(0.0, start_vertex)

    visited_set: Set[str] = set()
    visited_order: List[str] = []
    trace_log: List[str] = [
        f"Initialized source vertex '{graph.get_vertex_name(start_vertex)}' with distance 0 m.",
        f"Initialized remaining {len(vertices) - 1} vertices with distance ∞ m."
    ]

    # Step 2: Main relaxation loop
    while not min_heap.is_empty():
        current_dist, current_vertex = min_heap.pop()

        # If already visited with an equal or better distance, skip stale entry
        if current_vertex in visited_set:
            continue

        visited_set.add(current_vertex)
        visited_order.append(current_vertex)
        curr_name = graph.get_vertex_name(current_vertex)

        trace_log.append(
            f"Visiting '{curr_name}' [Settled distance: {int(current_dist)} m]."
        )

        # Early termination optimization: If target is settled, shortest path is guaranteed
        if current_vertex == target_vertex:
            trace_log.append(f"Destination '{curr_name}' reached with confirmed minimum distance.")
            break

        # Relax all outgoing edges from current_vertex
        for neighbor, weight, metadata in graph.get_neighbors(current_vertex):
            if neighbor in visited_set:
                continue

            new_dist = current_dist + weight
            neighbor_name = graph.get_vertex_name(neighbor)

            if new_dist < distances[neighbor]:
                old_dist_str = "∞" if distances[neighbor] == float("inf") else f"{int(distances[neighbor])} m"
                distances[neighbor] = new_dist
                previous[neighbor] = current_vertex
                min_heap.push(new_dist, neighbor)
                trace_log.append(
                    f"  ↳ Relaxed edge to '{neighbor_name}' via {metadata.get('path_type', 'path')}: "
                    f"Updated {old_dist_str} ➔ {int(new_dist)} m (+{weight} m)."
                )

    # Step 3: Check if target was reachable
    if distances[target_vertex] == float("inf"):
        return {
            "success": False,
            "path": [],
            "path_names": [],
            "total_distance": 0,
            "visited_count": len(visited_order),
            "visited_order": visited_order,
            "distances": distances,
            "trace_log": trace_log + [
                f"No connected path exists between '{graph.get_vertex_name(start_vertex)}' and '{graph.get_vertex_name(target_vertex)}'."
            ],
            "message": "No walking route exists between the selected locations."
        }

    # Step 4: Reconstruct shortest path by backtracking
    path = []
    curr: Optional[str] = target_vertex
    while curr is not None:
        path.append(curr)
        curr = previous[curr]
    path.reverse()

    path_names = [graph.get_vertex_name(node_id) for node_id in path]

    # Build detailed path steps with individual leg distances
    path_legs = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        leg_weight = graph.get_edge_weight(u, v) or 0
        path_legs.append({
            "from_id": u,
            "from_name": graph.get_vertex_name(u),
            "to_id": v,
            "to_name": graph.get_vertex_name(v),
            "distance": leg_weight
        })

    return {
        "success": True,
        "path": path,
        "path_names": path_names,
        "path_legs": path_legs,
        "total_distance": int(distances[target_vertex]),
        "visited_count": len(visited_order),
        "visited_order": visited_order,
        "distances": distances,
        "trace_log": trace_log,
        "message": f"Optimal shortest path found ({int(distances[target_vertex])} meters across {len(path)} locations)."
    }


def bfs_traversal(graph: Graph, start_vertex: str) -> Dict[str, Any]:
    """
    Breadth-First Search (BFS) graph traversal starting from start_vertex.
    Explores neighbors level-by-level using a FIFO queue.

    Viva Concepts:
    - Queue Data Structure (First-In, First-Out)
    - Level-order traversal
    - Finds the shortest path in terms of number of hops (unweighted edges)
    - Time Complexity: O(V + E)
    - Space Complexity: O(V)
    """
    if start_vertex not in graph.adj_list:
        return {
            "success": False,
            "traversal_order": [],
            "traversal_names": [],
            "levels": {},
            "message": f"Start vertex '{start_vertex}' not found."
        }

    visited: Set[str] = {start_vertex}
    queue: List[str] = [start_vertex]
    traversal_order: List[str] = []
    levels: Dict[str, int] = {start_vertex: 0}
    parents: Dict[str, Optional[str]] = {start_vertex: None}
    trace: List[str] = [f"Enqueue start node '{graph.get_vertex_name(start_vertex)}' at Level 0."]

    head_ptr = 0
    while head_ptr < len(queue):
        u = queue[head_ptr]
        head_ptr += 1
        traversal_order.append(u)
        curr_name = graph.get_vertex_name(u)
        curr_lvl = levels[u]

        # Explore all unvisited neighbors
        for neighbor, weight, _ in graph.get_neighbors(u):
            if neighbor not in visited:
                visited.add(neighbor)
                levels[neighbor] = curr_lvl + 1
                parents[neighbor] = u
                queue.append(neighbor)
                trace.append(
                    f"Visited '{graph.get_vertex_name(neighbor)}' (Level {curr_lvl + 1}) discovered from '{curr_name}'."
                )

    return {
        "success": True,
        "traversal_order": traversal_order,
        "traversal_names": [graph.get_vertex_name(n) for n in traversal_order],
        "levels": levels,
        "parents": parents,
        "trace": trace,
        "total_visited": len(traversal_order)
    }


def dfs_traversal(graph: Graph, start_vertex: str) -> Dict[str, Any]:
    """
    Depth-First Search (DFS) graph traversal starting from start_vertex.
    Explores as deep as possible along each branch before backtracking.
    Implemented iteratively using an explicit LIFO Call Stack.

    Viva Concepts:
    - Stack Data Structure (Last-In, First-Out) / Recursion
    - Backtracking exploration
    - Time Complexity: O(V + E)
    - Space Complexity: O(V)
    """
    if start_vertex not in graph.adj_list:
        return {
            "success": False,
            "traversal_order": [],
            "traversal_names": [],
            "message": f"Start vertex '{start_vertex}' not found."
        }

    visited: Set[str] = set()
    stack: List[Tuple[str, Optional[str]]] = [(start_vertex, None)]
    traversal_order: List[str] = []
    trace: List[str] = [f"Pushed start node '{graph.get_vertex_name(start_vertex)}' to stack."]

    while stack:
        u, parent = stack.pop()

        if u not in visited:
            visited.add(u)
            traversal_order.append(u)
            curr_name = graph.get_vertex_name(u)
            if parent:
                trace.append(f"Popped '{curr_name}', exploring depth branch from '{graph.get_vertex_name(parent)}'.")
            else:
                trace.append(f"Popped '{curr_name}' as root of DFS tree.")

            # Add unvisited neighbors to stack (reverse order so first neighbor is popped first)
            neighbors = graph.get_neighbors(u)
            for neighbor, weight, _ in reversed(neighbors):
                if neighbor not in visited:
                    stack.append((neighbor, u))

    return {
        "success": True,
        "traversal_order": traversal_order,
        "traversal_names": [graph.get_vertex_name(n) for n in traversal_order],
        "trace": trace,
        "total_visited": len(traversal_order)
    }
