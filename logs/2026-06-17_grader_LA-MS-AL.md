# Run Log — Shipper Grader (Contract 05) — LA / MS / AL

- **Date/time:** 2026-06-17
- **Contract:** contracts/05-shipper-grader.md
- **Operator-initiated or scheduled:** Operator-initiated (supervised)
- **Inputs:** EPA FRS rosters in `inbox/` (raw, unfiltered — Prospector not run for this pass)
  - `inbox/epa_roster_LA.csv` — 14,820 facilities
  - `inbox/epa_roster_MS.csv` — 3,387 facilities
  - `inbox/epa_roster_AL.csv` — 7,559 facilities
  - Combined regional input (LA+MS+AL, header-merged) — 25,766 facilities
- **Outputs:** (to `outbox/`, 4 artifacts × 4 runs = 16 files)
  - Per state: `2026-06-17_{LA,MS,AL}_grader_{flatbed_ranked,other_vertical,summary,discard_log}.{csv,md}`
  - Region: `2026-06-17_LA-MS-AL_grader_{flatbed_ranked,other_vertical,summary,discard_log}.{csv,md}`
- **Result:** success — grader ran mechanically (name + NAICS only, no web) on all three states and the merged region; outputs staged for operator. Nothing imported, no CRM writes.

## Bucket counts (calibration table)

| Run | Rows in | Distinct cos | FLATBED-YES | UNSURE | OTHER-VERT | DISCARD |
|---|---:|---:|---:|---:|---:|---:|
| LA | 14,820 | 11,219 | 1,071 | 1,815 | 288 | 8,045 |
| MS | 3,387 | 2,587 | 565 | 332 | 235 | 1,455 |
| AL | 7,559 | 5,905 | 1,104 | 757 | 378 | 3,666 |
| **LA-MS-AL (region)** | 25,766 | 19,392 | 2,679 | 2,872 | 868 | 12,973 |

### Other-vertical breakdown (seed for future verticals)
- LA: dump 104, tanker 132, van 31, heavy-haul 21
- MS: dump 127, tanker 81, van 25, heavy-haul 2
- AL: dump 208, tanker 96, van 64, heavy-haul 10
- Region: dump 430, tanker 294, van 112, heavy-haul 32

## Anomalies / data-quality notes
- **Raw rosters, Prospector not run.** Inputs are raw EPA FRS exports, so the large
  DISCARD column (12,973 region) is expected self-protection on an unfiltered feed —
  same pattern as the 2026-06-14 TX first run. In production the Prospector pre-filters
  to flatbed NAICS and the discard shrinks.
- **Regional dedupe < sum of per-state dedupes** (19,392 vs 11,219+2,587+5,905 = 19,711).
  The ~319 difference is multi-state companies (same first-3-token key in >1 state)
  collapsing in the merged pile. Expected behavior of `normalize_company`.
- **Top-of-rank spot check (region) is clean:** Atlas Fabrication, Gulf Coast Marine
  Fabricators, Nufab Rebar, Rinker Pipe, Clemons/Paul Davis Lumber, Design Precast — all
  genuine open-deck product shippers. Residual oil-adjacent names (Gulf Coast Marine
  Fabricators w/ 211111, Petroleum Fabricators) correctly survive via the fabricator
  name + product-rescue path; any false-positives are the Researcher's catch, per contract.
- **Combined regional output carries no `state` column** (the grader output schema is
  rank/score/bucket/company/naics/city/address/zip/source). Geography for the region is
  preserved by the three per-state files; the combined file is a pure regional ranking.

## Method deviations from the bare run card (operator-approved this session)
- Operator asked for **both** per-state files and a combined regional map. Ran the grader
  4× into temp subdirs, then moved outputs into `outbox/` with `{LA|MS|AL|LA-MS-AL}` tokens
  inserted into the contract filenames to prevent the date-only names from colliding.
- The combined regional input was built by header-merging the three rosters (written to a
  temp file under `outbox/`, deleted after the run). `inbox/` was read-only throughout;
  `skills/` (the grader) was not modified.

## Proposed promotions (operator decides)
- **Multi-input / state-tagged output naming.** This pass needed a state/region token to
  run >1 roster in a day without collision. Consider promoting an optional `--label` (or
  `--tag`) arg to `grade_shippers.py` so the filename token is first-class instead of a
  post-run rename. Evidence: this run + any future regional grading.
- **Optional `state` passthrough column.** If regional/merged grading becomes routine,
  carrying `state` through to the flatbed/other-vertical output would keep geography intact
  for the future Matchmaker without forcing per-state files. Evidence: combined output here
  lost state; only per-state files retain it.

## Research worklist prepared (2026-06-17, same session)
- **Request:** operator asked for a random assortment of 200 companies from ranks 1-1000
  to prepare for research (Researcher hand-off, Contract 06).
- **Source:** `outbox/2026-06-17_LA-MS-AL_grader_flatbed_ranked.csv`, ranks 1-1000 (pool of
  1,000 — entirely FLATBED-YES, since the yes bucket is 2,679).
- **Method:** uniform random sample of 200, **seed = 20260617** (reproducible; reseed for a
  new draw). State re-attached by exact-name lookup against the source rosters in LA→MS→AL
  order (the same first-occurrence order the regional dedup used).
- **Output:** `outbox/2026-06-17_research_worklist_LA-MS-AL_n200.csv`
  (cols: research_id, rank, score, bucket, company, state, city, naics, address, zip, source).
- **Draw stats:** even spread across rank bands (1-250: 53, 251-500: 46, 501-750: 48,
  751-1000: 53); state mix LA 67 / MS 39 / AL 94; 0 rows unmatched on state; rank range 11-1000.
- No web, no CRM, no import — staged worklist only.
