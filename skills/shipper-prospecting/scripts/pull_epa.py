#!/usr/bin/env python3
"""
pull_epa.py — The PROSPECTOR (Stage 1), Ace Dispatch shipper pipeline.

Pulls the EPA Facility Registry Service (FRS) state single-file CSVs for all 50
states (or a given subset), filters WIDE to manufacturing + mining sectors
(NAICS 21/31/32/33), tags each facility with a broad flatbed-plausible bin, and
writes the rosters into inbox/ for the Grader.

DESIGN LAW: the net is deliberately RIDICULOUSLY WIDE. When unsure, INCLUDE.
The Prospector does no grading, no ranking, no web, no geography filtering — it
casts the widest sensible net and lets the Grader narrow. A wider front means a
larger refined pile out the bottom.

OUTPUT:
  inbox/epa_roster_<ST>.csv         — one per state (flexible: re-pull / per-state grade)
  inbox/epa_roster_ALL.csv          — combined national file (one-shot grading)
  logs/<date>_prospector_run.md     — run log (counts per state)

USAGE:
  python skills/shipper-prospecting/scripts/pull_epa.py                 # all 50 states
  python skills/shipper-prospecting/scripts/pull_epa.py --states TX,OK  # subset
  python skills/shipper-prospecting/scripts/pull_epa.py --skip-existing # resume a partial pull
  python skills/shipper-prospecting/scripts/pull_epa.py --localdir stage_zero/data  # use pre-downloaded zips
"""

import argparse, csv, io, os, sys, zipfile, datetime, time

try:
    import requests
except ImportError:
    sys.exit("Need requests: python -m pip install requests")

NAICS_WIDE = ("21", "31", "32", "33")  # mfg + mining — the wide net
# EPA FRS per-state single-file zip. Pattern is state_single_<lowercase>.zip
# (the older national_single_<UPPER>.zip path was retired by EPA and now 404s — fixed 2026-06-13).
FRS_STATE_URL = "https://ordsext.epa.gov/FLA/www3/state_files/state_single_{state}.zip"

STATES = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
          "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
          "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
          "VA","WA","WV","WI","WY"]

# ---- wide flatbed-plausible bins (NAICS family -> bin name). When unsure, INCLUDE. ----
BINS = {
    "structural_fab_metal": set("332311 332312 332313 332321 332322 332323 332420 332439 332510 332618 332999 332410".split()),
    "steel_metal_production": set("331110 331221 331222 331318 331420 331491 331492 331511 331513 331523 331524 332111 332112 332114 332119 332215 332216".split()),
    "pipe_tube_valve": set("331210 332910 332911 332912 332919 332996".split()),
    "concrete_precast_stone": set("327120 327310 327320 327331 327332 327390 327991 327992 327999".split()),
    "lumber_wood_building": set("321113 321114 321211 321212 321213 321214 321215 321219 321911 321912 321918 321920 321991 321992 321999".split()),
    "machinery_heavy_equip": set("333111 333120 333131 333132 333241 333242 333243 333249 333413 333414 333415 333511 333922 333923 333924".split()),
    "transport_equip_oversized": set("336212 336214 336510 336611 336999".split()),
    "glass_heavy_materials": set("327211 327212 327213 327215 327993".split()),
}


def bin_for(codes):
    """Return the first matching bin, else 'other_wide' (kept — the net is wide)."""
    for code in codes:
        for binname, members in BINS.items():
            if code in members:
                return binname
    return "other_wide"  # no specific bin but passed the 21/31/32/33 net — INCLUDE it


def find_facility_csv(zf):
    for name in zf.namelist():
        u = name.upper()
        if u.endswith(".CSV") and ("FACILITY" in u or "SINGLE" in u):
            return name
    for name in zf.namelist():
        if name.upper().endswith(".CSV"):
            return name
    return None


def load_zip_bytes(state, localdir):
    if localdir:
        # look for a pre-downloaded zip for this state
        for fn in os.listdir(localdir):
            if state.upper() in fn.upper() and fn.lower().endswith(".zip"):
                with open(os.path.join(localdir, fn), "rb") as f:
                    return f.read()
        return None
    url = FRS_STATE_URL.format(state=state.lower())
    try:
        r = requests.get(url, timeout=300)
    except Exception as e:
        print(f"  {state}: download error {e}")
        return None
    if r.status_code != 200:
        print(f"  {state}: HTTP {r.status_code} (skipped)")
        return None
    return r.content


