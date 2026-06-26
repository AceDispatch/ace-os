# Contract 06 — Shipper Prospector (Stage 1)

**Job (one sentence):** Pull the EPA FRS facility rosters for all 50 states (or a
subset), filter WIDE to mfg/mining sectors, tag each with a flatbed-plausible
bin, and write them to `inbox/` for the Grader. Nothing else.

## Input
- None required — the Prospector pulls from the EPA FRS public download API.
- Optional: `--states TX,OK` to pull a subset; `--localdir <dir>` to use
  pre-downloaded EPA state zips; `--skip-existing` to resume a partial pull.

## Method
- Run `skills/shipper-prospecting/scripts/pull_epa.py` exactly as documented in
  `skills/shipper-prospecting/SKILL.md`.
- WIDE net: keep any facility with a NAICS in sectors 21/31/32/33 (mfg + mining).
  When unsure, INCLUDE — width is the goal. Tag each with a flatbed-plausible
  bin; facilities with no specific bin but in-sector are kept as `other_wide`.
- No grading, no ranking, no web, no geography filter. Those are downstream jobs.
- If EPA's download URL 404s for a state, the script logs it and continues;
  re-run the failed states with `--states <list>` or `--localdir` after a manual
  download from epa.gov/frs/epa-frs-facilities-state-single-file-csv-download.

## Output (to `inbox/`)
1. `epa_roster_<ST>.csv` — one per state (re-pull / per-state grade flexibility).
2. `epa_roster_ALL.csv` — combined national file for one-shot grading.
   Columns: name, address, city, county, state, zip, naics, source, bin.
3. Run log to `logs/YYYY-MM-DD_prospector_run.md` — per-state counts, bin
   breakdown, any failed states.

## Explicit non-goals
- Does NOT grade, score, rank, or verify. That's the Grader (Contract 05) and
  the Researcher (Contract 07).
- Does NOT filter by geography or trailer type. The net stays wide; the Grader
  sorts equipment type and the Matchmaker (future) handles geography.
- Does NOT touch the web beyond the EPA FRS public download. No enrichment.
- Writes to `inbox/` (it is the pipeline's intake) — the one agent that does, by
  design, since it is the source. Never deletes existing inbox files.

## Handoff
- After the pull, run the Grader on `inbox/epa_roster_ALL.csv` (national) or a
  specific `inbox/epa_roster_<ST>.csv` (single state).

## Run card
```
python skills/shipper-prospecting/scripts/pull_epa.py                 # all 50 states
python skills/shipper-prospecting/scripts/pull_epa.py --states TX,OK  # subset
python skills/shipper-prospecting/scripts/pull_epa.py --skip-existing # resume
```
Or: **"Run the Shipper Prospector per contract 06."**
Needs network (EPA downloads). No CRM writes. Polite 1s delay between states.

## Note on scale (operator direction 2026-06-13)
The net is intentionally RIDICULOUSLY WIDE. A wider intake means a larger refined
pile out the Grader's bottom and more research targets down the line. The Grader
proved it churns ~28k rows in seconds, so the Prospector does not pre-narrow —
it floods the Grader on purpose. The design law: the systems feed each other; a
wider front widens everything downstream.
