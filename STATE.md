# ACE-OS — STATE.md (System State & Architecture)

**This is the bridge document.** It is the single canonical description of what
ace-os is, as it currently exists. The Desktop chat (right brain) holds the
*why* and the reasoning; this file holds the *what* and the *current shape*.
When the two conflict, this file outranks memory for facts; the conversation
record outranks this file for intent. Carry this file up to the Desktop chat at
the start of any design session so the architect works from ground truth.

**Version:** 0.4 · **Last updated:** 2026-06-22 (voice caller-ID reputation layer added — the voice twin of A2P/SMS)

---

## GOVERNING PHILOSOPHY

**The systems refine themselves and feed each other — each piece makes the
others stronger.** This is the design law, not a sentiment. Every organ's
output is another organ's intelligence. A part is built simple and does one
job; complexity lives in the interfaces between parts; and the parts form loops
where what one learns sharpens the next. When designing any new part, the test
is: *what does this part feed, and what feeds it?* If a part is a dead end —
takes input but improves nothing downstream and teaches nothing upstream — it is
probably the wrong part.

This recurs throughout ace-os under many names: the consolidation cycle, the
hippocampus, "hunts that inform other hunts." They are all the same principle:
**recursive self-refinement through clean interfaces.**

---

## THE TWO-HEMISPHERE MODEL

- **Right brain — Desktop chat.** Design, judgment, legislation, memory, the
  *why*. Fluid and exploratory. Where parts are designed and revised. Cannot
  run scheduled jobs; sandbox is network-locked (cannot reach arbitrary APIs).
- **Left brain — Claude Code in the `ace-os` folder.** Execution, the *what*,
  the running parts. Rigid and reliable. Open network access. Where agents run.
- **The bridge — this STATE.md.** Carried by the operator (Anthony) between the
  hemispheres. The one human-carried interface; nothing crosses automatically.

Design flows down (architect → files → folder). Evidence flows up (runs → logs →
analysis). The operator is the only carrier and ratifies everything that crosses.

---

## THE SEVEN DOCTRINES (the unbroken law)

1. **Two-Hemisphere Doctrine.** Legislate in the right brain; execute in the
   left. Never redesign mid-run in Code; never run production tasks from chat.
2. **State Doctrine.** Any session that changes the system's structure updates
   this STATE.md before closing. An unrecorded change is a broken law.
3. **One-Carrier Rule.** The operator is the only bridge. Files cross by hand,
   both directions. This is the safety property and the ratification mechanism.
4. **Earned Authority.** Every part is born propose-only. Write access is
   granted one narrow warrant at a time, only after a documented record of
   flawless supervised runs, and is instantly revocable. Authority is never
   granted by category.
5. **Single Source of Truth, split by kind.** For facts about the system, this
   file outranks all. For intent (the why), the conversation record outranks
   all. A conflict between them is itself a finding to repair.
6. **Proposal Flow.** Parts may propose law (via logs, via proposals), but
   proposals only become law by crossing the bridge, being deliberated with
   full context, ratified by the operator, and deployed back as files.
7. **Forgetting Clause.** Every consolidation prunes. Stale parts retired, old
   logs archived, contradicted structure corrected. The system describes what
   IS, not everything that ever was. Accumulation without pruning is the enemy.

---

## STANDING LEGAL RULES (govern every stage, intake to outreach)

These were derived from analysis of federal Census law (13 U.S.C. §§ 8, 9),
copyright/contract law around data, and the outreach statutes. They are
governing constraints on the whole pipeline.

1. **Census data is counts-only and never enters a company record.** Census/BLS
   data is statistical (establishment counts by NAICS by geography), legally
   confidential at the respondent level. **DECISION 2026-06-13: Census is SET
   ASIDE. The shipper operation runs strictly on the EPA roster (public domain).
   Census is NOT used as a pipeline component for now.** Rationale: the § 9
   re-identification tripwire and the attribution condition are incurred ENTIRELY
   by using Census data; the EPA roster supplies the ore AND its own NAICS codes
   for targeting, so Census is not needed for the current goal (produce
   onboardable shippers). By not using Census, the § 9 exposure does not exist —
   there is no confidential data in the system to combine with names.
   **IF Census is ever reintroduced** (only as an isolated coverage-measurement
   instrument for scaling/spend decisions), it must be kept counts-only, in its
   own layer, NEVER joined to named records at the identity level, and the
   attribution string below reactivates. Until then, this rule is dormant.
