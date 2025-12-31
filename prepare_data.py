import pandas as pd
import json
import numpy as np
from datetime import datetime

# Read the Excel file
df = pd.read_excel('tetra_pak_final_data_finish.xlsx')

# Convert Transaction Date to string format for JSON
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
df = df.dropna(subset=['Transaction Date'])
df['Transaction Date'] = df['Transaction Date'].dt.strftime('%Y-%m-%d')

# Convert numeric columns
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)

# Fill missing values
df['Quantity unit'] = df['Quantity unit'].astype(str).str.strip().fillna('Unknown')
df['category_group'] = df['category_group'].astype(str).fillna('Unknown')
df['standardized_name'] = df['standardized_name'].astype(str).fillna('Unknown')

# Get supplier column name (it might be 'Supplier Name' or similar)
supplier_cols = [col for col in df.columns if 'supplier' in col.lower() or 'vendor' in col.lower()]
if supplier_cols:
    supplier_col = supplier_cols[0]
    df['Supplier'] = df[supplier_col].astype(str).fillna('Unknown')
else:
    # If no supplier column, try to infer from standardized_name
    df['Supplier'] = df['standardized_name']

# CRITICAL: Replace ALL NaN, inf, and -inf values with None (which becomes null in JSON)
# This is the fix for the JSON parsing error
df = df.replace([np.nan, np.inf, -np.inf], None)

# Convert to JSON
data_json = df.to_dict('records')

# Save to JSON file with proper handling of None values
with open('tetra_pak_data.json', 'w') as f:
    json.dump(data_json, f, allow_nan=False)

print(f"Data exported successfully!")
print(f"Total records: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"Date range: {df['Transaction Date'].min()} to {df['Transaction Date'].max()}")
print(f"Unique Quantity units: {df['Quantity unit'].unique()[:10]}")
print(f"Unique category_groups: {df['category_group'].unique()[:10]}")
