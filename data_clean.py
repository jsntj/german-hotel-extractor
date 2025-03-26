import pandas as pd
import unicodedata

def clean_german_text(text):
    """Normalize German text and fix common encoding issues"""
    if pd.isna(text):
        return text
    text = str(text)
    # Fix common mojibake for German characters
    replacements = {
        'ÃŸ': 'ß', 'Ã ': 'à', 'Ã¡': 'á', 'Ã¢': 'â', 'Ã¤': 'ä',
        'Ã§': 'ç', 'Ã¨': 'è', 'Ã©': 'é', 'Ãª': 'ê', 'Ã«': 'ë',
        'Ã¬': 'ì', 'Ã­': 'í', 'Ã®': 'î', 'Ã¯': 'ï', 'Ã°': 'ð',
        'Ã±': 'ñ', 'Ã²': 'ò', 'Ã³': 'ó', 'Ã´': 'ô', 'Ã¶': 'ö',
        'Ã·': '÷', 'Ã¸': 'ø', 'Ã¹': 'ù', 'Ãº': 'ú', 'Ã»': 'û',
        'Ã¼': 'ü', 'Ã½': 'ý', 'Ãþ': 'þ'
    }
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    # Normalize unicode
    text = unicodedata.normalize('NFKC', text)
    return text.strip()

# Try multiple encodings to read the file
encodings = ['utf-8', 'latin1', 'cp1252']
df = None

for encoding in encodings:
    try:
        df = pd.read_csv('hotels_optimized_20250326_0925.csv', encoding=encoding)
        print(f"Successfully read with {encoding} encoding")
        break
    except UnicodeDecodeError:
        continue

if df is None:
    raise ValueError("Failed to read file with tried encodings")

# Clean text columns that might contain German characters
text_columns = ['name', 'address', 'region', 'city']  # adjust as needed
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].apply(clean_german_text)

# Remove rows where 'name' is NA (including 'N/A', empty strings, pandas NA, etc.)
df = df[~df['name'].isna()]  # Remove pandas NA/NaN
df = df[df['name'].astype(str) != 'N/A']  # Remove string 'N/A'
df = df[df['name'].astype(str) != '']  # Remove empty strings if needed

# Save the cleaned dataset with proper encoding
df.to_csv('cleaned_dataset.csv', index=False, encoding='utf-8-sig')

# Print summary
original_count = len(df) + sum(df['name'].astype(str).str.upper().str.contains('N/A')) + sum(df['name'].isna())
print(f"Original rows: {original_count}")
print(f"Rows after cleaning: {len(df)}")
print("Rows with NA values in name column have been removed and German characters normalized.")