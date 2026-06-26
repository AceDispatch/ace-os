# ACE-OS SKILL PROPOSALS — ratification status (2026-06-13)

Derived from the verified hand-run phase (two deep-research passes, 102 real
companies, the EPA-only decision, the legal analysis).

## THE ACTIVE PIPELINE (ratified — build these now)

  PROSPECTOR  →  GRADER (Refiner Job 1)  →  RESEARCHER (Refiner Job 2)
  [RATIFIED]      [RATIFIED]                 [RATIFIED]
   pull EPA        grade whole pile,         deep-research 50 at a time,
   bin wide        sort by equipment type,   marching the ranks
   when unsure,    rank flatbed-yes          (the official 2nd refining pass)
   INCLUDE        (mechanical, no web)       (slow, web-heavy, batched)

## PARKED (real, but not this phase)
- ASSAYER — on-demand new-mine assessment protocol. One mine (EPA), already
  assayed. Invoke only when adding a new source later. PARKED.
- MATCHMAKER — separate system for when there are more carriers to match.
  Refiner output already feeds it. PARKED.

## Files
- PROPOSAL_prospector.md ......... [RATIFIED] pull EPA + bin wide, when-unsure-include
- PROPOSAL_refiner_1_grader.md .... [RATIFIED] grade + sort by equipment vertical (mechanical)
- PROPOSAL_refiner_2_researcher.md  [RATIFIED] deep-research 50/chunk through the ranks
- PROPOSAL_assayer.md ............. [PARKED] new-mine protocol, dormant
- PROPOSAL_matchmaker.md .......... [PARKED] future carrier-matching system

## Ratified decisions
1. Prospector: when unsure, INCLUDE (width wins).
2. Grader: mechanical/no-web; buckets = flatbed-YES / flatbed-UNSURE /
   OTHER-VERTICAL (dump/van/heavy-haul/tanker, sorted for separate future
   vertical directories) / DISCARD. One pass feeds flatbed now AND seeds every
   future equipment vertical.
3. Researcher: official 2nd refiner pass; runs in chunks of 50 through the ranks;
   parent-company check stays in.
4. Assayer + Matchmaker PARKED — not stressed this phase.

## NEXT: convert the three RATIFIED proposals into skill files (ace-os/skills/),
   wrap in agent contracts, stand up Prospector → Grader → Researcher in Code.
