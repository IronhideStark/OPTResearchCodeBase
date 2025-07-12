import polars as pl

# Load dataset
file_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_tw_posts_president_scored_anon_cleaned.csv"
df = pl.read_csv(file_path)

# Print basic shape
print(f"Dataset shape: {df.shape}\n")

# === General Descriptive Statistics (Numeric Columns) ===
numeric_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype in [pl.Float64, pl.Int64]]
numeric_df = df.select(numeric_cols)

print("=== General Descriptive Statistics (Numeric Columns) ===")
print(numeric_df.describe())

# === Unique Values per Column ===
print("\n=== Unique Values per Column ===")
for col in df.columns:
    try:
        unique_count = df.select(pl.col(col).n_unique()).item()
        print(f"{col}: {unique_count}")
    except Exception as e:
        print(f"{col}: Error getting unique values - {e}")

# === Value Counts for Selected Categorical Columns ===
# === Value Counts for Selected Categorical Columns ===
# === Value Counts for Selected Categorical Columns ===
# === Value Counts for Selected Categorical Columns ===
categorical_cols = [
    "id", "url", "source", "lang", "quoteid", "inreplytoid", 
    "isreply", "isquote", "isretweet", "isconversationcontrolled"
]

for col in categorical_cols:
    if col in df.columns:
        print(f"\n=== Value Counts for '{col}' Column ===")
        try:
            # Compute value counts and then sort descending manually
            vc = (
                df.select([col])
                .to_series()
                .value_counts()
                .sort("count", descending=True)
                .head(10)
            )
            print(vc)
        except Exception as e:
            print(f"Error generating value counts for {col}: {e}")
