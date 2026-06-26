# Ace Shipper Database — Architecture & Methodology

**Established:** 2026-06-25. This supersedes the flatbed-only registry approach. All future prospecting/grading/research follows this model so the methodology stays consistent as we scale across verticals and regions.

## North Star
Build ONE master database of **FTL-confirmed, onboardable shippers** serving **every Ace carrier type** — van, reefer, flatbed, dump, tanker, heavy-haul, hopper. Not a flatbed silo. Every shipper we ever touch lands in this DB, sorted to the correct equipment bin, at the correct research stage.

## Operating principles
1. **Sort, don't discard.** A company that isn't the current target vertical is **binned by equipment for later research**, never thrown away. Only true non-shippers go to the audit/discard log (still recoverable).
2. **Quality over token-frugality.** Within the vertical we're researching, be **comprehensive** — research the whole target slice (YES + UNSURE), don't pre-prune to save tokens. We are NOT optimizing for cheap tokens; we're optimizing for coverage and correctness.
3. **Defer across verticals, not within.** The only research we postpone is *other* equipment classes — they wait in the DB at stage=GRADED until their campaign. Touch as many bases as possible; just don't research a van lead during a flatbed run.
4. **The qualifier = FTL-confirmed + onboardable.** Target a shipper IF we can (a) confirm it moves **full-truckload** freight (not LTL/parcel/local-only) AND (b) reach an **onboarding/contact path**. Rank by onboarding ease: self-serve portal > direct desk/contact > navigate-in > captive-only. Easy onboarding is preferred, not required.

## The master record (schema) — `shippers_master.csv`
Identity: `shipper_id, company_name, dba, parent_company, address, city, county, state, zip, naics, source`
Equipment: `equipment_class` (flatbed|van|reefer|dump|tanker|heavy-haul|hopper|mixed|unknown) · `equipment_confidence` (high|med|low)
**FTL qualifier:** `ftl_status` (CONFIRMED|LIKELY|UNCONFIRMED|LTL-ONLY|NO) · `ftl_evidence`
Freight: `ships, outbound_lanes, volume_signal`
Onboarding: `door_status` (GREEN|UNCONFIRMED) · `door_type` · `onboarding_ease` (self-serve-portal|direct-contact|navigate-in|captive-only|none|unknown) · `onboarding_url` · `effort_tier` (1-4)
Contact: `phone, email, website, contact_grade`
Workflow: `research_stage` (PROSPECTED|GRADED|RESEARCHED) · `flags` (DEFUNCT|NAME_COLLISION|CAPTIVE_ONLY|...) · `region, researched_date, notes`

Master CSV is the single source of truth. Per-vertical and per-region dial sheets are **views** generated from it (filter equipment_class + ftl_status + onboarding_ease). Scale-up path: move to SQLite when the master exceeds comfortable CSV size.

## The pipeline (roles)
1. **Prospect** — slice EPA roster (or other source) by region. → stage PROSPECTED.
2. **Classify & Sort (the Grader, rebuilt as a MULTI-VERTICAL CLASSIFIER):** assign every company an `equipment_class` + FTL pre-signal and route ALL of them into the master DB at stage GRADED. No longer a flatbed yes/no filter — it's an equipment router. Non-shippers → audit log (recoverable).
3. **Research (per-vertical campaign, comprehensive):** run the Researcher on one equipment_class slice at a time. Its job: **CONFIRM FTL movement**, find the **onboarding door / direct contact**, capture **outbound lanes** + volume. Research the *entire* target slice (quality-first). Updates records to stage RESEARCHED with ftl_status + door + onboarding_ease. Wrong-equipment catches are **re-binned** (equipment_class corrected, left at stage GRADED), not deleted.
4. **Dial sheets (views):** generate call-ready lists filtered by vertical, region, FTL-confirmed, and onboarding ease.

## Research-stage discipline
- PROSPECTED → raw roster row.
- GRADED → equipment-classified, in a bin, awaiting its vertical's research turn (the "seed bank").
- RESEARCHED → FTL + door + contact verified.
Nothing is ever deleted; it just moves stages or bins.

## Status
- 2026-06-25: Architecture established. Master DB instantiated by migrating all prior researched registries + grader other-vertical seed bank. Grader rebuild (→ multi-vertical classifier) and resumed campaign run under this model are the next builds.
