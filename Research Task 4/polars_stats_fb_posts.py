# polars_stats_fb_posts.py

import polars as pl

# Load dataset
file_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_fb_posts_president_scored_anon_cleaned.csv"
df = pl.read_csv(file_path, infer_schema_length=1000)

print(f"Dataset shape: {df.shape}\n")

# === Descriptive Statistics ===
print("=== General Descriptive Statistics (Numeric Columns) ===")
numeric_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype in [pl.Float64, pl.Int64]]
numeric_stats = df.select(numeric_cols).describe()
print(numeric_stats)

# === Unique Values per Column ===
print("\n=== Unique Values per Column ===")
for col in df.columns:
    try:
        unique_count = df[col].n_unique()
        print(f"{col}: {unique_count}")
    except Exception as e:
        print(f"{col}: Error - {e}")

# === Value Counts for Key Categorical Columns ===
# === Value Counts for Key Categorical Columns ===
categorical_cols = ["facebook_id", "post_id", "page_category", "type", "video_share_status", "is_video_owner?"]

for col in categorical_cols:
    print(f"\n=== Value Counts for '{col}' Column ===")
    try:
        vc = (
            df.select([col])
            .group_by(col)
            .count()
            .sort("count", descending=True)
            .head(10)
        )
        print(vc)
    except Exception as e:
        print(f"Error generating value counts for {col}: {e}")


