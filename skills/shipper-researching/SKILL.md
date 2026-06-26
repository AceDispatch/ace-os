---
name: shipper-researching
description: Deep-research a CHUNK of graded flatbed shipper candidates for Ace Dispatch into verified, CRM-ready shipper records. This is Refiner Job 2 (the RESEARCHER) — the SECOND refining pass. Use after the Grader has produced a ranked flatbed roster; the operator points this skill at a slice (e.g. "research ranks 100-150"). It runs in CHUNKS OF 50, marching through the ranks. It is SLOW, web-research-heavy, and operator-directed. For each company it scans for a carrier onboarding DOOR (onboarding language / the shipper's own freight operation / a live signup portal), CHECKS THE PARENT COMPANY (where most doors hide), captures the reachable CONTACT, bins by EFFORT TIER (1 self-onboard / 2 reachable-low / 3 reachable-high / 4 no-contact), and catches EXCLUDE/FLAG conditions (wrong-trailer, defunct, misidentified NAICS, name-collision, captive-fleet-only). Trigger on "research shippers", "research ranks N-M", "second refining pass", "verify doors", "deep refine".
---

# Shipper Researching — Ace Dispatch (Refiner Job 2, the Researcher)

This skill runs the **Researcher**: the second and final refining pass. It takes a CHUNK
of the Grader's ranked flatbed roster — a slice the operator points it at — and does deep
per-company web research to produce **verified, CRM-stable shipper records**. It runs in
**chunks of 50**, marching through the ranks under operator direction. This is literally
what the two validated deep-research passes were.

## Governing philosophy — slow, batched, operator-directed; honest blanks

The Researcher's economics are the opposite of the Grader's: it is expensive and runs on
small chunks deliberately. The operator says "research ranks 100-150," it churns that ~50,
the operator reviews, then directs the next slice. It never manufactures certainty: a door
or contact that can't be found is recorded as not-found, never guessed.

## The door scan — three green-light triggers

For each company, scan its web presence (site, careers/logistics/transportation/carrier/
contact pages) for:
1. **Onboarding LANGUAGE** — "carrier onboarding/setup," "become a carrier," "haul for us,"
   "carrier requirements," a carrier/transportation page inviting carriers.
2. **The shipper's OWN freight operation** — captive logistics arm, in-house transport dept,
   named logistics subsidiary, OR captive FMCSA carrier/broker authority. Identify it; do
   NOT judge broker character.
3. **A live carrier-SIGNUP portal** — proprietary, or a named platform (RMIS,
   MyCarrierPackets, Highway, TRUX, KBX).

Any trigger fires → **GREEN** (verified door); the trigger is the citation.

## CHECK THE PARENT COMPANY — the biggest yield lesson

Most verified doors hid in **parent programs** (Nucor, Gerdau, Georgia-Pacific/KBX,
Forterra, Cornerstone, Tenaris, Mohawk). A division inherits the parent's carrier program.
**ALWAYS check the parent, not just the local plant.** One parent door can cover many sites
(Forterra = 7 TX sites under one door). This is the most expensive research step but it
found the most doors — it stays in.

## Capture the CONTACT regardless of door — the effort ladder

Most real shippers have NO portal but ARE reachable (the passes proved live portals are
RARE — ~1 clean-fit portal in 14 doors). So every confirmed flatbed shipper gets a contact
record, binned by effort-to-convert:
- **Tier 1 — self-onboard:** verified door (portal / carrier page / captive authority). Cheapest.
- **Tier 2 — reachable, low contact:** clear direct traffic/logistics desk or clean named contact. One call.
- **Tier 3 — reachable, high contact:** general switchboard/info only; navigate in.
- **Tier 4 — shipper confirmed, no contact found:** real shipper, needs more digging.

The effort tier is the dial-list sort order and the friction byproduct of the same scan.

## EXCLUDE / FLAG conditions (the Researcher must catch all of these)

- **Wrong trailer slipped through:** if the Grader mis-sorted a dump/van/heavy-haul shipper
  into the flatbed pile, route it to the OTHER-vertical bin (filed for the relevant future
  vertical, not discarded).
- **Defunct/closed:** verify the company still exists (passes found Aradyne, Blackhawk closed).
- **Misidentified NAICS:** name/NAICS mismatch (Intrapack = data-center enclosures not rebar;
  Bonanza = cultured marble not cut stone). Verify what they actually make.
- **NAME COLLISION — verify entity (DOT#/address) before trusting the record:** rampant
  (Trinity Forge != Trinity Industries != Trinity Logistics broker; Tejas, Atlas Pallet,
  Amega, "Texas Metal Fabricating" all have unrelated namesakes).
- **Captive-fleet-only != open door:** a tiny 1-2 truck intrastate DOT authority is a
  captive signal, not an outside-carrier invitation. Tag as contact-lead, not verified door.

## Confidence gradient within GREEN (verified is not uniform)

Record WHICH so the operator knows the friction:
- **Strongest** — live carrier-facing artifact actionable today (portal / carrier page).
- **Middle** — captive freight authority confirmed in records (FMCSA authority).
- **Softest** — "parent runs logistics, phone the desk" (real op, but a human door).

## UNCONFIRMED is honest

"Not found" is a real outcome, never upgraded by guessing. Precision over recall — same as
the FMCSA grader. A wrongly-confirmed door costs credibility on the call; an unconfirmed
shipper costs nothing, it just waits for a harder look.

## Output

CRM-stable shipper records for the chunk, tier-sorted, APPENDED to the running registry
(deduping parent-covered sites into one relationship):
`company_name, effort_tier, door_type, flatbed_fit, ships, city, state, phone, email,
website, onboarding_url, contact_grade, parent_company, naics, source, vertical, notes`

Honest blanks where nothing was found. Any wrong-trailer catches routed to the
other-vertical bin, not dropped.

## Run discipline

- **Chunks of 50**, marching through the Grader's ranks.
- **Operator picks the slice** each run (skip-the-top is valid).
- Review after each chunk before the next.
- **Fan-out: ~15-20 companies per agent** (token-aware default, ratified 2026-06-17).
  Fewer agents each doing more companies is markedly cheaper than many small agents. In a
  controlled 200-company A/B (everything held constant but fan-out), **10 agents x 20 cos cut
  total billed tokens ~37% and output tokens ~41%** vs the old 20 agents x 10 cos — at
  equal-or-better research quality (more GREEN doors, no within-block decay). Mechanism:
  per-agent cost scales **sublinearly** — each agent did 2x the work for only +25% cost,
  because the fixed per-agent overhead (system prompt + tool schemas + instructions, re-read
  on every tool call) is paid per AGENT, not per company. Caveats to honor:
  - Suspected context-bloat / quality ceiling past **~50 companies/agent** (unmapped — a 4x50
    arm would find where the savings flatten). Stay in the 15-20 band until that's tested.
  - **Keep the machine awake** on long unattended fan-outs (caffeinate / disable sleep). The
    one agent failure in the test was an AFK sleep/disconnect, NOT a batch-size effect.
  - Rough cost model: ~315k-505k billed tokens/company depending on fan-out, dominated by
    cache re-reads that scale with agent count more than company count.
