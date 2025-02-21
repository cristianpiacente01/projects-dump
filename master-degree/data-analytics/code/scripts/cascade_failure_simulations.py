import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium

from failure_simulations import compute_efficiency

# Load Data
STOPS_PATH = "../../data/processed/metro_stops.csv"
GRAPH_PATH = "../../data/graphs/paris_metro.graphml"

# Load graph
G = nx.read_graphml(GRAPH_PATH)

# Extract stop data to get names and coordinates
stops_df = pd.read_csv(STOPS_PATH)[['stop_id', 'stop_name', 'stop_lat', 'stop_lon']]
stop_id_to_name = dict(zip(stops_df['stop_id'], stops_df['stop_name']))
stop_id_to_coords = dict(zip(stops_df['stop_id'], zip(stops_df['stop_lat'], stops_df['stop_lon'])))

# Simulates cascading failures using betweenness centrality with a given failure threshold
def simulate_cascade_failures(graph, failure_threshold=0.1):
    efficiency_values = [compute_efficiency(graph)]
    largest_component_values = [len(max(nx.connected_components(graph), key=len)) / graph.number_of_nodes()]
    failed_nodes_cumulative = set()
    failed_nodes_list = []

    iteration = 1  # Start index from 1
    while True:
        if len(graph) == 0:
            break  # Stop if graph is empty

        betweenness = nx.betweenness_centrality(graph, weight="weight")
        
        # Determine failure threshold
        max_betweenness = max(betweenness.values())
        threshold_value = max_betweenness * failure_threshold
        
        # Find nodes exceeding threshold
        failed_nodes = [node for node, value in betweenness.items() if value >= threshold_value]
        
        # Stop if no more nodes fail
        if not failed_nodes:
            break

        # Add failed nodes to cumulative set before removing them
        failed_nodes_cumulative.update(failed_nodes)
        failed_nodes_list.append(failed_nodes)

        # Remove failed nodes
        graph.remove_nodes_from(failed_nodes)

        # Record new network efficiency
        efficiency_values.append(compute_efficiency(graph))

        # Check if graph is empty before computing the largest component
        if len(graph) > 0:
            largest_component_values.append(len(max(nx.connected_components(graph), key=len)) / G.number_of_nodes())
        else:
            largest_component_values.append(0)  # If empty, largest component fraction is 0

        # Stop the iteration if removing nodes results in an empty graph
        if len(graph) == 0:
            visualize_failed_nodes(failed_nodes_cumulative, failed_nodes, iteration)
            break  # Break before an extra iteration occurs

        # Visualization: Map failed nodes at each step with legend
        visualize_failed_nodes(failed_nodes_cumulative, failed_nodes, iteration)

        iteration += 1

    return efficiency_values, largest_component_values, failed_nodes_list

# OpenStreetMap visualization of failed nodes with a legend
def visualize_failed_nodes(failed_nodes_cumulative, failed_nodes, iteration):
    paris_map = folium.Map(location=[48.8566, 2.3522], zoom_start=12, tiles="OpenStreetMap")

    # Add nodes
    for node in stop_id_to_coords:
        lat, lon = stop_id_to_coords.get(node, (None, None))
        if lat is not None and lon is not None:
            station_name = stop_id_to_name.get(node, "Unknown Station")

            # Color nodes:
            if node in failed_nodes:  # Nodes that failed in this iteration (RED)
                color = "red"
            elif node in failed_nodes_cumulative:  # Nodes that failed previously (GRAY)
                color = "gray"
            else:  # Active nodes (BLUE)
                color = "blue"
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                color="black",
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                tooltip=f"{station_name} ({'Failed' if color != 'blue' else 'Active'})"
            ).add_to(paris_map)

    # Add Legend
    legend_html = f"""
     <div style="position: fixed;
                 bottom: 50px; left: 50px; width: 200px; height: 120px;
                 background-color: white; z-index:9999; font-size:14px;
                 border:2px solid gray; padding: 10px;">
     <b>Iteration {iteration}</b><br>
     <svg width="10" height="10"><circle cx="5" cy="5" r="5" fill="blue" /></svg> Active Stations <br>
     <svg width="10" height="10"><circle cx="5" cy="5" r="5" fill="red" /></svg> Failed This Iteration <br>
     <svg width="10" height="10"><circle cx="5" cy="5" r="5" fill="gray" /></svg> Previously Failed <br>
     </div>
    """
    paris_map.get_root().html.add_child(folium.Element(legend_html))

    # Save map
    map_filename = f"../../code/visualizations/cascade_iteration_{iteration}.html"
    paris_map.save(map_filename)
    print(f"Saved: {map_filename}")

# Execute Simulation
efficiency_values, largest_component_values, failed_nodes_list = simulate_cascade_failures(G)

# Plot Results
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(efficiency_values) + 1), efficiency_values, 'r-', marker='o', label="Network Efficiency")
plt.xlabel("Iteration")
plt.ylabel("Efficiency")
plt.title("Network Efficiency Over Failure Cascade")
plt.legend()
plt.grid(True)
plt.xticks(range(1, len(efficiency_values) + 1))
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(largest_component_values) + 1), largest_component_values, 'b-', marker='o', label="Largest Component (Fraction of Total)")
plt.xlabel("Iteration")
plt.ylabel("Fraction of Largest Connected Component")
plt.title("Largest Component Size Over Failure Cascade")
plt.legend()
plt.grid(True)
plt.xticks(range(1, len(largest_component_values) + 1))
plt.show()

# Failure Data
failures_table = pd.DataFrame({
    "Iteration": range(1, len(failed_nodes_list) + 1),
    "Failed Stations": [len(f) for f in failed_nodes_list]
})
print("\nIterations with Number of Failed Stations:")
print(failures_table.to_string(index=False))
