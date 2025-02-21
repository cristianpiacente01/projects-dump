import networkx as nx
import random
import matplotlib.pyplot as plt

# Load Graph
GRAPH_PATH = "../../data/graphs/paris_metro.graphml"
G = nx.read_graphml(GRAPH_PATH)

# Computes Average Degree
def compute_average_degree(graph):
    degrees = [d for _, d in graph.degree()]
    return sum(degrees) / len(degrees) if len(degrees) > 0 else 0

# Computes Percolation Threshold
def simulate_percolation(graph, removal_strategy, fraction=0.3, steps=50):
    G_temp = graph.copy()
    num_remove = int(len(G_temp) * fraction)
    step_size = max(1, num_remove // steps)

    avg_degree_values = []
    giant_component_sizes = []
    removed_nodes = []
    
    for _ in range(steps):
        if len(G_temp) == 0:
            break
        
        # Select and remove nodes
        if removal_strategy == "random":
            nodes_to_remove = random.sample(list(G_temp.nodes()), min(step_size, len(G_temp)))
        elif removal_strategy == "degree":
            degree_centralities = sorted(G_temp.degree(), key=lambda x: x[1], reverse=True)
            nodes_to_remove = [x[0] for x in degree_centralities[:step_size]]
        elif removal_strategy == "betweenness":
            betweenness = nx.betweenness_centrality(G_temp, weight='weight')
            nodes_to_remove = sorted(betweenness, key=betweenness.get, reverse=True)[:step_size]
        else:
            raise ValueError("Invalid removal strategy")

        # Remove nodes
        removed_nodes.extend(nodes_to_remove)
        G_temp.remove_nodes_from(nodes_to_remove)

        # Compute metrics
        avg_degree_values.append(compute_average_degree(G_temp))
        if len(G_temp) > 0:
            giant_component_sizes.append(len(max(nx.connected_components(G_temp), key=len)) / len(graph))
        else:
            giant_component_sizes.append(0)

    return avg_degree_values, giant_component_sizes

# Simulate Percolation
print("Simulating Percolation Process...")
avg_deg_random, gc_size_random = simulate_percolation(G, "random")
avg_deg_degree, gc_size_degree = simulate_percolation(G, "degree")
avg_deg_betweenness, gc_size_betweenness = simulate_percolation(G, "betweenness")

# Plot Percolation Threshold
plt.figure(figsize=(8, 6))
plt.plot(avg_deg_random, gc_size_random, label="Random Failures", color="blue")
plt.plot(avg_deg_degree, gc_size_degree, label="Targeted Attack (Degree)", color="red")
plt.plot(avg_deg_betweenness, gc_size_betweenness, label="Targeted Attack (Betweenness)", color="green")

plt.xlabel("Average Degree")
plt.ylabel("Size of Giant Component (Fraction)")
plt.title("Percolation Threshold of Paris Metro Network")
plt.legend()
plt.grid(True)
plt.show()

print("Percolation Analysis Completed!")
