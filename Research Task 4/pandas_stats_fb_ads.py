import pandas as pd

# Load the dataset
file_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_fb_ads_president_scored_anon_cleaned.csv"  # Change if needed
df = pd.read_csv(file_path)

# Print basic DataFrame shape
print(f"Dataset shape: {df.shape}")
print("\n=== General Descriptive Statistics (Numeric Columns) ===")
print(df.describe())

print("\n=== Unique Values per Column ===")
print(df.nunique())

print("\n=== Value Counts for 'page_id' Column ===")
print(df['page_id'].value_counts())

# Select only numeric columns for aggregation
numeric_cols = df.select_dtypes(include='number').columns

# Perform grouped statistics only on numeric columns
print("\n=== Grouped Analysis by ['page_id'] (Numerics Only) ===")
group_by_page = df.groupby("page_id")[numeric_cols].agg(['count', 'mean', 'min', 'max', 'std'])
print(group_by_page)