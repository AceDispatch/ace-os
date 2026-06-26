# Run Log — Shipper Researcher (Refiner Job 2) — LA/MS/AL first run

- **Date/time:** 2026-06-17
- **Skill / contract:** `skills/shipper-researching/SKILL.md` (Refiner Job 2, the Researcher).
  NOTE: no ratified contract file yet — STATE.md lists the Researcher as pending **Contract 07**.
  This was an operator-directed run against the built skill; flag for contract ratification.
- **Operator-initiated or scheduled:** Operator-initiated (supervised).
- **Inputs:** `outbox/2026-06-17_research_worklist_LA-MS-AL_n200.csv` — 200 companies
  (random sample of regional flatbed ranks 1-1000; LA 67 / MS 39 / AL 94).
- **Outputs (to `outbox/`):**
  - `2026-06-17_shipper_registry_LA-MS-AL.csv` — 200 CRM-stable records, tier-sorted
    (the "running registry"; created this run). Schema per skill: company_name, effort_tier,
    door_type, flatbed_fit, ships, city, state, phone, email, website, onboarding_url,
    contact_grade, parent_company, naics, source, vertical, notes.
  - `2026-06-17_researcher_summary_LA-MS-AL.md` — tier counts, door list, flag counts.
- **Result:** success — all 200 researched; door scan + parent check + FMCSA SAFER captive-authority
  check + contact capture + effort-tiering + EXCLUDE/FLAG applied. Read-only web only; no company
  contacted; no CRM write; nothing imported.

## Result table (calibration)
| Effort tier | Count | Meaning |
|---|---:|---|
| T1 self-onboard | 6 | verified carrier portal / parent program |
| T2 reachable-low | 24 | direct logistics desk / captive FMCSA authority / named contact |
| T3 reachable-high | 113 | general switchboard only |
| T4 no contact found | 57 | confirmed shipper, needs harder dig / unverified / defunct |

- **Verified carrier doors (GREEN): 31** (T1: 6, T2: 14, T3+: 11).
- **flatbed_fit:** yes 140 / unsure 60.
- **EXCLUDE/FLAG caught:** DEFUNCT 21 · UNVERIFIED-ENTITY (name-collision/unconfirmable) 25 ·
  WRONG-TRAILER 27 · CAPTIVE-ONLY 16.
- **Top doors:** CMC (myCMC portal — Capitol Steel LA + SMI Steel AL), Nucor/Harris Rebar
  (nlg.contract@nucor.com — Ambassador Steel LA + Jackson MS), Georgia-Pacific/KBX (Rocky Creek
  Lumber AL; REQS: 20-truck min, $1M auto / $100K cargo), West Fraser (Maplesville AL carrier app),
  plus captive-authority T2s (Tindall Precast, Zachry, Vallourec, Southland Steel, Hood Industries).

## Anomalies / data-quality notes
- **Worker CSV tail-misalignment — 30 of 200 rows.** A few research workers emitted a stray
  extra/missing field in the tail, shifting `contact_grade`→`notes` by one position (rich note
  spilled into the row's overflow / `vertical`). The leading columns (company…onboarding_url) and
  the note text were intact. **Repaired by content-based reconstruction** (NAICS = numeric token,
  notes = the prose field, grade = the enum value, source = constant EPA_FRS, vertical = from
  WRONG-TRAILER flag). On those 30 rows `parent_company` was reset to blank — **the parent detail
  is preserved inside `notes`**, just not in the dedicated column. Verified post-repair: 0 bad
  source, 0 bad vertical, 0 off-enum grade.
- One row (`LA TREATED LUMBER`) had `contact_grade="not found"` → normalized to `unconfirmed`.
- Residual top-of-rank false-positives expected and present (oilfield-adjacent fabricators, tiny
  shops with tier-1 NAICS) — consistent with the Grader's "Researcher catches them" design.

## Method deviations (operator-approved this session)
- **Ran all 200 in one pass.** The skill's discipline is "chunks of 50, operator reviews between
  chunks." Operator directed the full 200, so it ran as one consolidated pass with NO inter-chunk
  review. Noted for the record; revert to 50-at-a-time review cadence by default.
- **Execution = parallel subagents.** Run as 1 pilot + 19 worker subagents (Sonnet), each handling
  10 companies and writing a validated CSV part; the Code-side executor then consolidated +
  tier-sorted into the single registry. This is an execution strategy for one skill's workload, not
  ACE-OS pipeline agents invoking each other (the no-agent-calls-agent rule is intact — coordination
  was file-based, one registry out).

## Proposed promotions (operator decides)
- **Lock the Researcher's output as a strict schema.** 30/200 rows misaligned because free-form CSV
  column order isn't enforced. Promote either (a) an explicit "emit columns in EXACTLY this order,
  quote any field with a comma" rule into the skill, or (b) a JSON-per-record structured-output
  contract that's validated before it lands. This removes the repair step entirely on future runs.
- **Ratify Contract 07 (Researcher).** The skill is built and now battle-tested on 200; STATE.md
  still lists it as pending a contract. Worth formalizing input/output/permissions like 05.
- **Parent-door dedup.** Several sites share a parent door (CMC ×2, Nucor/Harris Rebar ×2). A future
  pass could collapse parent-covered sites into one relationship per the skill's dedupe note.
