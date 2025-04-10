import streamlit as st
import pandas as pd

# Load the cleaned hotel data
df = pd.read_csv("/workspaces/german-hotel-extractor/german-hotel-extractor/data/hotels_cleaned.csv")

# Set the title of the dashboard
st.title("Hotel Finder Dashboard")

# Sidebar for filtering options
st.sidebar.header("Filter Options")

# Filter by region
regions = df['region'].unique()
selected_region = st.sidebar.selectbox("Select a Region", regions)

# Filter by distance
max_distance = st.sidebar.slider("Max Distance (km)", 0, int(df['distance_km'].max()), int(df['distance_km'].max()))

# Filter the dataframe based on user input
filtered_hotels = df[(df['region'] == selected_region) & (df['distance_km'] <= max_distance)]

# Display the number of hotels found
st.write(f"Found {len(filtered_hotels)} hotels in {selected_region} within {max_distance} km.")

# Display the filtered hotels in a table
st.dataframe(filtered_hotels[['name', 'city', 'distance_km', 'bus_time', 'address', 'stars', 'website']])

# Display statistics
if not filtered_hotels.empty:
    st.subheader("Statistics")
    st.write("Distance Statistics (km):")
    st.write(filtered_hotels['distance_km'].describe())

    st.subheader("Top 5 Closest Hotels")
    st.write(filtered_hotels.nsmallest(5, 'distance_km')[['name', 'city', 'distance_km', 'bus_time']])