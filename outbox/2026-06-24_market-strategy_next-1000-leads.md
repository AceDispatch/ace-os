# Next-1,000 Lead Strategy — Southeast Flatbed Pull
**Date:** 2026-06-24 · **Equipment focus:** Flatbed-led (reefer/dry-van fill) · **Status:** PROPOSAL (operator ratifies; no CRM writes made)

Reconciles three sources — the DAT Market Conditions heat maps (flatbed), our HubSpot book, and 15 days of Aircall outbound call data — into a concrete, executable pull plan for the next 1,000 carrier leads.

---

## 1. The thesis in one line
**Stop re-dialing the exhausted SE core; pivot the next 1,000 into the wide-open hot markets inside the same flatbed belt — Florida above all.**

All three sources agree:
- **Map:** the Southeast is the most consistent block of "hot" (red) flatbed — high outbound load-to-truck ratio. The reddest, most consistent states are AL, GA, MS, TN, AR, LA, SC, NC, VA, the FL panhandle/north, and Houston/East TX. A carrier domiciled here has freight; that's the carrier easiest for Ace to keep loaded and worth the most.
- **Book:** we are already correctly SE-weighted, but unevenly. We hammered the easy core (GA, NC, TN, AL, SC, MS) and barely touched FL, VA, LA, OK, AR.
- **Calls:** the saturated core is burning out (SC 0% real-connect on 195 dials, TN 2%, NC 3%, MO 2%), while the fresh/open markets convert at or above average (FL 10%, LA 11%, GA 10%). Houston/East TX is the single best converter (14%, 66s avg talk).

---

## 2. What the data showed

### 2a. Coverage vs. opportunity (HubSpot book × FMCSA flatbed universe)
The flatbed universe = 1×1 owner-ops, active authority, flatbed-cargo flags (from our 171k clean DB). Saturation = current book ÷ universe.

| State | Flatbed universe | In book now | Saturation | Read |
|---|---|---|---|---|
| **FL** | 1,385 | 56 | **4%** | biggest open pool in the hot zone |
| **VA** | 525 | 14 | **3%** | open + hot |
| **OK** | 314 | 6 | **2%** | open |
| **LA** | 286 | 1 | **0.3%** | wide open |
| **AR** | 290 | 50 | 17% | open |
| MO | 564 | 140 | 25% | worked |
| SC | 695 | 191 | 27% | worked |
| AL | 706 | 194 | 27% | worked |
| NC | 1,152 | 370 | 32% | worked |
| KY | 349 | 123 | 35% | worked |
| MS | 393 | 159 | 40% | worked |
| GA | 1,039 | 439 | 42% | heavily worked |
| **TN** | 474 | 328 | **69%** | nearly exhausted |
| TX | 2,712 | 534 | 20% | Houston/East only (west TX cold) |

The SE/belt holds **~11,000** flatbed-capable 1×1 carriers — the next 1,000 is ~9% of the well. Supply is not the constraint; *where we fish* is.

### 2b. Who answers (Aircall, 2,964 outbound dials, 2026-06-09→06-23)
Connect = answered **and** ≥60s talk (a real conversation), by carrier area code.

| Market | Dials | Answer% | **Connect%** | Avg talk | Read |
|---|---|---|---|---|---|
| TX (Houston/E) | 361 | 69% | **14%** | 66s | best converter — real flatbed freight |
| LA | 27 | 96% | **11%** | 38s | tiny sample, but answers + connects |
| FL | 177 | 68% | **10%** | 57s | converts above SE avg, under-fished |
| GA | 61 | 74% | **10%** | 39s | still converts despite being worked |
| AL | 177 | 63% | 6% | 34s | solid |
| AR | 64 | 73% | 6% | 28s | ok |
| MS | 135 | 73% | 5% | 37s | ok |
| KY | 129 | 61% | 4% | 31s | ok |
| **NC** | 376 | 66% | **3%** | 27s | over-dialed, fading |
| **TN** | 242 | 73% | **2%** | 23s | over-dialed, fading |
| **MO** | 198 | 68% | **2%** | 24s | over-dialed |
| **VA** | 41 | 76% | **2%** | 29s | open but weak early — TEST before scaling |
| **SC** | 195 | 70% | **0%** | 19s | answers then hangs up — list fatigue |
| SE+belt | 2,199 | 69% | **6%** | — | overall low (see §4) |

**Caveat:** area code ≈ carrier domicile (true for most owner-op cells, not all); small samples (LA 27, VA 41, OK 11, WV 5) are directional only. The relative pattern — worked markets convert worst, fresh markets best — is the robust signal.

---

## 3. The allocation (sums to 1,000)
Weighted by open headroom × map heat × connect performance. Full detail in `2026-06-24_market-strategy_pull-allocation.csv`.

