#!/usr/bin/env python3
"""pipeline/run_region.py — the standardized region routine.
Prospect (slice rosters by county) -> Classify (multi-vertical) -> emit the target-vertical
research worklist + chunked args for the research fan-out.
(Research = the AI workflow; Sync = db/sync.py — the follow-on steps it prints.)

Usage:
  python pipeline/run_region.py --region memphis \
     --counties "TN:Shelby,Fayette,Tipton;MS:DeSoto,Marshall,Tate,Tunica;AR:Crittenden" \
     --vertical flatbed
"""
import csv, sys, os, json, argparse
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import classify_rows, COLS

ap = argparse.ArgumentParser()
ap.add_argument("--region", required=True)
ap.add_argument("--counties", required=True, help='"ST:County,County;ST:County"')
ap.add_argument("--vertical", default="flatbed")
ap.add_argument("--inbox", default="inbox")
ap.add_argument("--per", type=int, default=18, help="companies per research agent")
a = ap.parse_args()

want = {}
for part in a.counties.split(";"):
    part = part.strip()
    if not part or ":" not in part: continue
    st, cos = part.split(":", 1)
    want[st.strip().upper()] = set(c.strip().upper() for c in cos.split(",") if c.strip())

outdir = f"outbox/{a.region}"
os.makedirs(outdir, exist_ok=True)

# 1. PROSPECT — slice rosters by county
roster = []
for st, cos in want.items():
    f = os.path.join(a.inbox, f"epa_roster_{st}.csv")
    if not os.path.exists(f):
        print(f"  WARN: no roster {f}"); continue
    for r in csv.DictReader(open(f, encoding="utf-8", errors="replace")):
        if (r.get("county") or "").strip().upper() in cos:
            roster.append(r)
ncos = sum(len(c) for c in want.values())
print(f"[Prospect] {len(roster)} facilities across {ncos} counties in {len(want)} state(s)")

# 2. CLASSIFY — multi-vertical
cl = classify_rows(roster)
clpath = f"{outdir}/{a.region}_classified.csv"
with open(clpath, "w", encoding="utf-8", newline="") as g:
    w = csv.DictWriter(g, fieldnames=COLS); w.writeheader()
    for r in cl: w.writerow(r)
print(f"[Classify] {len(cl)} companies -> {clpath}")
print("  bins:", dict(Counter(r["equipment_class"] for r in cl).most_common()))

# 3. WORKLIST — the target vertical, ranked
work = sorted([r for r in cl if r["equipment_class"] == a.vertical], key=lambda x: -int(x["flatbed_score"]))
wlpath = f"{outdir}/{a.region}_worklist_{a.vertical}.csv"
with open(wlpath, "w", encoding="utf-8", newline="") as g:
    w = csv.DictWriter(g, fieldnames=COLS); w.writeheader()
    for r in work: w.writerow(r)
recs = [{"name": r["company"], "naics": r["naics"], "city": r["city"], "addr": r["address"], "zip": r["zip"]} for r in work]
chunks = [recs[i:i + a.per] for i in range(0, len(recs), a.per)]
json.dump(chunks, open(f"{outdir}/{a.region}_research_args.json", "w", encoding="utf-8"), separators=(",", ":"))
print(f"[Worklist] {len(work)} {a.vertical} candidates -> {wlpath}")
print(f"  research fan-out: {len(chunks)} agents x ~{a.per}/agent -> {outdir}/{a.region}_research_args.json")
print(f"\nNEXT:")
print(f"  • AI runs the research workflow on {a.region}_research_args.json (verify FTL + door + lanes)")
print(f"  • then sync verified results:  python db/sync.py {outdir}/{a.region}_shipper_registry.csv")
