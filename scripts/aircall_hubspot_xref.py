#!/usr/bin/env python3
"""
aircall_hubspot_xref.py — one-shot join of an Aircall call pull against HubSpot
Company phone numbers (Contract 02 style, read-only).

Inputs:
  - outbox/_xref_aggregates.json : per-number call aggregates (built upstream)
  - <tool-results dir>/*search_crm_objects*.txt : raw HubSpot MCP search results
    (companies matched by `phone IN [...]`), one JSON object per file.

Match rule: normalize both sides to digits-only last-10; a call number is
"matched" if it equals a HubSpot Company.phone. One number can map to several
company records (CRM duplicates) — all are kept and flagged.

Outputs (outbox/):
  - 2026-06-13_xref_matched_calls.csv
  - 2026-06-13_xref_orphan_calls.csv
  - 2026-06-13_xref_summary.md
"""
import csv, glob, json, os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "outbox")
TR = (r"C:\Users\nineo\.claude\projects"
      r"\C--Users-nineo-OneDrive-Desktop-Ace-Dispatch-Claude"
      r"\4424839e-b64f-496f-80a9-9faacad59695\tool-results")

def norm(d):
    d = "".join(c for c in (d or "") if c.isdigit())
    return d[-10:] if len(d) >= 10 else d

def uts(s):
    return datetime.fromtimestamp(int(s), tz=timezone.utc).strftime("%Y-%m-%d %H:%M") if s else ""

# ---- load HubSpot company records from every saved search result --------------
by_id = {}
files = sorted(glob.glob(os.path.join(TR, "*search_crm_objects*.txt")))
for fp in files:
    raw = open(fp, encoding="utf-8").read()
    i = raw.find("{")
    if i < 0:
        continue
    try:
        obj = json.loads(raw[i:])
    except json.JSONDecodeError:
        continue
    for r in obj.get("results", []):
        by_id[r["id"]] = r.get("properties", {})

# phone -> list of company dicts
phone_map = {}
for cid, p in by_id.items():
    ph = norm(p.get("phone"))
    if ph:
        phone_map.setdefault(ph, []).append(p)

# ---- load call aggregates -----------------------------------------------------
agg = json.load(open(os.path.join(OUT, "_xref_aggregates.json"), encoding="utf-8"))

matched_rows, orphan_rows = [], []
multi = 0
for num, a in agg.items():
    base = {
        "number": num,
        "calls": a["n_calls"],
        "answered": a["n_answered"],
        "max_talk_sec": a["max_dur"],
        "total_talk_sec": a["total_dur"],
        "last_call_utc": uts(a["last_started"]),
        "directions": a["directions"],
        "reps": a["reps"],
    }
    comps = phone_map.get(num)
    if comps:
        if len(comps) > 1:
            multi += 1
        # primary = highest ace_lead_score
        comps_sorted = sorted(
            comps, key=lambda c: int(c.get("ace_lead_score") or 0), reverse=True)
        c = comps_sorted[0]
        names = " | ".join(sorted({x.get("name", "") for x in comps}))
        matched_rows.append({**base,
            "crm_matches": len(comps),
            "company": c.get("name", ""),
            "all_company_names": names if len(comps) > 1 else "",
            "dot_number": c.get("dot_number", ""),
            "mc": c.get("mc", ""),
            "state": c.get("state", ""),
            "equipment_types": c.get("equipment_types", ""),
            "ace_lead_score": c.get("ace_lead_score", ""),
            "priority_tier": c.get("priority_tier", ""),
            "lifecyclestage": c.get("lifecyclestage", ""),
            "lead_source_detail": c.get("lead_source_detail", ""),
        })
    else:
        orphan_rows.append(base)

# sort: matched by talk time desc; orphans by answered then calls desc
matched_rows.sort(key=lambda r: (r["answered"], r["max_talk_sec"], r["calls"]), reverse=True)
orphan_rows.sort(key=lambda r: (r["answered"], r["calls"]), reverse=True)

