# ACE-OS — Operating Manual

The execution layer ("left brain") of Ace Dispatch — the code, data pipeline, and backend that turn raw
rosters into onboardable shippers and power the Ace platform. This README is the **front door**: what's
here and how to run it. The *law* is `CLAUDE.md`; the *current state* is `STATE.md`; the *methodology*
lives in `skills/`.

## The canonical pipeline — Prospect → Classify → Research → Match
| Stage | Job | Skill | Output |
|---|---|---|---|
| **Prospect** | Pull a region's raw facilities from the EPA roster | `skills/shipper-prospecting` | candidate roster |
| **Classify** | Sort every company by equipment (flatbed/van/dump/tanker/heavy-haul) + FTL signal — multi-vertical, mechanical, no web | `skills/shipper-grading` | binned, ranked roster |
| **Research** | Confirm FTL + find the onboarding door + capture outbound lanes (web) | `skills/shipper-researching` | verified records |
| **Match** | Cross shippers against the carrier book | *(future)* | carrier ↔ shipper matches |

Doctrine: **sort, don't discard** (everything binned by equipment for later) · **quality over token-frugality**
(research the whole target vertical) · the bar is **FTL-confirmed + onboardable**.
*(A parked optional organ — the Assayer — grades data SOURCES, not companies; see STATE.md. Not a core stage.)*

## Source of truth — Supabase
The shipper/carrier database lives in **Supabase** (Postgres), defined by `db/schema.sql`. CSVs are
**exports / working files**, never the truth, and are git-ignored. The AI operates the DB live through the
**Supabase MCP**; `db/sync.py` is the headless write path. Live views (e.g. `v_ready_to_onboard`) are the dial sheets.

## How to run it
- **A region:** `pipeline/run_region.py --region <name> --counties "ST:County,…" --vertical flatbed`
  → Prospect → Classify → Research → sync to Supabase → deliverable. *(the standardized routine — Phase 3 build)*
- **Sync a CSV into the DB:** `python db/sync.py [path]`
- **Query / dial sheets:** live SQL via the Supabase MCP, or the `v_ready_to_onboard` view.

## Structure
- `db/` — schema + sync (**source of truth**) · `pipeline/` — the standardized routine
- `skills/` — methodology (read-only) · `contracts/` — agent contracts · `docs/` — specs & build plans
- `inbox/` — raw rosters (data) · `outbox/` — ratify-ready deliverables · `logs/` — run logs · `archive/` — retired
- `web/` — acedispatch.us source · `compliance/` — a2p + voice · `course/` `scripts/` `data/` `stage_zero/`

## Working rhythm
Operate from **VS Code**. The AI commits as it works; you hit **Sync Changes** to push to GitHub
(`AceDispatch/ace-os`, private). Data layers (`inbox/ outbox/ data/`) stay local + in Supabase — never pushed.
Record any structural change in `STATE.md` (State Doctrine).

**Status (2026-06-25):** vocabulary standardized · Supabase live (16k shippers, RLS-sealed) · GitHub backup · MCP connected.
