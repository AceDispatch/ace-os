# SKILL PROPOSAL — Refiner Job 1: The GRADER  [RATIFIED 2026-06-13]

**Status:** RATIFIED. Mechanical, no web, runs on the WHOLE pile at once.
Splits raw EPA ore into graded buckets AND fans it out by equipment vertical.

## What this hat is

The Grader turns the Prospector's wide bins into a graded, ranked pile — AND
sorts ore by EQUIPMENT TYPE so flatbed is processed now while other types
(dump/van/heavy-haul) accumulate as seed inventory for future verticals. Pure
data processing: name + NAICS → grade + bucket + vertical. NEVER touches the web.

### Ratified doctrine

**1. Mechanical only — NO web, NO door-checking, NO contact capture.**
Name + NAICS signals → grade. Runs the whole pile in one fast pass. (Web research
is exclusively the Researcher's job, Job 2.)

**2. Grade flatbed-plausibility, dual-axis** (proven in the passes):
- NAICS tier (almost-always open-deck product vs ambiguous)
- Name signal (Steel/Fab/Precast/Lumber vs Plating/Recycling/Service)

**3. THE BUCKETS — sort by freight type, not just yes/no:**
- **FLATBED-YES** — strong NAICS + clean name, genuine open-deck product.
- **FLATBED-UNSURE** — ambiguous (NAICS vs name conflict); kept, not discarded
  (the AERT lesson — a real decking maker "recycling" almost killed).
- **OTHER-VERTICAL** — a real shipper but WRONG EQUIPMENT for flatbed: dump,
  van, heavy-haul, tanker. Routed to a SEPARATE bin, sub-tagged by suspected type
  (dump / van / heavy-haul / tanker). This bin is NOT processed by the flatbed
  Researcher — it is SEED for building future vertical directories (dump-truck
  directory first). One Grader pass simultaneously feeds the flatbed pipeline AND
  accumulates every other equipment vertical's raw material. Nothing discarded
  for being wrong-trailer — it is FILED by trailer.
- **DISCARD** — genuine non-shippers: plating, coating, recycling, scrap,
  service/finishing with no product-shipper signal.

**4. Dedupe to company** (collapse 15x-CMC / 7x-Hanson facility repeats; rank by
company, not EPA site).

**5. RANK the FLATBED-YES bucket.** The rank steers the Researcher ("research
ranks 100-150 next"). PROVEN predictive: higher slice ~2x richer (100-150 vs
200-250). The rank is the steering wheel for the expensive Researcher.

### Known limitation (carry honestly)
Scale-proxy surfaces obvious national anchors (CMC, Trinity) at the top. Operator
may SKIP the top to find non-obvious mid-size gold — a valid, proven move. The
rank is a tool the operator steers by, not gospel.

### Output
- Flatbed graded roster: `rank, score, company, naics, city, bucket(yes/unsure), source`
- Other-vertical roster: `company, naics, city, suspected_vertical(dump/van/heavy-haul/tanker), source` — parked for future vertical processing
- Discard pile: dropped (or logged separately for audit)

### Open questions — RESOLVED
- Buckets: flatbed-yes / flatbed-unsure / OTHER-vertical (sorted by type for
  separate future processing) / discard. RATIFIED.
- Mechanical, no web. RATIFIED.
- Rank steers the Researcher. RATIFIED.
