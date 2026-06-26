# Contract 05 — Shipper Grader (Refiner Job 1)

**Job (one sentence):** Turn a raw EPA shipper candidate roster into a graded,
ranked flatbed list plus a sorted other-vertical seed file. Mechanical only.

## Input
- An EPA candidate roster CSV in `inbox/` (the Prospector's output, or a raw
  EPA FRS export). Must have `name` and `naics` columns; `city/address/zip/
  source` used if present. Original headers fine.

## Method
- Run `skills/shipper-grading/scripts/grade_shippers.py --in inbox/<file>
  --outdir outbox` exactly as documented in `skills/shipper-grading/SKILL.md`.
- Mechanical scoring only: name + NAICS signals from
  `skills/shipper-grading/references/NAICS_TIERS.md`. **NEVER touch the web** —
  no lookups, no enrichment. Web research is the Researcher's job (Contract 06).
- Do not modify the NAICS tiers, name-signal lists, or scoring in-flight.
  Tuning proposals go in the run log.

## Output (to `outbox/`)
1. `YYYY-MM-DD_grader_flatbed_ranked.csv` — ranked flatbed pile (yes + unsure).
   This is the MAP the operator steers the Researcher by.
2. `YYYY-MM-DD_grader_other_vertical.csv` — dump/van/heavy-haul/tanker shippers,
   sub-tagged by suspected type. SEED for future vertical directories. Not flatbed.
3. `YYYY-MM-DD_grader_summary.md` — rows in, distinct companies, bucket counts,
   other-vertical breakdown, top-25 flatbed preview.
4. `YYYY-MM-DD_grader_discard_log.csv` — dropped non-shippers (audit, not silent).

## Explicit non-goals
- Does NOT touch the web, check doors, or capture contacts. That's the Researcher.
- Does NOT research, verify, or rank by anything but mechanical name+NAICS score.
- Does NOT process the other-vertical bin — that's parked for a future
  vertical-directory process (dump truck directory first).
- Does NOT import anywhere. Staged files only.

## Operator handoff
- After the Grader runs, the operator reads the summary and points the Researcher
  (Contract 06) at a slice of the flatbed-ranked file — e.g. "research ranks
  1-50" or "skip the anchors, research ranks 100-150." The Researcher works in
  chunks of 50.

## Log
- Standard run log to `logs/`. Include the bucket-count table (yes/unsure/other/
  discard) and other-vertical breakdown — that table is how mis-sorting and
  calibration drift get caught.

## Name-penalty system (added 2026-06-13)
- The name discriminates HARD (like the FMCSA grader). Facility/service signals —
  paint shop, machine shop, repair, plating, "services", welding, etc. — apply
  heavy score penalties so non-truckload-shipper facilities SINK to the bottom of
  the rank. See references/NAICS_TIERS.md for the penalty tiers.
- Penalties REORDER, they do not delete — a penalized real shipper waits lower in
  line, never lost. So aggression here is safe.
- A heavy penalty drops even a tier-1-NAICS name out of "confident yes" into
  "unsure" (the name says this facility doesn'''t ship TL).

## Calibration note (from first real run, 2026-06-13)
- A tier-1 flatbed NAICS alone qualifies as flatbed-YES (the NAICS is the strong
  signal; a name keyword is not also required). Rows with neither a flatbed NAICS
  nor a flatbed name are discarded (self-protection if fed an unfiltered roster).
- Residual false-positives at the top (e.g. an oilfield-services firm with a
  flatbed NAICS) are EXPECTED — the Researcher catches them on the web check.
  The Grader produces the plausible ranked pile, not a perfect one.

## Run card (how a Code session runs this agent)
```
# 1. Ensure an EPA roster is in inbox/ (Prospector output, or a raw EPA FRS export
#    with name + naics columns). Example already present: inbox/epa_roster_TX.csv
# 2. Run:
python skills/shipper-grading/scripts/grade_shippers.py --in inbox/epa_roster_TX.csv --outdir outbox
# 3. Four dated files land in outbox/. Read the _summary.md. Write a run log to logs/.
```
Or just tell the Code session: **"Run the Shipper Grader per contract 05."**
No network. No CRM writes. Output is staged for the operator; nothing autonomous.
