# STAGE ZERO — Run Guide (transition from Desktop to Code)

This package was designed in the Desktop chat (the architect's office) but
**must run in Claude Code on your machine** (the factory floor), because the
Desktop sandbox is network-locked and cannot reach the Census/EPA hosts. Your
local Claude Code has open network access, so it runs here cleanly.

## What stage zero does
Proves the two-layer shipper-discovery architecture on real data for one state:
- **Layer 1 (landscape):** what manufacturing/mining categories exist in the
  region and how concentrated — FREE, from Census CBP. Counts, no names.
- **Layer 2 (roster):** actual company names+addresses with NAICS — FREE, from
  EPA FRS. Partial (skews heavy/permitted), the free floor.
- **Scorecard:** coverage % of roster vs landscape, per industry — tells us
  where free data is enough and where we need ThomasNet/Chrome or paid data.

## One-time setup (5 minutes)
1. **Get a free Census API key:** https://api.census.gov/data/key_signup.html
   (email arrives in seconds).
2. **Add it to `ace-os/.env`** (same file as the Aircall keys):
   ```
   CENSUS_API_KEY=your_key_here
   ```
3. **Install deps** (in the ace-os folder, in your terminal or Code):
   ```
   pip install requests python-dotenv
   ```

## Running it (in a Claude Code session pointed at ace-os)

You can either run the commands yourself in the terminal, or just tell Claude
Code in that session: *"Run stage zero for Texas per stage_zero/RUN_GUIDE.md."*

**Step 1 — landscape (Texas, DFW core counties):**
```
python stage_zero/scripts/01_census_landscape.py --state 48 --counties 113,439,121,085,139,251,257,397,367,497
```
(Drop `--counties` to pull all of Texas. 48 = Texas. The 10 counties listed are
the DFW core: Dallas, Tarrant, Denton, Collin, Ellis, Johnson, Kaufman,
Rockwall, Parker, Wise.)
→ writes `output/census_landscape_48.csv` and `..._48_summary.csv`, and prints
the top 15 industries by establishment count.

**Step 2 — free roster (Texas):**
```
python stage_zero/scripts/02_epa_roster.py --state TX
```
→ writes `output/epa_roster_TX.csv`. If EPA's download URL has changed and it
errors, follow the printed instructions: download the TX file from
https://www.epa.gov/frs/epa-frs-facilities-state-single-file-csv-download ,
drop it in `stage_zero/data/`, and rerun with `--localzip stage_zero/data/<file>.zip`.

**Step 3 — coverage scorecard:**
```
python stage_zero/scripts/03_coverage_check.py --state-fips 48 --state TX
```
→ writes `output/coverage_TX.csv` and prints overall coverage % plus the
biggest gaps to target next.

## What to bring back to the Desktop chat
Once it runs, the analysis is a right-brain job. Bring back (paste or upload):
- `census_landscape_48_summary.csv` — so we read the real landscape together
- `coverage_TX.csv` — so we see where free data is strong vs thin

Then we analyze: which NAICS categories are the real flatbed-freight targets,
which are well-covered by free data, and which need ThomasNet/Chrome or paid
MNI to complete. That analysis sets the next stage of the hunt.

## Where this fits the architecture
- This is the **prototype** of the national pipeline, run on one state.
- It is **read-only** — pulls public data, writes only to `stage_zero/output/`.
  No CRM writes, no external posts. Consistent with the ace-os constitution.
- The national 50-state version is a documented next-phase build (see STATE.md),
  not part of the 10-day window. Stage zero proves the loop; scale comes later.

## Honest expectations
- Census data lags ~18 months — treat counts as recent-historical, not live.
- EPA FRS under-covers small/light manufacturers (the gold-mine small shippers),
  so expect coverage % to be lower in small-shop NAICS — that's the signal
  telling us where browser/paid sources earn their place, not a failure.
