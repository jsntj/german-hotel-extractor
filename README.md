# german-hotel-extractor

# Hotel Data Extractor for Germany
📌 Project Overview
This Python script extracts comprehensive hotel and accommodation data across Germany, with special features for analyzing properties relative to Hamburg. It gathers:

Basic hotel information (names, addresses, contact details)

Location data with coordinates

Distance calculations from Hamburg

Estimated bus travel times

Water proximity analysis

🌟 Key Features
Copy
1. Multi-Source Data Collection
   - OpenStreetMap API integration
   - Handles both point (nodes) and area (ways) data types

2. Advanced Location Analytics
   - Haversine distance calculations
   - Bus travel time estimates (60km/h average)
   - Waterfront property detection (1km threshold)

3. Data Processing
   - Parallel processing with ThreadPoolExecutor
   - Automatic duplicate removal
   - Robust error handling and retries

4. Output
   - Clean CSV exports with timestamps
   - Data validation flags
   - Summary statistics
🛠 Technical Implementation
python
Copy
- Python 3.8+
- Required Packages:
  • overpy (OpenStreetMap API)
  • pandas (data processing)
  • concurrent.futures (parallel processing)
- Modular architecture with 8 core functions
📊 Sample Data Output
name	city	distance_km	bus_time	is_near_water
Hotel Hafen	Hamburg	0.0	0m	Yes
Ostsee Resort	Lübeck	58.2	58m	Yes
Berlin Plaza	Berlin	255.9	4h16m	No
🚀 Getting Started
Install requirements:

bash
Copy
pip install overpy pandas
Run the extractor:

bash
Copy
python hotel_extractor.py
Outputs:

hotels_optimized_<timestamp>.csv

Console summary statistics

📈 Potential Enhancements
Copy
• Add booking.com API integration (requires API key)
• Implement hotel price monitoring
• Add interactive map visualization
• Expand to other European cities
