# Staged Lead Pull — 1,000 true-tractor carriers (FL/VA/LA core + SE-belt topup)
**Date:** 2026-06-24 · **Status:** STAGED for operator import (propose-only — no CRM writes) · **File:** `2026-06-24_pull_FL-VA-LA-belt_1000.csv`

The next-1,000, built to the operator's spec: **true tractors, all dispatchable equipment** (not flatbed-only), concentrated in the wide-open FL/VA/LA markets with a fresh topup from the neighboring hot belt.

## Composition
| Segment | Leads | Window | Source states |
|---|---|---|---|
| **FL/VA/LA core** | 743 | true age ≤270d | FL 571 · VA 127 · LA 45 |
| **SE-belt topup** | 257 | true age ≤180d | GA 158 · NC 43 · AL 31 · SC 25 |
| **Total** | **1,000** | | |

**By tier:** P1 29 · P2 204 · P3 326 · P4 441 (233 P1+P2 cream).
**By age:** ≤90d 336 · 91–180d 401 · 181–270d 263 → **737 are ≤180d** (peak-ish); the 263 older are all FL/VA/LA core, the operator-chosen middle-window stretch.
**By equipment flag:** general-freight 825 · flatbed 98 · reefer 77.

## Method (all read-only / propose-only)
1. **Live FMCSA census** (`.csv`, reliable) for the 7 states — pulled the `OWNTRACT/TRMTRACT/TRPTRACT` vehicle counts that our 06-18 local files never captured. **This is the only source of truth for "true tractor."**
2. **True authority age** joined from `owner_operators_1x1_true_age_under_1yr_2026-06-18.csv` (AuthHist-derived).
3. **Net-new only** — deduped against all 2,949 book DOTs (live HubSpot pull).
4. **v4 grader** (`skills/fmcsa-lead-grading/grade_leads.py`, run unmodified): tractor gate ON, true-age gate, active operating authority, name filter (patched), full completeness, dispatchable-cargo. Precision-over-recall.

## Honest notes (read before importing)
- **The tractor gate dropped 57%** of the candidates as box trucks/hotshots — confirming these fresh markets run ~50% box trucks (LA 64%). This is exactly why the FL/VA/LA fresh pool couldn't reach 1,000 alone and the window had to stretch to ≤270d + a belt topup.
- **Equipment is general-freight-heavy, not flatbed.** Only 98 carriers flag flatbed commodities; 825 flag general freight. Per the v4 finding, **cargo flags are commodity *inference*, not equipment truth** — every one of these 1,000 is a verified tractor-trailer (equipment-flexible), but this is NOT a flatbed-loaded batch. That matches the operator's direction ("doesn't need to be flatbed only, just true tractors").
- **Topup was re-weighted** to prefer GA/AL over NC/SC, because the 45-day Aircall data showed NC (3% connect) and especially SC (0% on 195 dials) are over-dialed/fatigued. If you'd rather avoid NC/SC entirely, MS/AR/MO are clean alternative topup sources (not pulled here).
- **True age is a 2026-06-18 snapshot** (6 days old). A re-pull through the canonical `extract_leads.py` at import time would refresh ages by a few days; it won't change the picture.

## Next steps (operator)
- Import `2026-06-24_pull_FL-VA-LA-belt_1000.csv` (HubSpot Company fields, ranked, tiered).
- **Dial through the warmed number pool, dead numbers scrubbed first** — not the flagged 561-291-8209 Sales line (`compliance/voice-reputation/`). Fresh leads down a clean pipe is the compounding win.
- Florida is the anchor (571) — lean the new dialing there; it's the biggest open, above-average-converting market in the book.

*Read-only run. No CRM or Aircall writes. Staging assembled in `scripts/` (census `.csv` + true-age join) to avoid the AuthHist throttle path and keep `skills/` untouched; the grader ran as-is.*
