#!/usr/bin/env python3
"""
02_epa_roster.py — STAGE ZERO, Layer 2 (the free company roster)

Downloads the EPA Facility Registry Service (FRS) single-state CSV and filters
to manufacturing + mining facilities (NAICS sectors 21, 31, 32, 33). This is
the free company-NAME layer: actual facility names, addresses, NAICS codes.

WHAT YOU GET:
- output/epa_roster_<state>.csv — real facilities with name, address, county,
  lat/long, NAICS code + description, filtered to mfg/mining.

IMPORTANT — this is the partial/heavy-skewed roster:
  FRS covers environmentally REGULATED facilities, so it over-represents larger
  / permitted manufacturers and under-represents small/light shops. It is the
  free FLOOR, measured later against the Census counts to see coverage gaps.

SETUP:
  pip install requests
  (No API key needed. The FRS state files are public downloads.)

RUN:
  python stage_zero/scripts/02_epa_roster.py --state TX

HOW IT WORKS:
  EPA publishes per-state ZIPs of FRS facilities. This script downloads the
  state file, unzips, finds the NATIONAL_SINGLE / facility CSV, and filters to
  rows whose NAICS code begins with 21/31/32/33. If EPA changes the URL format,
  the script prints the directory it tried so you can drop the file in manually
  into stage_zero/data/ and re-run with --localzip.

NOTE ON URL: EPA's FRS download paths change periodically. The script tries the
  known state-single-file pattern; if it 404s, follow the printed instructions
  to grab the file from https://www.epa.gov/frs/epa-frs-facilities-state-single-file-csv-download
  (download the state CSV/ZIP, place in stage_zero/data/, rerun with --localzip path).
"""

import argparse, csv, io, os, sys, zipfile
import requests

NAICS_PREFIXES = ("21", "31", "32", "33")
# EPA FRS state single-file download base (subject to change; see module docstring).
# Pattern is state_single_<lowercase>.zip — the older national_single_<UPPER>.zip path
# was retired by EPA and now 404s (fixed 2026-06-13).
FRS_STATE_URL = "https://ordsext.epa.gov/FLA/www3/state_files/state_single_{state}.zip"


def find_facility_csv(zf: zipfile.ZipFile):
    # the facility file is typically NATIONAL_FACILITY_FILE.CSV inside the zip
    for name in zf.namelist():
        upper = name.upper()
        if upper.endswith(".CSV") and ("FACILITY" in upper or "SINGLE" in upper):
            return name
    # fallback: first CSV
    for name in zf.namelist():
        if name.upper().endswith(".CSV"):
            return name
    return None


def load_zip_bytes(state, localzip):
    if localzip:
        with open(localzip, "rb") as f:
            return f.read()
    url = FRS_STATE_URL.format(state=state.lower())
    r = requests.get(url, timeout=300)
    if r.status_code != 200:
        sys.exit(
            f"Could not download FRS state file (HTTP {r.status_code}).\n"
            f"Tried: {url}\n"
            f"Manual path: visit "
            f"https://www.epa.gov/frs/epa-frs-facilities-state-single-file-csv-download , "
            f"download the {state} file, place it in stage_zero/data/, then rerun:\n"
            f"  python stage_zero/scripts/02_epa_roster.py --state {state} "
            f"--localzip stage_zero/data/<file>.zip"
        )
    return r.content


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", required=True, help="Two-letter state, e.g. TX")
    ap.add_argument("--localzip", default="", help="Path to a manually-downloaded FRS state zip")
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = args.outdir or os.path.join(here, "..", "output")
    os.makedirs(outdir, exist_ok=True)

    raw = load_zip_bytes(args.state, args.localzip or None)
    try:
        zf = zipfile.ZipFile(io.BytesIO(raw))
    except zipfile.BadZipFile:
        sys.exit("Downloaded file is not a valid zip. Use --localzip after manual download.")

    csv_name = find_facility_csv(zf)
    if not csv_name:
        sys.exit(f"No CSV found in zip. Contents: {zf.namelist()[:10]}")

    kept = []
    with zf.open(csv_name) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
        reader = csv.DictReader(text)
        # find the NAICS + name + address columns (FRS column names vary in case)
        cols = {c.lower(): c for c in (reader.fieldnames or [])}
        def col(*cands):
            for c in cands:
                if c in cols: return cols[c]
            return None
        naics_col = col("naics_codes", "naics_code", "naics")
        name_col  = col("primary_name", "facility_name", "name")
        addr_col  = col("location_address", "street_address", "address")
        city_col  = col("city_name", "city")
        cnty_col  = col("county_name", "county")
        zip_col   = col("postal_code", "zip_code", "zip")
        lat_col   = col("latitude83", "latitude", "lat")
        lon_col   = col("longitude83", "longitude", "long", "lon")
        for row in reader:
            naics_val = (row.get(naics_col) or "") if naics_col else ""
            # NAICS field may hold multiple codes; check if ANY starts with our prefixes
            codes = [c.strip() for c in naics_val.replace(";", ",").split(",") if c.strip()]
            if not any(code[:2] in NAICS_PREFIXES for code in codes):
                continue
            kept.append({
                "name": row.get(name_col, "") if name_col else "",
                "address": row.get(addr_col, "") if addr_col else "",
                "city": row.get(city_col, "") if city_col else "",
                "county": row.get(cnty_col, "") if cnty_col else "",
                "zip": row.get(zip_col, "") if zip_col else "",
                "naics": ";".join(codes),
                "latitude": row.get(lat_col, "") if lat_col else "",
                "longitude": row.get(lon_col, "") if lon_col else "",
            })

    out_path = os.path.join(outdir, f"epa_roster_{args.state.upper()}.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name", "address", "city", "county", "zip",
                                          "naics", "latitude", "longitude"])
        w.writeheader(); w.writerows(kept)

    print(f"Manufacturing/mining facilities kept: {len(kept)}")
    print(f"Roster: {out_path}")
    print("Reminder: FRS skews to permitted/heavy facilities; treat as the free floor, not a complete roster.")


if __name__ == "__main__":
    main()
