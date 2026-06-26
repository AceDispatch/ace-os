# Contract 01 — Lead Intake Pipe

**Job (one sentence):** Turn a raw FMCSA Company Census CSV into a graded,
ranked, HubSpot-import-ready lead file. Nothing else.

## Input
- A raw FMCSA census CSV in `inbox/` (typically `Company_Census_File_*.csv`).
  Original headers, no renaming required.

## Method
- Run `skills/fmcsa-lead-grading/scripts/grade_leads.py` exactly as documented
  in `skills/fmcsa-lead-grading/SKILL.md`. Perfect-only gates, then the
  weighted rubric. Do not modify gates, weights, or keyword lists in-flight.
- If the file's columns don't match the field reference, STOP, log the
  mismatch, and flag the operator. Do not guess column mappings.

## Output (to `outbox/`)
1. `YYYY-MM-DD_leadpipe_graded.csv` — full ranked output.
2. `YYYY-MM-DD_leadpipe_summary.md` — rows in, qualified count, discard
   buckets with counts, tier split (P1–P4), top 25 preview.

## Explicit non-goals
- Does NOT import to HubSpot. Staged file only; the operator imports.
- Does NOT dedupe against existing CRM records (future part, own contract).
- Does NOT adjust scoring. Tuning proposals go in the run log.

## Log
- Standard run log to `logs/`. Include the discard-reason table — that table
  is how methodology drift gets caught.
