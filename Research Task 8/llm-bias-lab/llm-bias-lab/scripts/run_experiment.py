"""
run_experiment.py
Executes LLM prompt experiments and logs responses in structured JSON.

Usage:
  python run_experiment.py \
    --prompts prompts/prompt_bank.jsonl \
    --out results/responses.jsonl \
    --model "chatgpt-gpt4" \
    --manual

Modes:
  --manual   : prompts will be displayed one by one; user pastes model responses.
  --api-key  : optional flag to load API calls (future integration).
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime
import time

BASE = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def load_prompts(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def write_record(path: Path, record: dict):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def manual_mode(prompt: dict, model: str):
    print("=" * 80)
    print(f"[{prompt['hypothesis']} | {prompt['condition']}]")
    print(prompt["model_input"])
    print("-" * 80)
    print("Paste or type the model's response below. Finish input with a blank line.")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", default="prompts/prompt_bank.jsonl")
    ap.add_argument("--out", default="results/responses.jsonl")
    ap.add_argument("--model", default="chatgpt-gpt4")
    ap.add_argument("--manual", action="store_true")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Running experiment — model={args.model}")
    print(f"Prompts loaded from {args.prompts}")
    print(f"Logging responses to {out_path}\n")

    for prompt in load_prompts(args.prompts):
        timestamp = datetime.utcnow().isoformat(timespec="seconds")

        if args.manual:
            response_text = manual_mode(prompt, args.model)
        else:
            # Placeholder for API call integration if added later
            response_text = "[API not enabled]"

        record = {
            "timestamp": timestamp,
            "model": args.model,
            "prompt_id": prompt["prompt_id"],
            "hypothesis": prompt["hypothesis"],
            "condition": prompt["condition"],
            "prompt_text": prompt["model_input"],
            "response_text": response_text,
            "metadata": prompt.get("metadata", {}),
        }

        write_record(out_path, record)
        print(f"Logged: {prompt['prompt_id']}")

        # Throttle for manual pacing or rate limits
        time.sleep(0.5)

    print(f"\nAll responses logged at: {out_path}")

if __name__ == "__main__":
    main()
