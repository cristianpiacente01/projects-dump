import os
import networkx as nx
import pandas as pd
import numpy as np
import folium
import branca.colormap as cm

# Load Data
GRAPH_PATH = "../../data/graphs/paris_metro.graphml"
STOPS_PATH = "../../data/processed/metro_stops.csv"
output_dir = "../../code/visualizations/"
os.makedirs(output_dir, exist_ok=True)

G = nx.read_graphml(GRAPH_PATH)
stops_df = pd.read_csv(STOPS_PATH)[['stop_id', 'stop_name']]  # Load station names

# Compute Centrality Measures
print("\nComputing Centrality Measures...")

degree = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G, weight='weight')
closeness = nx.closeness_centrality(G, distance='weight')
eigenvector = nx.eigenvector_centrality_numpy(G)
pagerank = nx.pagerank(G)

# Extract latitude and longitude from the graph
lat_dict = nx.get_node_attributes(G, "lat")
lon_dict = nx.get_node_attributes(G, "lon")

# Convert to DataFrame
centrality_df = pd.DataFrame({
    "Station": list(G.nodes()),
    "Degree_Centrality": list(degree.values()),
    "Betweenness_Centrality": list(betweenness.values()),
    "Closeness_Centrality": list(closeness.values()),
    "Eigenvector_Centrality": list(eigenvector.values()),
    "PageRank_Centrality": list(pagerank.values()),
    "stop_lat": [lat_dict[node] for node in G.nodes()],  # Get lat from graph
    "stop_lon": [lon_dict[node] for node in G.nodes()]   # Get lon from graph
})

# Merge station names
centrality_df = centrality_df.merge(stops_df, left_on="Station", right_on="stop_id")
centrality_df = centrality_df.drop(columns=["stop_id"])

# Compute Spectral Gap & Algebraic Connectivity
print("\nComputing Spectral Properties...")
L = nx.laplacian_matrix(G).toarray()
eigenvalues = np.linalg.eigvalsh(L)
eigenvalues = sorted(eigenvalues)

spectral_gap = eigenvalues[1] - eigenvalues[0]
algebraic_connectivity = eigenvalues[1]

print("\nSpectral Analysis of Paris Metro Network:")
print(f"Spectral Gap: {spectral_gap:.6f}")
print(f"Algebraic Connectivity: {algebraic_connectivity:.6f}")

# Identify Bottleneck Stations (Lowest Degree)
print("\nIdentifying Bottleneck Stations...")
degree_df = centrality_df[['stop_name', 'Degree_Centrality']].sort_values(by="Degree_Centrality")

print("\nTop 10 Bottleneck Stations (Lowest Degree):")
print(degree_df.head(10).to_string(index=False))

# Compute Efficiency Drop for Key Stations
print("\nComputing Network Efficiency Impact...")

original_efficiency = nx.global_efficiency(G)
removal_impact = []

for station in centrality_df.sort_values(by="Betweenness_Centrality", ascending=False).head(10)['stop_name']:
    station_id = stops_df[stops_df['stop_name'] == station]['stop_id'].values[0]
    
    G_temp = G.copy()
    G_temp.remove_node(station_id)
    new_efficiency = nx.global_efficiency(G_temp)
    efficiency_drop = (original_efficiency - new_efficiency) / original_efficiency * 100
    removal_impact.append((station, efficiency_drop))

removal_impact_df = pd.DataFrame(removal_impact, columns=['Station', 'Efficiency Drop (%)'])
removal_impact_df = removal_impact_df.sort_values(by="Efficiency Drop (%)", ascending=False)

print("\nEfficiency Impact of Removing Top 10 Central Stations:")
print(removal_impact_df.to_string(index=False))

# Top Stations by Centralities
top_metrics = ["Degree_Centrality", "Betweenness_Centrality", "Closeness_Centrality", "Eigenvector_Centrality", "PageRank_Centrality"]

for metric in top_metrics:
    print(f"\nTop 10 Stations by {metric.replace('_', ' ')}:")
    print(centrality_df.sort_values(by=metric, ascending=False)[["stop_name", metric]].head(10).to_string(index=False))

# Centrality Visualization Maps
print("\nCreating Centrality Visualization Maps...")

for metric in top_metrics:
    print(f"Generating {metric} visualization...")

    metro_map = folium.Map(location=[48.8566, 2.3522], zoom_start=12, tiles="OpenStreetMap")
    centrality_values = np.array(centrality_df[metric])
    min_c, max_c = centrality_values.min(), centrality_values.max()
    colormap = cm.LinearColormap(["blue", "orange", "red"], vmin=min_c, vmax=max_c, caption=metric.replace("_", " "))

    for u, v, data in G.edges(data=True):
        lat1, lon1 = lat_dict[u], lon_dict[u]
        lat2, lon2 = lat_dict[v], lon_dict[v]
        folium.PolyLine(
            [(lat1, lon1), (lat2, lon2)],
            color="gray",
            weight=2,
            opacity=0.6,
        ).add_to(metro_map)

    for index, row in centrality_df.iterrows():
        centrality_score = row[metric]
        size = 5 + 15 * (centrality_score / max_c)

        folium.CircleMarker(
            location=[row['stop_lat'], row['stop_lon']],
            radius=size,
            color="black",
            fill=True,
            fill_color=colormap(centrality_score),
            fill_opacity=0.9,
            popup=f"<b>{row['stop_name']}</b><br>{metric.replace('_', ' ')}: {centrality_score:.4f}"
        ).add_to(metro_map)

    metro_map.add_child(colormap)
    metro_map.save(os.path.join(output_dir, f"paris_metro_{metric.lower()}.html"))
    print(f"{metric} visualization saved!")

print("All visualizations saved!")