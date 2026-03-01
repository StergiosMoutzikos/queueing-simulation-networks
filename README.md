#  Queueing Theory & Network Pathfinding Simulation

> **Computer Networks & AI — Project 1**  
> Στέργιος Μουτζίκος 

---

##  Project Overview

This project consists of two parts:

1. **Queueing Theory Simulations** — Discrete-event simulation of M/M/1 and M/M/K queuing systems using SimPy, comparing simulated results against theoretical values.
2. **Network Pathfinding Comparison** — Construction of a random geometric graph and benchmarking of BFS, Dijkstra, and A* algorithms across path distance, number of steps, and execution time.

---

##  Repository Structure

```
├── MM1.py                             # M/M/1 queue simulation
├── MMK.py                             # M/M/K queue simulation (multi-server)
├── project1_networks.py               # Network pathfinding (BFS, Dijkstra, A*)
├── MM1_MMK.pdf                        # Full project report (queues)
├── Project1_networks_explanation.pdf  # Full project report (networks)
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

##  Part 1 — Queueing Theory (M/M/1 & M/M/K)

### M/M/1 Queue (`MM1.py`)

Simulates a single-server queue with Poisson arrivals and exponential service times.

**Metrics tracked:**
- Average waiting time
- Average queue size
- Processor utilization

Simulated results are plotted against theoretical M/M/1 formulas for utilization factors ρ ∈ [0.1, 0.9].

**Run:**
```bash
python MM1.py
```
You will be prompted to enter:
- Arrival rate λ (e.g. `1`)
- Service rate μ (e.g. `2`)
- Simulation time (e.g. `1000`)

---

### M/M/K Queue (`MMK.py`)

Extends the simulation to K parallel servers. Each arriving customer is routed to the server with the shortest queue.

**Run:**
```bash
python MMK.py
```
Additional prompt:
- Number of servers K (e.g. `2`)

---

##  Part 2 — Network Pathfinding (`project1_networks.py`)

Generates a random geometric graph of 50 nodes in a 1000×1000 area. The connection radius `rc` is increased incrementally until the graph is fully connected.

Then compares three shortest-path algorithms:

| Algorithm | Weight-aware | Heuristic |
|-----------|-------------|-----------|
| BFS       | ❌ No       | ❌ No    |
| Dijkstra  | ✅ Yes      | ❌ No    |
| A\*       | ✅ Yes      | ✅ Euclidean |

**Metrics compared (bar charts):**
- Average & median path distance
- Average number of hops (steps)
- Average execution time

**Run:**
```bash
python project1_networks.py
```

---

##  Key Results

### Queueing
- Simulated values closely follow theoretical curves, especially at higher simulation times
- Queue size and waiting time grow sharply as ρ → 1
- M/M/K systems significantly reduce waiting times compared to M/M/1 under the same load

### Pathfinding
- **BFS** is the fastest but produces longer distances (ignores edge weights)
- **Dijkstra & A\*** produce optimal (shorter) paths; similar distance results (~726 vs 755 for BFS)
- **A\*** has the highest execution time due to heuristic computation overhead
- All algorithms produce similar hop counts (~4.84–4.89 average steps)

---

##  Installation & Requirements

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**
```
simpy
numpy
matplotlib
networkx
scipy
```

> Python 3.8+ recommended

---

##  Reports

- [`MM1_MMK.pdf`](./MM1_MMK.pdf) — Detailed explanation of the M/M/1 and M/M/K simulations with sample outputs
- [`Project1_networks_explaination.pdf`](./Project1_networks_explaination.pdf) — Detailed explanation of the network pathfinding code and result analysis

---

##  Technologies Used

- **Python 3**
- **SimPy** — Discrete-event simulation
- **NumPy** — Numerical computation
- **Matplotlib** — Plotting
- **NetworkX** — Graph construction and pathfinding
- **SciPy** — Euclidean distance computation

---

##  Author

**Στέργιος Μουτζίκος**  
Department of Informatics
