# Shipper Researcher Summary — LA/MS/AL — 2026-06-17

Refiner Job 2 (Researcher) on 200 companies sampled from regional flatbed ranks 1-1000.
Read-only web + FMCSA SAFER. Precision over recall; honest blanks. No contact made.

- Registry: `outbox/2026-06-17_shipper_registry_LA-MS-AL.csv` (200 CRM-stable records, tier-sorted)
- States: LA 67 / MS 39 / AL 94

## Effort tiers (dial-list sort order)
- **T1 self-onboard (verified door):** 6
- **T2 reachable-low (direct contact/captive authority):** 24
- **T3 reachable-high (general line):** 113
- **T4 confirmed shipper, no contact found:** 57

## Verified carrier doors (GREEN): 31
- flatbed_fit yes: 140 / unsure: 60

### T1 — self-onboard doors
- **CMC STEEL FABRICATORS INC DBA CMC CAPITOL STEEL** (LA) — portal:proprietary; parent: Commercial Metals Company (CMC); https://www.cmc.com/en-us/mycmc/request-access
- **GP - ROCKY CREEK LUMBER** (AL) — parent-carrier-portal; parent: Georgia-Pacific / KBX Logistics; https://kbx.com/become-a-carrier/
- **HARRIS REBAR NUFAB LLC - AMBASSADOR STEEL CORP** (LA) — parent carrier program (Nucor Transportation & Logistics); parent: Nucor Corporation; https://nucor.com/transportation-logistics/
- **NUCOR HARRIS REBAR JACKSON LLC** (MS) — live signup portal; parent: Nucor Corporation; https://www.nucorapps.com/
- **SMI STEEL LLC** (AL) — carrier_portal; parent: Commercial Metals Company (CMC); https://www.cmc.com/en-us/mycmc/request-access
- **WEST FRASER MAPLESVILLE LUMBER MILL** (AL) — carrier-application-portal; parent: West Fraser Timber Co Ltd; https://forms.office.com/r/mRQQvdQQQk

### T2 — reachable doors / captive authority (named)
- **CAROLINA STEEL GROUP, LLC** (AL) — parent-carrier-authority; 334-265-6702; parent: W&W/AFCO Steel
- **CELLXION LLC - SABRE BUILDING SYSTEMS BY CELLXION** (LA) — captive-authority; 318-213-2847; parent: Sabre Industries Inc (Alvarado TX)
- **COTTONDALE WOOD PRODUCTS** (AL) — captive FMCSA carrier authority; (205) 758-2761; parent: Hinton Lumber Products LLC
- **FERGUSON FIRE & FABRICATION (FACILITY 2567)** (AL) — captive FMCSA carrier (Ferguson Enterprises DOT 997796); (256) 582-3245; parent: Ferguson Enterprises LLC
- **GENERAL SOUTHERN INDUSTRIES, INC.** (AL) — captive private fleet (Warrior River Steel division operates tractors/trailers/flatbeds); 256-332-6652
- **HOOD INDUSTRIES INC, WAYNESBORO** (MS) — captive_fmcsa_carrier; (601) 735-5038; parent: Hood Industries Inc
- **L & L LUMBER CO., INC** (AL) — captive_carrier; (256) 533-9220
- **LAUREL MACHINE AND FOUNDRY COMPANY INC, LAUREL** (MS) — captive FMCSA private carrier (DOT 89683); 601-428-0541
- **METRO BOILER TUBE COMPANY, INC.** (LA) — captive-authority; 225-647-9207
- **SOUTHLAND STEEL FABRICATORS** (LA) — captive FMCSA carrier + broker authority (SOUTHLAND TRUCKING INC DOT 4418643 MC-1736857 at same address 251 Greensburg St); (225) 222-4141
- **STEELCASE INC** (AL) — carrier_contact_email; (256) 232-9600
- **TINDALL PRECAST CONCRETE** (MS) — captive FMCSA carrier (Tindall Haul & Erect DOT 359960 MC-215848); 800-280-0302; parent: Tindall Corporation (SC)
- **VALLOUREC TUBE-ALLOY, LLC** (LA) — captive-authority; 337-837-8942; parent: Vallourec SA (France)
- **ZACHRY MOSS POINT FABRICATION FACILITY** (MS) — ISNetworld vendor/carrier portal (zachrygroup.com/procurement); 228-475-5823; parent: Zachry Group (Zachry Holdings Inc.)

## EXCLUDE / FLAG counts (caught by Researcher)
- DEFUNCT/closed: 21
- UNVERIFIED-ENTITY (name-collision / can't confirm): 25
- WRONG-TRAILER (van/dump/tanker/heavy-haul): 27
- CAPTIVE-ONLY (small private fleet): 16
