# Contract 04 — Consolidation Agent (NOT YET COMMISSIONED)

**Job (one sentence):** Weekly, read all run logs since the last pass and
PROPOSE promotions from episodic memory (logs) to semantic memory (skills) —
the hippocampus of ACE-OS.

## Status
Do not run this agent until the operator commissions it. It exists in the
roster so the slot and contract shape are fixed early.

## Input
- All files in `logs/` newer than the last consolidation marker.
- Current `skills/` contents (read only).

## Method
1. Extract every "Proposed promotions" entry and recurring observation
   (e.g. a name keyword that wasted dials three runs running).
2. Draft the exact skill-file diffs that would encode each lesson.
3. Identify stale structure: skill content contradicted by recent runs, or
   ledger entries that should be compressed/retired. Forgetting is a feature —
   propose retirements, never silently keep everything.

## Output (to `outbox/`)
- `YYYY-MM-DD_consolidation_proposals.md` — each proposal as: evidence (which
  logs), proposed diff, risk note. The operator approves/rejects; ONLY the
  operator applies changes to `skills/`.

## Explicit non-goals
- Never edits `skills/` directly. Never deletes logs. Proposals only.
