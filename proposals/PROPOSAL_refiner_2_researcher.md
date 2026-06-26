# SKILL PROPOSAL — Refiner Job 2: The RESEARCHER (graded ore → verified shippers)

**Status:** RATIFIED 2026-06-13. Official SECOND refiner pass. Runs in CHUNKS OF 50, marching through the graded ranks.
**Operator direction (2026-06-13):** Job 2 of the split Refiner — the official
SECOND refining pass. Processes the graded list in CHUNKS OF 50, working through
the ranks. SLOW, EXPENSIVE, web-research-heavy, batch by batch. This is literally
what the two deep-research passes were (~50 companies each).

## What this hat is

The Researcher takes a CHUNK of the Grader's ranked ore (a slice the operator
points it at) and does deep per-company research into actual CRM records. It is a
SCANNER for doors + a CAPTURER of contacts. It runs batch by batch under operator
direction — the operator says "research ranks 100-150," it churns that ~50, the
operator reviews, then directs the next slice.

### Proposed doctrine (validated on 102 real companies across two passes)

**1. The door scan — three green-light triggers:**
- **Onboarding LANGUAGE** ("carrier onboarding/setup," "become a carrier," "haul for us")
- **The shipper's OWN freight operation** (captive logistics arm, in-house transport, named subsidiary, OR captive FMCSA carrier/broker authority) — identify it, don't judge broker character
- **Live carrier-SIGNUP portal** (proprietary, or RMIS/MyCarrierPackets/Highway/TRUX/KBX)
Any trigger fires → GREEN, trigger is the citation.

**2. CHECK THE PARENT COMPANY — the biggest yield lesson.**
Most verified doors hid in PARENT programs (Nucor, Gerdau, Georgia-Pacific/KBX,
Forterra, Cornerstone, Tenaris, Mohawk). A division inherits the parent's carrier
program. ALWAYS check the parent, not just the local plant. One parent door can
cover many sites (Forterra = 7 TX sites, one door).
*(This is the most expensive research step but found the most doors — operator
to confirm it's worth the cost.)*

**3. Capture the CONTACT regardless of door — the effort ladder:**
- **Tier 1 — self-onboard:** verified door (portal/carrier page/captive authority). Cheapest.
- **Tier 2 — reachable, low contact:** clear direct desk or clean named contact. One call.
- **Tier 3 — reachable, high contact:** general line only; navigate in.
- **Tier 4 — shipper confirmed, no contact found:** needs more digging.
Most real shippers have NO portal but ARE reachable — the passes proved live
portals are RARE (~1 clean-fit portal in 14 doors). Reachable-human is the main path.

**4. UNCONFIRMED / no-contact is honest, NEVER upgraded by guessing.**

**5. EXCLUDE/FLAG conditions (the Researcher must catch these — passes proved all):**
- **Wrong trailer slips through:** if the Grader mis-sorted a dump/van/heavy-haul
  shipper into the flatbed pile, the Researcher catches it and routes it to the
  OTHER-vertical bin (not discarded — filed for the relevant future vertical).
  (Most equipment-type sorting already happened at the Grader.)
- **Defunct/closed:** verify the company still exists (Aradyne, Blackhawk closed).
- **Misidentified NAICS:** name/NAICS mismatch (Intrapack = enclosures not rebar).
- **NAME COLLISION — verify entity (DOT#/address) before trusting the record:**
  rampant (Trinity Forge ≠ Trinity Industries ≠ Trinity Logistics; Tejas, Atlas
  Pallet, Amega, "Texas Metal Fabricating" all have unrelated namesakes).
- **Captive-fleet-only ≠ open door:** tiny 1-2 truck intrastate DOT authority is
  a captive signal, not an outside-carrier invitation. Tag as contact-lead.

**6. Confidence gradient within GREEN (verified ≠ uniform):**
- Strongest: live carrier-facing artifact actionable today (portal/carrier page).
- Middle: captive freight authority in records (FMCSA authority).
- Softest: "parent runs logistics, phone the desk" (real op, human door).
Record WHICH so the operator knows the friction.

### Output
CRM-stable shipper records, tier-sorted, for the chunk researched:
`company_name, effort_tier, door_type, flatbed_fit, ships, city, state, phone,
email, website, onboarding_url, contact_grade, parent_company, naics, source,
vertical, notes`. Honest blanks. Dump tagged not dropped. APPENDS to the running
CRM registry, deduping parent-covered sites into one relationship.

### Evidence base (what the two passes proved)
- 200-250: ~38 distinct → ~15 workable (~40%), ~5-7 verified doors.
- 100-150: 51 → ~43 workable (~84%), more doors, parent-clustered.
- Grade is PREDICTIVE (higher slice ~2x richer) → operator-directed slice choice works.
- 14 verified doors total (12 flatbed + 2 dump). Live portals rare; relationship model validated.

### Open question for operator
- Parent-company check (step 2): RATIFIED, stays in (found most doors).
- Batch size: 50 per run, marching through the ranks. RATIFIED.
