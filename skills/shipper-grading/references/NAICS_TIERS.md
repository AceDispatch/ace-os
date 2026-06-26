# NAICS Tiers & Equipment-Type Map (Grader reference)

Mechanical sorting tables. The Grader uses these with name-signals to bucket the pile.
NO web lookups — these are static reference tables.

## FLATBED tier-1 (strong open-deck product — base score 30)
331110 331221 331222 331210 332312 332311 332313 332321 332322 332323
332420 332910 332911 332919 332996 327320 327331 327332 327390 327991
321113 321114 321214 321920 333120 333132 336611 332111

## FLATBED tier-2 (plausible open-deck — base score 20)
331318 331511 331513 332439 332618 327992 327120 327310 321211 321212
321912 321918 321991 321992 333111 333131 333922 333923 333924 336212
336510 332112 332119 332510 332999 332410

## EQUIPMENT-TYPE OVERRIDES (route to OTHER-VERTICAL, sub-tag the type)
# Real shipper of the WRONG trailer for flatbed. Sort to other-vertical roster
# with the suspected type; do NOT put in flatbed buckets.

dump (loose aggregate / cement / sand-gravel):
  - name signals: AGGREGATE, SAND, GRAVEL, READY MIX, READY-MIX, CEMENT (loose),
    CRUSHED STONE, QUARRY
  - note: precast PRODUCTS / PIPE / CULVERTS in 327xxx stay FLATBED — only LOOSE material is dump

van (boxed / palletized / drummed light goods):
  - name signals: POWDER, ATOMIZED, PACKAGING, DRUM, TOTE, ENCLOSURE, CABINET,
    SHEET METAL (light enclosures/HVAC)

tanker (liquids / gas):
  - name signals: CHEMICAL, LIQUID, PROPANE, FUEL, ASPHALT (liquid),
    TANK (when carrying liquid, not making tanks)

heavy-haul (oversized beyond standard flatbed):
  - name signals: CRANE, TRANSFORMER, TURBINE, oversized PRESSURE VESSEL,
    very large MODULAR BUILDING

## NAME SIGNALS — flatbed YES
STEEL IRON FABRICAT STRUCTURAL REBAR PIPE TUBE PRECAST CULVERT BEAM TRUSS
LUMBER FOUNDRY FORGING EXTRUSION "METAL BUILDING" "BUILDING SYSTEMS" TANK
BRICK BLOCK "CONCRETE PRODUCT" MILLWORK MANUFACTURING MFG PRODUCTS SUPPLY INDUSTRIES

## NAME SIGNALS — DISCARD (non-shipper service/finishing)
PLATING COATING ANODIZ POLISH GALVANIZ "POWDER COAT" PAINT RECYCL SALVAGE
SCRAP WASTE DISPOSAL "ENVIRONMENTAL SERVICES" "ENERGY SERVICES" "OILFIELD SERVICE"
"MACHINE SHOP" "TOOL & DIE" REPAIR "HEAT TREAT" ELECTROPLAT LABORATOR TESTING
INSPECTION DENTAL JEWELR

## Grading logic (mechanical)
1. Base score from NAICS tier (tier-1=30, tier-2=20, else 8).
2. +20 strong flatbed name-signal, +10 medium, 0 none.
3. If an equipment-type override fires -> OTHER-VERTICAL (sub-tag type), skip flatbed.
4. Else if DISCARD signal dominates with no flatbed signal -> DISCARD.
5. Else: strong NAICS + clean name -> FLATBED-YES; ambiguous -> FLATBED-UNSURE.
6. Dedupe to company; rank flatbed-yes by score.

## NAME PENALTIES — discipline, not a flat word list (refined 2026-06-13)

The penalty must understand a word IN CONTEXT — its pairing and its connotation —
not just its presence. "Paint" is a good word (coatings ship!); "paint shop" is a
finishing operation. "Welding" is a plausible fabricator; "welding shop" is jobbing.
Three distinct mechanisms:

