# Contract 02 — Connect Reconciliation (one-shot audit)

**Job (one sentence):** Find every carrier Anthony Smart actually connected
with on the phone (June 1–5, 2026) that has no corresponding note/activity in
HubSpot, so no warm lead dies undocumented.

## Input
- Aircall call records for 2026-06-01 through 2026-06-05, pulled via
  `scripts/aircall_pull.py` (requires `AIRCALL_API_ID` / `AIRCALL_API_TOKEN`
  in `.env`).
- HubSpot Company records and Notes owned by Anthony Smart
  (ownerId 164918656), via the HubSpot MCP connection. READ ONLY.

## Method
1. Pull all calls in the window. Keep answered/connected calls above a
   minimum-duration threshold (default ≥ 60s talk time; log the threshold).
2. Match call phone numbers against HubSpot Company phone fields
   (normalize to digits-only, match on last 10).
3. For each matched company, check for any Note or logged activity within
   48h of the call. No note → flag as "connected, undocumented."
4. Unmatched numbers (a call with no CRM record at all) are their own
   bucket — these may be the most valuable finds.

## Output (to `outbox/`)
1. `YYYY-MM-DD_reconciliation_undocumented.csv` — company, DOT if known,
   number, call date/time, duration, current HubSpot status.
2. `YYYY-MM-DD_reconciliation_orphan_calls.csv` — connected calls matching
   no CRM record.
3. `YYYY-MM-DD_reconciliation_summary.md` — counts, method notes, threshold
   used, and any data-quality observations.

## Explicit non-goals
- NO status changes, NO note creation, NO CRM writes of any kind. This audit
  exists precisely because statuses were frozen pending it. Findings are
  staged; the operator acts on them.

## Log
- Standard run log. Record API pagination details and any calls that could
  not be classified.
