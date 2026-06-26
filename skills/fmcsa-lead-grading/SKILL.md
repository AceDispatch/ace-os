---
name: fmcsa-lead-grading
description: Grade and rank carrier sales leads from raw FMCSA Company Census data for Ace Dispatch. Use whenever the user uploads or references an FMCSA census file, a "company census" CSV, a carrier lead list, or asks to score, grade, rank, filter, or prune carrier leads. Ace dispatches INTERSTATE for-hire carriers only and targets carriers under 180 days of authority, peaking ~90 days. v4 adds a VEHICLE-TYPE gate that requires a real TRACTOR (ruling out box trucks, hotshots, sprinter/cargo vans, and passenger vans/buses — which the cargo flags do NOT catch), TRUE authority age cross-referenced from the AuthHist dataset (instead of the unreliable ADD_DATE proxy), and an active-operating-authority gate. Runs a strict perfect-only filter then a weighted scoring rubric and outputs a ranked CSV ready for HubSpot import on the Company object. Trigger on file names like "Company_Census_File_*.csv".
---

# FMCSA Lead Grading — Ace Dispatch (Perfect-Only, v4)

This skill turns FMCSA carrier data into a scored, ranked, HubSpot-ready lead list.
It encodes Ace's target: a young, for-hire, **interstate**, **tractor-trailer**
carrier (1–3 trucks) far enough into its first months to be running real freight and
shopping for a dispatcher, but not so established it already has dispatch handled.

**Governing philosophy — precision over recall.** Carrier supply is effectively
unlimited; rep dial-time is the scarce resource. A wrongly-kept lead wastes a dial; a
wrongly-dropped lead costs nothing. The engine **discards when in doubt** and imports
only complete, verifiable, on-profile carriers.

## What's new in v4 (the three fixes proven against the live datasets)
1. **Vehicle-type gate — must run a TRACTOR.** Cargo (`CRGO_*`) flags are *commodity*
   signals, not equipment; FMCSA never records trailer body type. ~28-29% of
   "general freight" interstate 1×1 carriers are actually **box trucks**. The census
   vehicle counts (`OWNTRACT`/`TRMTRACT`/`TRPTRACT` = tractors vs `OWNTRUCK` = straight
   trucks) let us require a real tractor-trailer op — concretely ruling out box
   trucks, hotshots, sprinter/cargo vans, and passenger vans/buses. Cargo flags are
   kept only for *scoring* (body-type inference: reefer strong, flatbed moderate,
   dry-van ambiguous).
2. **True authority age.** Age is computed from the real operating-authority grant
   date (AuthHist `9mw4-x3tu`), not `ADD_DATE` — which resets on routine MCS-150
   updates and mis-ages ~37% of verifiable leads (a 26-yr-old carrier can read 46
   days old). The grader uses `TRUE_AUTHORITY_AGE_DAYS` if present, else falls back
   to `ADD_DATE` (and warns).
3. **Active operating authority.** `DOCKET1_STATUS_CODE='A'` — a live carrier *record*
   is not the same as a live operating *authority*.

## How to run it (two steps — enrichment is upstream, grader stays offline)
```bash
# 1. Extract + enrich (live API: census filter + AuthHist true-age + vehicle columns)
python3 scripts/extract_leads.py --out leads_enriched.csv --states TX,GA,TN --power-units 1
# 2. Grade (offline; reads the enriched CSV)
python3 scripts/grade_leads.py leads_enriched.csv --out /mnt/user-data/outputs/graded_leads.csv --top 25
```
`grade_leads.py` flags:
- `--out`   output path
- `--top N` print a top-N preview
- `--max-age` authority-age ceiling in days (default `180`)

The grader prints, every run: kept/discarded counts, the **vehicle-gate ON/OFF** state,
the **age source (TRUE vs PROXY)**, the tier split, and the top discard reasons — so you
can sanity-check that the v4 gates actually fired. If you feed a raw census export
(no `OWNTRACT`/`TRUE_AUTHORITY_AGE_DAYS` columns) it still grades, but prints loud
warnings that the vehicle gate is OFF and age is on the proxy — re-run `extract_leads.py`.

## The hard gates (fail any → discarded, never scored)
1. **Interstate** — `CARRIER_OPERATION == 'A'`.
2. **For-hire** — `CLASSDEF` contains `AUTHORIZED FOR HIRE`.
3. **Active record** — `STATUS_CODE == 'A'`.
4. **Active authority** — `DOCKET1_STATUS_CODE == 'A'` (when present).
5. **Never revoked** — `PRIOR_REVOKE_FLAG != 'Y'`.
6. **Tractor (vehicle type)** — `OWNTRACT`/`TRMTRACT`/`TRPTRACT` > 0. Rules out box
   trucks, hotshots, sprinters, vans/buses.
7. **Authority age 0–180 days** — from `TRUE_AUTHORITY_AGE_DAYS` (AuthHist); `ADD_DATE` fallback.
8. **Real trucking name** — hard- and soft-negative names discarded.
9. **Dispatchable cargo** — flatbed/reefer/dry-van flagged; specialized/regulated discarded.
10. **Full completeness** — phone, cargo, authority date, power units, officer, city,
    state, classification, DOT, MC docket all present.

## The scoring rubric (only leads that pass all gates)
| Component | Range | Logic |
|---|---|---|
| **Equipment fit** | up to 40 | flatbed+reefer+van → 40; flatbed/reefer → 32-35; dry-van-only → 12. (Cargo-inferred body type.) |
| **Authority age** | up to 30 | peaks **61–105 days** (=30); 31–60 → 24; ≤30 → 15; 106–135 → 22; 136–180 → 12. Measured on **true** age. |
| **Name signal** | up to 15 | strong +15 / moderate +8 / neutral 0. |
| **Fleet size** | up to 10 | 1–3 power units → 10. |
| **Interstate intensity** | up to 5 | runs beyond 100 mi +3, has interstate drivers +2. |

### Priority tiers
- **P1** ≥ 85 · **P2** 70–84 · **P3** 55–69 · **P4** < 55

## What FMCSA can / cannot tell you about equipment
- **Cannot** verify flatbed vs reefer vs dry van — no FMCSA dataset records trailer
  body type (confirmed across census + the inspection files). Only commodity inference.
- **Can** concretely rule out box trucks / hotshots / sprinters / vans — the tractor
  counts (the v4 gate). That is the real equipment discriminator.

## HubSpot
Records are created on the **Company** object (portal 245837044), owner Anthony Smart
(164918656), custom fields in "Ace Dispatch – Carrier Info": `ace_lead_score`,
`priority_tier`, `equipment_types`, `dot_number`, `power_units`, `company_officer`,
`carrier_classification`, `fmcsa_add_date`, `lead_source_detail`. Note: HubSpot has no
delete tool on this connection — to "remove" leads, clear the owner (`hubspot_owner_id=""`).

## Files
- `scripts/extract_leads.py` — live census pull + AuthHist true-age + vehicle columns → enriched CSV.
- `scripts/grade_leads.py` — offline perfect-only filter + weighted rubric → ranked CSV.
- `references/RUBRIC.md` — the rubric as a checklist. `references/FIELD_REFERENCE.md` — the field map.
