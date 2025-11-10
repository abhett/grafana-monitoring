import pandas as pd

# Read the CSV file
file_path = 'MySQL_Grafana_Monitoring/Nifty Bank Historical Data (1).csv'  # Replace with your actual CSV file path
df = pd.read_csv(file_path)

# Clean 'Change %' column:
# 1. Remove '%' and any whitespace
# 2. Convert to float
# 3. Take absolute value for categorization
df['Change%'] = df['Change %'].str.replace('%', '', regex=False).str.strip()
df['Change%'] = pd.to_numeric(df['Change%'], errors='coerce').abs()

# Define bins and labels
bins = [0, 2, 3, 4, float('inf')]
labels = ['0-2%', '2-3%', '3-4%', '4%+']

# Categorize based on absolute Change%
df['Change_Range'] = pd.cut(df['Change%'], bins=bins, labels=labels, right=False)

# Count and show results
change_counts = df['Change_Range'].value_counts().sort_index()

print("\nChange% Distribution:")
print(change_counts)
