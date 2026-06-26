# Voice Caller-ID Reputation — Ace Dispatch

The **voice twin** of the A2P/SMS layer (`../a2p/`). A2P 10DLC governs whether our
**texts** deliver; this layer governs whether our **calls** ring through clean
instead of showing "Spam Likely" / "Scam Likely" — or getting silently blocked.
They are entirely separate systems. Registering for 10DLC did nothing for voice;
that gap is why the Sales line got flagged.

## The governing model (earned reputation, not a one-time filing)

Voice caller-ID reputation is scored continuously by carrier analytics engines —
**Hiya (AT&T), TNS (Verizon), First Orion (T-Mobile)** — plus apps like Truecaller
and Robokiller. They operate **independently** (clean on AT&T ≠ clean on Verizon).
Four levers move the score, in order of leverage for us:

1. **Behavior** (biggest lever). Velocity, answer rate, call duration, repeat
   dials, complaints. A new line jumping to hundreds of cold dials/day with low
   answers is the textbook scammer signature. **No registration survives bad
   behavior.**
2. **Registration.** Free Caller Registry (one form → all three engines) tells the
   engines who we are and asks them to reconsider a flag. Backstop, not a fix.
3. **STIR/SHAKEN attestation.** Each call is signed A/B/C. A = carrier fully
   vouches we own the number. B (common on ported/BYOC lines) alone can draw spam
   treatment. Confirm A-level with Aircall per line.
4. **Branded Caller ID / CNAM.** Our name on the screen instead of an unknown 561
   number → higher answers, fewer "report spam" taps. Phase-2 paid layer.

## Our two numbers — why one is clean and one is burned

| Line | Number | Use | Status |
|---|---|---|---|
| **Main / dispatch** ("the 2023 number") | **+1 561-231-2023** | Inbound + dispatch; every call answered, real conversations, no rotation | **CLEAN — earned reputation. KEEP IT OUT of cold rotation forever.** |
| **Sales** | **+1 561-291-8209** | All cold outbound: 200–300 dials/day, one line, no rotation, a stretch of low-answer junk leads | **FLAGGED — every spam signal stacked at once.** |

The contrast IS the diagnosis: the 2023 line proves clean behavior keeps a number
clean. The Sales line proves the opposite. The fix copies the 2023 line's behavior
onto a *pool* of lines and never overloads one again.

## Compliance / behavioral guardrails (standing)
- **The 2023 dispatch line never makes cold sales dials.** Protect the one clean asset.
- **Only graded leads get dialed.** Low-answer junk leads are a reputation tax;
  the `fmcsa-lead-grading` skill (9 hard gates, precision-over-recall) exists to
  prevent exactly this. Dial lists come from graded output only.
- **Per-number daily cold-dial ceiling is enforced** (see `Number_Pool_Plan.md`).
- **Dead/disconnected numbers are scrubbed** before dialing (they crater answer rate).
- Honors the existing dialing-compliance architecture (TCPA/TSR/DNC) — this layer
  is reputation, not consent; consent rules in `../a2p/` and STATE.md still apply.

## Files
- `Remediation_SOP.md` — the fix, sequenced (stop the bleeding → remediate → build the pool → monitor).
- `Free_Caller_Registry_Worksheet.md` — paste-ready FCR submission fields per number.
- `Number_Pool_Plan.md` — rotation + warm-up architecture and line-count sizing.

## Status (2026-06-22)
- Layer created. Diagnosis confirmed (behavioral overload on one un-registered line).
- **NOT YET EXECUTED** — every step below is operator-only (Aircall settings, buying
  lines, FCR submission). Per the constitution, agents are read-only on Aircall.
- **BLOCKING INPUT NEEDED to finalize pool size:** current rep count and dials/day per rep.
