# SKILL PROPOSAL — The Assayer (PROTOCOL, not a standing agent)

**Status:** PARKED 2026-06-13 — not stressed this phase. One mine (EPA),
already assayed. Hold as written; invoke only when adding a new mine later.
**Operator direction (2026-06-13):** The Assayer is NOT an organ in the running
pipeline. It is a PROTOCOL invoked ONLY when we want to find or assess a NEW mine
to prospect from. Right now there is one mine (EPA), it's assessed, it's clean,
we're working it. The Assayer sits on the shelf, dormant, until we've mined EPA
enough to want a new source — THEN we run Assayer protocols on the candidate mine.

## What this hat is

A standalone source-assessment procedure. Invoke-on-demand at mine-acquisition
time. It evaluates whether and how to draw from a NEW candidate source. It is an
AGNOSTIC REPORTER — observes a source's conditions, reports facts, flags concerns
for the operator; never auto-clears or auto-blocks. The human decides.

### When it runs
Only when the operator wants to add a new mine (e.g. after EPA is well-mined and
we want ThomasNet, a state directory, a paid database, a gated roll). NOT every
pipeline run. NOT on EPA again (already assessed).

### The protocol (the three axes, observe-and-report)
For a candidate source, report:
- **Legality:** accepted ToS? click-through? login wall? robots.txt? no-scraping
  clause? sanctioned access (download/API/license) vs scraped-public? Report the
  FACTS; flag anything "careful." Counsel triggers (route to lawyer):
  scrape-at-scale, resale, term-uncertainty.
- **Richness:** expected yield, novelty vs what we have, coverage if measurable.
- **Reusability:** worth returning to, leaning on, or one-off?

Output buckets: clean / careful / counsel — careful & counsel FLAGGED for the
operator, never auto-acted. Builds/updates the durable SOURCE MAP.

### Current SOURCE MAP (from the one assay done so far)
- **EPA FRS** — CLEAN, zero flags, public domain, rich, the active mine. (Assessed; in use.)
- **Census API** — clean-but-conditional (§9 wall + attribution); SET ASIDE/dormant. (Assessed; not used.)
- **ThomasNet** — pre-flagged TERMS-BOUND, browser-only, scrape-at-scale =
  counsel trigger. (NOT yet assessed in full — would be a future Assayer run.)
- Future candidates assessed when the operator decides to add a mine.

### Open question for operator
- Confirm the Assayer is shelf/on-demand (invoked at mine-acquisition), not a
  per-run pipeline stage. And that EPA needs no re-assay until something changes.