def process_state(state, localdir):
    """Return list of wide-net facility dicts for one state, or None on failure."""
    raw = load_zip_bytes(state, localdir)
    if raw is None:
        return None
    try:
        zf = zipfile.ZipFile(io.BytesIO(raw))
    except zipfile.BadZipFile:
        print(f"  {state}: bad zip (skipped)")
        return None
    csv_name = find_facility_csv(zf)
    if not csv_name:
        print(f"  {state}: no CSV in zip (skipped)")
        return None

    kept = []
    with zf.open(csv_name) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
        reader = csv.DictReader(text)
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
        st_col    = col("state_code", "state", "fac_state")
        for row in reader:
            naics_val = (row.get(naics_col) or "") if naics_col else ""
            codes = [c.strip() for c in naics_val.replace(";", ",").split(",") if c.strip()]
            # WIDE net: keep if ANY code is in mfg/mining sectors
            if not any(code[:2] in NAICS_WIDE for code in codes):
                continue
            kept.append({
                "name": (row.get(name_col, "") if name_col else "").strip(),
                "address": (row.get(addr_col, "") if addr_col else "").strip(),
                "city": (row.get(city_col, "") if city_col else "").strip(),
                "county": (row.get(cnty_col, "") if cnty_col else "").strip(),
                "state": (row.get(st_col, "") if st_col else state.upper()).strip() or state.upper(),
                "zip": (row.get(zip_col, "") if zip_col else "").strip(),
                "naics": ";".join(codes),
                "source": "EPA_FRS",
                "bin": bin_for(codes),
            })
    return kept


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--states", default="", help="Comma list e.g. TX,OK (default: all 50)")
    ap.add_argument("--inbox", default="inbox")
    ap.add_argument("--logdir", default="logs")
    ap.add_argument("--localdir", default="", help="Use pre-downloaded zips from this dir")
    ap.add_argument("--skip-existing", action="store_true", help="Skip states already in inbox")
    args = ap.parse_args()

    states = [s.strip().upper() for s in args.states.split(",") if s.strip()] or STATES
    os.makedirs(args.inbox, exist_ok=True)
    os.makedirs(args.logdir, exist_ok=True)
    today = datetime.date.today().isoformat()

    fields = ["name","address","city","county","state","zip","naics","source","bin"]
    per_state_counts = {}
    all_rows = []
    failed = []

    print(f"PROSPECTOR — pulling EPA FRS for {len(states)} state(s). Wide net (NAICS 21/31/32/33).\n")
    for i, st in enumerate(states, 1):
        out_path = os.path.join(args.inbox, f"epa_roster_{st}.csv")
        if args.skip_existing and os.path.exists(out_path):
            n = sum(1 for _ in open(out_path)) - 1
            per_state_counts[st] = n
            # still load into combined
            with open(out_path, encoding="utf-8") as f:
                all_rows.extend(list(csv.DictReader(f)))
            print(f"  [{i:>2}/{len(states)}] {st}: skip-existing ({n} rows)")
            continue

        rows = process_state(st, args.localdir or None)
        if rows is None:
            failed.append(st)
            per_state_counts[st] = 0
            continue
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
        per_state_counts[st] = len(rows)
        all_rows.extend(rows)
        print(f"  [{i:>2}/{len(states)}] {st}: {len(rows):>6} facilities -> {os.path.basename(out_path)}")
        if not args.localdir:
            time.sleep(1)  # be polite to EPA's server

    # combined national file
    all_path = os.path.join(args.inbox, "epa_roster_ALL.csv")
    with open(all_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(all_rows)

    # bin breakdown
    from collections import Counter
    bins = Counter(r["bin"] for r in all_rows)

    # run log
    log_path = os.path.join(args.logdir, f"{today}_prospector_run.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# Prospector Run — {today}\n\n")
        f.write(f"- States pulled: {len(states) - len(failed)} / {len(states)}\n")
        f.write(f"- Total facilities (wide net): {len(all_rows)}\n")
        f.write(f"- Combined file: inbox/epa_roster_ALL.csv\n")
        if failed:
            f.write(f"- FAILED states (re-run): {', '.join(failed)}\n")
        f.write(f"\n## Bin breakdown (wide flatbed-plausible families)\n")
        for b, n in bins.most_common():
            f.write(f"- {b}: {n}\n")
        f.write(f"\n## Per-state counts\n")
        for st in states:
            f.write(f"- {st}: {per_state_counts.get(st, 0)}\n")
        f.write(f"\n## Next\nRun the Grader on inbox/epa_roster_ALL.csv (or per-state).\n")

    print(f"\nPROSPECTOR complete.")
    print(f"  Total facilities (wide net): {len(all_rows)}")
    print(f"  Per-state files + combined: inbox/epa_roster_ALL.csv")
    if failed:
        print(f"  FAILED (re-run with --states {','.join(failed)}): {', '.join(failed)}")
    print(f"  Bin breakdown: {dict(bins)}")
    print(f"\nNext: python skills/shipper-grading/scripts/grade_shippers.py --in inbox/epa_roster_ALL.csv --outdir outbox")


if __name__ == "__main__":
    main()
