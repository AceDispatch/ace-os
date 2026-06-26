# Run Log — Shipper Grader (Contract 05) — First Run

**Date:** 2026-06-14
**Agent:** Shipper Grader (Refiner Job 1)
**Input:** inbox/epa_roster_TX.csv (28,640 EPA TX facilities — raw, unfiltered test)
**Operator:** Anthony (supervised first run)

## Result
- Rows in: 28,640 -> 25,221 distinct companies (after dedupe)
- FLATBED-YES: 4,033
- FLATBED-UNSURE: 1,993
- OTHER-VERTICAL: 1,182 (dump 482, tanker 459, van 169, heavy-haul 72)
- DISCARD: 18,013 (non-flatbed remainder — Prospector normally pre-filters these)

## Calibration event (caught in this run)
- FIRST attempt mis-bucketed: 21,210 to "unsure" because yes required a NAME
  signal. 1,966 tier-1-NAICS shippers were wrongly in unsure.
- FIX: tier-1 flatbed NAICS alone -> YES (NAICS is the strong signal). Rows with
  neither flatbed NAICS nor flatbed name -> DISCARD (self-protection vs raw feed).
- Re-run produced the sane distribution above.

## Notes
- Test fed the RAW roster (skipped Prospector). In production the Prospector
  pre-filters to flatbed NAICS, so the 18k discard shrinks dramatically.
- Residual top-of-rank false-positives (Anadrill/Schlumberger oilfield svc w/
  flatbed NAICS; an "Abilene Paint Shop") are EXPECTED — Researcher catches them.
- The ~4,000 flatbed-yes matches the by-hand pass. Grader validated.

## Tuning proposals for operator review
- Consider adding "PAINT SHOP", "ANADRILL", oilfield-service names to discard
  signals if false-positive rate at top of rank proves annoying. (Or leave —
  the Researcher catches them, and over-filtering risks losing real shippers.)

## Update — name-penalty system added (2026-06-13)
Per operator: name should derank HARD like the sales leads. Added penalty tiers:
- HEAVY -35 (paint shop, machine shop, repair, plating, testing, rental...)
- MED -20 (services, coating, shop, contractor, erection, maintenance...)
- LIGHT -10 (welding, distribution, warehouse, ornamental, custom...)
Result: "Hirschfeld Steel Paint Shop" dropped from rank #2 (score 50) to score 15,
sunk deep. 177 penalized service/facility names moved to ranks 1110-6026 (bottom).
Clean production-shipper names (Strong Structural Steel, Kyoei Steel, Gulf Marine
Fab, Texas Precast) hold the top. Bucket sizes barely moved (4009 yes) — penalty
REORDERS, doesn't delete. Floor clamped at 1. Heavy-penalized tier-1 names -> unsure.

## Refinement — penalty discipline (2026-06-13)
Operator: the penalty must read words in CONTEXT, not as a flat list. Three fixes:
- "welding" is NOT a penalty — it's a plausible fabricator (moved to positive). A
  flat -10 on welding was a discipline error.
- "shop" alone isn't the disqualifier — the PAIRING is. "paint shop"/"machine shop"
  sink (-35 phrase match); "wood shop"/"steel shop" do NOT (can be real producers).
- even a clean bare "shop" is a faint SIZE signal -> gentle -6 nudge, not a sink.
Rebuilt name_penalty() with 3 mechanisms: disqualifying PHRASES, standalone
disqualifiers (no dual reading), size nudge. Verified on real data: welding cos
rank 101+ at score 50; both Hirschfeld paint shops sank to rank 5969-70; top of
rank stayed clean. This was a DISCIPLINE correction, not a methodology change.

## FINALIZED 2026-06-13
Added oilfield/extraction/tanker discipline (role-in-freight, not industry):
- Services/extraction majors (Schlumberger->rank 5390, Baker Hughes->5419, Pure
  Resources->2759) SINK out of the working region.
- Tank STORAGE/farm hard-blocked; tank MAKERS (Overland Tank rank 2, Permian Tank)
  spared. Product-makers (motor oil, auto parts, oilfield EQUIPMENT) spared.
- Dedup strengthened: 25221->22844 companies (~2400 facility-dupes collapsed).
  Honest flatbed pile: 5518 (yes 2984 + unsure 2534).
- Working-region audit (top 1000): 3 dup-stems, 7 oilfield names (mostly equipment
  MAKERS that correctly survive; 1 true miss now fixed by tank-storage block).
VERDICT: working region ~99% clean. Grader LOCKED. Residual noise is Researcher's job.
