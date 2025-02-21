import random
import networkx as nx
import matplotlib.pyplot as plt
import folium

# Load Graph
GRAPH_PATH = "../../data/graphs/paris_metro.graphml"
G = nx.read_graphml(GRAPH_PATH)

# Get node coordinates from the graph
lat_dict = nx.get_node_attributes(G, "lat")
lon_dict = nx.get_node_attributes(G, "lon")

# Computes Network Efficiency
def compute_efficiency(graph):
    n = len(graph)
    if n <= 1:
        return 0
    path_lengths = dict(nx.all_pairs_dijkstra_path_length(graph, weight='weight'))
    efficiency = sum(1 / path_lengths[u][v] for u in graph for v in graph if u != v and v in path_lengths[u])
    return efficiency / (n * (n - 1))

# Simulates network failure scenarios by removing nodes using a specified strategy
def simulate_removal(graph, removal_strategy, fraction=0.3):
    G_temp = graph.copy()
    num_remove = int(len(G_temp) * fraction)
    
    efficiency_values = []
    largest_component_sizes = []
    removed_nodes = []

    for _ in range(num_remove):
        if len(G_temp) == 0:
            break
        
        # Select node based on strategy
        if removal_strategy == "random":
            node_to_remove = random.choice(list(G_temp.nodes()))
        elif removal_strategy == "degree":
            node_to_remove = max(G_temp.degree, key=lambda x: x[1])[0]  # Max degree
        elif removal_strategy == "betweenness":
            betweenness = nx.betweenness_centrality(G_temp, weight='weight')
            node_to_remove = max(betweenness, key=betweenness.get)
        else:
            raise ValueError("Invalid removal strategy")

        # Remove node and store it
        removed_nodes.append(node_to_remove)
        G_temp.remove_node(node_to_remove)
        efficiency_values.append(compute_efficiency(G_temp))
        largest_component_sizes.append(len(max(nx.connected_components(G_temp), key=len)) / len(graph))

    return efficiency_values, largest_component_sizes, removed_nodes

# Plots the network with removed nodes highlighted and a legend
def plot_network_on_map(graph, removed_nodes, filename):
    metro_map = folium.Map(location=[48.8566, 2.3522], zoom_start=12, tiles="OpenStreetMap")

    # Draw edges
    for u, v, _ in graph.edges(data=True):
        lat1, lon1 = lat_dict[u], lon_dict[u]
        lat2, lon2 = lat_dict[v], lon_dict[v]
        folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="gray", weight=2, opacity=0.6).add_to(metro_map)

    # Draw remaining nodes
    for node in graph.nodes():
        if node in removed_nodes:
            color = "black"  # Removed nodes in black
            size = 10
        else:
            color = "blue"  # Remaining nodes in blue
            size = 5
        
        folium.CircleMarker(
            location=[lat_dict[node], lon_dict[node]],
            radius=size,
            color="black",
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=f"<b>{node}</b>"
        ).add_to(metro_map)

    # Add a legend explaining the removed nodes
    legend_html = f'''
     <div style="position: fixed;
                 bottom: 50px; left: 50px; width: 250px; height: 70px;
                 background-color: white; z-index:9999; font-size:14px;
                 padding: 10px; border: 2px solid gray; border-radius: 5px;">
     <b>Legend {'Degree' if 'degree' in filename else 'Betweenness'} Attack</b><br>
     <i class="fa fa-circle" style="color: black"></i> Removed Stations<br>
     <i class="fa fa-circle" style="color: blue"></i> Remaining Stations
     </div>
     '''
    
    metro_map.get_root().html.add_child(folium.Element(legend_html))

    # Save the map
    metro_map.save(f"../../code/visualizations/{filename}")
    print(f"Map saved: {filename}")

if __name__ == '__main__':
    # Simulating Failures
    print("Simulating Random Failures...")
    eff_random, size_random, removed_random = simulate_removal(G, "random")

    print("Simulating Targeted Degree-Based Attack...")
    eff_degree, size_degree, removed_degree = simulate_removal(G, "degree")

    print("Simulating Targeted Betweenness-Based Attack...")
    eff_betweenness, size_betweenness, removed_betweenness = simulate_removal(G, "betweenness")

    # Plotting Efficiency Decrease
    plt.figure(figsize=(10, 6))
    plt.plot(eff_random, label="Random Failures", color="blue")
    plt.plot(eff_degree, label="Targeted Attack (Degree)", color="red")
    plt.plot(eff_betweenness, label="Targeted Attack (Betweenness)", color="green")
    plt.xlabel("Number of Removed Stations")
    plt.ylabel("Network Efficiency")
    plt.title("Impact of Node Removal on Network Efficiency")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plotting Largest Component Size
    plt.figure(figsize=(10, 6))
    plt.plot(size_random, label="Random Failures", color="blue")
    plt.plot(size_degree, label="Targeted Attack (Degree)", color="red")
    plt.plot(size_betweenness, label="Targeted Attack (Betweenness)", color="green")
    plt.xlabel("Number of Removed Stations")
    plt.ylabel("Fraction of Largest Connected Component")
    plt.title("Impact of Node Removal on Network Connectivity")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot Graphs After Attack on OpenStreetMap
    plot_network_on_map(G, removed_degree, "network_after_degree_attack.html")
    plot_network_on_map(G, removed_betweenness, "network_after_betweenness_attack.html")

    print("Failure Simulations Completed!")
