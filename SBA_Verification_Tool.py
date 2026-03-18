#!/usr/bin/env python3
"""
SBA_Verification_Tool_v2.py
Author: Marco Oppido
Description:
  Exhaustive formal verification utilities for the Specular Bit Architecture (SBA).
  - Enumerates canonical patterns for window length L (default 5).
  - Identifies critical ordered pairs that produce a center overflow |d_center| = 2.
  - Exports results in human-readable and machine-friendly formats (TXT, CSV).
Usage:
  python3 SBA_Verification_Tool_v2.py            # run with defaults (L=5)
  python3 SBA_Verification_Tool_v2.py --L 5      # explicit window length
  python3 SBA_Verification_Tool_v2 --outdir out  # specify output directory
Requirements:
  Python 3.8+ (only standard library used)
License: MIT
"""

from __future__ import annotations
import argparse
import csv
import itertools
import json
import os
from typing import List, Tuple, Dict

ALPHABET = (-1, 0, 1)

def is_sba_compliant(vector: Tuple[int, ...]) -> bool:
    """Return True if vector satisfies non-adjacency constraint (no adjacent non-zero entries)."""
    for a, b in zip(vector, vector[1:]):
        if a != 0 and b != 0:
            return False
    return True

def enumerate_canonical_patterns(L: int) -> List[Tuple[int, ...]]:
    """Enumerate all canonical patterns of length L under SBA non-adjacency constraint."""
    all_combinations = itertools.product(ALPHABET, repeat=L)
    return [tuple(p) for p in all_combinations if is_sba_compliant(tuple(p))]

def find_critical_pairs(patterns: List[Tuple[int, ...]], center_index: int) -> List[Dict]:
    """
    Identify ordered pairs (A,B) of canonical patterns that produce |d_center| == 2
    at the specified center_index.
    Returns list of dicts with pattern ids and overflow value.
    """
    critical = []
    for i, pa in enumerate(patterns, start=1):
        for j, pb in enumerate(patterns, start=1):
            s = pa[center_index] + pb[center_index]
            if abs(s) == 2:
                critical.append({
                    "patternA_id": i,
                    "patternB_id": j,
                    "patternA": pa,
                    "patternB": pb,
                    "overflow_value": int(s)
                })
    return critical

def write_patterns_csv(patterns: List[Tuple[int, ...]], outpath: str) -> None:
    """Write canonical patterns to CSV with ID and vector representation."""
    with open(outpath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Vector_Representation"])
        for idx, p in enumerate(patterns, start=1):
            writer.writerow([idx, "(" + ",".join(str(x) for x in p) + ")"])

def write_critical_pairs_csv(pairs: List[Dict], outpath: str) -> None:
    """Write critical ordered pairs to CSV (IDs and overflow)."""
    with open(outpath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["PairIndex", "PatternA_ID", "PatternB_ID", "Overflow"])
        for k, pair in enumerate(pairs, start=1):
            writer.writerow([k, pair["patternA_id"], pair["patternB_id"], pair["overflow_value"]])

def write_report_txt(patterns: List[Tuple[int, ...]], pairs: List[Dict], outpath: str) -> None:
    """Write a human-readable verification report."""
    with open(outpath, "w") as f:
        f.write("====================================================\n")
        f.write("SBA FORMAL VERIFICATION REPORT\n")
        f.write("====================================================\n\n")
        f.write(f"Window length L = {len(patterns[0]) if patterns else 'N/A'}\n")
        f.write(f"Canonical patterns found: {len(patterns)}\n\n")
        f.write("PART 1: CANONICAL PATTERNS (ID : pattern)\n")
        f.write("-" * 60 + "\n")
        for i, p in enumerate(patterns, 1):
            f.write(f"{i:02d}: {p}\n")
        f.write("\nPART 2: CRITICAL ORDERED PAIRS (center overflow |d|=2)\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total critical ordered pairs: {len(pairs)}\n\n")
        for k, pair in enumerate(pairs, 1):
            f.write(f"Pair {k:03d}: A_ID={pair['patternA_id']} B_ID={pair['patternB_id']} -> overflow={pair['overflow_value']:+d}\n")
        f.write("\nJSON summary saved alongside this report.\n")

def write_summary_json(patterns: List[Tuple[int, ...]], pairs: List[Dict], outpath: str) -> None:
    """Write a compact JSON summary for programmatic consumption."""
    summary = {
        "window_length": len(patterns[0]) if patterns else 0,
        "canonical_count": len(patterns),
        "critical_pairs_count": len(pairs),
        "critical_pairs_sample": [
            {"A_id": p["patternA_id"], "B_id": p["patternB_id"], "overflow": p["overflow_value"]}
            for p in pairs[:50]
        ]
    }
    with open(outpath, "w") as f:
        json.dump(summary, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="SBA formal verification (enumeration + critical pairs).")
    parser.add_argument("--L", type=int, default=5, help="window length (default 5)")
    parser.add_argument("--outdir", type=str, default=".", help="output directory (default current dir)")
    parser.add_argument("--center", type=int, default=None, help="center index for overflow check (0-based). Defaults to floor(L/2).")
    args = parser.parse_args()

    L = args.L
    center_index = args.center if args.center is not None else (L // 2)
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    patterns = enumerate_canonical_patterns(L)
    pairs = find_critical_pairs(patterns, center_index)

    # Output files
    patterns_csv = os.path.join(outdir, f"SBA_Canonical_Patterns_L{L}.csv")
    critical_csv = os.path.join(outdir, f"SBA_Critical_Pairs_L{L}_center{center_index}.csv")
    report_txt = os.path.join(outdir, f"SBA_Verification_Report_L{L}.txt")
    summary_json = os.path.join(outdir, f"SBA_Verification_Summary_L{L}.json")

    write_patterns_csv(patterns, patterns_csv)
    write_critical_pairs_csv(pairs, critical_csv)
    write_report_txt(patterns, pairs, report_txt)
    write_summary_json(patterns, pairs, summary_json)

    # Console summary
    print(f"SBA verification completed for L={L}")
    print(f"Canonical patterns: {len(patterns)}  (saved: {patterns_csv})")
    print(f"Critical ordered pairs (|d_center|=2): {len(pairs)}  (saved: {critical_csv})")
    print(f"Human report: {report_txt}")
    print(f"JSON summary: {summary_json}")

if __name__ == "__main__":
    main()
