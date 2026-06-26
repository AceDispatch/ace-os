# Contract 03 — Morning Sales Brief (the eagle's first feather)

**Job (one sentence):** Before business hours, read the sales surface
(HubSpot + Aircall) and write a one-page brief. Sees and reports. No goals,
no writes, no opinions beyond flagging.

## Schedule
- Headless run, weekday mornings (e.g. 7:00 AM ET via Task Scheduler):
  `claude -p "Run the Morning Sales Brief per contracts/03-morning-sales-brief.md"`

## Input (all READ ONLY)
- HubSpot via MCP: companies owned by Anthony Smart (ownerId 164918656) —
  lead statuses, notes from the last 24h, any follow-up/task dates due.
- Aircall via `scripts/aircall_pull.py`: previous business day's call volume,
  connects, talk time.

## Output (to `outbox/`)
- `YYYY-MM-DD_morning_brief.md`, one page, in this order:
  1. **Countdown clocks** — time-critical leads first. Standing entry:
     Robert Gill / A&W Gill Transport (score 95), lease-on expiring ~June 23 —
     days remaining and last-touch date, every brief, until converted or dead.
  2. **Due today** — follow-ups and tasks dated today or overdue.
  3. **Yesterday in numbers** — dials, connects, talk time, notes logged.
     Flag gaps (connects without notes) — feeds the reconciliation habit.
  4. **Movement** — status changes and new notes in the last 24h, one line each.
  5. **Flags** — anything anomalous. Flag, don't interpret.

## Explicit non-goals
- No CRM writes, no recommendations on deal strategy, no lead re-scoring,
  no outbound communication. The brief informs the conductor; it does not act.

## Log
- Standard run log, including any source that failed to respond (a brief
  built on partial data must say so at the top of the brief itself).
