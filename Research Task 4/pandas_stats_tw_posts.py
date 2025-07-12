import pandas as pd

# Load dataset
file_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_tw_posts_president_scored_anon_cleaned.csv"  # Change if needed
df = pd.read_csv(file_path)

# Dataset shape
print(f"Dataset shape: {df.shape}\n")

# General descriptive statistics
print("=== General Descriptive Statistics (Numeric Columns) ===")
print(df.describe(include=[float, int]))
print("\n")

# Unique values per column
print("=== Unique Values per Column ===")
print(df.nunique())
print("\n")

# Value counts for selected categorical columns (edit if more needed)
categorical_columns = ['author_id', 'tweet_id', 'language', 'source', 'possibly_sensitive']
for col in categorical_columns:
    if col in df.columns:
        print(f"=== Value Counts for '{col}' Column ===")
        print(df[col].value_counts(dropna=False).head(10))  # Top 10 values
        print("\n")

# Grouped statistics by 'author_id'
if 'author_id' in df.columns:
    numeric_cols = df.select_dtypes(include=['number']).columns
    group_by_author = df.groupby('author_id')[numeric_cols].agg(['count', 'mean', 'min', 'max', 'std'])
    print("=== Grouped Analysis by ['author_id'] (Numerics Only) ===")
    print(group_by_author.head(10))  # Display only first 10 groups
    print("\n")

# Grouped statistics by ['author_id', 'tweet_id'] if tweet_id exists
if 'author_id' in df.columns and 'tweet_id' in df.columns:
    group_by_author_tweet = df.groupby(['author_id', 'tweet_id'])[numeric_cols].agg(['count', 'mean', 'min', 'max', 'std'])
    print("=== Grouped Analysis by ['author_id', 'tweet_id'] (Numerics Only) ===")
    print(group_by_author_tweet.head(10))  # Display only first 10 groups
