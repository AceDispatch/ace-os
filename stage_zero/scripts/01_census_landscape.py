#!/usr/bin/env python3
"""
01_census_landscape.py — STAGE ZERO, Layer 1 (the targeting map)

Pulls the manufacturing + mining LANDSCAPE for a region from the US Census
County Business Patterns (CBP) API: establishment counts, employment, and
payroll by NAICS industry, per county. This is the "what is made where" layer.
It returns COUNTS, never company names (federal confidentiality).

WHAT YOU GET:
- output/census_landscape_<state>.csv  — every manufacturing/mining NAICS
  industry x county, with establishment counts, employment, payroll
- output/census_landscape_<state>_summary.csv — ranked: which industries are
  biggest by establishment count across the region

SETUP (one time):
  1. Get a FREE Census API key: https://api.census.gov/data/key_signup.html
     (arrives by email in seconds)
  2. Put it in ace-os/.env :  CENSUS_API_KEY=your_key_here
  3. pip install requests python-dotenv

RUN:
  python stage_zero/scripts/01_census_landscape.py --state 48
  python stage_zero/scripts/01_census_landscape.py --state 48 --counties 113,439,121,085,139,251,257,397,367,497
  # 48 = Texas. DFW core counties shown above (Dallas, Tarrant, Denton, Collin,
  #   Ellis, Johnson, Kaufman, Rockwall, Parker, Wise). Omit --counties for whole state.

NOTES:
- Default dataset year is 2022 (most recent stable CBP at time of writing). If
  Census publishes a newer year, change --year; if a year 404s, step back one.
- NAICS sectors pulled: 21 (mining/quarrying) + 31,32,33 (manufacturing).
  The script pulls the 6-digit detail under each so you see real categories
  (e.g. 331110 iron/steel mills, 321113 sawmills, 327332 concrete pipe).
"""

import argparse, csv, os, sys, time
import requests

try:
    from dotenv import load_dotenv
    # load ace-os/.env regardless of where script is invoked from
    here = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(here, "..", "..", ".env"))
except Exception:
    pass

BASE = "https://api.census.gov/data"
SECTORS = ["21", "31", "32", "33"]  # mining + manufacturing


def get_key():
    k = os.getenv("CENSUS_API_KEY")
    if not k:
        sys.exit("Missing CENSUS_API_KEY in ace-os/.env "
                 "(free key: https://api.census.gov/data/key_signup.html)")
    return k


def pull_sector(year, state, counties, sector, key):
    """Pull all 6-digit NAICS rows under a 2-digit sector for the geography."""
    geo = f"county:{counties}" if counties else "county:*"
    url = f"{BASE}/{year}/cbp"
    params = {
        "get": "ESTAB,EMP,PAYANN,NAICS2017,NAICS2017_LABEL",
        "for": geo,
        "in": f"state:{state}",
        "NAICS2017": f"{sector}*",   # wildcard = all NAICS starting with sector
        "key": key,
    }
    for attempt in range(4):
        r = requests.get(url, params=params, timeout=90)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 503):
            time.sleep(2 * (attempt + 1)); continue
        # 204 = no data; treat as empty
        if r.status_code == 204:
            return []
        sys.stderr.write(f"[warn] sector {sector}: HTTP {r.status_code} {r.text[:160]}\n")
        return []
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", required=True, help="State FIPS, e.g. 48 = Texas")
    ap.add_argument("--counties", default="", help="Comma county FIPS; omit for whole state")
    ap.add_argument("--year", default="2022")
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    key = get_key()
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = args.outdir or os.path.join(here, "..", "output")
    os.makedirs(outdir, exist_ok=True)

    rows = []  # flat: naics, label, county, estab, emp, payann
    for sector in SECTORS:
        data = pull_sector(args.year, args.state, args.counties, sector, key)
        if not data:
            continue
        hdr = data[0]
        for rec in data[1:]:
            d = dict(zip(hdr, rec))
            naics = d.get("NAICS2017", "")
            # keep only 6-digit detail rows (real industries), skip rollups
            if len(naics) != 6:
                continue
            rows.append({
                "naics": naics,
                "label": d.get("NAICS2017_LABEL", ""),
                "county_fips": d.get("county", ""),
                "establishments": int(d.get("ESTAB") or 0),
                "employment": int(d.get("EMP") or 0),
                "annual_payroll_k": int(d.get("PAYANN") or 0),
            })
        time.sleep(0.5)

    if not rows:
        sys.exit("No data returned. Check state/county FIPS, year, and API key.")

    # detailed file
    detail_path = os.path.join(outdir, f"census_landscape_{args.state}.csv")
    with open(detail_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["naics", "label", "county_fips",
                                          "establishments", "employment", "annual_payroll_k"])
        w.writeheader(); w.writerows(rows)

    # summary: aggregate by NAICS across all counties, ranked by establishments
    agg = {}
    for r in rows:
        a = agg.setdefault(r["naics"], {"label": r["label"], "establishments": 0,
                                        "employment": 0, "annual_payroll_k": 0})
        a["establishments"] += r["establishments"]
        a["employment"] += r["employment"]
        a["annual_payroll_k"] += r["annual_payroll_k"]
    ranked = sorted(agg.items(), key=lambda kv: kv[1]["establishments"], reverse=True)
    summary_path = os.path.join(outdir, f"census_landscape_{args.state}_summary.csv")
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["naics", "label", "total_establishments", "total_employment", "total_annual_payroll_k"])
        for naics, a in ranked:
            w.writerow([naics, a["label"], a["establishments"], a["employment"], a["annual_payroll_k"]])

    print(f"Landscape rows: {len(rows)}  |  distinct NAICS industries: {len(agg)}")
    print(f"Detail : {detail_path}")
    print(f"Summary: {summary_path}")
    print("\nTop 15 manufacturing/mining industries in region by establishment count:")
    for naics, a in ranked[:15]:
        print(f"  {naics}  {a['establishments']:>5} estab  {a['label'][:60]}")


if __name__ == "__main__":
    main()