2. **(DORMANT while Census is set aside) Attribution for Census data.** If Census
   data is reintroduced and reaches any customer-facing surface, it must display:
   "This product uses the Census Bureau Data API but is not endorsed or certified
   by the Census Bureau." Not applicable while EPA-only.
3. **Each source is used per its own terms; sanctioned access is preferred.**
   Prefer official downloads / APIs / licenses over scraping. Where scraping,
   only genuinely public pages with no accepted terms, taking facts only, never
   copying a whole curated database, never circumventing a login/paywall/CAPTCHA
   (that crosses into CFAA territory and is a hard no). The Assayer (below) is
   the organ that tracks per-source terms.
4. **The outreach layer remains governed by dialing-compliance architecture.**
   The exit end (calling/texting shippers and carriers) carries the real
   regulatory risk — TCPA, TSR, DNC, A2P/10DLC. This is governed by the existing
   compliance work, separate from intake-side data law.

**Hard nos, across the board:** breaching accepted ToS; circumventing technical
access controls (logins, paywalls, CAPTCHAs); copying an entire curated database
wholesale; contacting people in violation of TCPA/TSR/DNC. (Re-identifying
suppressed Census entities is moot while Census is set aside, but the prohibition
stands if Census is ever reintroduced.)

**Counsel triggers (route to a lawyer, like the Florida dialing questions):**
scraping a terms-bound source at scale; reselling data rather than using it
internally; uncertainty about whether a specific source's terms permit a use.

---

## THE SHIPPER-REGISTRY PIPELINE (four organs)

The shipper engine is a funnel of four parts. Each is simple, does one job, and
feeds the others. **Build order and current status noted per organ.**

### 1. PROSPECTOR — casts the net, tags the source
- **Job:** Produce a wide, unverified, source-tagged roster of candidate
  shippers in a territory. Breadth, not rigor. Noise acceptable.
- **Key output property:** every candidate is stamped with its SOURCE (which
  mine produced it). This provenance tag is what lets the Assayer grade mines.
- **Does NOT:** verify doors, judge legality, rank, or assess quality.
- **Status:** Skill exists at v0.1 (`skills/shipper-prospecting/`), validated by
  one hand-run on the Dallas–Midlothian–Irving cluster. Four discipline laws,
  in-universe plausibility screen, retired Layer 5. NEEDS: source-tagging made
  rigorous per above; future guidance from the Assayer's source map.

### 2. ASSAYER — grades the MINES (sources), agnostic reporter
- **Job:** Evaluate the SOURCES the Prospector drew from — not the companies.
  For each source/mine, report: (a) **legality** — observed terms, click-through,
  login walls, robots.txt, no-scraping clauses; (b) **richness** — yield, novelty,
  overlap; (c) **reusability** — should we dig here again, lean harder, or
  abandon. Builds a durable, growing SOURCE MAP.
- **Stance — AGNOSTIC REPORTER, NOT JUDGE.** The Assayer observes and reports
  facts about sources against our criteria, and FLAGS anything in "careful"
  territory for the operator's attention. It does NOT render legal verdicts or
  auto-clear/auto-block sources. It senses and flags; the human decides. Same
  discipline as the Prospector reporting honestly. Ambiguous/login-gated sources
  are flagged as possible disruptions, never silently cleared.
- **Why it exists / why here:** separates *evaluating the source* from
  *evaluating the find* — a job we were wrongly bundling into verification. Makes
  legality tractable: vet the handful of SOURCES once each, and that ruling
  covers every record from that mine, instead of vetting millions of records.
- **Feeds:** the Prospector (guides future hunts toward proven/clean mines, off
  worked-out/risky ones) and the Refiner (only passes ore from cleared mines).
- **The source map is itself a compounding asset** — the meta-knowledge of where
  the gold is and which claims are clean to work, valuable across every territory.
