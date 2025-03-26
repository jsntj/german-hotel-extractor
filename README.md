# german-hotel-extractor
Overview
This project cleans and preprocesses hotel location data containing German special characters (ä, ö, ü, ß). The script handles encoding issues, removes invalid entries, and ensures proper formatting for analysis.

🛠 Key Tasks Performed
Character Encoding Fixes

Corrects mojibake (corrupted characters) in German text (e.g., "MÃ¼hlenstraÃŸe" → "Mühlenstraße")

Handles special characters through Unicode normalization

Data Cleaning

Removes rows with:

Missing values (NA) in the hotel name field

"N/A" placeholders (case insensitive)

Empty name strings

Robust File Handling

Automatic detection of file encoding (UTF-8, Latin1, Windows-1252)

Outputs Excel-compatible CSV with BOM (UTF-8-sig)

📂 Files
hotel_data_cleaner.py: Main cleaning script

hotels_optimized_[date].csv: Raw input file

cleaned_dataset.csv: Processed output

🚀 Usage
bash
Copy
python hotel_data_cleaner.py
💡 Technical Notes
Preserves all valid data columns unchanged

Provides row count before/after cleaning

Specifically designed for German location data
