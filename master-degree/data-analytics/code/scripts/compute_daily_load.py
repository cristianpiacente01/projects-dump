import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Load Data
STOPS_PATH = "../../data/processed/metro_stops.csv"
STOP_TIMES_PATH = "../../data/processed/metro_stop_times.csv"
GRAPH_PATH = "../../data/graphs/paris_metro.graphml"

# Load station information
stops_df = pd.read_csv(STOPS_PATH)[['stop_id', 'stop_name']]

# Load stop times (which contains timestamps)
stop_times_df = pd.read_csv(STOP_TIMES_PATH)[['trip_id', 'stop_id', 'arrival_time']]

# Load graph to get centrality measures
G = nx.read_graphml(GRAPH_PATH)
betweenness = nx.betweenness_centrality(G, weight='weight')
degree = nx.degree_centrality(G)

# Process Data
# Convert time column to datetime format
stop_times_df['arrival_time'] = pd.to_datetime(stop_times_df['arrival_time'], format='%H:%M:%S')

# Filters stop times for a given rush hour window
def filter_rush_hour(df, start_hour, end_hour):
    return df[(df['arrival_time'].dt.hour >= start_hour) & (df['arrival_time'].dt.hour < end_hour)]

morning_rush = filter_rush_hour(stop_times_df, 7, 10)
evening_rush = filter_rush_hour(stop_times_df, 17, 20)

# Compute station load for rush hours
morning_load = morning_rush['stop_id'].value_counts().reset_index()
morning_load.columns = ['stop_id', 'morning_count']

evening_load = evening_rush['stop_id'].value_counts().reset_index()
evening_load.columns = ['stop_id', 'evening_count']

# Total Daily Load
daily_load = stop_times_df['stop_id'].value_counts().reset_index()
daily_load.columns = ['stop_id', 'total_count']

# Merge all counts into a single DataFrame
load_df = stops_df.merge(morning_load, on='stop_id') \
    .merge(evening_load, on='stop_id') \
        .merge(daily_load, on='stop_id')

# Top 10 Stations During Peak and Total Load
top_stations = load_df.nlargest(10, 'total_count')

# Grouped Bar Chart for Load Visualization
fig, ax = plt.subplots(figsize=(14, 7))  # Wider figure for readability

bar_width = 0.3  # Width of each bar
x = np.arange(len(top_stations))  # Positions for each station

# Plot individual bars
ax.bar(x - bar_width, top_stations['morning_count'], bar_width, color='blue', label='Morning Rush (7-10 AM)')
ax.bar(x, top_stations['evening_count'], bar_width, color='red', label='Evening Rush (5-8 PM)')
ax.bar(x + bar_width, top_stations['total_count'], bar_width, color='green', label='Total Daily Load', alpha=0.6)

# Labels & Formatting
ax.set_xticks(x)
ax.set_xticklabels(top_stations['stop_name'], rotation=45, ha="right")
ax.set_ylabel("Station Load")
ax.set_title("Top 10 Busiest Stations - Load During Rush Hours and Total Daily Load")
ax.legend()

# Show with rotated text
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Hourly Load Evolution
stop_times_df['hour'] = stop_times_df['arrival_time'].dt.hour
hourly_load = stop_times_df.groupby('hour')['stop_id'].count()

plt.figure(figsize=(12, 6))
plt.plot(hourly_load.index, hourly_load.values, marker='o', linestyle='-', color='black')
plt.xlabel("Hour of the Day")
plt.ylabel("Total Station Load")
plt.title("Hourly Station Load in Paris Metro")
plt.grid(True)
plt.show()

# Load vs. Centrality Analysis
# Merge load with centrality measures
load_df['betweenness_centrality'] = load_df['stop_id'].map(betweenness)
load_df['degree_centrality'] = load_df['stop_id'].map(degree)

# Scatter Plot: Load vs. Betweenness Centrality
plt.figure(figsize=(8, 6))
plt.scatter(load_df['betweenness_centrality'], load_df['total_count'], alpha=0.6, color='blue')
plt.xlabel("Betweenness Centrality")
plt.ylabel("Total Station Load")
plt.title("Station Load vs. Betweenness Centrality")
plt.grid(True)
plt.show()

# Scatter Plot: Load vs. Degree Centrality
plt.figure(figsize=(8, 6))
plt.scatter(load_df['degree_centrality'], load_df['total_count'], alpha=0.6, color='red')
plt.xlabel("Degree Centrality")
plt.ylabel("Total Station Load")
plt.title("Station Load vs. Degree Centrality")
plt.grid(True)
plt.show()

print("Load analysis completed!")