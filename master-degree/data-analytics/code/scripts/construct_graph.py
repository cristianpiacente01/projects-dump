import os
import pandas as pd
import networkx as nx
import folium
import branca.colormap as cm

# Paths
DATA_PATH = "../../data/processed/"
GRAPH_OUTPUT_DIR = "../../data/graphs/"
VISUALIZATION_OUTPUT_DIR = "../../code/visualizations/"

# Ensure output directories exist
os.makedirs(GRAPH_OUTPUT_DIR, exist_ok=True)
os.makedirs(VISUALIZATION_OUTPUT_DIR, exist_ok=True)

# Load Processed GTFS Data
stops = pd.read_csv(os.path.join(DATA_PATH, "metro_stops.csv"))
stop_times = pd.read_csv(os.path.join(DATA_PATH, "metro_stop_times.csv"))
transfers = pd.read_csv(os.path.join(DATA_PATH, "metro_transfers.csv"))

# Ensure datetime parsing for travel times
stop_times["arrival_time"] = pd.to_datetime(stop_times["arrival_time"], format="%H:%M:%S")
stop_times["departure_time"] = pd.to_datetime(stop_times["departure_time"], format="%H:%M:%S")

# Create Undirected Weighted Graph
G = nx.Graph()

# Add Stations as Nodes (Separate Latitude & Longitude)
for _, stop in stops.iterrows():
    G.add_node(
        stop["stop_id"], 
        name=stop["stop_name"], 
        lat=stop["stop_lat"], 
        lon=stop["stop_lon"]
    )

# Add Edges Based on Stop Sequences (Weighted by Travel Time)
for trip_id, group in stop_times.groupby("trip_id"):
    group = group.sort_values("stop_sequence")
    stop_sequence = group["stop_id"].tolist()
    travel_times = (group["departure_time"].diff().dt.total_seconds() / 60).fillna(1).tolist()

    for i in range(len(stop_sequence) - 1):
        from_stop, to_stop = stop_sequence[i], stop_sequence[i + 1]
        travel_time = max(1, travel_times[i + 1])  # Ensure minimum weight of 1 min

        # If edge exists, keep the minimum travel time
        if G.has_edge(from_stop, to_stop):
            G[from_stop][to_stop]['weight'] = min(G[from_stop][to_stop]['weight'], travel_time)
        else:
            G.add_edge(from_stop, to_stop, weight=travel_time)

# Add Transfer Edges (Weighted by Minimum Transfer Time)
for _, row in transfers.iterrows():
    from_stop, to_stop = row["from_stop_id"], row["to_stop_id"]
    transfer_time = max(1, row["min_transfer_time"] / 60)  # Convert seconds to minutes

    # If edge exists, keep the minimum transfer time
    if G.has_edge(from_stop, to_stop):
        G[from_stop][to_stop]['weight'] = min(G[from_stop][to_stop]['weight'], transfer_time)
    else:
        G.add_edge(from_stop, to_stop, weight=transfer_time)

# Save Graph
graph_path = os.path.join(GRAPH_OUTPUT_DIR, "paris_metro.graphml")
nx.write_graphml(G, graph_path)
print(f"Graph saved: {graph_path}")

# Interactive Map Visualization
def save_folium_map(graph, filename):
    # Map style
    metro_map = folium.Map(
        location=[48.8566, 2.3522], 
        zoom_start=12, 
        tiles="OpenStreetMap"
    )

    # Extract lat/lon and name
    lat_dict = nx.get_node_attributes(graph, "lat")
    lon_dict = nx.get_node_attributes(graph, "lon")
    name_dict = nx.get_node_attributes(graph, "name")

    # Collect travel times for color mapping
    travel_time_values = [d["weight"] for _, _, d in graph.edges(data=True)]
    colormap = cm.LinearColormap(["blue", "orange", "red"], vmin=min(travel_time_values), vmax=max(travel_time_values))
    
    # Add Nodes (Stations) with Hover Tooltip
    for node in graph.nodes():
        folium.CircleMarker(
            location=[lat_dict[node], lon_dict[node]],
            radius=4,
            color="black",
            fill=True,
            fill_color="blue",
            fill_opacity=0.8,
            popup=f"<b>Station:</b> {name_dict[node]}<br><b>Lat:</b> {lat_dict[node]}<br><b>Lon:</b> {lon_dict[node]}",
        ).add_to(metro_map)
    
    # Add Edges (Metro Connections) with color-coded travel times
    for u, v, data in graph.edges(data=True):
        lat1, lon1 = lat_dict[u], lon_dict[u]
        lat2, lon2 = lat_dict[v], lon_dict[v]
        travel_time = data["weight"]

        folium.PolyLine(
            [(lat1, lon1), (lat2, lon2)],
            color=colormap(travel_time),
            weight=3,
            opacity=0.8,
            tooltip=f"<b>From:</b> {name_dict[u]}<br><b>To:</b> {name_dict[v]}<br><b>Travel Time:</b> {travel_time:.1f} min"
        ).add_to(metro_map)

    # Add Color Legend
    colormap.caption = "Travel Time (minutes)"
    metro_map.add_child(colormap)

    # Save the map
    output_file = os.path.join(VISUALIZATION_OUTPUT_DIR, filename)
    metro_map.save(output_file)
    print(f"Saved: {output_file}")

save_folium_map(G, "paris_metro_graph.html")

print("Interactive map saved!")
