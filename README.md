# OPTResearchCodeBase
This repository contains a data summarization system designed to assist researchers in generating descriptive analyses of real-world datasets.

# 2024 U.S. Election Social Media Dataset Analysis
This project is part of an academic research task focused on building a data summarizing system using Pure Python, Pandas, and Polars. It explores three datasets related to social media activity during the 2024 U.S. Presidential Election. 
Summary of Insights

# Across all datasets, we generated descriptive statistics using:
Pure Python (custom functions)
Pandas (high-level abstractions)
Polars (fast, lazy-evaluation based)

# Key Findings:
Polars consistently outperformed Pandas in speed, especially on larger datasets (~27K rows).
Several columns required parsing or cleanup, particularly:
Boolean values represented as strings (e.g., 'Yes', 'No')
Mixed types in numeric columns
Value counts and nunique across platforms highlighted behavioral and engagement patterns across Facebook Ads, Facebook Posts, and Twitter Posts.

# Visualizations Overview & Key Observations
Our goal was to visually summarize both numeric and categorical variables to help uncover patterns, trends, and structural characteristics within the datasets. Below is a summary of the types of visualizations created and general observations. 

# Numeric Feature Visualizations
Histograms were used to observe the distribution of numeric features such as impressions, spend, likes, views, and engagement metrics.
These visualizations helped identify common data characteristics such as skewness, concentration of values, and the presence of long-tailed distributions.
Boxplots were created to examine the spread and outliers in selected numeric columns.
They were useful in identifying variability in ad engagement or post performance across campaigns.

# Categorical Feature Visualizations
Bar charts (count plots) were employed to visualize the frequency of values in categorical fields such as: Message types (attack_msg_type_illuminating, issue_msg_type_illuminating), Platforms and sources (publisher_platforms, tweet source), Boolean indicators like is_reply, is_quote, or scam_illuminating.
These visualizations provided an overview of message classification, platform distribution, and the prevalence of various types of content.

# General Observation
The datasets showed a broad range of engagement levels, with some entries reflecting significantly higher activity.
Categorical indicators suggested varied messaging strategies and platform usage.
The visualization process highlighted the need for data cleaning and preprocessing, especially with mixed-type or nested fields.
Visualizing these datasets helped surface structural insights that might guide further qualitative or statistical analysis.

