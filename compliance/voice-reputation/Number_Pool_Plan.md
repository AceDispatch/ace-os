# Outbound Number Pool — Architecture, Warm-Up, Sizing

The structural fix: cold volume is spread across a pool of warmed, registered lines,
each held under a daily ceiling, so **no single number can be overloaded into a flag
again.** The 2023 dispatch line is never in this pool.

## The per-number ceiling (planning heuristic)
There is no published carrier number, but the engines flag on velocity + low answers.
A warmed, well-behaved cold line stays clean at roughly **50–75 dials/day**. Treat
**~60/day** as the planning ceiling per line; with strong answer rates a line can
carry more, with weak ones less. This is a heuristic to size the pool, not a hard rule.

## Sizing formula
```
lines needed = ceil( total daily cold dials / per-line ceiling )
```
**Worked example at today's volume (200–300/day, ceiling ~60):**
- 200/day → ceil(200/60) = **4 lines**
- 300/day → ceil(300/60) = **5 lines**
- Add **+1 spare** for rotation slack / a line in time-out → **plan ~4–6 lines.**

> ⚠️ To finalize: I need **# of reps** and **dials/day per rep**. That sets both the
> line count and how lines map to reps/regions. Placeholder math above assumes the
> 200–300/day is the whole floor on one line today.

## Warm-up schedule (every NEW line)
Register on Free Caller Registry **before** day 1. Never start a fresh line hot.

| Phase | Daily cold dials | Focus |
|---|---|---|
| Week 1 | 10–20 | Get real connects + conversations; leave voicemails; build "answered" history |
| Week 2 | 30–40 | Steady ramp; watch the per-engine status |
| Week 3 | 50–60 | Approach the ceiling; confirm still clean before holding there |
| Steady | ≤ ~60 | Hold at ceiling; monitor weekly |

## Distribution / rotation
- **Spread reps across lines** so no line concentrates the floor's volume.
- **[VERIFY]** whether Aircall rotates outbound caller ID across a pool natively, or
  whether it needs a connected power-dialer. If not native, the practical model is:
  assign lines to reps/regions and rotate which line a rep dials from, manually or
  via an integration. Flag for operator — don't assume Aircall does it automatically.
- **Local presence:** prefer a line whose area code matches the lead's region
  (561 → a TX/Southeast carrier is an area-code mismatch that lowers answers and
  raises spam scoring). A few region-matched lines materially help where volume
  concentrates.

## Protect the clean asset
- **+1 561-231-2023 (dispatch / "the 2023 number") never enters cold rotation.**
  It is the proof that clean behavior keeps a line clean; don't spend it.

## Cost note
Each Aircall line is a paid number (and possibly a seat, depending on plan). 4–6
lines is a real but modest monthly cost — cheap against a sales floor whose calls
don't connect. **[VERIFY]** exact per-number/seat pricing on the current Aircall plan
before provisioning.
