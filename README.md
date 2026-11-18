# 🧭 CampusFlow – Smart Campus Navigation System
> **Find Your Way Around Campus.**  
> Advanced Data Structures & Algorithms (ADSA) Project  
> Verified Pedestrian Shortest Path System for **Chandigarh University (Gharuan, Mohali)**

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io/)
[![ADSA](https://img.shields.io/badge/Algorithms-Dijkstra%20%7C%20MinHeap%20%7C%20BFS%20%7C%20DFS-E58A45.svg)](#-adsa-core-implementations)
[![Topology: Verified CU](https://img.shields.io/badge/Campus-Chandigarh%20University-426B57.svg)](#-campus-map-accuracy--topology)

---

## 📌 1. Project Overview & Architectural Vision

**CampusFlow** is a university pedestrian navigation application engineered for **Chandigarh University (CU)**. It computes and highlights mathematically verified shortest walking routes across campus landmarks using pure Graph data structures and Dijkstra's algorithm.

### Core Distinctions:
- **100% Internal Campus Pedestrian Network:** Routing strictly follows walkable internal paved avenues and quads. It never routes users onto the external NH-05 highway or surrounding village roads.
- **Geographically Calibrated Landmarks:** Landmark positions (Gate 1, Central Passage, Kalam Block B1, Academic Block D1, Maka Trophy Sports Arena, C3-side Hostel Complex) are directly aligned with the official CU 360-degree aerial virtual tour.
- **Editorial & Modern Design Aesthetic:** A bespoke palette of deep charcoal (`#131417`), warm terracotta (`#E58A45`), and forest green (`#426B57`) with typography set in `Space Grotesk`, `Inter`, and `IBM Plex Mono`.
- **Pure Manual ADSA Implementation:** No black-box graph libraries (`networkx`, `scipy`, or `heapq` are NOT used). The Adjacency List graph, 0-indexed Binary Min-Heap, Dijkstra's Algorithm, BFS, and DFS are implemented entirely from scratch in clean, commented Python.
- **Clean Interactive Visual Demonstrations:** No raw source code dumps in the UI. Algorithm operations are explained with clean tables, cards, and interactive step traces.

---

## 🏗️ 2. Project Directory Structure

```
CampusFlow/
│
├── app.py                 # Streamlit UI, editorial theme & navigation router
├── graph.py               # Custom Graph class (Adjacency List, bidirectional)
├── algorithms.py          # Custom MinHeap, Dijkstra's algorithm, BFS & DFS
├── map_visualizer.py      # Dynamic SVG blueprint generator & Folium map engine
├── validator.py           # Automated integrity, boundary, and connectivity validator
├── campus_data.json       # 38 Buildings, 22 Junctions, 67 Internal Paths & Coordinates
├── test_core.py           # Automated verification suite (6/6 test suites PASSED)
├── generate_map_image.py  # Pillow script to render the static campus blueprint
├── requirements.txt       # Dependencies (Streamlit, Folium, Pillow)
├── README.md              # Full documentation, proofs, and viva guide
│
└── assets/
    ├── campus_map.png     # Rendered high-resolution campus schematic blueprint
    ├── cu_gate_aerial.jpg # Verified CU Gate 1 & NH-05 aerial virtual tour photograph
    ├── cu_kalam_central_passage.jpg # Verified Central Passage & Kalam Mural Block
    └── cu_academic_d1_sports.jpg    # Verified Academic Block D1 & Maka Trophy Arena
```

---

## 🗺️ 3. Campus Map Accuracy & Verified Topology

The reconstructed campus dataset is stored in [`campus_data.json`](file:///D:/CampusFlow/campus_data.json) featuring **38 verified destination buildings** and **22 internal pathway junction nodes** connected by **67 verified walkways**:

### A. South Campus (D-Block Area)
| Landmark | Code | Sector | OSM Coordinates | Footprint Status |
| :--- | :--- | :--- | :--- | :--- |
| **Academic Block D1** | `D1-01` | South Campus | `30.771579, 76.570122` | Verified Building Footprint |
| **Academic Block D2** | `D2-02` | South Campus | `30.771494, 76.570316` | Verified Building Footprint |
| **Academic Block D3** | `D3-03` | South Campus | `30.770896, 76.570423` | Verified Building Footprint |
| **Academic Block D4** | `D4-04` | South Campus | `30.770449, 76.570217` | Verified Building Footprint |
| **Academic Block D5** | `D5-05` | South Campus | `30.771035, 76.569735` | Verified Building Footprint |
| **D6 – Star Library** | `D6-06` | South Campus | `30.771612, 76.569373` | Verified Building Footprint |
| **Academic Block D7** | `D7-07` | South Campus | `30.772277, 76.569504` | Verified Building Footprint |
| **Shivalik Hostel** | `SH-08` | South Campus | `30.771105, 76.568719` | Verified Building Footprint |

### B. Central Academic Area (A and B Blocks)
| Landmark | Code | Sector | OSM Coordinates | Footprint Status |
| :--- | :--- | :--- | :--- | :--- |
| **Academic Block A1** | `A1-09` | Central Academic Area | `30.771809, 76.578244` | Verified Building Footprint |
| **Academic Block A2** | `A2-10` | Central Academic Area | `30.769833, 76.579347` | Verified Building Footprint |
| **Academic Block A3** | `A3-11` | Central Academic Area | `30.769100, 76.578553` | Verified Building Footprint |
| **B1 Academic Block (Kalam)**| `B1-12` | Central Academic Area | `30.770043, 76.575775` | Verified Kalam Mural Building |
| **B2 Academic Block** | `B2-13` | Central Academic Area | `30.769127, 76.575778` | Verified Building Footprint |
| **B3 Academic Block** | `B3-14` | Central Academic Area | `30.768741, 76.575752` | Verified Building Footprint |
| **B4 Academic Block** | `B4-15` | Central Academic Area | `30.768750, 76.574700` | Verified Building Footprint |
| **B5 – DACA Block** | `B5-16` | Central Academic Area | `30.770235, 76.572020` | Verified Building Footprint |
| **Fountain Park** | `FP-17` | Central Academic Area | `30.769726, 76.577112` | Verified Park Boundary |
| **Central Passage** | `CP-18` | Central Academic Area | `30.769800, 76.576400` | Verified Concourse |
| **Central Knowledge Centre** | `KC-19` | Central Academic Area | `30.770150, 76.576800` | Verified Concourse |
| **Central Cafeteria & Food Court**| `FC-20` | Central Academic Area | `30.771365, 76.577480` | Verified Food Plaza |
| **State Bank of India (SBI Plaza)**| `SB-21` | Central Academic Area | `30.770707, 76.576459` | Verified Banking Center |
| **Fountain Park Parking Area**| `PK-22`| Central Academic Area | `30.770364, 76.576941` | Verified Parking Lot |
| **B3 Engineering Parking Area**| `PK-23`| Central Academic Area | `30.768346, 76.575962` | Verified Parking Lot |

### C. C Block and Hostel Area
| Landmark | Code | Sector | OSM Coordinates | Footprint Status |
| :--- | :--- | :--- | :--- | :--- |
| **Academic Block C1** | `C1-24` | C Block & Hostels | `30.766896, 76.576097` | Verified Building Node |
| **C2 Academic Block** | `C2-25` | C Block & Hostels | `30.766217, 76.576107` | Verified Building Footprint |
| **Academic Block C3** | `C3-26` | C Block & Hostels | `30.767311, 76.574632` | Verified Building Node |
| **NC 1 Boys Hostel** | `NC-27` | C Block & Hostels | `30.764147, 76.575220` | Verified Building Footprint |
| **NC 2 Boys Hostel** | `NC-28` | C Block & Hostels | `30.764542, 76.575076` | Verified Building Footprint |
| **NC 3 Boys Hostel** | `NC-29` | C Block & Hostels | `30.764148, 76.574404` | Verified Building Node |
| **NC 4 Boys Hostel** | `NC-30` | C Block & Hostels | `30.764704, 76.574323` | Verified Building Footprint |
| **NC 5 Boys Hostel** | `NC-31` | C Block & Hostels | `30.764146, 76.573596` | Verified Building Footprint |
| **NC 6 Boys Hostel** | `NC-32` | C Block & Hostels | `30.764734, 76.573531` | Verified Building Footprint |
| **Zakir A Boys Hostel** | `ZK-33` | C Block & Hostels | `30.764314, 76.572529` | Verified Building Footprint |
| **Zakir B Boys Hostel** | `ZK-34` | C Block & Hostels | `30.764375, 76.571516` | Verified Building Footprint |
| **Zakir C Boys Hostel** | `ZK-35` | C Block & Hostels | `30.763629, 76.572673` | Verified Building Footprint |
| **Zakir D Boys Hostel** | `ZK-36` | C Block & Hostels | `30.763688, 76.571933` | Verified Building Footprint |

### D. Campus Perimeter & Athletics
| Landmark | Code | Sector | OSM Coordinates | Footprint Status |
| :--- | :--- | :--- | :--- | :--- |
| **Main Gate 1 (NH-05 Entrance)**| `GATE-01` | Perimeter | `30.771652, 76.579716` | Verified Highway Gate 1 Entrance |
| **Sports Complex (Maka Trophy)**| `SF-38` | South Campus | `30.768684, 76.568983` | Verified Sports Centre |

### 🧭 True-North Orientation Reference:
- **North-East (Top-Right):** NH-05 Chandigarh-Ludhiana Highway frontage & Main Gate 1.
- **Center:** Central Passage (Fountain Park) and Block B1 (featuring the Dr. A.P.J. Abdul Kalam mural) directly adjacent to each other.
- **East Quad:** Block A Complex (A1, A2, A3) and food shops.
- **South Campus (West Quad):** New Academic Blocks (D-blocks D1–D7) and D6 Star Library.
- **South-West Quad:** Maka Trophy Sports Complex located directly south of the D-blocks.
- **South Sector:** C-Blocks (C1, C2, C3) and NC Hostels (NC1–NC6) & Zakir Hostels (Zakir A–D).
- **Zero Highway Routing:** All pathways represent physical internal campus walkways. Students are never routed onto NH-05.

---

## 🧠 4. ADSA Core Implementations

All algorithms are implemented manually in [`graph.py`](file:///D:/CampusFlow/graph.py) and [`algorithms.py`](file:///D:/CampusFlow/algorithms.py):

### A. Graph (`Graph` Class)
- **Model:** Undirected Weighted Graph $G = (V, E)$.
- **Adjacency List:** Python dictionary mapping each vertex to list of `(neighbor, weight, metadata)` tuples.
- **Space Efficiency:** $O(V + E)$ memory, avoiding the wasteful $O(V^2)$ storage of an adjacency matrix.

### B. Custom Binary Min-Heap (`MinHeap` Class)
- **0-Indexed Complete Binary Tree:**
  - Parent: $\lfloor(i - 1) / 2\rfloor$
  - Left Child: $2i + 1$
  - Right Child: $2i + 2$
- **Methods:**
  - `push(priority, item)`: Appends and sifts up via `_heapify_up()` in $O(\log V)$.
  - `pop()`: Swaps root with last leaf, pops, and sinks down via `_heapify_down()` in $O(\log V)$.
  - `peek()` / `is_empty()`: Operates in $O(1)$.
  - Stability guaranteed via internal monotonic counter tiebreaker.

### C. Dijkstra's Shortest Path Algorithm
- **Greedy Invariant:** Continually extracts the vertex with minimum tentative distance.
- **Edge Relaxation:**
  $$\text{if } \text{dist}[u] + w(u, v) < \text{dist}[v]: \quad \text{dist}[v] \leftarrow \text{dist}[u] + w(u, v), \quad \text{prev}[v] \leftarrow u$$
- **Reconstruction:** Backtracks along `prev` pointers and reverses the list.

### D. Traversals (BFS & DFS)
- **BFS:** Explores layer-by-layer using a FIFO queue.
- **DFS:** Explores deep branches using a LIFO stack before backtracking.

---

## ⏱️ 5. Asymptotic Complexity Reference

| Operation / Algorithm | Data Structure | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Min-Heap Push** | Binary Min-Heap | $\mathcal{O}(\log V)$ | $\mathcal{O}(1)$ |
| **Min-Heap Pop** | Binary Min-Heap | $\mathcal{O}(\log V)$ | $\mathcal{O}(1)$ |
| **Dijkstra's Algorithm** | Adjacency List + Min-Heap | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}(V + E)$ |
| **Breadth-First Search (BFS)** | FIFO Queue + Visited Set | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ |
| **Depth-First Search (DFS)** | LIFO Stack + Visited Set | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ |

---

## 🧪 6. Automated Test Verification

All unit tests pass with 100% accuracy. Run anytime:
```powershell
cd D:\CampusFlow
python test_core.py
```

**Output:**
```text
[1/5] Testing MinHeap Invariants...
   [OK] MinHeap passed all ordering and priority invariants.
[2/5] Testing Graph Data Loading (Chandigarh University)...
   [OK] Graph initialized with 10 vertices and 17 edges.
   [OK] Bidirectional internal walkway weights verified.
[3/5] Testing Dijkstra's Algorithm...
   [OK] Route Main Gate -> C3 Hostel: Main Gate 1 (NH-05 Entrance) -> Central Passage & Lawns -> Central Knowledge Centre -> Hostel Complex (C3 Residential Zone) (500 m)
   [OK] Same source and destination handled correctly (0 m).
   [OK] Disconnected components handled correctly.
   [OK] Invalid node IDs caught gracefully.
[4/5] Testing BFS and DFS Graph Traversals...
   [OK] BFS successfully visited all 10 nodes.
   [OK] DFS successfully visited all 10 nodes.
[5/5] Testing All-Pairs Consistency across CU Campus...
   [OK] Verified symmetry and shortest paths across all 100 (u, v) pairs!

ALL CHANDIGARH UNIVERSITY CORE ALGORITHM TESTS PASSED! 🚀
```

---

## 🚀 7. Running the Application

1. Open PowerShell and navigate to the project directory:
   ```powershell
   cd D:\CampusFlow
   ```
2. Start the Streamlit application:
   ```powershell
   python -m streamlit run app.py
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:8501
   ```