| State | Pull | Why |
|---|---|---|
| **FL** | **300** | The anchor. Biggest open pool (1,385 / 4% sat), hot, 10% connect. N/Central FL flatbed + reefer (produce). **Avoid Miami/Hialeah drayage** (305/786/954/754); target Jacksonville, Orlando, Tampa, Lakeland, Ocala, Tallahassee. |
| **TX** | **110** | Best converter (14%, 66s). **Houston + East TX flatbed only** (713/281/832/346/409/903/430/936). Skip west TX oilfield/cold. |
| **VA** | **80** | Open + hot. Weak early connect → pull 80 as a graded test, watch connect before scaling. Richmond/Roanoke/Norfolk. |
| **GA** | **80** | Worked but pool remains and still converts at SE-high. Atlanta/Savannah/Macon, freshest flatbed only. |
| **AL** | **70** | Deep-red flatbed, solid connect. Birmingham/Mobile (steel, building materials). |
| **NC** | **70** | Large pool but over-dialed — pull only fresh tractors. Charlotte/Triad/Raleigh. |
| **SC** | **55** | Hot map but 0% connect now = fatigue. Smaller, freshest-only. Greenville/Columbia/Charleston. |
| **LA** | **50** | Wide open (1 in book), 96% answer. High-value fresh ground. Baton Rouge/Lafayette/Shreveport. |
| **MS** | **45** | Deep-red flatbed; worked but pool remains. Jackson/Gulfport. |
| **AR** | **40** | Open + hot. Little Rock/Fort Smith. |
| **MO** | **30** | The Mid-MO market on the screenshot; over-dialed now — fresh only. |
| **KY** | **30** | Louisville flatbed, moderate. |
| **TN** | **20** | 69% saturated + 2% connect = nearly tapped. Freshest handful only. |
| **OK** | **20** | Open but tiny sample; Tulsa/OKC test. |
| **TOTAL** | **1,000** | |

**Equipment priority within every market:** flatbed-cargo first (CRGO_METALSHEET / BLDGMAT / MACHLRG / LOGPOLE / CONSTRUCT) → reefer fill where flatbed is thin and produce is strong (esp. FL, GA) → dry-van last. Target mix ≈ 65% flatbed / 20% reefer / 15% dry van.

---

## 4. Execution spec (how to actually pull these)
Run through the **v4** `fmcsa-lead-grading` pipeline so every lead is tractor-verified and true-age-fresh:

1. **`scripts/extract_leads.py`** per state (or batched), `--states FL,TX,VA,...` `--power-units 1`, which adds the AuthHist true-age + vehicle columns.
2. **`scripts/grade_leads.py`** (v4): tractor gate ON, true authority age ≤180d (peak 61–105d), active operating authority, for-hire interstate, patched name filter, full completeness. Precision-over-recall.
3. **Dedup against the live HubSpot book on DOT** — pull NET-NEW only (we already own ~2,600 of these states; don't re-import).
4. **Geo-restrict by area code / metro** per the allocation `avoid`/`priority_area_codes` columns (esp. exclude Miami drayage and west-TX oilfield).
5. Stage the ranked, deduped output in `outbox/` for the operator to import — **propose-only, no autonomous CRM writes** (constitution).

### Ties to the voice-reputation layer (don't skip)
The overall ~6% SE connect rate is not just geography — it's the spam-flagged Sales line (`compliance/voice-reputation/`) compounding with stale lists. The two fixes multiply:
- This pull delivers **fresh, graded, tractor-verified** leads → higher answer/connect than the burned core.
- But they must dial out through the **warmed, registered number pool** (not the single flagged 561-291-8209 line), with dead numbers scrubbed first. Fresh leads down a clean pipe is the compounding win; fresh leads down the flagged line wastes the pull.

---

## 5. Why this is the right call (and the risks)
**Right:** we're not abandoning the SE — we're reallocating *within* the proven hot belt from exhausted ground (TN/SC/NC/MO at 0–3% connect) to open ground with equal/greater heat and bigger pools (FL/LA/VA/AR/OK). FL alone is the largest single opportunity in the entire book: hot, 1,385 deep, 4% touched.

**Risks / watch-items:**
- **VA** shows weak early connect (2% on 41 dials) — treated as a graded test (80), not a heavy bet.
- **FL Miami metro** is container/drayage, not flatbed — the area-code exclusions matter or we re-import the wrong segment.
- **Small Aircall samples** (LA, OK, WV) are directional; let the first 200 dials in each confirm before the next wave.
- The connect signal partly reflects list *freshness*, not just market — which is itself the argument for pulling fresh here.

---
*Sources: DAT Market Conditions (flatbed, Load Density + Loads-to-Trucks); HubSpot CRM (read-only); Aircall `/calls` 2026-06-09→06-23 (read-only); FMCSA clean 1×1 DB (171,181) + graded true-age pool (20,706). No CRM or Aircall writes performed.*
