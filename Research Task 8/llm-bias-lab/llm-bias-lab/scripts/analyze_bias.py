import json
import re
import argparse
from pathlib import Path
from collections import defaultdict
import pandas as pd
from textblob import TextBlob

def clean_text(text):
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return text.lower().strip()

def sentiment_score(text):
    try:
        return TextBlob(text).sentiment.polarity
    except Exception:
        return 0.0

def load_responses(path):
    responses = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                responses.append(json.loads(line))
    return responses

def analyze_word_differences(responses):
    """
    Measures lexical overlap across prompt conditions for each hypothesis.
    """
    summary = []
    grouped = defaultdict(list)

    for r in responses:
        grouped[r["hypothesis"]].append((r["condition"], r["response_text"]))

    for hyp, items in grouped.items():
        base_words = None
        base_condition = None

        for condition, text in items:
            words = set(clean_text(text).split())
            if base_words is None:
                base_words = words
                base_condition = condition
                continue

            overlap = len(base_words.intersection(words)) / max(len(base_words), 1)
            summary.append({
                "hypothesis": hyp,
                "base_condition": base_condition,
                "compare_condition": condition,
                "word_overlap_ratio": round(overlap, 3)
            })

    return pd.DataFrame(summary)

def analyze_sentiment_differences(responses):
    """
    Measures average sentiment per condition within each hypothesis.
    """
    data = []
    for r in responses:
        data.append({
            "hypothesis": r["hypothesis"],
            "condition": r["condition"],
            "sentiment": sentiment_score(r["response_text"])
        })

    df = pd.DataFrame(data)
    sentiment_summary = (
        df.groupby(["hypothesis", "condition"])["sentiment"]
        .mean()
        .reset_index()
        .pivot(index="hypothesis", columns="condition", values="sentiment")
        .fillna(0)
    )

    sentiment_summary["sentiment_gap"] = sentiment_summary.max(axis=1) - sentiment_summary.min(axis=1)
    sentiment_summary = sentiment_summary.reset_index()
    return sentiment_summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="results/responses.jsonl", help="Path to model responses JSONL file")
    ap.add_argument("--outdir", default="analysis", help="Output directory for CSV summaries")
    args = ap.parse_args()

    path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"Loading responses from {path}...")
    responses = load_responses(path)
    print(f"Loaded {len(responses)} entries")

    print("Analyzing word-level overlap...")
    df_words = analyze_word_differences(responses)
    df_words.to_csv(outdir / "word_overlap_summary.csv", index=False)

    print("Analyzing sentiment bias...")
    df_sentiment = analyze_sentiment_differences(responses)
    df_sentiment.to_csv(outdir / "sentiment_summary.csv", index=False)

    print("\n✅ Analysis complete.")
    print(f"Files saved in {outdir.resolve()}")

if __name__ == "__main__":
    main()
