import csv
import math
from collections import defaultdict, Counter

# -------- Configuration --------
FILE_PATH = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\Cleaned\2024_tw_posts_president_scored_anon_cleaned.csv" # File Path
SAMPLE_SIZE = None  # Use None to load full file
GROUP_LIMIT = 10     # Limit number of groups shown
# --------------------------------

def load_csv(file_path, sample_size=None):
    data = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            data.append(row)
            if sample_size and i + 1 >= sample_size:
                break
    return data


def is_numeric(val):
    try:
        float(val)
        return True
    except:
        return False


def compute_numeric_stats(values):
    numbers = [float(v) for v in values if is_numeric(v)]
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
    clean_vals = [v.strip() for v in values if v.strip()]
    counter = Counter(clean_vals)
    most_common = counter.most_common(1)[0] if counter else (None, 0)
    return {
        "unique_count": len(counter),
        "most_common": most_common
    }


def summarize_data(data):
    if not data:
        return {}

    summary = {}
    columns = data[0].keys()

    for col in columns:
        values = [row[col] for row in data]
        if all(is_numeric(v) or v.strip() == "" for v in values):
            summary[col] = compute_numeric_stats(values)
        else:
            summary[col] = compute_non_numeric_stats(values)

    return summary


def group_data(data, keys):
    grouped = defaultdict(list)
    for row in data:
        try:
            group_key = tuple(row[k].strip() for k in keys if k in row)
            if len(group_key) == len(keys) and all(group_key):
                grouped[group_key].append(row)
        except KeyError:
            continue
    print(f"🔍 Grouped {len(data)} rows into {len(grouped)} groups using keys {keys}")
    return grouped


def summarize_groups(data, group_keys, limit=GROUP_LIMIT):
    grouped = group_data(data, group_keys)
    print(f"\n📊 Summary by {group_keys} (Showing up to {limit} groups):")

    for i, (group_key, group_rows) in enumerate(grouped.items()):
        if i >= limit:
            print(f"...and {len(grouped) - limit} more groups not shown.\n")
            break
        group_label = " | ".join(f"{k}={v}" for k, v in zip(group_keys, group_key))
        print(f"\n=== Group: {group_label} ===")
        summary = summarize_data(group_rows)
        for col, stats in summary.items():
            print(f"\n-- Column: {col}")
            for stat, val in stats.items():
                print(f"   {stat:>12}: {val}")


# -------- Main Execution --------
if __name__ == "__main__":
    print(f"📥 Loading dataset: {FILE_PATH}")
    data = load_csv(FILE_PATH, SAMPLE_SIZE)
    print(f"✅ Loaded {len(data)} rows and {len(data[0])} columns")
    print("🧩 Columns detected:", list(data[0].keys()))
    print("🧩 Available columns:", list(data[0].keys()))

    print("\n📊 Overall Descriptive Statistics:")
    overall_summary = summarize_data(data)
    for col, stats in overall_summary.items():
        print(f"\n-- Column: {col}")
        for stat, val in stats.items():
            print(f"   {stat:>12}: {val}")

    # Grouped summaries for Facebook Posts dataset
    summarize_groups(data, ["source"], limit=10)
    summarize_groups(data, ["source", "month_year"], limit=10)



