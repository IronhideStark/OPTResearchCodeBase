import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load dataset (example: Facebook Posts)
df = pd.read_csv(r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_fb_posts_president_scored_anon_cleaned.csv")

plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['likes', 'comments', 'shares']])
plt.title("Distribution of Engagement Metrics (FB Posts)")
plt.ylabel("Count")
plt.grid(True)
plt.tight_layout()
plt.show()

incivility_counts = df[['incivility_illuminating', 'scam_illuminating', 'fraud_illuminating']].sum()
incivility_counts.plot(kind='bar', figsize=(8,5), title="Content Flagged for Incivility, Scam or Fraud")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


topic_cols = [col for col in df.columns if "_topic_illuminating" in col]
topic_counts = df[topic_cols].sum().sort_values(ascending=False)

topic_counts.plot(kind='bar', figsize=(12,6), title="Frequency of Topics Discussed")
plt.ylabel("Number of Posts")
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="type", y="total_interactions")
plt.yscale('log')
plt.title("Post Type vs Engagement (Log Scale)")
plt.xlabel("Post Type")
plt.ylabel("Total Interactions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()


