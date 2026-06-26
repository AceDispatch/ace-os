# SKILL PROPOSAL — The Prospector (v0.2, simplified)

**Status:** RATIFIED 2026-06-13. "When unsure, include" confirmed.
**Operator direction (2026-06-13):** Keep it simple. Pull from the EPA API we
have plugged in, churn it, and bin WIDE into broad flatbed-plausible families.
Deliberately leave deep discrimination to the Refiner. Wide net, loose bins.

## What this hat is now

Dumb, wide, fast. The Prospector's only job: pull EPA facility data and rough-sort
it into broad bins. It does NOT grade, narrow, resolve trailer types, or research.
A wide net with loose bins gives the downstream Grader+Researcher maximum raw
material to churn — the "more for the analyst to churn" principle.

### Proposed doctrine

**1. Source = EPA API (already plugged in), single mine.**
Pull from the EPA roster. Public domain, NAICS-tagged, legally unconditional.
Every candidate stamped `source: EPA_FRS`. No other source at this stage.

**2. Bin WIDE into flatbed-plausible families.**
Sort by NAICS into broad bins — do NOT agonize over edges. The families:
- Structural / fabricated / plate / architectural metal
- Steel & metal production / forming
- Pipe / tube / valve
- Concrete / precast / pipe / stone (broad — includes maybe-dump; Researcher resolves)
- Lumber / wood / building materials
- Machinery / heavy equipment
- Transportation equipment (oversized)
- Prefab / metal buildings / tanks
Anything plausibly open-deck goes in a bin. When unsure, INCLUDE it — width is
the goal; the Grader and Researcher narrow later.

**3. Geographically agnostic.** No geography filter (it's a Matchmaker concern,
and EPA's geo fields are too dirty anyway). NAICS is the only sort axis.

**4. No grading, no scoring, no door-checking, no ranking.** Those are the
Grader's and Researcher's jobs. The Prospector outputs raw, binned, source-tagged
candidates and nothing more.

### Output
Wide binned candidate roster: `name, address, city, zip, naics, source, bin`.
Raw. Ungraded. As wide as the net catches.

### Open question for operator
- "When unsure, include" — RATIFIED. Width wins; downstream narrows by type.
