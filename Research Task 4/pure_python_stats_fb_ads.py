import csv
import math
from collections import Counter

# -------- Configuration --------
FILE_PATH = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_fb_ads_president_scored_anon_cleaned.csv" # File Path
SAMPLE_SIZE = 1000  # Use None to load full file
GROUP_LIMIT = 10     # Limit number of groups shown
# --------------------------------

def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


def compute_numeric_stats(values):
    numbers = [float(v) for v in values if is_float(v)]
    if not numbers:
        return {}

    count = len(numbers)
    mean = sum(numbers) / count
    min_val = min(numbers)
    max_val = max(numbers)
    stddev = math.sqrt(sum((x - mean) ** 2 for x in numbers) / count)

    return {
        "count": count,
        "mean": round(mean, 2),
        "min": round(min_val, 2),
        "max": round(max_val, 2),
        "stddev": round(stddev, 2)
    }


def compute_non_numeric_stats(values):
    clean_vals = [v for v in values if v.strip() != ""]
    counter = Counter(clean_vals)
    most_common = counter.most_common(1)[0] if counter else (None, 0)
    return {
        "unique_count": len(counter),
        "most_common": most_common
    }


def load_csv(file_path, sample_size=None):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = []
        for i, row in enumerate(reader):
            data.append(row)
            if sample_size and i + 1 >= sample_size:
                break
    return data


def summarize_data(data):
    if not data:
        return {}

    summary = {}
    columns = data[0].keys()

    for col in columns:
        values = [row[col] for row in data]
        if all(is_float(v) or v.strip() == "" for v in values):
            summary[col] = compute_numeric_stats(values)
        else:
            summary[col] = compute_non_numeric_stats(values)

    return summary


def print_summary(summary):
    for col, stats in summary.items():
        print(f"\n--- Column: {col} ---")
        for stat_name, value in stats.items():
            print(f"{stat_name:>15}: {value}")


if __name__ == "__main__":
    print(" Loading data...")
    data = load_csv(FILE_PATH, sample_size=SAMPLE_SIZE)

    print(f" Loaded {len(data)} rows")

    print("\n Computing summary stats...")
    summary = summarize_data(data)

    print_summary(summary)


# code for grouped stats using pure python

print("grouped stats using pure python")

from collections import defaultdict

def group_data(data, keys):
    grouped = defaultdict(list)
    for row in data:
        group_key = tuple(row[k] for k in keys)
        grouped[group_key].append(row)
    return grouped


def summarize_groups(data, group_keys, limit=GROUP_LIMIT):
    grouped_data = group_data(data, group_keys)
    group_summaries = {}

    for group_key, group_rows in grouped_data.items():
        group_summary = summarize_data(group_rows)
        group_summaries[group_key] = group_summary

    return group_summaries


def print_group_summary(group_summaries, group_keys):
    for group_key, summary in group_summaries.items():
        group_label = " | ".join(f"{k}={v}" for k, v in zip(group_keys, group_key))
        print(f"\n\n=== Group: {group_label} ===")
        for col, stats in summary.items():
            print(f"\n-- Column: {col}")
            for stat_name, value in stats.items():
                print(f"  {stat_name:>15}: {value}")


# Run group-level summaries

if __name__ == "__main__":
    data = load_csv(FILE_PATH, sample_size=SAMPLE_SIZE)
    print(f" Loaded {len(data)} rows")
    print("🧩 Columns detected:", list(data[0].keys()))
    print("🧩 Available columns:", list(data[0].keys()))
    print("\n Overall Summary:")
    summary = summarize_data(data)
    print_summary(summary)

    # Group by page_id
    print("\n Grouped by page_id:")
    page_summary = summarize_groups(data, ["page_id"], limit=10)
    print_group_summary(page_summary, ["page_id"])

    # Group by page_id and ad_id
    print("\n Grouped by page_id + ad_id:")
    combo_summary = summarize_groups(data, ["page_id", "ad_id"], limit=10)
    print_group_summary(combo_summary, ["page_id", "ad_id"])
