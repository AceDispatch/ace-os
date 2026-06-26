# Aircall ↔ HubSpot Cross-Reference — 6/8–6/13 (2026)

**Generated:** 2026-06-14 14:41 UTC · read-only

## Method
- Source calls: `outbox/2026-06-13_aircall-pull_calls.csv` (1,357 calls, 6/8–6/13).
- Reduced to **1013 unique phone numbers** (digits-only, last 10).
- Matched each against HubSpot **Company.phone** (2,499 companies, owner Anthony
  Smart) via `phone IN [...]` batch search. Company phones are stored as clean
  10-digit strings, so matching is exact on the last 10 digits.
- HubSpot companies loaded for matching: **735** distinct records.
- "Answered" = Aircall recorded an answer timestamp; "connected≥60s" = max talk
  time on that number ≥ 60 seconds.

## Headline
| Bucket | Unique numbers | of which answered | of which ≥60s talk |
|---|---:|---:|---:|
| **In CRM (matched)** | 719 | 529 | 21 |
| **Not in CRM (orphan)** | 294 | 234 | 59 |
| **Total** | 1013 | 763 | 80 |

- **71.0%** of dialed numbers matched an existing HubSpot company.
- **294 orphan numbers** had a call but no CRM record — of those, **59**
  had a 60s+ conversation (most likely to be worth creating a record for).
- **9 matched numbers** map to MORE THAN ONE company record (duplicate
  companies sharing a phone in the CRM) — see `all_company_names` / `crm_matches`.

## Outputs
- `2026-06-13_xref_matched_calls.csv` — dialed numbers found in HubSpot, with the
  company (highest ace_lead_score if duplicates), DOT/MC, state, equipment,
  score, tier, and call stats.
- `2026-06-13_xref_orphan_calls.csv` — dialed numbers with no CRM match.

## Non-goals (constitution)
No CRM writes, no status changes, no note creation. Findings are staged for the
operator to act on.