mfields = ["number", "company", "crm_matches", "all_company_names", "dot_number",
           "mc", "state", "equipment_types", "ace_lead_score", "priority_tier",
           "lifecyclestage", "lead_source_detail", "calls", "answered",
           "max_talk_sec", "total_talk_sec", "last_call_utc", "directions", "reps"]
ofields = ["number", "calls", "answered", "max_talk_sec", "total_talk_sec",
           "last_call_utc", "directions", "reps"]

mpath = os.path.join(OUT, "2026-06-13_xref_matched_calls.csv")
opath = os.path.join(OUT, "2026-06-13_xref_orphan_calls.csv")
with open(mpath, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=mfields); w.writeheader(); w.writerows(matched_rows)
with open(opath, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=ofields); w.writeheader(); w.writerows(orphan_rows)

# ---- summary ------------------------------------------------------------------
tot = len(agg)
nm, no = len(matched_rows), len(orphan_rows)
m_ans = sum(1 for r in matched_rows if r["answered"] > 0)
o_ans = sum(1 for r in orphan_rows if r["answered"] > 0)
m_conn60 = sum(1 for r in matched_rows if r["max_talk_sec"] >= 60)
o_conn60 = sum(1 for r in orphan_rows if r["max_talk_sec"] >= 60)

summary = f"""# Aircall ↔ HubSpot Cross-Reference — 6/8–6/13 (2026)

**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · read-only

## Method
- Source calls: `outbox/2026-06-13_aircall-pull_calls.csv` (1,357 calls, 6/8–6/13).
- Reduced to **{tot} unique phone numbers** (digits-only, last 10).
- Matched each against HubSpot **Company.phone** (2,499 companies, owner Anthony
  Smart) via `phone IN [...]` batch search. Company phones are stored as clean
  10-digit strings, so matching is exact on the last 10 digits.
- HubSpot companies loaded for matching: **{len(by_id)}** distinct records.
- "Answered" = Aircall recorded an answer timestamp; "connected≥60s" = max talk
  time on that number ≥ 60 seconds.

## Headline
| Bucket | Unique numbers | of which answered | of which ≥60s talk |
|---|---:|---:|---:|
| **In CRM (matched)** | {nm} | {m_ans} | {m_conn60} |
| **Not in CRM (orphan)** | {no} | {o_ans} | {o_conn60} |
| **Total** | {tot} | {m_ans + o_ans} | {m_conn60 + o_conn60} |

- **{nm/tot*100:.1f}%** of dialed numbers matched an existing HubSpot company.
- **{no} orphan numbers** had a call but no CRM record — of those, **{o_conn60}**
  had a 60s+ conversation (most likely to be worth creating a record for).
- **{multi} matched numbers** map to MORE THAN ONE company record (duplicate
  companies sharing a phone in the CRM) — see `all_company_names` / `crm_matches`.

## Outputs
- `2026-06-13_xref_matched_calls.csv` — dialed numbers found in HubSpot, with the
  company (highest ace_lead_score if duplicates), DOT/MC, state, equipment,
  score, tier, and call stats.
- `2026-06-13_xref_orphan_calls.csv` — dialed numbers with no CRM match.

## Non-goals (constitution)
No CRM writes, no status changes, no note creation. Findings are staged for the
operator to act on.
"""
open(os.path.join(OUT, "2026-06-13_xref_summary.md"), "w", encoding="utf-8").write(summary)

print(f"HubSpot company records loaded : {len(by_id)} (from {len(files)} result files)")
print(f"unique call numbers            : {tot}")
print(f"matched (in CRM)               : {nm}  (answered {m_ans}, >=60s {m_conn60})")
print(f"orphan  (not in CRM)           : {no}  (answered {o_ans}, >=60s {o_conn60})")
print(f"numbers with multiple CRM cos  : {multi}")
print(f"wrote: {mpath}")
print(f"wrote: {opath}")
print(f"wrote: {os.path.join(OUT, '2026-06-13_xref_summary.md')}")
