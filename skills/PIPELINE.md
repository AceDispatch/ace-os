# ACE-OS Shipper Pipeline — Skills Map

Three skills, run in order. Each does ONE job with sharp edges.

## The pipeline
  shipper-prospecting  →  shipper-grading  →  shipper-researching
  (Prospector)            (Grader/Refiner J1)   (Researcher/Refiner J2)

### 1. shipper-prospecting — PULL & BIN WIDE
Pull EPA roster, bin into broad flatbed-plausible NAICS families. When unsure,
INCLUDE. No grading, no web, no geography. Output: raw binned candidate roster.

### 2. shipper-grading — GRADE & FAN BY EQUIPMENT TYPE (mechanical, no web)
Grade flatbed-plausibility (name+NAICS). Sort into:
  FLATBED-YES / FLATBED-UNSURE / OTHER-VERTICAL (dump/van/heavy-haul/tanker) / DISCARD
Dedupe to company. RANK the flatbed-yes bucket (steers the Researcher).
The OTHER-VERTICAL bin = seed for future vertical directories (dump truck dir first).
Output: ranked flatbed roster + parked other-vertical roster.

### 3. shipper-researching — DEEP RESEARCH 50 AT A TIME (slow, web-heavy)
Operator points it at a slice ("research ranks 100-150"). Runs in CHUNKS OF 50.
Per company: scan for door (3 triggers) + CHECK PARENT + capture contact + effort-tier
+ EXCLUDE/FLAG (wrong-trailer/defunct/misidentified/name-collision/captive-only).
Output: CRM-stable records appended to the running registry.

## Related skills (existing)
- fmcsa-lead-grading — the TRUCKING workflow (carrier leads), separate pipeline. v4 adds a
  tractor gate (rules out box trucks/hotshots/sprinters) + TRUE authority age (AuthHist,
  not ADD_DATE); two-step run: `extract_leads.py` → `grade_leads.py`.

## Parked (not built — see /proposals)
- Assayer — new-mine assessment protocol (one mine EPA, already assayed).
- Matchmaker — carrier<->shipper matching (future, needs more carriers).

## Source of truth
Doctrine derived from the verified hand-run phase (two deep-research passes, 102
companies). Ratified 2026-06-13. See /proposals for the ratified proposals and
STATE.md for the governing architecture.
