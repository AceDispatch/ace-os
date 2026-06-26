# Search Doctrine — Shipper Prospecting

How the Prospector hunts *well* and knows *when to quit*. This is methodology guidance —
it shapes effort allocation, never per-company verification.

## Query patterns that worked
- Structural fabricators: `"structural steel fabricator [city]"` + an `"AISC certified
  [region]"` qualifier to filter to real fabricators rather than erectors/suppliers.
- Rebar: `"rebar fabricator [city] [state]"`, `"post-tension [city]"`.
- Service centers: `"steel service center [city]"`, `"flat-rolled [city]"`,
  `"coil processing [city]"`.
- Pipe/tube/PVF: `"pipe and tube distributor [city]"`, `"PVF [city]"`,
  `"OCTG [region]"`.
- Lumber/building materials: `"lumber wholesale [city]"`, `"building material
  distributor [region]"`, `"hardwood plywood [city]"`.
- Precast/pipe: pull the state DOT approved-producer PDF directly rather than searching
  for individual plants.

## The forum rule (critical)
Carrier forums are a **verification** instrument, not a **discovery** instrument.
- RIGHT: you already have a candidate name → search `getting loaded at [name] [city]` to
  confirm it ships flatbed volume.
- WRONG: searching forums for unknown shippers ("who ships flatbed out of [city]") — this
  produces generic chatter and near-zero usable names. Don't do it.

## Yield-based stop rules (effort allocation)
- **The 20% rule.** If a directory or vein yields fewer than ~20% names not already on the
  roster, abandon it and move to the next vein. Diminishing returns are the signal to
  move, not to grind.
- **Cap Layer 1 fast.** Once the obvious anchors in the territory are listed, stop. Effort
  spent adding more anchors is effort not spent on the high-value small-shipper layers.
- **Spend the MOST effort where volume is LOWEST.** Layers 2–3 produce the valuable
  non-obvious names; if Layer 1 is producing most of the roster, the pass is failing even
  if the raw count looks healthy. Inverse yield is the health check.
- **A dry layer is a finding, not a failure.** If Layer 4 produces one hit or none, record
  that truthfully (discipline law 2). Do not pad it.

## Territory adaptation (plug-and-play)
This doctrine is territory-agnostic. To run a new area:
1. Swap the city/region tokens in the query patterns for the new territory.
2. Find the territory's equivalent government producer rosters (state DOT producer lists,
   state manufacturer registries) — these are the highest-yield Layer 2 veins everywhere.
3. The national directories (Blue Book, Procore, MSCI/CRSI/NASPD/NPCA, Yellow Pages) and
   the dead-end list apply unchanged in any US territory.
4. Commodity families shift by region — a steel-corridor area yields metals/pipe; a timber
   region yields lumber/building materials. Let the territory's industrial base set which
   veins are richest, and record that in the methods analysis so the next run of that
   territory starts informed.
