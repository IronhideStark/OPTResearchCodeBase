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

