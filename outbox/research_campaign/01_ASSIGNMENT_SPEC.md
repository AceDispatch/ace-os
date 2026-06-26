# Researcher Assignment Spec — one deep-research unit (per company)

Derived verbatim from `skills/shipper-researching/SKILL.md` + `references/DOOR_TRIGGERS.md`.
This is the FIXED procedure every research agent runs on every company so that 5,735
companies get the SAME treatment regardless of which wave or agent handles them.
**Read the skill; do not improvise criteria** (Constitution: methodology rule).

## Inputs (one row from the queue)
`company, naics, product_family, city, state, address, zip`

## The procedure (run in order; stop early only on EXCLUDE)

**Step 0 — Resolve the entity (do this FIRST; name collision is rampant).**
- Find the company's real web presence. Confirm it matches the queue row by **city/state/address**,
  not just the name. If the obvious hit is a different company in a different place, keep digging
  or record `entity_resolved=no` and stop at Tier 4. (Trinity Forge ≠ Trinity Industries ≠
  Trinity Logistics; Tejas / Atlas Pallet / Amega / "Texas Metal Fabricating" all have namesakes.)

**Step 1 — EXCLUDE / FLAG gates (any hit → record reason, route, stop):**
- **Defunct/closed** → `flag=defunct`, exclude.
- **NAICS mismatch** — verify what they ACTUALLY make. (Intrapack = enclosures not rebar;
  Bonanza = cultured marble not cut stone.) If they don't ship open-deck product → flag.
- **Wrong trailer** — if they're really dump/van/heavy-haul/tanker → `vertical=<type>`, route to
  the OTHER-vertical bin (filed, NOT discarded).
- **Captive-fleet-only** — a tiny 1–2 truck intrastate DOT authority is a captive signal, a
  contact-lead, NOT an open door.

**Step 2 — Door scan (3 green-light triggers; ANY fires → GREEN, the trigger is the citation):**
1. **Onboarding LANGUAGE** — "carrier onboarding/setup," "become a carrier," "haul for us,"
   "carrier requirements," a transportation/carrier page inviting carriers.
2. **OWN freight operation** — captive logistics arm, in-house transport dept, named logistics
   subsidiary, OR captive FMCSA carrier/broker authority (check SAFER/DOT#).
3. **Live carrier-SIGNUP portal** — proprietary, or named platform (RMIS, MyCarrierPackets,
   Highway, TRUX, KBX).

**Step 3 — CHECK THE PARENT (the biggest yield lesson — most doors hide here).**
- Identify the parent/holding company. Check the PARENT's carrier program, not just the local
  plant. One parent door can cover many sites. Consult `LESSONS_LEDGER.md` known-parents list FIRST.
- Record `parent_company` and whether the door is inherited from the parent.

**Step 4 — Capture the CONTACT + assign the effort tier (every confirmed shipper gets a contact):**
- **Tier 1 — self-onboard:** verified door (portal / carrier page / captive authority). Cheapest.
- **Tier 2 — reachable, low:** clear direct traffic/logistics desk or clean named contact. One call.
- **Tier 3 — reachable, high:** general switchboard/info only; navigate in.
- **Tier 4 — confirmed shipper, no contact found:** real, needs more digging.

**Step 5 — Confidence gradient within GREEN (record WHICH, so the operator knows the friction):**
- **Strongest** — live carrier-facing artifact actionable today (portal / carrier page).
- **Middle** — captive freight authority confirmed in records (FMCSA authority).
- **Softest** — "parent runs logistics, phone the desk" (real op, human door).

## Hard discipline
- **Precision over recall.** "Not found" is an HONEST outcome, NEVER upgraded by guessing.
  A wrongly-confirmed door costs credibility on the call; an unconfirmed shipper just waits.
- Honest blanks where nothing was found. Cite the trigger/page for every GREEN.

## Output (one CRM-stable row, the 17-column registry schema)
`company_name, effort_tier, door_type, flatbed_fit, ships, city, state, phone, email,
website, onboarding_url, contact_grade, parent_company, naics, source, vertical, notes`
- `notes` carries: entity-resolution evidence (the address/DOT match), the door citation,
  the confidence gradient, and any EXCLUDE/FLAG reason.
- Wrong-trailer catches go out with `vertical` set, not dropped.

## Verify pass (adversarial, before a row is trusted as GREEN/Tier-1)
A second agent re-checks every GREEN/Tier-1 row: is the entity really this company (address/DOT),
and does the cited door actually invite OUTSIDE carriers (not a customer portal, not captive-only)?
Default to DOWNGRADE if the citation doesn't hold. This is the name-collision / false-door guard.
