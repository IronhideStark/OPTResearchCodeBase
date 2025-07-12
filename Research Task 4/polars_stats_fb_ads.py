import polars as pl

# Load the dataset
df = pl.read_csv(r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_fb_ads_president_scored_anon_cleaned.csv")

print("Dataset shape:", df.shape)

# === General Descriptive Statistics for Numeric Columns ===
print("\n=== General Descriptive Statistics (Numeric Columns) ===")
numeric_df = df.select([col for col in df.columns if df[col].dtype in [pl.Int64, pl.Float64]])
print(numeric_df.describe())

# === Unique Values per Column ===
print("\n=== Unique Values per Column ===")
for col in df.columns:
    unique_count = df[col].n_unique()
    print(f"{col}: {unique_count}")

# === Value Counts for Selected Categorical Columns ===
categorical_cols = ["page_id", "ad_id", "currency", "publisher_platforms"]
for col in categorical_cols:
    if col in df.columns:
        print(f"\n=== Value Counts for '{col}' Column ===")
        print(df[col].value_counts().sort("count", descending=True).head(10))
