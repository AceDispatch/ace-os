---
name: shipper-grading
description: Grade and sort a raw EPA candidate shipper pile for Ace Dispatch into ranked flatbed buckets AND separate equipment-type verticals. This is Refiner Job 1 (the GRADER) — the FIRST refining pass. Use after the Prospector has pulled a raw binned roster and before the Researcher deep-researches it. The Grader is MECHANICAL and NEVER touches the web — it works on name + NAICS signals only, runs on the WHOLE pile at once, and is fast. It sorts into FLATBED-YES, FLATBED-UNSURE, OTHER-VERTICAL (dump/van/heavy-haul/tanker — parked as seed for future vertical directories), and DISCARD, dedupes to company, and RANKS the flatbed-yes bucket so the operator can direct the Researcher to a slice. Trigger on "grade the pile", "grade shippers", "rank the candidates", "first refining pass", "sort the ore".
---

# Shipper Grading — Ace Dispatch (Refiner Job 1, the Grader)

This skill runs the **Grader**: the first of the two refining passes. It turns the
Prospector's wide, raw, binned pile into a **graded, ranked flatbed roster** AND **fans
the ore out by equipment type** so flatbed is processed now while other equipment types
accumulate as seed inventory for future verticals. It is pure data processing — name +
NAICS signals only — and **never touches the web**. Web research is exclusively the
Researcher's job (Refiner Job 2).

## Governing philosophy — mechanical, whole-pile, fast; sort don't discard

The Grader's economics are the opposite of the Researcher's: it processes the entire
universe in one cheap pass and produces the **map** that tells the expensive Researcher
where to dig. Its second principle is **file by trailer, don't discard by trailer** — a
real shipper that hauls dump/van/heavy-haul isn't waste for the flatbed pipeline, it's
seed for a future vertical directory. One Grader pass simultaneously feeds the flatbed
pipeline AND accumulates raw material for every other equipment type Ace will dispatch.

## The grade — dual axis, name + NAICS only

For each candidate, score flatbed-plausibility on two axes (proven across both research passes):
- **NAICS tier** — does the code almost-always mean an open-deck product shipper, or is it
  ambiguous? (tier-1 strong open-deck vs tier-2 plausible)
- **Name signal** — does the name say `STEEL / FABRICAT / STRUCTURAL / REBAR / PIPE /
  PRECAST / LUMBER / TRUSS / BEAM / TANK / FORGING / FOUNDRY` (yes-signal) or `PLATING /
  COATING / ANODIZ / GALVANIZ / RECYCL / SALVAGE / SCRAP / WASTE / MACHINE SHOP / REPAIR /
  ENERGY SERVICES / OILFIELD SERVICE` (no-signal)?

## The buckets — sort by FREIGHT TYPE, not just yes/no

- **FLATBED-YES** — strong NAICS + clean name, genuine open-deck product. The pile the
  Researcher works first.
- **FLATBED-UNSURE** — ambiguous (NAICS vs name conflict). KEPT, not discarded. (The AERT
  lesson: a composite-decking maker the word "recycling" almost killed — the unsure bucket
  rescues real shippers a pure no-filter would lose.)
- **OTHER-VERTICAL** — a real shipper but WRONG EQUIPMENT for flatbed: dump, van,
  heavy-haul, tanker. Routed to a SEPARATE roster, **sub-tagged by suspected type**
  (`dump` / `van` / `heavy-haul` / `tanker`). NOT processed by the flatbed Researcher —
  this is SEED for building future vertical directories (dump-truck directory first).
  Examples: loose aggregate / cement (`dump`), metal powders & drums (`van`), liquids
  (`tanker`). Nothing discarded for being wrong-trailer — it is FILED by trailer.
- **DISCARD** — genuine non-shippers: plating, coating, recycling, scrap, service/finishing
  with no product-shipper signal. (Logged separately for audit, not silently deleted.)

## Dedupe to company

Collapse facility repeats (the 15x-CMC / 7x-Hanson problem) so the rank is by **company**,
not by EPA site. Normalize names (strip " DBA ", " PLANT", " - " suffixes) before dedup.

## Rank the FLATBED-YES bucket

Produce a rank within flatbed-yes. **The rank is the steering wheel for the Researcher** —
the operator points the Researcher at a slice ("research ranks 100-150 next"). This ranking
is PROVEN predictive: the 100-150 slice yielded ~2x the workable shippers of the 200-250
slice. The rank is a tool the operator steers by, not gospel.

## Known limitation (carry honestly)

The scale-proxy in the grade surfaces obvious national anchors (CMC, Trinity, Hanson) at
the top — the names the operator may want to SKIP to find non-obvious mid-size gold.
"Skip the top, take the middle" is a valid, proven move. The Grader produces the rank; the
operator chooses the slice.

## Hard rules

- **NEVER touch the web.** Name + NAICS only. (Web = Researcher's job.)
- **No door-checking, no contact capture, no verification.** That's the Researcher.
- Runs the WHOLE pile in one pass, then stops.

## Output

- **Flatbed graded roster:** `rank, score, company, naics, city, bucket(yes|unsure), source`
- **Other-vertical roster:** `company, naics, city, suspected_vertical(dump|van|heavy-haul|tanker), source` — parked for future vertical processing
- **Discard log:** dropped names + reason (audit only)

The flatbed graded roster is the map the Researcher works, 50 at a time.
