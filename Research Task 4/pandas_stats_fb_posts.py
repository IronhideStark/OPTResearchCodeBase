import pandas as pd

# === Load the dataset ===
file_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_fb_posts_president_scored_anon_cleaned.csv"  # Change if needed
df = pd.read_csv(file_path)
print(f"Dataset shape: {df.shape}\n")

# === Descriptive statistics for numeric columns ===
print("=== General Descriptive Statistics (Numeric Columns) ===")
print(df.describe())
print("\n")

# === Unique value counts for each column ===
print("=== Unique Values per Column ===")
print(df.nunique())
print("\n")

# === Most common values for a few key categorical columns ===
for col in ['facebook_id', 'post_id', 'page_category', 'type', 'video_share_status', 'is_video_owner?']:
    if col in df.columns:
        print(f"=== Value Counts for '{col}' Column ===")
        print(df[col].value_counts(dropna=False).head(10))  # show top 10 values
        print("\n")

# === Grouped analysis by 'facebook_id' ===
group_key = 'facebook_id'
numeric_cols = df.select_dtypes(include=['number']).columns
group_by_page = df.groupby(group_key)[numeric_cols].agg(['count', 'mean', 'min', 'max', 'std'])

print(f"=== Grouped Analysis by ['{group_key}'] (Numerics Only) ===")
print(group_by_page.head(10))  # show only first 10 groups
