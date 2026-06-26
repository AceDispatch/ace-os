---
name: shipper-prospecting
description: Pull a WIDE, raw, source-tagged candidate roster of potential flatbed-freight shippers for Ace Dispatch by querying the EPA Facility Registry Service. Use whenever the task is to prospect, hunt, pull, or build a candidate shipper list from the EPA mine. This is the FIRST stage of the pipeline (Prospector -> Grader -> Researcher): it PULLS and BINS WIDE only — it does NOT grade, rank, verify doors, or research. When unsure whether a facility belongs, it INCLUDES it (width wins; downstream narrows). Single source: EPA FRS (public domain, NAICS-tagged, legally unconditional). Geographically agnostic. Trigger on "prospect shippers", "pull EPA", "pull candidates", "build the shipper pile".
---

# Shipper Prospecting — Ace Dispatch (Pull & Bin Wide)

This skill runs the **Prospector**: stage one of the shipper-registry pipeline. Its only
job is to **pull raw candidate shippers from the EPA mine and bin them wide** into broad
flatbed-plausible families. It is deliberately dumb, wide, and fast. The downstream
**Grader** (Refiner Job 1) grades and sorts this pile; the **Researcher** (Refiner Job 2)
deep-researches chunks of it. The Prospector does none of that.

## Governing philosophy — width wins

A wide net with loose bins gives the Grader and Researcher maximum raw material to churn.
The small non-obvious shippers are exactly what a too-narrow filter buries. So the rule is
simple: **when unsure whether a facility belongs, INCLUDE it.** Over-inclusion is cheap
(downstream narrows); wrongful exclusion is invisible and permanent.

## The mine — EPA Facility Registry Service, single source

- Pull from the EPA roster (EPA API / FRS state files already wired into ace-os).
- EPA is public domain, NAICS-tagged, no accepted terms, no scraping restriction —
  legally unconditional (per STATE.md / EPA-only decision).
- Every candidate is stamped `source: EPA_FRS`.
- No other source at this stage. (New mines are assessed by the Assayer protocol only
  when the operator decides to add one — not here.)

## What to pull and how to bin

Filter the EPA roster to flatbed-plausible NAICS and sort into BROAD bins. Do not agonize
over edges — anything plausibly open-deck goes in a bin.

**The bins (by NAICS family):**
- `structural_fab_metal` — 332311,332312,332313,332321,332322,332323,332420,332439,332510,332618,332999,332410
- `steel_metal_production` — 331110,331221,331222,331318,331420,331491,331492,331511,331513,331523,331524,332111,332112,332114,332119,332215,332216
- `pipe_tube_valve` — 331210,332910,332911,332912,332919,332996
- `concrete_precast_stone` — 327120,327310,327320,327331,327332,327390,327991,327992,327999 (broad — includes maybe-dump; the Grader sorts equipment type)
- `lumber_wood_building` — 321113,321114,321211,321212,321213,321214,321215,321219,321911,321912,321918,321920,321991,321992,321999
- `machinery_heavy_equip` — 333111,333120,333131,333132,333241,333242,333243,333249,333413,333414,333415,333511,333922,333923,333924
- `transport_equip_oversized` — 336212,336214,336510,336611,336999
- `glass_heavy_materials` — 327211,327212,327213,327215,327993

If a facility's NAICS plausibly fits open-deck freight but isn't listed, **include it** in
the closest bin rather than dropping it.

## Hard rules (what the Prospector must NOT do)

- **No grading, no scoring, no ranking.** That's the Grader's job.
- **No web research, no door-checking, no contact capture.** That's the Researcher's job.
- **No geography filter.** Matching is a Matchmaker concern; EPA's geo fields are too dirty
  to filter on anyway. NAICS is the only sort axis.
- **No equipment-type sorting.** The Prospector bins by NAICS family only; the Grader
  separates flatbed from dump/van/heavy-haul.

## The script

`scripts/pull_epa.py` pulls EPA FRS for all 50 states (or `--states TX,OK`),
filters wide to NAICS 21/31/32/33, tags bins, and writes per-state +
`epa_roster_ALL.csv` to inbox/. Run: `python skills/shipper-prospecting/scripts/pull_epa.py`.
Use `--skip-existing` to resume, `--localdir` for pre-downloaded zips.

## Output

A wide, raw, binned, source-tagged candidate roster:
`name, address, city, zip, naics, source, bin`

Raw and ungraded — as wide as the net catches. This feeds the Grader.

## Why this stays simple

Every instinct to make the Prospector "smarter" (pre-filter, pre-grade, resolve trailer
types, narrow geographically) is the bundling failure — pulling a downstream job upstream.
The Prospector's discipline is restraint: pull wide, bin loose, tag the source, stop.
