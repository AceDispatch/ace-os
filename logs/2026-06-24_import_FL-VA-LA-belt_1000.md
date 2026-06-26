# Run Log — HubSpot Import of the 1,000 FL/VA/LA-belt leads to Anthony Smart

- **Date/time:** 2026-06-24 → 2026-06-25 (UTC create timestamps 06-25 ~01:45–02:07)
- **Contract:** trucking-leads pipeline; operator-directed bulk import
- **Operator-initiated or scheduled:** Operator-initiated (Anthony) — "Import the full 1000" → "I push via API to Anthony Smart" → "Keep grinding via API".
- **Write warrant:** One-time operator-granted CRM write warrant for this specific 1,000-lead import. HubSpot is otherwise PROPOSE-ONLY. No other CRM writes performed; Aircall untouched (read-only); skills/ untouched.

## What was imported
- **Source of truth:** `outbox/2026-06-24_pull_FL-VA-LA-belt_1000.csv` (1,000 ranked, tiered, tractor-verified, net-new leads).
- **Owner:** Anthony Smart (`hubspot_owner_id = 164918656`).
- **Tag:** `lead_source_detail = "FMCSA FL/VA/LA-belt 0624"`.
- **Method:** HubSpot MCP `manage_crm_objects` createRequest, `confirmationStatus: CONFIRMED`, **10 objects/call**, 100 calls total.
- **Fields mapped (per company):** name←Legal Name, phone, address←Street, city, state, zip, dot_number, ace_lead_score, priority_tier, equipment_types, power_units, company_officer←Officer, carrier_classification←Classification, fmcsa_add_date (YYYY-MM-DD). Empty values omitted.

## Result
- **1,000 / 1,000 created. 0 failures across all 100 batches.**
- **Reconciliation:** `search_crm_objects` on the tag returns `total: 1000` — exact match to the 1,000-row source. No spurious/duplicate records. (The earlier mid-run "370 created + 631 remaining = 1001" arithmetic resolved cleanly; the dedup-safe rebuild prevented any double-create.)
- **By state:** FL 571 · GA 158 · VA 127 · LA 45 · NC 43 · AL 31 · SC 25.
- **By tier:** P1 29 · P2 204 · P3 326 · P4 441.

## Method notes / resilience
- Grind ran in waves of 5 batches (50 records) with a within-session checkpoint in `data/import_payloads/_RESUME.md` and a self-healing reconciliation path (`scripts/_rebuild.py`): re-query the tag for created DOTs, regenerate `data/import_payloads/all.jsonl` to uncreated-only, resume from line 1. Used once after a transcription-drift scare; held 0-dup.
- Payloads were pre-built deterministically from the CSV (`scripts/_make_payloads.py` / `_rebuild.py`), not hand-typed, so field mapping was identical across all 1,000.

## Anomalies / data-quality notes (name-filter gap — for grader follow-up)
- ~25 P3/P4 **tail** leads passed the v4 **tractor gate** (verified tractor-trailers per the live vehicle-count gate) but carry **non-dispatch-sounding names** the name filter didn't flag. They are equipment-legitimate but worth an eyeball before dialing, and are the basis for a SOFT_NEGATIVE / name-filter expansion on the next pull. Notable examples (DOT):
  - DE ARMAS APPLIANCE DELIVERY AND INSTALLATION (4226031), LEBLANC'S FAB AND EQUIPMENT (4553050), M&M FLORIDA TILE (4525063), GT HEAVY EQUIPMENT SERVICES (4388605), LUMAI TECH (4468643), UPSTREAM PETROLEUM (4414263), BLACKWATER ENVIRONMENTAL SERVICES (4523983), PRAGMATIC CONSULTATION (4251087), M&Y FAST CHARGING (4567453), RESET CONTAINER SERVICE (4502723), STACEYS PRODUCTS (4548316), BELFLEUR EQUIPS (4507529), ACQUIRING BETTER THINGS (4419573), MORE THAN WORKS (4513946), VSPROBUY (4515572), SHIPPER DIRECT (4407869), JOEOFALLTRADES (4513122), ETHIOUS IMPORT EXPORT (4507446), ECARSTOGO COM TECHNOLOGIES (4041291), ALLS SHOPPING SOLUTION (4475230), CARBON BALANCE (4468324), WESBAY TRADING (3825094), MDR QUALITY (4252050).
  - These tokens (appliance, tile, equipment, tech, petroleum, environmental, consultation, charging, container, products, equips, trading, shopping, import/export) are candidate additions to the grader's SOFT_NEGATIVE list so future pulls down-rank or drop them. NOTE: do not hard-reject blindly — several (petroleum hauler, container/drayage, heavy-equipment hauler) can be legitimate dispatchable freight; treat as soft down-rank, not a kill.

## Grader patch applied (2026-06-24, operator-directed, post-import)
`skills/fmcsa-lead-grading/scripts/grade_leads.py` — name filter reworked now that the tractor gate handles equipment:
- **HARD_NEGATIVE = different-industry business that happens to own a tractor only** (will never buy dispatch). Added `appliance`, `tile`. Kept all trades (roof/coating, construction, automotive/dealership, salon, realty, pest control, etc.).
- **Moved car-hauling/auto-transport + `energy services` from HARD → SOFT** — those are real (or off-profile) freight, not another industry; per operator they should down-rank, not be killed. (Also consistent with the note-protected SON TRUCK AUTO TRANSPORT keep, which is no longer auto-dropped.)
- **SOFT_NEGATIVE is now a DOWN-RANK penalty (`SOFT_PENALTY = -15`), not a `-1000` discard.** Added off-profile/ambiguous tokens: petroleum, container, environmental, consultation/consulting, trading, products, shopping, technologies, tech, charging, import export, heavy equipment, equips, energy.
- **Fixed ordering bug:** trucking signal is computed first, then the soft penalty stacks on top — so a name with both a trucking word and a soft token (e.g. "…TRUCK… REPAIR") is down-ranked instead of scoring full Strong.
- Verified with a smoke test (tile/appliance/roof/automotive → discard; petroleum/container/trading/products → −15; clean trucking names → +15; SON TRUCK AUTO TRANSPORT → neutral, kept).

## Outreach guardrails (carried from the pull)
- Dial via the **warmed number pool**, dead numbers scrubbed first — NOT the flagged 561-291-8209 Sales line. Florida (571) is the anchor; lean new dialing there.
- CELL_PHONE column must NOT feed an autodialer/bulk-text without TCPA guardrails (cold = call; warm = text only after opt-in). Never imply FMCSA/USDOT affiliation in outreach.
