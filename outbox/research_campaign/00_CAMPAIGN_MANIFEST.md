# Researcher Campaign — top-50 band (5,735 companies, 115 batches)

**Created:** 2026-06-13 · **Source pile:** `outbox/2026-06-13_grader_flatbed_ranked.csv` (score-50 band only)
**Role:** Refiner Job 2 (the Researcher), run in chunks of 50 per `skills/shipper-researching`.

## What this campaign is
Deep-research all 5,735 score-50 flatbed candidates (tier-1 NAICS **and** strong name signal —
the cleanest tier) into verified, CRM-ready shipper records. 115 assignments of ~50 companies.

## Folder layout (all under `outbox/`, per the Constitution threading standard)
```
outbox/research_campaign/
  00_CAMPAIGN_MANIFEST.md                       # this file — plan + progress backbone
  01_ASSIGNMENT_SPEC.md                         # the fixed per-company procedure (the "assignment")
  LESSONS_LEDGER.md                             # growing memory + proposed skill promotions
  2026-06-13_researcher_queue_top50band.csv     # the 5,735, ordered, with batch + status columns
  2026-06-13_batch_index.csv                    # 115 rows: batch -> primary_state, family, status
  results/
    shipper_registry.csv                        # running CRM-ready registry (17 cols, APPENDED)
    YYYY-MM-DD_researcher_batch_<NNN>.csv        # per-batch import-ready output
logs/
    YYYY-MM-DD_researcher_batch_<NNN>.md         # per-batch run log (episodic memory)
```

## Ordering (state-clustered, density-first — RECOMMENDED, ratify before scaling)
Batches are grouped by state (most-dense states first), then by product family within a state.
A single batch therefore stays in ONE market + ONE freight type — which makes the parent-company
check and the eventual dial-list both more efficient. First states:
CA (b1–10) → TX (b10–17) → PA (b17–23) → OR (b23–28) → FL (b28–33) → AL (b33–38) → MO → MI → TN → NC …
*Alternatives if the operator prefers: literal grader-rank order, or family-first across all states.*

## The engine (how agents run an assignment) — RATIFIED 2026-06-14
Each batch = a 2-stage pipeline over its 50 companies:
1. **Research stage** — one agent per company runs `01_ASSIGNMENT_SPEC.md`, with `LESSONS_LEDGER.md`
   injected so it knows every parent/collision found so far.
2. **Verify stage** — a second agent adversarially re-checks each GREEN/Tier-1–2 (entity match by
   address/DOT, door really invites outside carriers) and **re-emits the full corrected row**.
   Default to downgrade if the citation fails.

**PERSIST = ORCHESTRATOR WRITES (ratified after the wave-1 stall).** Workflow agents do NOT write
any file — a background agent's `Bash`/`Write` would hang on an un-answerable permission prompt
(this stalled wave 1 at persist). Instead the workflow ends after Verify and the orchestrator
parses `journal.jsonl` (every agent result is a structured payload there) to assemble the registry,
per-batch CSVs, run log, and ledger update with its own tools. Read-only research tools
(WebSearch/WebFetch/Read/ToolSearch) are auto-approved in `.claude/settings.json`; no write perms
are granted to background agents.

### Constitution reconciliation (operator must ratify)
`CLAUDE.md` rule 4: *"agents never call other agents; coordination routes through files or the
operator."* That rule governs the named ACE-OS pipeline agents. This campaign parallelizes the
SINGLE Researcher role across a batch under operator-reviewed waves — the orchestrator fans out,
all state lives in files (queue/ledger/registry), and the operator gates each wave. **Ratify that
this is an allowed implementation of the Researcher, not a new autonomous agent-calls-agent loop.**

## Cadence & review
- Run a **pilot of 1 batch** first; operator reviews quality before any scale-up.
- Then waves of N batches; **operator reviews after each wave**, updates priority, continues.
- CRM is **PROPOSE-ONLY**: registry is staged import-ready; the operator does the HubSpot import.

## The learning loop ("research better as we go")
After each batch the orchestrator appends to `LESSONS_LEDGER.md`: new parent programs, new
name-collisions, new door phrasings, wasted-effort patterns. Those feed the NEXT batch's prompt
immediately, and the durable ones are flagged as **proposed promotions** for the operator to move
into `skills/shipper-researching/` (logs = episodic, skills = semantic; operator promotes).

## Progress
- Status tracked in `2026-06-13_batch_index.csv` (`status` column: PENDING → DONE).
- **5 / 115 batches complete (batches 1–5, all CA). 250 / 5,735 companies researched.**
- Wave 1 (2026-06-14): 228 flatbed kept, 22 wrong-trailer routed out, 37 GREEN doors (16%),
  14 verify-downgrades, 8 new parent programs. See `logs/2026-06-14_researcher_wave1.md`.
- **Next slice:** batches 6–10 (CA steel/concrete/lumber tail → into TX at b10).
