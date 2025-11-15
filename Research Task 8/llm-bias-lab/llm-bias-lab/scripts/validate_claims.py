
#!/usr/bin/env python3
"""
validate_claims.py
Checks LLM-generated claims against ground-truth data.

Supported inputs
----------------
Claims:
  1) CSV with columns: example_id,key,claimed_value
  2) JSONL with objects containing either:
     - {"example_id": "...", "claims": [{"key": "...", "value": ...}, ...]}
     - {"example_id": "...", "key": "...", "claimed_value": ...}

Truth:
  - CSV/JSON/JSONL that resolves into a mapping: key -> truth_value
    * CSV: columns: key,truth_value (additional columns ignored)
    * JSON/JSONL: either an object {key: value, ...} or JSONL lines of {"key": "...", "truth_value": ...}

Matching rules
--------------
- Strings: casefold, strip, collapse internal whitespace
- Numbers: compared within tolerances (absolute and relative)
- Booleans: normalized {"true","false","yes","no","1","0"}
- Lists (comma/semicolon separated): order-insensitive string element compare
- Missing keys/claims are reported
- Outputs a CSV report + a JSON summary

Usage
-----
python validate_claims.py --claims llm_claims.csv --truth ground_truth.csv --out report.csv
"""

import argparse
import csv
import json
import math
import os
import re
from collections import defaultdict, Counter
from typing import Any, Dict, Iterable, List, Tuple, Union

# ------------------------- IO helpers -------------------------

def load_truth(path: str) -> Dict[str, Any]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return _load_truth_csv(path)
    elif ext in {".json"}:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        elif isinstance(data, list):
            # list of {"key": ..., "truth_value": ...}
            out = {}
            for obj in data:
                if isinstance(obj, dict) and "key" in obj:
                    out[str(obj["key"])] = obj.get("truth_value")
            return out
        else:
            raise ValueError("Unsupported JSON truth format")
    elif ext in {".jsonl", ".ndjson"}:
        out = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                obj = json.loads(line)
                if isinstance(obj, dict) and "key" in obj:
                    out[str(obj["key"])] = obj.get("truth_value")
        return out
    else:
        raise ValueError(f"Unsupported truth file type: {ext}")

def _load_truth_csv(path: str) -> Dict[str, Any]:
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Accept various column names
        key_col = None
        val_col = None
        headers = [h.strip() for h in reader.fieldnames or []]
        for h in headers:
            if key_col is None and h.lower() in {"key","id","name"}:
                key_col = h
            if val_col is None and h.lower() in {"truth_value","value","expected"}:
                val_col = h
        if key_col is None or val_col is None:
            # fallback: first two columns
            if len(headers) >= 2:
                key_col, val_col = headers[0], headers[1]
            else:
                raise ValueError("Truth CSV must have at least two columns")
        for row in reader:
            k = str(row[key_col])
            v = row[val_col]
            out[k] = v
    return out

def load_claims(path: str) -> List[Tuple[str, str, Any]]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return _load_claims_csv(path)
    elif ext in {".json"}:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _claims_from_json_like(data)
    elif ext in {".jsonl", ".ndjson"}:
        claims = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                obj = json.loads(line)
                claims.extend(_claims_from_json_like(obj))
        return claims
    else:
        raise ValueError(f"Unsupported claims file type: {ext}")

