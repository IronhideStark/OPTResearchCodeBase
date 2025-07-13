import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv(r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_fb_ads_president_scored_anon_cleaned.csv")

# Set plot style
sns.set(style="whitegrid")

# Plot: Histogram of estimated impressions
plt.figure(figsize=(10, 5))
sns.histplot(df['estimated_impressions'], bins=30, kde=True)
plt.title("Distribution of Estimated Impressions")
plt.xlabel("Estimated Impressions")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Plot: Boxplot of estimated spend
plt.figure(figsize=(10, 5))
sns.boxplot(y=df['estimated_spend'])
plt.title("Boxplot of Estimated Spend")
plt.ylabel("Estimated Spend")
plt.tight_layout()
plt.show()


# categorical vizualizations

# Set plot style
sns.set(style="whitegrid")

# Countplot for scam_illuminating
plt.figure(figsize=(6, 4))
sns.countplot(x='scam_illuminating', data=df)
plt.title("Scam Illuminating Distribution")
plt.xlabel("Scam Illuminating")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Countplot for attack_msg_type_illuminating
plt.figure(figsize=(8, 4))
sns.countplot(x='attack_msg_type_illuminating', data=df)
plt.title("Attack Message Type Distribution")
plt.xlabel("Attack Msg Type")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
