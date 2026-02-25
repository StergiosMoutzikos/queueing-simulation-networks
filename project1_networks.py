import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
import time

# Parameters
num_nodes, area_size, rc = 50, 1000, 0
positions = np.random.rand(num_nodes, 2) * area_size

# Function to create the network with radius rc
def create_network(rc):
    G = nx.Graph()
    for i in range(num_nodes):
        G.add_node(i, pos=positions[i])
        
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            dist = euclidean(positions[i], positions[j])
            if dist <= rc:
                G.add_edge(i, j, weight=dist)
    return G if nx.is_connected(G) else None

# Create a connected graph with increasing radius rc until connectivity is ensured
while not (G := create_network(rc := rc + 10)):
    pass

# Function to calculate paths and statistics
def calculate_paths(graph, algorithm):
    path_lengths, num_steps, times = [], [], []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            start_time = time.time()
            
            # Choose algorithm and calculate path
            if algorithm == 'bfs':  # BFS without weights
                path = nx.shortest_path(graph, i, j)
                length = sum(graph[u][v]['weight'] for u, v in zip(path, path[1:]))
            elif algorithm == 'dijkstra':  # Dijkstra with weights
                path = nx.dijkstra_path(graph, i, j, weight='weight')
                length = nx.path_weight(graph, path, weight='weight')
            else:  # A* with Euclidean heuristic
                path = nx.astar_path(graph, i, j, heuristic=lambda u, v: euclidean(positions[u], positions[v]), weight='weight')
                length = nx.path_weight(graph, path, weight='weight')
                
            path_lengths.append(length)
            num_steps.append(len(path) - 1)  # Number of steps in path
            times.append(time.time() - start_time)
    
    # Return measurements: average distance, median distance, average steps, average time
    return np.mean(path_lengths), np.median(path_lengths), np.mean(num_steps), np.mean(times)

# Calculations for each algorithm
results = {alg: calculate_paths(G, alg) for alg in ['bfs', 'dijkstra', 'astar']}
avg_distances, median_distances, avg_steps, avg_times = zip(*results.values())

# Plotting results
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
algorithms = ['BFS', 'Dijkstra', 'A*']

# Graph for distances (Average and Median)
for ax, data, title, ylabel in zip(
        axes, [(avg_distances, median_distances), (avg_steps,), (avg_times,)],
        ["Path Distance", "Number of Steps", "Execution Time (s)"], ["Distance", "Steps", "Time (s)"]):
    
    bars1 = ax.bar(algorithms, data[0], color=['#4c72b0', '#55a868', '#c44e52'], label='Average')
    
    # Median values if applicable for distances
    if len(data) > 1:
        bars2 = ax.bar(algorithms, data[1], color=['#8da0cb', '#66c2a5', '#fc8d62'], alpha=0.6, label='Median')
    
    # Titles and labels
    ax.set(title=title, ylabel=ylabel)
    ax.legend()
    
    # Display values above bars
    for bar, avg in zip(bars1, data[0]):
        offset = 0.5 if title == "Path Distance" else 0.1
        ax.text(bar.get_x() + bar.get_width() / 2, avg + offset, f"{avg:.2f}", ha='center', fontweight='bold')

plt.tight_layout()
plt.show()
