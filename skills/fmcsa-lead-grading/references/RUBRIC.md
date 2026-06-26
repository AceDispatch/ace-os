# Grading Rubric v4 - "Perfect-Only" - Quick Checklist

## Governing philosophy
Carrier supply is effectively unlimited; rep dial-time is the scarce resource.
PRECISION beats recall. A wrongly-kept lead wastes a dial; a wrongly-dropped
lead costs nothing because thousands more wait behind it. **When in doubt, discard.**

## v4 — what changed (the box-truck + proxy-age fixes)
1. **Vehicle-type gate (NEW HARD GATE):** must run a **tractor**. Cargo flags are
   commodity inference, not equipment — ~28-29% of "general freight" 1×1 carriers
   are actually box trucks. The tractor gate is the real filter.
2. **True authority age:** age from the AuthHist grant date, not the `ADD_DATE`
   proxy (proxy mis-ages ~37% of verifiable leads). Enriched upstream by `extract_leads.py`.
3. **Active operating authority:** `DOCKET1_STATUS_CODE='A'`, not just `STATUS_CODE='A'`.

## Step 1 - Hard gates (ANY failure = discard)
- [ ] Interstate: `CARRIER_OPERATION = A`
- [ ] For-hire: `CLASSDEF` includes `AUTHORIZED FOR HIRE`
- [ ] Active record: `STATUS_CODE = A`
- [ ] **Active authority: `DOCKET1_STATUS_CODE = A`** (when present)
- [ ] Never revoked: `PRIOR_REVOKE_FLAG != Y`
- [ ] **TRACTOR: `OWNTRACT` or `TRMTRACT` or `TRPTRACT` > 0** — rules out box trucks,
      hotshots, sprinters/cargo vans, passenger vans/buses (enforced when vehicle
      columns present)
- [ ] Authority age 0-180 days — from **`TRUE_AUTHORITY_AGE_DAYS`** (AuthHist); `ADD_DATE` only as fallback
- [ ] Name is a real trucking company (not hard- OR soft-negative)
- [ ] Cargo is flatbed / reefer / dry van (no tanker, oilfield/hotshot, chemical,
      passenger, livestock, garbage, mail, tow-away, coal, water-well, mobile-home)
- [ ] Cargo actually flagged (no "unknown" carriers)
- [ ] COMPLETENESS - every one present: phone, cargo, authority date, power units,
      officer, city, state, classification, DOT number, MC docket

## Step 2 - Score (max 100)
```
Equipment fit        0-40   flatbed+reefer+van=40; flatbed/reefer=32-35; dry-van-only=12   (cargo-INFERRED body type)
Authority age        0-30   peak 61-105d (=30), the ~90-day target                          (TRUE age preferred)
Name signal          0-15   strong trucking +15 / moderate +8 / neutral 0
Fleet size           0-10   1-3 power units = 10
Interstate intensity 0-5    runs long-haul (beyond 100mi + interstate drivers)
```

## Step 3 - Tier
```
P1  >= 85     call first
P2  70-84
P3  55-69
P4  < 55      kept but weakest
```

## What FMCSA can and cannot tell you about equipment
- **CANNOT** verify flatbed vs reefer vs dry van — no FMCSA dataset records trailer
  body type. Cargo flags only *infer* it (reefer strong, flatbed moderate, dry-van
  ambiguous). Used for scoring, never as a hard equipment filter.
- **CAN** concretely rule out box trucks / hotshots / sprinters / vans via the
  tractor counts (the v4 gate). That is the real equipment discriminator.

## The 90-day logic
Brand-new carriers (≤30d) often aren't running freight yet. By 60-105 days they've
felt the pain of self-dispatching and are actively shopping — highest intent. After
~135 days intent decays. The age curve peaks at 90 — measured on **true** authority
age so a reset ADD_DATE can't fake a fresh lead.
