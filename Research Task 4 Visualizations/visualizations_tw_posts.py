import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


# Load datasets
df = pd.read_csv(r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_tw_posts_president_scored_anon_cleaned.csv")


# Set plot style
sns.set(style="whitegrid")

# Histogram: Like Count
plt.figure(figsize=(10, 5))
sns.histplot(df['likecount'], bins=30, kde=True)
plt.title("Distribution of Like Count")
plt.xlabel("Like Count")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Boxplot: View Count
plt.figure(figsize=(10, 5))
sns.boxplot(y=df['viewcount'])
plt.title("Boxplot of View Count")
plt.ylabel("View Count")
plt.tight_layout()
plt.show()

# categorical vizualizations

# Set plot style
sns.set(style="whitegrid")

# Countplot for Tweet Source
plt.figure(figsize=(12, 6))
top_sources = df['source'].value_counts().head(10).index
sns.countplot(data=df[df['source'].isin(top_sources)], x='source')
plt.title("Top 10 Tweet Sources")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Countplot for Language
plt.figure(figsize=(8, 4))
sns.countplot(x='lang', data=df, order=df['lang'].value_counts().index)
plt.title("Tweet Language Distribution")
plt.xlabel("Language")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

