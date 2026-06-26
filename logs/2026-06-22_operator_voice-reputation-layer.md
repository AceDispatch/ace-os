# Run Log — Operator Session: Voice Caller-ID Reputation Layer

- **Date/time:** 2026-06-22
- **Contract:** none — operator-initiated compliance work (twin of the 2026-06-21 A2P session), not a pipeline agent run
- **Operator-initiated or scheduled:** Operator-initiated (Anthony)
- **Inputs:** Operator report (Sales line flagged as spam, some calls not connecting; 200–300 cold dials/day on ONE line, no rotation, a stretch of low-answer junk leads; the 2023 dispatch line stays clean because every call is answered). Current best-practice research on STIR/SHAKEN, Free Caller Registry, Hiya/TNS/First Orion, Aircall's own spam guidance.

## Diagnosis
- Root cause: **voice spam labeling is a separate system from A2P 10DLC** (which only governs SMS). The 10DLC registration did nothing for calls; the voice side was never set up. Compounded by behavioral overload: all cold volume on one un-registered line + low answer rate + no rotation = textbook spammer signature to carrier analytics engines.
- The clean 2023 dispatch line (+1 561-231-2023) vs the flagged Sales line (+1 561-291-8209) is the proof: answered-call behavior is what keeps a number clean.

## Outputs
- `compliance/voice-reputation/` — new compliance layer (twin of `compliance/a2p/`):
  - `README.md` — governing model (behavior > registration > attestation > CNAM), number mapping, standing guardrails, status.
  - `Remediation_SOP.md` — sequenced fix, Tracks A–D (stop the bleeding → remediate the burned number → build the pool → monitor).
  - `Free_Caller_Registry_Worksheet.md` — paste-ready FCR fields for both numbers.
  - `Number_Pool_Plan.md` — rotation + warm-up architecture, per-line ceiling, sizing formula (~4–6 lines at current volume).
- `STATE.md` → v0.4 (added Voice Reputation to the compliance section + decision-log entry).

## Result
- **Partial — design complete, execution pending.** Layer legislated; NOT yet executed. Every action is operator-only (Aircall settings, buying lines, FCR submission, attestation request) — agents are read-only on Aircall per the constitution.

## Anomalies / data-quality notes
- The `fmcsa-lead-grading` skill already exists to prevent the low-answer "junk lead" half of the problem; it simply wasn't being enforced on the dial list. The fix is partly enforcing a tool already built.
- Open verifies flagged for the operator (flag-don't-guess): does the Aircall plan rotate outbound caller ID natively or need a power-dialer; Aircall CNAM/Branded Caller ID support; per-number/seat pricing; whether 561-291-8209 was ported (B-attestation risk).

## Proposed promotions / remaining work
- **BLOCKING INPUT:** rep count + dials/day per rep, to finalize pool size and line→rep/region mapping.
- Standing guardrail worth promoting to skill/contract level: dial lists draw from graded output only; the 2023 dispatch line never makes cold dials; per-line daily cold-dial ceiling enforced.
- Execution checklist lives in `Remediation_SOP.md` Tracks A–D.
