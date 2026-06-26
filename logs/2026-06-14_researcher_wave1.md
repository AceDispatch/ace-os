# Run Log — Researcher Wave 1 (batches 1–5)

- **Date:** 2026-06-14
- **Agent:** Researcher (Refiner Job 2), run as orchestrated workflow `wf_4e54547a-21d`
- **Input:** `outbox/research_campaign/2026-06-13_researcher_queue_top50band.csv`, batches 1–5 (250 companies, all CA, mostly structural-fab)
- **Method:** per-company research (assignment spec) + adversarial verify on GREEN/Tier-1–2
- **Outputs:** appended to `results/shipper_registry.csv`; per-batch `results/2026-06-14_researcher_batch_001..005.csv`; raw `results/2026-06-13_wave1_raw.json`

## Incident — persist step stalled (recovered, no data loss)
The workflow's final **persist agent chose to write via `Bash`**, which was not in the auto-approved
read-only research allowlist (WebSearch/WebFetch/Read/ToolSearch). In a background workflow that
permission prompt could not be surfaced, so the agent hung (~7 min idle, output JSON never written;
journal showed 304 started / 303 returned). **Recovery:** the persist agent's prompt embedded the full
250-row result set, so the data was extracted directly from its transcript and written by the operator
side; the stuck workflow was then stopped. **Fix for next wave:** the persist step must use the `Write`
tool (not Bash), OR add `Write(outbox/**)` to the allowlist, OR have the orchestrator (not a workflow
agent) do the final file write. Recommended: orchestrator writes; workflow returns data only.

## Results (250 researched)
- Flatbed kept: 228 · Wrong-trailer routed to other-vertical: 22
- flatbed_fit: yes 131 · no 63 · unsure 38 · wrong-trailer 18
- Entity resolved: 240/250 (9 name-collision-unresolved, kept at low tier)
- **GREEN verified doors: 37 / 228 flatbed (16%)** — consistent with skill doctrine (live portals rare)
- Effort tiers (post-verify, flatbed): T1 7 · T2 26 · T3 128 · T4 26 · excluded(0) 40
- Door types: captive-authority 28 · parent-program 7 · portal 2 · none 191
- **Verify stage: 52 needed verify, 14 downgraded (27%)** — skeptic is doing real work
- EXCLUDE/FLAG catches: defunct 17 · naics-mismatch 34 · captive-only 95 · wrong-trailer 16

## Proposed promotions (operator → skill)
- **New parent programs** (add to DOOR_TRIGGERS.md known-parents): Commercial Metals Co. (CMC, Irving TX);
  The Herrick Corporation; Atkore Inc. (Calpipe Industries); Schuff Steel / DBM Global; Nucor Buildings
  Group → CBC Steel Buildings (T1 door); 101 Pipe & Casing; American Tank Co.; Paso Robles Tank /
  Associated Construction & Engineering.
- **Engine fix:** persist via Write tool / orchestrator, not Bash (see incident above).
- **Pattern:** CA top-tier structural-fab is dominated by small captive-fleet shops (T3) — "captive-only"
  flag fired 95× — so GREEN-door yield here is low; parent-owned divisions are where the actionable doors are.
