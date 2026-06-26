# Run Log — Shipper Researcher (Refiner Job 2) — LA/MS/AL BATCH 2 (fan-out experiment)

- **Date/time:** 2026-06-17
- **Skill:** `skills/shipper-researching/SKILL.md` (Researcher). Operator-directed experiment.
- **Purpose:** Controlled test of the token-conservation hypothesis — does putting MORE companies per
  agent (fewer agents) reduce token use for the same work? Held everything constant vs the batch-1 run
  (same protocol text, same model = Sonnet, same 200-company workload, same consolidation) and changed
  ONLY the fan-out: **10 agents x 20 companies** (batch 2) vs **20 agents x 10 companies** (batch 1).
- **Input:** `outbox/2026-06-17_research_worklist_LA-MS-AL_n200_batch2.csv` (200 companies, disjoint from
  batch 1 — verified 0 overlap by rank and name; LA 60 / MS 41 / AL 99).
- **Output:** `outbox/2026-06-17_shipper_registry_LA-MS-AL_batch2.csv` — 200 records, tier-sorted.
  Tiers T1 9 / T2 25 / T3 95 / T4 71; 39 GREEN doors; flatbed_fit yes 149 / unsure 50.
- **Result:** success (200/200 researched). No CRM, no contact, read-only.

## TOKEN COMPARISON (from on-disk subagent transcripts, identical metric both runs)

| | batch 1 — 20x10 | batch 2 — 10x20 | delta |
|---|--:|--:|--:|
| Agents | 20 | 10 | half |
| Assistant turns | 1,809 | 1,022 | -44% |
| Tool calls | 1,626 | 937 | -42% |
| **Output tokens** | 207,107 | 121,397 | **-41%** |
| **Total billed (cache-incl)** | 100,884,023 | 63,154,953 | **-37%** |
| Total billed / company | 504,420 | 315,775 | -37% |
| Avg per agent (total) | 5,044,201 | 6,315,495 | +25% |

**Finding (hypothesis CONFIRMED):** halving the agent count (doubling companies/agent) cut total token
use ~37% and output ~41% for the *same* 200-company workload. Mechanism: per-agent cost scales
**sublinearly** — each agent did 2x the companies but cost only +25% more, because the fixed per-agent
overhead (system prompt + tool schemas + instructions, re-read on every tool call) is paid 10x instead of
20x. Tool-calls-per-company nearly halved (4.7 vs 8.1), so far less context was re-read. This extends the
earlier cross-session trend (305-agent "250 pull" = most expensive; 20x10 = middle; 10x20 = leanest).

## The one agent failure was ENVIRONMENTAL, not batch-size (corrected per operator)
- **1 of 10 agents (research_id 41-60) stalled and died** — ran ~148 min / 114 tool calls, socket closed
  on return. **Root cause confirmed by operator: the terminal was unattended (machine sleep / connection
  dropped).** Network tool calls hung, the agent retried for ~2.5h, then the socket closed. This is an
  external interruption, NOT an intrinsic failure mode of the 20-company batch.
- It had already written its part file, so no data was lost; its 17 shifted rows were repaired by content.
  Its real token use is counted in the 63.2M (the "subagent_tokens: 0" was just the error path).
- **Retraction:** my earlier conclusion ("larger batches = higher disconnect risk = fragility cost") is NOT
  supported. Absent the AFK/sleep event, 10x20 would have completed cleanly AND ~37% cheaper. The only
  residual nuance: longer-running agents sit in a wider time window, so they're more *exposed* to any
  unattended interruption — an argument for keeping long unattended runs shorter or expecting to resume,
  not an argument against batching.

## Data-quality note
- Same tail-column CSV misalignment as batch 1 (35/200 rows here, concentrated in the failed agent's
  file). Repaired by content (NAICS=numeric token, notes=prose, grade=enum, source=EPA_FRS). Reinforces
  the standing proposal to lock the Researcher output to a strict/JSON schema.

## Proposed promotions (operator decides)
- **Bias toward larger batches for token efficiency.** 10x20 beat 20x10 by ~37% on the same work, with no
  intrinsic reliability penalty (the one failure was an unattended sleep/disconnect). The real ceiling is
  per-agent CONTEXT BLOAT at very large batches (e.g., 50+), not 20. Worth mapping where savings flatten
  (a 4x50 arm) before fixing a default.
- **Operational note, not a batch-size limit:** for long unattended fan-outs, keep the machine awake
  (caffeinate / disable sleep) or expect to resume — longer agents are simply exposed to a wider time
  window for an external interruption.

## Research-quality audit — 10x20 vs 20x10 (added 2026-06-17)
Question: did bigger batches make agents STRUGGLE (thinner research / fatigue / interruption damage)?
Method: audit both registries; control for different company samples via within-block positional decay
(read-only, registries joined to worklists on normalized name; 200/200 and 199/200 matched).

- **No within-block decay (decisive test).** Back-half vs front-half of each agent's block:
  batch 2 (20-blocks) +3.8% notes / +0.07 contact-fields; batch 1 (10-blocks) back-half also richer.
  Agents did NOT fatigue or cut corners on later companies in a big batch.
- **Interrupted agent (ids 41-60) was mid-pack, not an outlier** (notes 364 / contact 1.20 / 4 doors);
  excluding it barely moves batch 2 (402->406 notes). The AFK disconnect cost TIME, not quality — it
  finished researching and writing before the socket dropped.
- **Core job equal-or-better:** door detection batch 2 = 39 green / 34 T1+T2 vs batch 1 = 31 / 30.
  Flag discipline comparable (DEFUNCT/UNVERIFIED/WRONG-TRAILER/CAPTIVE 18/24/30/20 vs 21/25/27/16).
- **Only real diff:** batch-2 notes ~14% more concise (402 vs 471 chars), contact-fill ~8% lower
  (1.60 vs 1.73) — uniform (not end-loaded), partly sampling (more AL/obscure shops in b2). Structured
  fields were not dropped.
- **Per-agent variance is company-driven** (0-9 doors/block tracks active-fabricator vs defunct-foundry
  mix), not batch-size-driven.
- **VERDICT:** bigger batches did not degrade quality. On a quality-per-token basis, 10x20 >= 20x10.

## Proposed promotion — token-aware research default (operator applies; skills are READ-ONLY)
Recommend updating the Researcher skill's "chunks of 50 / review between chunks" run discipline to a
**token-aware default of ~15-20 companies per agent** (the first run was effectively ~10/agent).
Evidence: 10x20 cost ~37% fewer tokens than 20x10 for the same 200-company workload, with equal-or-
better quality and no within-block decay. Caveats to encode: keep the machine awake for long unattended
fan-outs; suspected quality ceiling is per-agent CONTEXT BLOAT past ~50/agent (unconfirmed — a 4x50 arm
would map it). Per the operator's 2026-06-17 decision ("Adopt + record"), Claude Code will default to
~15-20 companies/agent on research fan-outs until/unless the operator ratifies a different skill change.
- Carry the experiment numbers into any future cost modeling: ~315k-505k billed tokens/company depending
  on fan-out, dominated by cache re-reads, which scale with agent count more than company count.
