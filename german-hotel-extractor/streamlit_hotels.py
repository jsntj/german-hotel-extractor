import streamlit as st
import pandas as pd
import os
import numpy as np

# Set the title of the dashboard
st.title("Hotel Finder Dashboard")

# Path to the data file
data_file_path = "/workspaces/german-hotel-extractor/german-hotel-extractor/data/hotels_cleaned.csv"

# Check if the file exists
if not os.path.exists(data_file_path):
    st.error(f"Data file not found at: {data_file_path}. Please ensure the file exists.")
else:
    # Load the cleaned hotel data
    df = pd.read_csv(data_file_path)

    # Convert bus_time to numeric (assuming it's in minutes, e.g., "10m" -> 10)
    df['bus_time_minutes'] = df['bus_time'].str.extract(r'(\d+)').astype(float)

    # Create hour groups for bus time
    bins = [0, 60, 120, 180, np.inf]  # Define bins for 0-1hr, 1hr-2hr, etc.
    labels = ["0-1hr", "1hr-2hr", "2hr-3hr", "3hr+"]
    df['bus_time_group'] = pd.cut(df['bus_time_minutes'], bins=bins, labels=labels, right=False)

    # Sidebar for filtering options
    st.sidebar.header("Filter Options")

    # Filter by region
    regions = df['region'].unique()
    selected_region = st.sidebar.selectbox("Select a Region", regions)

    # Filter by distance
    max_distance = st.sidebar.slider("Max Distance (km)", 0, int(df['distance_km'].max()), int(df['distance_km'].max()))

    # Filter by bus time group
    bus_time_groups = df['bus_time_group'].unique()
    selected_bus_time_group = st.sidebar.selectbox("Select Bus Time Group", bus_time_groups)

    # Filter the dataframe based on user input
    filtered_hotels = df[
        (df['region'] == selected_region) &
        (df['distance_km'] <= max_distance) &
        (df['bus_time_group'] == selected_bus_time_group)
    ]

    # Display the number of hotels found
    st.write(f"Found {len(filtered_hotels)} hotels in {selected_region} within {max_distance} km and bus time group {selected_bus_time_group}.")

    # Display the filtered hotels in a table
    if not filtered_hotels.empty:
        st.dataframe(filtered_hotels[['name', 'city', 'distance_km', 'bus_time', 'address', 'stars', 'website']])

        # Display statistics
        st.subheader("Statistics")
        st.write("Distance Statistics (km):")
        st.write(filtered_hotels['distance_km'].describe())

        st.subheader("Top 5 Closest Hotels")
        st.write(filtered_hotels.nsmallest(5, 'distance_km')[['name', 'city', 'distance_km', 'bus_time']])

        # Display map of hotels
        st.subheader("Map of Hotels")
        if 'latitude' in filtered_hotels.columns and 'longitude' in filtered_hotels.columns:
            st.map(filtered_hotels[['latitude', 'longitude']])
        else:
            st.warning("Latitude and Longitude columns are missing in the dataset.")
    else:
        st.warning("No hotels match the selected criteria.")