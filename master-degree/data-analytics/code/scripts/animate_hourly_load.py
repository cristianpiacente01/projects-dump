import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Load Data
STOPS_PATH = "../../data/processed/metro_stops.csv"
STOP_TIMES_PATH = "../../data/processed/metro_stop_times.csv"
GRAPH_PATH = "../../data/graphs/paris_metro.graphml"
OUTPUT_GIF = "../../code/visualizations/metro_load_animation.gif"

# Load metro graph
G = nx.read_graphml(GRAPH_PATH)

# Extract node positions (longitude, latitude for correct display)
pos = {node: (float(G.nodes[node]['lon']), float(G.nodes[node]['lat'])) for node in G.nodes()}

# Load stop data (to map IDs to names)
stops_df = pd.read_csv(STOPS_PATH)[['stop_id']]

# Load stop times and extract hour
stop_times_df = pd.read_csv(STOP_TIMES_PATH)[['trip_id', 'stop_id', 'arrival_time']]
stop_times_df['arrival_time'] = pd.to_datetime(stop_times_df['arrival_time'], format='%H:%M:%S')
stop_times_df['hour'] = stop_times_df['arrival_time'].dt.hour

# Compute station load per hour
hourly_load_df = stop_times_df.groupby(['hour', 'stop_id']).size().reset_index(name='station_load')

# Merge with station names
hourly_load_df = hourly_load_df.merge(stops_df, on='stop_id')

# Prepare hourly load dictionary {hour: {station_id: size}}
hourly_load_dict = {}
for hour in hourly_load_df['hour'].unique():
    load_at_hour = hourly_load_df[hourly_load_df['hour'] == hour].set_index('stop_id')['station_load'].to_dict()
    hourly_load_dict[hour] = load_at_hour

# ANIMATION FUNCTION
fig, ax = plt.subplots(figsize=(10, 8))

def update(hour):
    ax.clear()
    ax.set_title(f"Paris Metro Network - Hourly Load at {hour}:00", fontsize=16, fontweight='bold', pad=15)

    # Get load at current hour
    load_values = hourly_load_dict.get(hour, {})

    # Assign node sizes based on current hour's load (normalized)
    node_sizes = [max(load_values.get(node, 5) * 0.5, 10) for node in G.nodes()]
    
    # Draw network with improved style
    nx.draw(
        G, pos, ax=ax, 
        node_size=node_sizes, 
        node_color='red', 
        edge_color="gray", 
        alpha=0.7, 
        with_labels=False, 
        linewidths=0.5
    )

# Create animation
ani = animation.FuncAnimation(fig, update, frames=sorted(hourly_load_dict.keys()), repeat=True, interval=1000)

# Save animation as GIF
ani.save(OUTPUT_GIF, writer='pillow', fps=1)

plt.show()

print(f"Animation saved as {OUTPUT_GIF}")