# Voice Reputation — Remediation SOP

Sequenced fix for the flagged Sales line **+1 561-291-8209**. Tracks A–B stop the
damage and clean up; C–D make it durable. All steps are **operator-executed**
(Aircall + external portals); agents are read-only on Aircall.

Legend: ☐ to do · **[OPERATOR]** only you can do · **[VERIFY]** confirm Aircall
capability/plan first (flag-don't-guess).

---

## TRACK A — Stop the bleeding (today, costs nothing)

The fastest reputation gain is removing the signals that keep re-flagging it.

- ☐ **[OPERATOR] Cap the Sales line immediately.** Drop +1 561-291-8209 to a
  light load (~40–50 dials/day max) until the pool exists. Continuing 200–300/day
  on a flagged line just deepens the flag.
- ☐ **[OPERATOR] Dial graded leads only.** Route the floor onto the
  `fmcsa-lead-grading` output. Kill the "less desirable / low-answer" lists — every
  unanswered cold dial is a reputation debit. This is the single biggest behavioral fix.
- ☐ **[OPERATOR] Scrub dead numbers** out of any list before it's dialed
  (disconnected / invalid tank the answer rate that the engines score).
- ☐ **[OPERATOR] Behavioral hygiene for the floor** (make it a rule, not a suggestion):
  - Leave a short voicemail identifying Ace Dispatch + why calling (raises perceived legitimacy).
  - Never redial the same number multiple times in a day.
  - Don't machine-gun back-to-back dials; pace them.
  - Avoid call times that produce instant hang-ups.

## TRACK B — Remediate the burned number (this week)

- ☐ **[OPERATOR] Submit Free Caller Registry** for BOTH numbers using
  `Free_Caller_Registry_Worksheet.md` → https://www.freecallerregistry.com .
  One form pushes to Hiya + TNS + First Orion. Re-evaluation typically takes days,
  not instant. (Submitting the clean 2023 line too protects it pre-emptively.)
- ☐ **[OPERATOR][VERIFY] Confirm A-level STIR/SHAKEN** on both lines with Aircall
  support. If 561-291-8209 was ported in and is only getting B-attestation, that
  alone can sustain the flag — ask Aircall to sign it A.
- ☐ **[OPERATOR] Check current status per engine** (they're independent):
  - Hiya: hiya.com number lookup / Hiya for business.
  - Truecaller: truecaller.com (and request unflag if listed).
  - Test-call a real AT&T, Verizon, and T-Mobile handset and note the on-screen label.
- ☐ **[OPERATOR] File direct unflag/dispute** with any engine still showing spam
  after FCR propagates (each has a remediation/dispute path; FCR covers the bulk).
- ☐ **Decision — rest vs. push.** If 561-291-8209 stays flagged after FCR + A-attestation,
  **rest it** (light/no cold use for ~2–4 weeks while the pool carries volume) rather
  than fighting it hot. A rested + re-registered number recovers; a hammered one won't.

## TRACK C — Build the durable system (so it never recurs)

This is the real fix. Detail + sizing in `Number_Pool_Plan.md`.

- ☐ **[OPERATOR] Provision a pool of outbound lines** (~4–6, size per the plan once
  you give me rep/dial counts). Cold volume spreads across the pool; no single line
  carries the floor again.
- ☐ **[OPERATOR] Warm each new line** (low volume week 1, ramp over ~3 weeks) and
  register each on FCR at activation. Never point a fresh line at full volume.
- ☐ **[OPERATOR] Keep the 2023 dispatch line entirely out of cold rotation.**
- ☐ **[OPERATOR][VERIFY] Local presence.** 561 (S. Florida) calling carriers
  nationwide is an area-code mismatch (a spam signal + lower answers). Consider a
  few lines in the regions you target most (e.g. TX / Southeast, where the roster
  concentrates) so caller area code matches the lead. **[VERIFY]** whether your
  Aircall plan supports outbound caller-ID rotation natively or needs a power-dialer
  integration — Aircall does not always rotate caller ID across a pool on its own.
- ☐ **[OPERATOR][VERIFY] CNAM / Branded Caller ID.** Set the outbound display name
  ("Ace Dispatch") via Aircall CNAM if supported; rich Branded Caller ID (name+logo
  on screen) is a paid Phase-2 add via Hiya Connect / First Orion. Defer until the
  pool + FCR are in place.

## TRACK D — Monitor (ongoing, weekly)

- ☐ **[OPERATOR] Weekly spam-status check** of every active outbound line across
  Hiya / Truecaller / a live handset on each of the big-3 carriers. Log results.
- ☐ **[OPERATOR] Watch answer rate per line** in Aircall. A line trending down =
  early re-flag warning; rest it before it's labeled.
- ☐ **[OPERATOR] Re-submit FCR** if a line's display name/category/volume changes.

---

### Why this order
Track A removes the live signals that re-flag the number daily — biggest, fastest,
free. Track B is the registration/attestation backstop you skipped at setup. Track C
makes the behavior structurally impossible to repeat (no line CAN be overloaded).
Track D catches the next slip before it costs you. Registration without A is a number
that gets re-flagged in days — which is the trap to avoid.
