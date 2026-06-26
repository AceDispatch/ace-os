# FMCSA Census Field Reference (v4)

The fields the grading engine reads. The input CSV should be produced by
`scripts/extract_leads.py` (which adds the vehicle-type columns and the true
authority-age columns); a raw census export still grades, but with the vehicle
gate OFF and on the ADD_DATE proxy.

## Eligibility / gating fields
| Field | Used for | Notes |
|---|---|---|
| `CARRIER_OPERATION` | **Interstate gate** | `A`=Interstate, `B`=Intrastate Hazmat, `C`=Intrastate Non-Hazmat. Keep `A` only. Authoritative — do not infer from cargo/CLASSDEF. |
| `CLASSDEF` | For-hire gate | Must contain `AUTHORIZED FOR HIRE`. |
| `STATUS_CODE` | Active **record** gate | `A`=Active, `I`=Inactive, `P`=Pending. Keep `A`. |
| `DOCKET1_STATUS_CODE` | Active **authority** gate | `A`=active operating authority. A live *record* (`STATUS_CODE=A`) is NOT the same as live *authority*. Reject when present and ≠ `A`. |
| `PRIOR_REVOKE_FLAG` | Revocation gate | `Y` discards. Often null = never revoked. |
| `TRUE_AUTHORITY_AGE_DAYS` | **Authority-age gate + score (PREFERRED)** | Integer days since the real operating-authority grant (from AuthHist `9mw4-x3tu`, `orig_served_date` of GRANTED). Added by `extract_leads.py`. |
| `TRUE_AUTHORITY_GRANT_DATE` | Authority-age (alt) | The real grant date (`YYYY-MM-DD`). Used if `TRUE_AUTHORITY_AGE_DAYS` is absent. |
| `ADD_DATE` | Authority-age **FALLBACK only** | Format `YYYYMMDD [HHMM]`. MCS-150 record add/reactivation date. **Resets on routine MCS-150 updates**, so it mis-ages ~37% of verifiable leads (a 26-yr-old carrier can read 46 days). Used only when no true-age column is present. |
| `PHONE`, `CELL_PHONE` | Contactable gate | At least one required. (Keep `CELL_PHONE` out of any autodialer/text path — TCPA.) |
| `LEGAL_NAME` | Name gate + score | Screened against keyword lists. |

## Vehicle-TYPE gate (v4 — the real equipment filter)
FMCSA records vehicle COUNTS by type but **never records trailer body type**. The
owned/term-leased/trip-leased counts let us require a real tractor-trailer operation:
| Field group | Meaning |
|---|---|
| `OWNTRACT` / `TRMTRACT` / `TRPTRACT` | **TRACTORS** (own / term-lease / trip-lease). Any `>0` ⇒ tractor operation ⇒ **KEEP**. |
| `OWNTRUCK` / `TRMTRUCK` / `TRPTRUCK` | **Straight / box trucks.** With no tractor ⇒ box truck ⇒ discard. |
| `OWN*VAN` / `OWN*COACH` / `OWN*BUS` / `OWN*LIMO` | Passenger vans/coaches/buses/limos — excluded upstream. |

**Gate:** a lead must have a tractor (`OWNTRACT`/`TRMTRACT`/`TRPTRACT` > 0). This
concretely rules out **box trucks, hotshots (light pickups), sprinter/cargo vans,
and passenger vans/buses** — none of which the cargo flags catch (~28-29% of
"general freight" 1×1 interstate carriers are actually box trucks). For a 1×1
owner-op the single power unit is unambiguously a tractor or it isn't. Coverage
~99%; the ~1% with no vehicle counts are dropped under precision-over-recall.

## Scoring fields
| Field | Used for |
|---|---|
| `POWER_UNITS` | Fleet-size score (1–3 sweet spot) |
| `EMAIL_ADDRESS` | (carried through to output) |
| `INTERSTATE_BEYOND_100_MILES`, `DRIVER_INTER_TOTAL` | Interstate-intensity score |
| `CRGO_*` flags | Equipment classification — see below |

## Cargo flags (`X` = carrier hauls this) — body-type INFERENCE, scoring only
FMCSA does not record flatbed/reefer/dry-van. These commodity flags only *infer*
it (reefer strong; flatbed moderate; dry-van ambiguous). They are **not** an
equipment filter — that is the tractor gate above.
- **Flatbed bucket:** `CRGO_METALSHEET`, `CRGO_BLDGMAT`, `CRGO_MACHLRG`, `CRGO_LOGPOLE`, `CRGO_CONSTRUCT`
- **Reefer bucket:** `CRGO_COLDFOOD`, `CRGO_PRODUCE`, `CRGO_MEAT`, `CRGO_BEVERAGES`
- **Dry van bucket:** `CRGO_GENFREIGHT`, `CRGO_PAPERPROD`, `CRGO_DRYBULK`, `CRGO_FARMSUPP`
- **Hard discard:** `CRGO_PASSENGERS`, `CRGO_LIQGAS`, `CRGO_CHEM`, `CRGO_OILFIELD`, `CRGO_LIVESTOCK`, `CRGO_GARBAGE`, `CRGO_USMAIL`, `CRGO_DRIVETOW`, `CRGO_MOBILEHOME`, `CRGO_COALCOKE`, `CRGO_WATERWELL`

## Output / identity fields carried through
`DOT_NUMBER`, `DOCKET1` (MC number), `DBA_NAME`, `PHY_STREET`, `PHY_CITY`,
`PHY_STATE`, `PHY_ZIP`, `COMPANY_OFFICER_1`.

## Cross-reference datasets (not in the census)
- **AuthHist `9mw4-x3tu`** — `orig_served_date` of `original_action_desc='GRANTED'` = the real authority grant date (text `MM/DD/YYYY`; lags ~6-8 wks). Source of `TRUE_AUTHORITY_AGE_DAYS`.
- **Revocation `sa6p-acbp`**, **Carrier `6eyk-hxee`** — supporting authority/never-revoked checks.
