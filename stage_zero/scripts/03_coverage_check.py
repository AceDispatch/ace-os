#!/usr/bin/env python3
"""
03_coverage_check.py — STAGE ZERO, the scorecard

Reconciles the free company roster (EPA FRS, Layer 2) against the authoritative
establishment COUNTS (Census CBP, Layer 1) to answer the one question that makes
the two-layer architecture powerful:

   "Of the manufacturers the Census says exist in this region, what fraction did
    our free roster actually find?"

This is the coverage percentage. It tells you, per NAICS industry, where the
free roster is good enough and where you need browser harvesting (ThomasNet) or
paid data (MNI) to fill the gap. You can only compute this because the landscape
layer gives you a denominator a roster alone never has.

RUN (after 01 and 02 have produced their outputs):
  python stage_zero/scripts/03_coverage_check.py --state-fips 48 --state TX

OUTPUT:
  output/coverage_<state>.csv — per-NAICS: census establishment count,
  roster facilities found, coverage %, flagged HIGH-GAP industries to target
  with browser/paid sources next.
"""

import argparse, csv, os, sys
from collections import defaultdict


def load_census_summary(path):
    counts = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            counts[row["naics"]] = {
                "label": row["label"],
                "establishments": int(row["total_establishments"] or 0),
            }
    return counts


def load_roster(path):
    # count roster facilities per 6-digit NAICS (use first code if multiple)
    per_naics = defaultdict(int)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            codes = [c.strip() for c in (row.get("naics") or "").split(";") if c.strip()]
            seen6 = set(c for c in codes if len(c) == 6)
            if not seen6 and codes:
                # if only shorter codes present, skip 6-digit matching for this row
                continue
            for c in seen6:
                per_naics[c] += 1
    return per_naics


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state-fips", required=True, help="e.g. 48")
    ap.add_argument("--state", required=True, help="e.g. TX")
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = args.outdir or os.path.join(here, "..", "output")
    census_path = os.path.join(outdir, f"census_landscape_{args.state_fips}_summary.csv")
    roster_path = os.path.join(outdir, f"epa_roster_{args.state.upper()}.csv")

    for p in (census_path, roster_path):
        if not os.path.exists(p):
            sys.exit(f"Missing {p}. Run scripts 01 and 02 first.")

    census = load_census_summary(census_path)
    roster = load_roster(roster_path)

    rows = []
    for naics, c in census.items():
        est = c["establishments"]
        found = roster.get(naics, 0)
        cov = (found / est * 100) if est else 0.0
        rows.append({
            "naics": naics, "label": c["label"],
            "census_establishments": est,
            "roster_found": found,
            "coverage_pct": round(cov, 1),
            "gap": max(est - found, 0),
        })
    rows.sort(key=lambda r: r["gap"], reverse=True)

    out_path = os.path.join(outdir, f"coverage_{args.state.upper()}.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["naics", "label", "census_establishments",
                                          "roster_found", "coverage_pct", "gap"])
        w.writeheader(); w.writerows(rows)

    total_est = sum(r["census_establishments"] for r in rows)
    total_found = sum(min(r["roster_found"], r["census_establishments"]) for r in rows)
    overall = (total_found / total_est * 100) if total_est else 0
    print(f"Overall free-roster coverage vs Census: {overall:.1f}%  "
          f"({total_found} found / {total_est} establishments)")
    print(f"Coverage report: {out_path}")
    print("\nBiggest gaps (target these with ThomasNet/Chrome or paid data):")
    for r in rows[:15]:
        print(f"  {r['naics']}  gap {r['gap']:>5}  ({r['coverage_pct']:>4}% covered)  {r['label'][:50]}")


if __name__ == "__main__":
    main()