def _load_claims_csv(path: str) -> List[Tuple[str, str, Any]]:
    claims: List[Tuple[str,str,Any]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = [h.strip() for h in reader.fieldnames or []]
        # Try standard columns
        ex_col = None
        key_col = None
        val_col = None
        for h in headers:
            if ex_col is None and h.lower() in {"example_id","id","prompt_id","sample_id"}:
                ex_col = h
            if key_col is None and h.lower() in {"key","field","metric","name"}:
                key_col = h
            if val_col is None and h.lower() in {"claimed_value","value","answer","prediction"}:
                val_col = h
        if key_col is None or val_col is None:
            raise ValueError("Claims CSV must have columns for key and claimed_value")
        if ex_col is None:
            ex_col = key_col  # group by key if no example id
        for row in reader:
            claims.append((str(row[ex_col]), str(row[key_col]), row[val_col]))
    return claims

def _claims_from_json_like(data: Any) -> List[Tuple[str,str,Any]]:
    out: List[Tuple[str,str,Any]] = []
    if isinstance(data, list):
        for obj in data:
            out.extend(_claims_from_json_like(obj))
    elif isinstance(data, dict):
        # pattern 1: {"example_id": "...", "claims": [{"key": "...", "value": ...}, ...]}
        if "claims" in data and isinstance(data["claims"], list):
            example_id = str(data.get("example_id", ""))
            for c in data["claims"]:
                if isinstance(c, dict) and "key" in c and "value" in c:
                    out.append((example_id, str(c["key"]), c["value"]))
        # pattern 2: {"example_id": "...", "key": "...", "claimed_value": ...}
        elif "key" in data and ("claimed_value" in data or "value" in data):
            example_id = str(data.get("example_id", ""))
            value = data.get("claimed_value", data.get("value"))
            out.append((example_id, str(data["key"]), value))
        # pattern 3: {"example_id": "...", "response": "..."} -> attempt key:value extraction
        elif "response" in data:
            example_id = str(data.get("example_id", ""))
            extracted = extract_key_value_pairs(str(data["response"]))
            for k,v in extracted:
                out.append((example_id, k, v))
    return out

# ------------------------- Normalization -------------------------

_WS_RE = re.compile(r"\s+")

def norm_string(x: str) -> str:
    return _WS_RE.sub(" ", x.strip().casefold())

_BOOL_MAP = {
    "true": True, "false": False,
    "yes": True, "no": False,
    "y": True, "n": False,
    "1": True, "0": False,
    "t": True, "f": False
}

def to_bool_maybe(x: Any) -> Union[bool, None]:
    if isinstance(x, bool):
        return x
    if x is None:
        return None
    s = str(x).strip().casefold()
    return _BOOL_MAP.get(s, None)

_NUM_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?$")

def to_number_maybe(x: Any) -> Union[float, None]:
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return float(x)
    s = str(x).strip().replace(",", "")
    if _NUM_RE.match(s):
        try:
            return float(s)
        except Exception:
            return None
    # percentages "12.3%"
    if s.endswith("%"):
        try:
            return float(s[:-1]) / 100.0
        except Exception:
            return None
    return None

def split_list_maybe(x: Any) -> Union[List[str], None]:
    if x is None:
        return None
    s = str(x)
    if "," in s or ";" in s:
        parts = re.split(r"[;,]", s)
        return [norm_string(p) for p in parts if p.strip()]
    return None

def levenshtein(a: str, b: str) -> int:
    # classic DP, iterative
    a, b = a, b
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            curr.append(min(prev[j]+1, curr[j-1]+1, prev[j-1]+cost))
        prev = curr
    return prev[-1]

# ------------------------- Comparison -------------------------

def compare_values(claim, truth, atol=0.0, rtol=0.0) -> Tuple[bool, str, str]:
    # Return (match, error_type, diff_info)
    # Try boolean
    bc = to_bool_maybe(claim)
    bt = to_bool_maybe(truth)
    if bc is not None or bt is not None:
        if bc is None or bt is None:
            return (False, "type_mismatch_bool", f"claim={claim} truth={truth}")
        return (bc == bt, "ok" if bc == bt else "mismatch_bool", "")

    # Try number
    nc = to_number_maybe(claim)
    nt = to_number_maybe(truth)
    if (nc is not None) or (nt is not None):
        if nc is None or nt is None:
            return (False, "type_mismatch_number", f"claim={claim} truth={truth}")
        # relative + absolute tolerance
        delta = abs(nc - nt)
        tol = atol + rtol * max(1.0, abs(nt))
        return (delta <= tol, "ok" if delta <= tol else "mismatch_number", f"delta={delta} tol={tol}")

    # Try list
    lc = split_list_maybe(claim)
    lt = split_list_maybe(truth)
    if lc is not None or lt is not None:
        if lc is None or lt is None:
            return (False, "type_mismatch_list", f"claim={claim} truth={truth}")
        # multiset equality
        return (Counter(lc) == Counter(lt), "ok" if Counter(lc) == Counter(lt) else "mismatch_list", "")

    # Fallback: normalized string compare
    sc = norm_string(str(claim))
    st = norm_string(str(truth))
    match = sc == st
    if match:
        return (True, "ok", "")
    # provide edit distance as diff
    d = levenshtein(sc, st)
    return (False, "mismatch_string", f"levenshtein={d}")

# ------------------------- Extraction (optional) -------------------------

KV_RE = re.compile(r"(?P<key>[A-Za-z0-9_ .\-/]+)\s*[:=]\s*(?P<val>[^\n;]+)")

def extract_key_value_pairs(text: str) -> List[Tuple[str,str]]:
    pairs = []
    for m in KV_RE.finditer(text):
        k = norm_string(m.group("key"))
        v = m.group("val").strip()
        pairs.append((k, v))
    return pairs

# ------------------------- Main -------------------------

def run(claims_path: str, truth_path: str, out_csv: str, out_json: str, atol: float, rtol: float):
    truth = load_truth(truth_path)
    claims = load_claims(claims_path)

    rows = []
    summary = {
        "total_claims": 0,
        "matched": 0,
        "mismatched": 0,
        "missing_in_truth": 0,
        "by_error_type": {}
    }

    for example_id, key, claimed_value in claims:
        summary["total_claims"] += 1
        if key not in truth:
            rows.append({
                "example_id": example_id,
                "key": key,
                "claimed_value": claimed_value,
                "truth_value": "",
                "match": False,
                "error_type": "missing_truth_key",
                "diff": ""
            })
            summary["missing_in_truth"] += 1
            continue

        truth_value = truth[key]
        ok, err_type, diff = compare_values(claimed_value, truth_value, atol=atol, rtol=rtol)
        if ok:
            summary["matched"] += 1
        else:
            summary["mismatched"] += 1

        rows.append({
            "example_id": example_id,
            "key": key,
            "claimed_value": claimed_value,
            "truth_value": truth_value,
            "match": ok,
            "error_type": err_type if not ok else "",
            "diff": diff
        })
        summary["by_error_type"][err_type] = summary["by_error_type"].get(err_type, 0) + (0 if ok else 1)

    # write CSV
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["example_id","key","claimed_value","truth_value","match","error_type","diff"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    # write JSON summary
    if summary["total_claims"] > 0:
        summary["accuracy"] = summary["matched"] / summary["total_claims"]
    else:
        summary["accuracy"] = None
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

def parse_args():
    ap = argparse.ArgumentParser(description="Validate LLM claims against ground-truth data.")
    ap.add_argument("--claims", required=True, help="Path to claims file (CSV/JSON/JSONL).")
    ap.add_argument("--truth", required=True, help="Path to ground-truth file (CSV/JSON/JSONL).")
    ap.add_argument("--out", default="validate_report.csv", help="Path to output CSV report.")
    ap.add_argument("--summary", default="validate_summary.json", help="Path to output JSON summary.")
    ap.add_argument("--atol", type=float, default=0.0, help="Absolute tolerance for numeric comparison.")
    ap.add_argument("--rtol", type=float, default=0.0, help="Relative tolerance for numeric comparison.")
    return ap.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run(args.claims, args.truth, args.out, args.summary, args.atol, args.rtol)
