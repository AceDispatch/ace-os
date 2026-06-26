# Aircall ↔ HubSpot Cross-Reference — 2026-05-10 → 06-24
**Generated:** 2026-06-24 · **read-only** (no CRM writes, no status changes, no notes created)

## Method
- **Calls:** `outbox/2026-06-24_aircall-pull_45d.csv` — **4,949 calls** (45 days, all lines/directions) pulled via `scripts/aircall_pull.py` (read-only GETs). Reduced to **2,702 unique phone numbers** (digits-only, last 10).
- **Book:** all **3,064** HubSpot Company records (every owner), pulled read-only via `query_crm_data`. Matched on `Company.phone` (clean 10-digit), exact on last-10.
- **Answered** = Aircall recorded an answer timestamp. **Connected (≥60s)** = max talk time on that number ≥ 60s — i.e. a real conversation, not a hang-up.

## Headline
| | Numbers | Answered | **Connected ≥60s** |
|---|---:|---:|---:|
| **In CRM (matched)** | 2,443 | — | **103** |
| **Not in CRM (orphan)** | 259 | — | 167 |
| **Total dialed** | 2,702 | — | — |

- **Book coverage: 80%** — 2,443 of 3,064 companies have been dialed; **621 never dialed.**
- **Match rate: 90%** of dialed numbers are tracked in the CRM. Tracking is good.
- Of dialed leads: **1,807 answered at least once (74%)** but only **103 had a ≥60s conversation (4.2%)**. Huge answer-to-conversation gap → the spam-flagged Sales line + stale lists (see `compliance/voice-reputation/`). People pick up, then hang up.

## Finding 1 — 67 warm leads with NO status logged (act first)
**103 carriers we held a real (≥60s) conversation with; 67 of them have no lead status set.** These are warm conversations at risk of dying undocumented.
- File: **`2026-06-24_xref_warm_followup.csv`** (company, DOT, state, tier, score, equipment, call stats, rep).
- By state: **TX 42**, GA 18, TN 14, NC 8, AL 6, MS 5, KY 3, MO 3, OH 2, FL 1, AR 1.
- By tier: P1 **55**, P2 23, P3 1, blank 24. *P1 leads convert to conversations best.*
- Note: warm conversations cluster in TX/GA/TN/NC — exactly where the leads are. **FL = 1** only because we've barely loaded FL (56 leads). This is the next-1,000 strategy in miniature: pull FL/VA/LA and the warm conversations follow.

## Finding 2 — 129 uncaptured outbound sales connects (create records)
**259 dialed numbers connected but have no CRM record. Splitting by direction:**
- **129 outbound-only, ≥60s** → the floor dialed out and had a real conversation with a carrier that was **never entered in HubSpot.** → `2026-06-24_xref_orphan_outbound_connected.csv`. These are the highest-value recoveries (triage for vendors/brokers, then create records).
- **49 involve inbound** → callbacks / dispatch-line (the clean 2023 line) conversations — operational, not prospecting; lower priority.
- Full orphan list: `2026-06-24_xref_orphan_calls.csv`.

## Finding 3 — data-quality flags (no action taken, staged)
- **Tier values are inconsistent:** `P1` vs `Priority 1`, `Priority 2`, `Priority 3` — two import conventions in the same field. Normalize before any tier-based automation.
- **113 phone numbers map to >1 company** — duplicate carrier records sharing a phone. Dedup candidate list is in the matched file (`crm_matches` > 1).

## Outputs (outbox/)
- `2026-06-24_xref_matched_calls.csv` — dialed numbers found in CRM, with company/DOT/state/tier/score/equipment/status/owner + call stats.
- `2026-06-24_xref_warm_followup.csv` — the 103 connected-conversation leads (67 with no status). **Start here.**
- `2026-06-24_xref_orphan_outbound_connected.csv` — 129 uncaptured outbound conversations (create-record candidates).
- `2026-06-24_xref_orphan_calls.csv` — all 259 orphan numbers.
- `2026-06-24_aircall-pull_45d.csv` — the raw call evidence.

## Non-goals (constitution)
No CRM writes, no status changes, no note creation, no Aircall changes. Findings are staged; the operator acts.
