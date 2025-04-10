# German Hotel Extractor

This project is designed to fetch, process, and visualize hotel data in Germany using Streamlit. It includes a Jupyter notebook for data processing and a Streamlit application for interactive data visualization.

## Project Structure

```
german-hotel-extractor
├── data
│   └── hotels_cleaned.csv       # Contains the cleaned data of hotels
├── notebooks
│   └── find_hotel.ipynb         # Jupyter notebook for fetching and processing hotel data
├── streamlit_hotels.py           # Main script for the Streamlit application
└── README.md                     # Documentation for the project
```

## Files Description

- **data/hotels_cleaned.csv**: This file contains the cleaned data of hotels, which will be used to populate the dashboard.

- **notebooks/find_hotel.ipynb**: This Jupyter notebook contains the logic for fetching and processing hotel data, including functions for calculating distances and travel times.

- **streamlit_hotels.py**: This file will be the main script for the Streamlit application. It will create an interactive dashboard to display hotel information, allowing users to filter and visualize data from the `hotels_cleaned.csv` file.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd german-hotel-extractor
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure that you have the cleaned hotel data in the `data` directory.

## Usage

To run the Streamlit application, execute the following command in your terminal:
```
streamlit run streamlit_hotels.py
```

This will start a local server, and you can view the dashboard in your web browser.

## Features

- Interactive filtering of hotel data based on various criteria.
- Visualization of hotel locations on a map.
- Display of hotel details including name, address, distance from Hamburg, and travel time.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.