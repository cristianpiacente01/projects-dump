import pandas as pd
import os

# Corrects times by applying modulo 24 to the hour part.
def fix_time_format(time_str):
    try:
        h, m, s = map(int, time_str.split(":"))
        h = h % 24  # Apply modulo to wrap around 24-hour format
        return f"{h:02d}:{m:02d}:{s:02d}"
    except:
        return time_str  # Return original if there's an issue

# Filters GTFS data to keep only Metro lines, related trips, stops, stop times, and transfers, merging duplicate stops.
def filter_metro_data():
    # Define paths
    raw_data_path = "../../data/raw/"
    processed_data_path = "../../data/processed/"

    # Ensure processed data directory exists
    os.makedirs(processed_data_path, exist_ok=True)

    # Load datasets
    routes = pd.read_csv(os.path.join(raw_data_path, "routes.csv"))
    trips = pd.read_csv(os.path.join(raw_data_path, "trips.csv"))
    stop_times = pd.read_csv(os.path.join(raw_data_path, "stop_times.csv"))
    stops = pd.read_csv(os.path.join(raw_data_path, "stops.csv"))
    transfers = pd.read_csv(os.path.join(raw_data_path, "transfers.csv"))

    # STEP 1: FILTER METRO ROUTES (route_type == 1)
    metro_routes = routes[routes["route_type"] == 1]
    metro_route_ids = metro_routes["route_id"].unique()

    # STEP 2: FILTER METRO TRIPS
    metro_trips = trips[trips["route_id"].isin(metro_route_ids)]
    metro_trip_ids = metro_trips["trip_id"].unique()

    # STEP 3: FILTER METRO STOP TIMES
    metro_stop_times = stop_times[stop_times["trip_id"].isin(metro_trip_ids)]
    metro_stop_ids = metro_stop_times["stop_id"].unique()

    # Apply time correction to arrival_time and departure_time
    metro_stop_times["arrival_time"] = metro_stop_times["arrival_time"].apply(fix_time_format)
    metro_stop_times["departure_time"] = metro_stop_times["departure_time"].apply(fix_time_format)

    # STEP 4: FILTER METRO STOPS
    metro_stops = stops[stops["stop_id"].isin(metro_stop_ids)]

    # STEP 5: FILTER METRO TRANSFERS (Only keep transfers within Metro stops)
    metro_transfers = transfers[
        (transfers["from_stop_id"].isin(metro_stop_ids)) & 
        (transfers["to_stop_id"].isin(metro_stop_ids))
    ].copy()

    # STEP 6: REMOVE DUPLICATE STOPS BY NAME & UPDATE ALL REFERENCES
    stop_mapping = {}  # Dictionary to store first occurrence of each stop name
    unique_stops = []  

    for _, stop in metro_stops.iterrows():
        stop_name = stop["stop_name"]
        
        # If this stop name was seen before, map it to the first occurrence
        if stop_name in stop_mapping:
            stop_mapping[stop["stop_id"]] = stop_mapping[stop_name]
        else:
            stop_mapping[stop["stop_id"]] = stop["stop_id"]
            stop_mapping[stop_name] = stop["stop_id"]  # Save first occurrence
            unique_stops.append(stop)

    # Convert the list back to a DataFrame
    metro_stops_cleaned = pd.DataFrame(unique_stops)

    # Ensure metro_transfers exists before modifying it
    if metro_transfers is not None and not metro_transfers.empty:
        # STEP 7: APPLY THE MAPPING TO OTHER DATASETS
        metro_stop_times["stop_id"] = metro_stop_times["stop_id"].map(lambda x: stop_mapping.get(x, x))
        metro_transfers["from_stop_id"] = metro_transfers["from_stop_id"].map(lambda x: stop_mapping.get(x, x))
        metro_transfers["to_stop_id"] = metro_transfers["to_stop_id"].map(lambda x: stop_mapping.get(x, x))

        # STEP 8: RE-FILTER METRO TRANSFERS (now using the cleaned stops)
        unique_stop_ids = set(metro_stops_cleaned["stop_id"].unique())
        metro_transfers = metro_transfers[
            (metro_transfers["from_stop_id"].isin(unique_stop_ids)) &
            (metro_transfers["to_stop_id"].isin(unique_stop_ids))
        ]

        # STEP 9: REMOVE SELF-LOOPS IN TRANSFERS (after merging stops)
        metro_transfers = metro_transfers[metro_transfers["from_stop_id"] != metro_transfers["to_stop_id"]]

    # Save cleaned datasets in data/processed/
    metro_stop_times.to_csv(os.path.join(processed_data_path, "metro_stop_times.csv"), index=False)
    metro_stops_cleaned.to_csv(os.path.join(processed_data_path, "metro_stops.csv"), index=False)
    
    # Only save metro_transfers if it exists and is not empty
    if metro_transfers is not None and not metro_transfers.empty:
        metro_transfers.to_csv(os.path.join(processed_data_path, "metro_transfers.csv"), index=False)

    print("Metro data filtered and deduplicated successfully!")
    print(f"Metro Routes: {metro_routes.shape}")
    print(f"Metro Trips: {metro_trips.shape}")
    print(f"Metro Stop Times: {metro_stop_times.shape}")
    print(f"Metro Stops (after deduplication): {metro_stops_cleaned.shape}")
    print(f"Metro Transfers: {metro_transfers.shape if 'metro_transfers' in locals() else 'Skipped (No Data)'}")

if __name__ == "__main__":
    filter_metro_data()