(1) DISQUALIFYING PHRASES (-35, or -20 for fab shop) — specific PAIRS naming a known
    non-shipper operation. Matched as PHRASES, not tokens:
      PAINT SHOP, PAINT BOOTH, MACHINE SHOP, BODY SHOP, REPAIR SHOP, WELD SHOP,
      WELDING SHOP, SIGN SHOP, PRINT SHOP, CHROME SHOP, MUFFLER SHOP, FAB SHOP(-20)
    Intentionally NOT disqualified: WOOD SHOP, STEEL SHOP, PIPE SHOP — those can be
    real producers. Only shops naming a finishing/jobbing/service trade sink.

(2) STANDALONE DISQUALIFIERS (-35 / -18) — words with NO dual reading; the business
    IS the finish/service so no pairing is needed:
      heavy: PLATING, ANODIZ, ELECTROPLAT, POWDER COAT, GALVANIZ, HEAT TREAT,
             POLISHING, CHROME PLAT, CALIBRAT, RENTAL(S), TOOL & DIE, NDT, TESTING LAB
      med:   COATING, FINISHING, REMANUFACTUR, RECONDITION, MAINTENANCE,
             INSTALLATION, ERECTION, ERECTORS

(3) SIZE NUDGE (-6) — a bare " SHOP " not in a disqualifying pair leans SMALL, so a
    GENTLE downweight, not a sink. Plenty of real shippers are a "shop."

NOT PENALIZED (these are positives or neutral): WELDING, FABRICATION, STEEL, IRON,
STRUCTURAL, etc. Welding belongs with the positive signals — pulling it into
penalties was a discipline error, now corrected.

WHY this is discipline not methodology: the method (penalize names) was right; the
JUDGMENT of which words, in which pairings, carry the signal is the discipline. A
flat scan for "shop" cannot tell "paint shop" from "wood shop" — the refined logic
matches the phrase and reads the connotation. Penalties REORDER, never delete, so a
mis-call costs only patience (a real shipper waits lower in line), never loss.
Heavy-penalized (<= -30) tier-1 names drop from confident-YES to UNSURE.


## OILFIELD / EXTRACTION / TANKER discipline (finalized 2026-06-13)

The distinction is the company ROLE IN THE FREIGHT, not its industry:
  SERVICES / EXTRACTION / TANKER -> not a flatbed product shipper -> SINK
  MANUFACTURED PRODUCT (even oil-adjacent) -> GREAT flatbed target -> SPARE

SINK (clear non-product-shippers):
  - Named services/extraction majors (-40): Schlumberger, Halliburton, Baker Hughes,
    Weatherford, Anadrill, Nabors, Conoco, Chevron, Exxon, Occidental, Devon, Pioneer, EOG...
  - Role signals (-22 to -35): oilfield service, well service, wireline, drilling, frac,
    flowback, exploration, E&P, oil & gas (producer), resources, petroleum corp,
    energy services, operating/production company
  - Tanker/gas (-30 to -35): air products, praxair, linde, airgas, crude, refining, LNG, LPG
  - Tank STORAGE hard-block (-35, never rescued): tank farm, crude oil storage, tank battery,
    terminal, storage facility

SPARE (product manufacturers — these are GREAT targets):
  - oil as PRODUCT: motor oil, lubricant, grease, blending, additive (packaged goods shipper)
  - automotive: auto parts, parts, filter, battery, brake, gasket, bearing, piston
  - any clear manufacturer: manufacturing, fabricat, steel, products inc/llc/corp
  - tank MAKERS only: tank manufacturing, tank & manufacturing, tank fab/works/systems
    (NOT bare "tank" — that also matches tank farms)

WHY oilfield EQUIPMENT names (Houston Oilfield Equipment, Southwest Oilfield Products,
Worldwide Oilfield Machine) correctly SURVIVE: they MAKE and SHIP physical product
(valves, tools, machined parts) on flatbeds. The product-rescue keeps them; only
services/extraction/storage sink. This is the nuance working correctly.

PRINCIPLE: catch the CLEAR false-positives; let ambiguous names pass to the Researcher.
A plausible-but-wrong target costs one web check; a wrongly-sunk real shipper may never
get looked at. The asymmetry favors letting plausible things through. The Grader produces
a ~99%-clean WORKING REGION (top ~1000), not a perfect list — perfection is the
Researcher job.

---
## STATUS: FINALIZED 2026-06-13. Grader locked. Ready to run as Agent (Contract 05).
