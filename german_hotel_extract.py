import overpy
import pandas as pd
import time
import math
from concurrent.futures import ThreadPoolExecutor
from functools import partial

# Configuration
HAMBURG_COORDS = (53.5533, 9.9924)
BUS_SPEED_KMH = 60
MAX_WORKERS = 3
REQUEST_DELAY = 2
MAX_RETRIES = 3
RETRY_DELAY = 5

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km"""
    if None in (lat1, lon1, lat2, lon2):
        return float('nan')  # Return NaN for invalid coordinates
    
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def calculate_travel_time(distance_km):
    """Calculate bus travel time handling NaN values"""
    if math.isnan(distance_km):
        return "N/A"
    
    total_minutes = int((distance_km / BUS_SPEED_KMH) * 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}h {minutes}m" if hours else f"{minutes}m"

def safe_api_query(api, query):
    """Wrapper with retry logic for API calls"""
    for attempt in range(MAX_RETRIES):
        try:
            return api.query(query)
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise
            print(f"Attempt {attempt + 1} failed. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    return None

def get_valid_coordinates(item):
    """Safely extract coordinates from OSM item"""
    try:
        lat = item.lat if hasattr(item, 'lat') else getattr(item, 'center_lat', None)
        lon = item.lon if hasattr(item, 'lon') else getattr(item, 'center_lon', None)
        
        # Convert to float if not None
        lat = float(lat) if lat is not None else None
        lon = float(lon) if lon is not None else None
        
        return lat, lon
    except (ValueError, TypeError):
        return None, None

def process_osm_item(item, region_name):
    """Process individual OSM node/way with robust error handling"""
    try:
        lat, lon = get_valid_coordinates(item)
        if lat is None or lon is None:
            return None
            
        distance = haversine_distance(
            HAMBURG_COORDS[0], HAMBURG_COORDS[1],
            lat, lon)
        
        return {
            "name": item.tags.get("name", "N/A"),
            "city": item.tags.get("addr:city", "N/A"),
            "region": region_name,
            "distance_km": round(distance, 2) if not math.isnan(distance) else "N/A",
            "bus_time": calculate_travel_time(distance),
            "latitude": lat,
            "longitude": lon,
            "address": format_address(item.tags),
            "type": item.tags.get("tourism", "unknown"),
            "stars": item.tags.get("stars", "N/A"),
            "website": item.tags.get("website", "N/A"),
            "coordinates_valid": "Yes" if (lat and lon) else "No"
        }
    except Exception as e:
        print(f"Error processing item: {str(e)}")
        return None

def format_address(tags):
    """Optimized address formatting"""
    address_parts = [
        tags.get('addr:street', ''),
        tags.get('addr:housenumber', ''),
        tags.get('addr:postcode', ''),
        tags.get('addr:city', '')
    ]
    return ', '.join(filter(None, address_parts)) or "N/A"

def fetch_region_data(region_name):
    """Fetch and process data for a single region"""
    api = overpy.Overpass()
    try:
        query = f"""
        [out:json][timeout:90];
        area["name"="{region_name}"]["admin_level"="4"]->.searchArea;
        (
          node["tourism"~"hotel|guest_house|hostel"](area.searchArea);
          way["tourism"~"hotel|guest_house|hostel"](area.searchArea);
        );
        out body;
        >;
        out skel qt;
        """
        
        start_time = time.time()
        result = safe_api_query(api, query)
        if not result:
            print(f"No results for {region_name}")
            return []
            
        print(f"Fetched {len(result.nodes) + len(result.ways)} items from {region_name} in {time.time() - start_time:.1f}s")
        
        # Process items in parallel
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            processor = partial(process_osm_item, region_name=region_name)
            accommodations = list(filter(None, executor.map(processor, result.nodes + result.ways)))
        
        return accommodations
    
    except Exception as e:
        print(f"Error fetching {region_name}: {str(e)}")
        return []

def main():
    states = ["Schleswig-Holstein", "Niedersachsen", "Mecklenburg-Vorpommern"]
    all_hotels = []
    
    print(f"Starting data collection for {len(states)} regions...")
    start_time = time.time()
    
    # Process regions sequentially
    for state in states:
        region_data = fetch_region_data(state)
        all_hotels.extend(region_data)
        time.sleep(REQUEST_DELAY)
    
    if all_hotels:
        df = pd.DataFrame(all_hotels)
        
        # Data cleaning
        df = df.sort_values('distance_km')
        df = df.drop_duplicates(subset=['name', 'city', 'latitude', 'longitude'])
        
        # Save results
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
        filename = f"hotels_optimized_{timestamp}.csv"
        df.to_csv(filename, index=False)
        
        print(f"\nCompleted in {time.time() - start_time:.1f} seconds")
        print(f"Saved {len(df)} hotels to {filename}")
        
        # Display stats
        valid_coords = df[df['coordinates_valid'] == 'Yes']
        print(f"\nFound {len(valid_coords)} items with valid coordinates")
        print("Distance statistics (km):")
        print(valid_coords['distance_km'].describe())
        
        print("\nTop 5 closest to Hamburg:")
        print(valid_coords[['name', 'city', 'distance_km', 'bus_time']].head())
    else:
        print("No valid hotels found. Check API connectivity or region names.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
    except Exception as e:
        print(f"Critical error: {str(e)}")