- **Status:** NOT YET BUILT. Newly architected. Next major build for the shipper
  engine. Needs its own contract/skill defining the three grading axes and the
  agnostic flag-don't-judge stance.

### 3. REFINER — deep research on cleared ore (the Investigator/analyst)
- **Job:** Take candidates from Assayer-cleared mines and do the deep per-company
  work: verify the carrier-accessible DOOR (the gate), and produce the actionable
  shipper profile. Turns raw ore into usable metal.
- **The door gate (verification standard, as a SCANNER not an analyst):** senses
  green-light triggers — (1) carrier-onboarding LANGUAGE on a page ("carrier
  onboarding/setup/become a carrier" — hard green light); (2) the shipper's OWN
  freight/brokerage operation (a captive logistics arm we can call for their
  freight — green; lean toward FINDING it, not warding against bad brokers —
  that discernment is later/analyst work); (3) a live carrier-SIGNUP portal.
  Any trigger fires → greenlit, trigger is the citation, and the firing trigger
  doubles as the friction byproduct (portal = lowest friction, language-door =
  next, captive-operation-you-call = a real door that takes a call). No trigger →
  UNCONFIRMED. Unconfirmed is an honest third outcome, NEVER upgraded by guessing.
- **Does NOT (these are deferred to later stages):** rank candidates; score
  freight quality as a sort order; judge brokerage character. Open/unconfirmed
  only; document and hand on.
- **Status:** NOT YET BUILT as a skill. Verification STANDARD is defined (above)
  from extended design. This is the 10-day keystone — see arc below.

### 4. MATCHMAKER — crosses refined gold against carriers
- **Job:** Match verified shipper profiles to the carrier book; suggest direct-
  shipper candidates to carriers (the moat: a carrier wired into direct doors
  near them doesn't leave). Acts only on Onboard-ability.
- **Status:** FUTURE (Phase 3). Schema being shaped now so this becomes a clean
  join later.

---

## STAGE ZERO — the data foundation (EPA-only as of 2026-06-13)

**DECISION 2026-06-13: The operation runs strictly on the EPA roster.** Census
is set aside (see legal rule 1). The substrate is now single-source and
legally unconditional.

- **THE ORE — EPA Facility Registry Service (the sole source).** Every
  environmentally-regulated facility, with name + address + NAICS, bulk CSV per
  state. **Assay: public domain, no accepted terms, no scraping restriction,
  facts-only, commercial use unrestricted — ZERO flags, the cleanest legal
  source in the pipeline.** Carries its own NAICS codes, so it supplies BOTH the
  raw candidate names AND the targeting signal (category mix + density readable
  directly from the file). Skews heavy/permitted; under-covers light/non-
  regulated categories — but those gaps fall mostly in non-flatbed industries we
  skip anyway, so for flatbed-relevant heavy industry the EPA roster is the
  effective base layer. **Texas pull complete: ~28,640 facilities.**

- **(DORMANT) Census landscape + coverage gauge.** Set aside. Was Layer 1
  (targeting) + the coverage denominator. Reclassified from "pipeline component"
  to "optional isolated measurement instrument" — pulled ONLY if a future
  scaling/spend decision needs to know roster completeness (e.g. "is it worth
  paying for MNI in this region"). If reintroduced: counts-only, isolated layer,
  never joined to names, attribution reactivates. **KNOWN TRADE: by going
  EPA-only we give up the coverage gauge — we work the ore without knowing what
  fraction of the universe it represents. Acceptable for producing first
  shippers; revisit at the scaling decision.**

- **Stage-zero scripts** (`stage_zero/`) still exist and ran successfully
  (proved the architecture, produced the Texas EPA roster + the now-set-aside
  Census landscape + a 76.6% coverage reading). Going forward, only the EPA
  roster feeds the pipeline. The Census/coverage scripts are retained but dormant.

---

## THE TRUCKING-LEADS PIPELINE (the other workflow)

Separate, mature, near-ready. FMCSA carrier-census leads → grade via the
`fmcsa-lead-grading` skill (9 hard gates + weighted rubric, precision-over-recall,
already scar-tissued) → stage HubSpot-import-ready output → log. Propose-only
(no autonomous CRM writes). This workflow is the CLOSEST to automated; its risk
is low. Future enhancement: FMCSA API for continuous fresh leads (Phase 2).

---

## WEB PRESENCE & A2P COMPLIANCE (added 2026-06-21)

The public site **acedispatch.us** and the SMS-outreach compliance layer now live
inside ace-os.

- **Website — self-hosted, off Horizons.** The site was an AI-built Hostinger
  Horizons app (React + Vite + Tailwind). It was exported, rebuilt for compliance,
  and is now self-hosted on Hostinger Business (Custom PHP/HTML, `public_html`).
  Canonical source: `web/acedispatch-site/`. Build with `npx vite build` (NOT
  `npm run build` — the Horizons export's build script breaks on Windows cmd), zip
  `dist/` with forward-slash paths, upload to `public_html`. Horizons AI editing is
  abandoned (one-way export); edits are now code edits in this folder.
- **What changed on the site:** added `/privacy` and `/terms` React pages (off the
  old Termify-hosted policy), an OPTIONAL SMS-consent checkbox on the contact form,
  and wired the form to post into HubSpot (it was a dead localStorage stub before —
  sent nothing).
- **A2P / SMS compliance** lives in `compliance/a2p/` (registration sheet, Terms,
  Privacy, worksheet, README). Governing model: **cold = call, warm = text after
  opt-in.** Registered as Low Volume Mixed; entity A&C Consulting Group LLC; Aircall
  Sales + Main lines on the campaign. This realizes Standing Legal Rule #4 (the
  outreach / A2P-10DLC layer).
- **Consent capture in HubSpot:** new contact properties `sms_consent`,
  `sms_consent_method`, `sms_consent_date`; website opt-ins self-tag as Website
  Form, reps log Verbal/Inbound. All other CRM writes remain PROPOSE-ONLY per the
  constitution.

## VOICE CALLER-ID REPUTATION (added 2026-06-22)

The **voice twin** of the A2P/SMS layer, in `compliance/voice-reputation/`. A2P
10DLC governs whether texts deliver; this governs whether **calls** ring through
clean vs. show "Spam Likely" / get blocked. They are separate systems — the 10DLC
registration did nothing for voice, which is why the Sales line got flagged.

- **Diagnosis:** voice spam labeling was never set up, AND all cold volume (200–300
  dials/day) ran through ONE un-registered line with no rotation and a stretch of
  low-answer junk leads — the spammer signature to carrier analytics engines
  (Hiya/AT&T, TNS/Verizon, First Orion/T-Mobile, which score independently).
- **The two lines:** **+1 561-231-2023** (Main/dispatch, "the 2023 number") is CLEAN
  — every call answered, real conversations — and is the proof that clean behavior
  keeps a line clean. **+1 561-291-8209** (Sales) is FLAGGED. Standing rule: the 2023
  line NEVER makes cold dials; it's the protected clean asset.
- **Governing model (leverage order):** behavior > Free Caller Registry registration
  > A-level STIR/SHAKEN attestation > CNAM/Branded Caller ID. No registration
  survives bad behavior — the structural fix is a warmed, registered **number pool**
  (~4–6 lines at current volume) under a per-line daily ceiling, so no line can be
  overloaded again. Dial lists draw from `fmcsa-lead-grading` output only.
- **Status:** layer designed/legislated; **NOT yet executed** — all steps are
  operator-only (Aircall settings, buying lines, FCR submission, attestation). Agents
  stay read-only on Aircall. Blocking input to size the pool: rep count + dials/rep/day.

## CAPABILITIES & PLUMBING

- **HubSpot MCP** — connected in both Desktop and Code (account-level). READ-only
  use per constitution (propose-only for all CRM writes).
- **Aircall** — API key in `.env`; `scripts/aircall_pull.py` (read-only) feeds
  the sales agents.
- **Census API** — free key in `.env` (`CENSUS_API_KEY`); used under its ToS
  (counts-only, attribution on customer-facing use). Stage-zero Layer 1.
- **EPA FRS/TRI** — public bulk downloads, no key. Stage-zero Layer 2 free floor.
- **Claude in Chrome** — NOT YET ADOPTED. Highest-trust capability (drives your
  logged-in browser; prompt-injection risk). Specific intended job: render
  public-but-bot-walled directories (AISC live cert search) and harvest browser-
  only sources (ThomasNet — but ThomasNet is terms-bound, Assayer-flag first).
  Pauses at logins/CAPTCHAs by design. Treat as supervised, narrow-scope,
  Phase-2. Decision to enable is a real trust call — operator's.
- **FMCSA API (QCMobile)** — NOT YET WIRED. Phase-2 plumbing serving BOTH the
  trucking Lead Pipe (continuous fresh leads) and the shipper Refiner (verify
  captive brokerages). Free WebKey registration.
- **VS Code** — near-term mastery goal, not this weekend. The unified cockpit
  for ace-os. David already uses it (shared workbench for engineering handoffs).
  Adopt after the agent loop is proven; everything built is already VS-Code-shaped
  (plain files in a folder).

---

## THE 10-DAY EXECUTION ARC (committed)

**Definition of "done" (agreed):** both workflows run headless on a schedule, end
to end, landing ratify-ready output in the outbox without the operator at the
keyboard — and the operator still ratifies all CRM/dial-list writes. NOT
autonomous writes (that earns in later, per Earned Authority).

- **Days 1–3 — Build & iterate the parts by hand (right brain).** Keystone:
  build the Refiner (Investigator) to v0.1 and run the Prospector→Refiner funnel
  by hand on Dallas (the mandatory iteration pass). Architect the Assayer. Lock
  the trucking-leads agent contract (nearly ready). Highest-risk phase, so it's
  first. **Refiner is the keystone and the least-built piece — the schedule's
  main risk; front-load it.**
- **Days 4–7 — Wrap validated parts into running agents (left brain, Code tab —
  the cockpit already known, so bugs are unambiguously agent bugs).** Trucking
  agent first (closest). Then shipper agents (Prospector + Assayer + Refiner as
  the funnel). Both workflows scheduled, landing ratify-ready output. FMCSA-API
  and Chrome-for-AISC slot in here IF room; they don't block "automated."
- **Days 8–10 — Unify & move into VS Code (cockpit upgrade).** Both workflows
  proven first; THEN take the focused VS Code session, open the unified ace-os
  structure, learn to operate from one cockpit. David = live reference. Buffer
  lives here (VS Code mastery can extend past day 10 without the WORKFLOWS being
  late).

---

## OPEN ITEMS / DECISION LOG

- **2026-06-25** — **ace-os pushed to a PRIVATE GitHub remote** (`github.com/AceDispatch/ace-os`)
  — first off-machine backup + the David-collaboration path; operating from VS Code as the cockpit (§15).
  *Amends the 2026-06-21 git stance:* `.gitignore` now EXCLUDES the data layers (`inbox/`, `data/`,
  `stage_zero/output/`, `outbox/**/*.{csv,json}`). Carrier/shipper PII is no longer git-tracked — it lives
  on local disk and is migrating into **Supabase as the source of truth**. Git history was rebuilt to a
  clean single-commit baseline so no PII ever reached the remote (217 files, code+docs only — verified).
- **2026-06-25** — **Architecture firm-up IN PROGRESS** (ratification pending): unified multi-vertical
  shipper DB to replace the flatbed-only registries (`outbox/shipper_db/ARCHITECTURE.md` + migrated
  16k-row master); Supabase backend (`db/schema.sql` ready for operator to provision); grader to be
  rebuilt as a multi-vertical classifier; a standardized `run_metro.py` routine to run the SE campaign
  metro-by-metro. Doctrine: sort-don't-discard (everything binned by equipment), quality over token-
  frugality, target = FTL-confirmed + onboardable.
- **2026-06-22** — **Voice caller-ID reputation layer created** (`compliance/voice-reputation/`),
  the voice twin of the A2P/SMS layer. *Why:* a majority of outbound Aircall calls
  show as spam and some don't connect; root cause is that voice spam labeling is a
  SEPARATE system from A2P 10DLC (texting-only) and was never set up — compounded by
  overloading all cold volume (200–300/day) on one un-registered line with no rotation
  and low answer rates. Fix = behavior first (graded leads only, scrub dead numbers,
  cap velocity), then Free Caller Registry + A-attestation, then a warmed number pool
  (~4–6 lines) so no line is overloaded again. The clean 2023 dispatch line is walled
  off from cold dialing. Execution is operator-only; pool sizing blocked on rep/dial
  counts. Detail + SOP in `compliance/voice-reputation/`.
- **2026-06-21** — **ace-os put under git** (operator decision). `git init` with a
  `.gitignore` that excludes secrets (`.env*`) and build/deps (`node_modules`,
  `dist`); lead data (inbox/outbox) IS tracked by operator choice. If a hosted
  remote is ever added, carrier PII must be reviewed before pushing.
- **2026-06-21** — **Website self-hosted off Horizons + made A2P-compliant.**
  acedispatch.us moved from the Hostinger Horizons AI builder to self-hosted Custom
  PHP/HTML (Business plan). Added /privacy + /terms pages, an SMS-consent checkbox,
  and HubSpot form wiring. Source now in `web/acedispatch-site/`; compliance docs in
  `compliance/a2p/`. *Why:* the generated privacy policy was over-broad (shared data
  with "marketing partners" — the #1 A2P rejection cause) and the contact form sent
  nothing; both blocked compliant SMS. Horizons AI editing abandoned (one-way
  export); future edits are code edits.
- **2026-06-21** — **A2P/SMS model ratified: cold = call, warm = text after opt-in.**
  No cold SMS to FMCSA lists (TCPA + carrier-block risk). Registered Low Volume
  Mixed. Realizes Standing Legal Rule #4. Detail in `compliance/a2p/README.md`.

- **2026-06-13** — **EPA-ONLY decision.** Shipper operation runs strictly on the
  EPA roster (public domain, zero legal conditions). Census set aside — not
  needed for ore (EPA supplies names) or targeting (EPA carries NAICS). *Why:*
  the § 9 re-identification exposure and attribution condition are incurred
  entirely by the Census layer; removing it makes the intake path legally
  unconditional. Known trade: lose the coverage gauge (a scaling-decision tool,
  not an ore source) — revisit if/when a spend decision needs it. Stage-zero run
  succeeded first (proved architecture, 76.6% coverage, ~28,640 TX facilities)
  before the decision to proceed EPA-only.
- **2026-06-13** — Assay recorded: EPA FRS = clean, rich (saturates flatbed-
  relevant heavy industry), reusable base ore mine, no flags. Census = clean-but-
  conditional measurement instrument with two tripwires (now dormant while set
  aside). Read at the right altitude: the landscape's job was to size/measure the
  ore pile, NOT to conclude regional strategy. Establishment counts are pile
  sizes, not target rankings; low-count categories are not bad targets. Success
  is measured at the NARROW end — onboardable shippers — where a search yielding
  100 candidates that the Refiner grinds to 2 easy-onboard shippers is a WIN.

- **2026-06-13** — Architected the four-organ shipper pipeline (Prospector →
  Assayer → Refiner → Matchmaker), splitting source-evaluation (Assayer) from
  find-evaluation (Refiner). *Why:* legality + source-quality are properties of
  SOURCES, gradable once per mine, not per record; bundling them into
  verification was a category error. Assayer is an AGNOSTIC REPORTER (flags,
  doesn't judge). *Reasoning lives in the 2026-06-13 Desktop conversation.*
- **2026-06-13** — Established standing legal rules from Census/contract/copyright
  analysis. Census = counts-only, never in a company record; sanctioned access
  preferred; per-source terms honored; outreach governed separately. Counsel
  triggers: scrape-at-scale, resale, source-term uncertainty.
- **2026-06-13** — Stage-zero prototype built (Texas). Pending: operator runs it
  in Code, brings landscape summary + coverage report back to Desktop for joint
  analysis → that analysis sets the next hunt stage and informs which sources the
  Assayer will need to grade.
- **PENDING DECISION** — Assayer legality grading: confirmed as agnostic
  report-and-flag (not bucketed verdicts). Build its contract next.
- **PENDING** — Refiner (Investigator) skill build — the 10-day keystone.
- **PENDING** — Whether to enable Claude in Chrome (trust decision, operator).
- **FUTURE COUNSEL** — data resale question, if model ever shifts to selling data.
