# FMCSA Extraction & Enrichment — datasets, joins, gotchas

The institutional knowledge behind `scripts/extract_leads.py`. The grader is offline;
all live cross-referencing happens here so a lead arrives already verified.

## Source: data.transportation.gov (Socrata)
Public U.S. DOT open data. No auth needed for normal queries; an **app token**
(`$SOCRATA_APP_TOKEN`) only lifts rate-throttling on heavy/repeated pulls. The API is
sanctioned (robots.txt allows `/resource/`); the data is U.S. government public-domain.
**Do not imply FMCSA/USDOT affiliation in any outreach** — that is the line FMCSA polices.

## The datasets used
| Dataset | id | What it gives |
|---|---|---|
| **Company Census** | `az4n-8mr2` | identity, contact, cargo (`CRGO_*`), **vehicle counts** (`OWNTRACT`/`TRMTRACT`/`TRPTRACT`/`OWNTRUCK`), `DOCKET1_STATUS_CODE`, `ADD_DATE` |
| **AuthHist** | `9mw4-x3tu` | `orig_served_date` of `original_action_desc='GRANTED'` = the **real authority grant date** |
| Revocation | `sa6p-acbp` | never-revoked cross-check (supporting) |
| Carrier (L&I) | `6eyk-hxee` | `common_stat`/`contract_stat` active-authority cross-check (supporting) |

## The two things the census CANNOT tell you
1. **Trailer body type (flatbed/reefer/dry van).** Not recorded by FMCSA anywhere
   (also absent from the inspection files `rbkj-cgst`/`fx4q-ay7w`). Only inferable
   from `CRGO_*` commodity flags. → kept for scoring, never a hard gate.
2. **True authority age** is NOT `ADD_DATE`. `ADD_DATE` is the MCS-150 record
   add/reactivation date and **resets on routine updates** → ~37% of verifiable
   leads mis-aged. The real grant date lives in AuthHist.

## The vehicle-type discriminator (the box-truck fix)
`OWNTRACT`/`TRMTRACT`/`TRPTRACT` (tractors) vs `OWNTRUCK` (straight/box trucks) vs
`OWN*VAN`/`OWN*COACH`/`OWN*BUS`/`OWN*LIMO` (passenger). Requiring a tractor rules out
box trucks (~29% of interstate for-hire 1×1), hotshots (light pickups), sprinter/cargo
vans, and buses/vans. For a 1×1 owner-op the single power unit is unambiguously a
tractor or not. ~99% coverage; the ~1% with no vehicle counts are dropped.

## AuthHist join — the gotchas (learned the hard way)
- `orig_served_date` is **TEXT `MM/DD/YYYY`** → you cannot `$where` range-filter or
  `$order` it server-side (text sort puts `12/31/2025` above `01/15/2026`). Pull
  GRANTED rows **by year** via `orig_served_date like '%/YYYY'` and parse locally.
- AuthHist `dot_number` is **zero-padded to 8** (`04475210`); census DOT is unpadded
  (`4475210`) → strip leading zeros before joining.
- AuthHist **lags real-time ~6-8 weeks** → carriers granted in the last ~6 weeks have
  no AuthHist row yet (true-age blank → grader falls back to `ADD_DATE` for those).
- Take the **max** GRANTED date per DOT = the current authority's grant (handles
  revoke-then-reinstate). True active-authority age = `as_of − max(GRANTED date)`.

## Throttling
Anonymous Socrata throttles heavy repeated pulls. Prefer the `.json` endpoint with
`$limit` up to 50000 + `$offset` pagination, an app token, and modest pacing. (In a
pinch the `.csv` endpoint via a streaming client was more robust than `.json` under load.)

## Census filter the extractor applies (the rest is the grader's job)
`carrier_operation='A' AND classdef like '%AUTHORIZED FOR HIRE%' AND status_code='A'
AND docket1_status_code='A' AND (prior_revoke_flag IS NULL OR prior_revoke_flag!='Y')`
plus optional `phy_state in(...)` and `power_units='N'`. Vehicle gate, cargo, name,
completeness, and age all run in `grade_leads.py`.
