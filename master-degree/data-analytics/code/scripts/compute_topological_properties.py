import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Paths
DATA_PATH = "../../data/graphs/"
GRAPH_FILE = os.path.join(DATA_PATH, "paris_metro.graphml")

# Load Graph
G = nx.read_graphml(GRAPH_FILE)

# Degree Distribution
degrees = [G.degree(n) for n in G.nodes()]
avg_degree = np.mean(degrees)

# Define the bins explicitly for integer degree values
bins = np.arange(min(degrees) - 0.5, max(degrees) + 1.5, 1)

plt.figure(figsize=(8, 5))
counts, bin_edges, bars = plt.hist(degrees, bins=bins, edgecolor="black", alpha=0.7)

# Annotate bars with frequency values
for bar, count in zip(bars, counts):
    if count > 0:  # Only label bars with nonzero values
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, int(count), 
                 ha="center", va="bottom", fontsize=10, color="black")

plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.title("Degree Distribution of Paris Metro Network")
plt.xticks(np.arange(min(degrees), max(degrees) + 1, 1))  # Ensure only integer ticks on x-axis
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

print(f"Average Degree: {avg_degree:.2f}")

# Network Diameter
diameter = nx.diameter(G)
print(f"Network Diameter: {diameter}")

# Network Density
density = nx.density(G)
print(f"Network Density: {density:.4f}")

# Network Efficiency (Latora & Marchiori)
efficiencies = []
for source in G.nodes():
    lengths = nx.single_source_dijkstra_path_length(G, source, weight="weight")
    inv_lengths = [1 / l for l in lengths.values() if l > 0]  # Ignore self-distance
    efficiencies.extend(inv_lengths)

network_efficiency = sum(efficiencies) / (len(G.nodes()) * (len(G.nodes()) - 1))
print(f"Network Efficiency: {network_efficiency:.4f}")

# Clustering Coefficient
clustering = nx.average_clustering(G, weight="weight")
print(f"Average Clustering Coefficient: {clustering:.4f}")

if nx.is_connected(G):
    avg_shortest_path = nx.average_shortest_path_length(G, weight="weight")
    print(f"Average Shortest Path Length: {avg_shortest_path:.2f}")
else:
    print("Graph is not connected. Shortest path length undefined.")

# Assortativity
assortativity = nx.degree_assortativity_coefficient(G)
print(f"Assortativity: {assortativity:.4f}")

print("Topological properties computed successfully.")
