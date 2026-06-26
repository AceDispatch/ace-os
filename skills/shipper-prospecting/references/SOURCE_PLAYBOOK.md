# Source Playbook — Shipper Prospecting

Ranked hunting sources by layer. **Evidence honesty:** sources are marked
**[PROVEN]** (produced real candidates in an actual run), **[GATED]** (high-value but
behind login/membership/paywall — a priority target per discipline law 4), or
**[UNTESTED]** (plausible but not yet validated — treat as a hypothesis, not a
guarantee). Do not present untested veins as proven.

## Layer 1 — Anchors
- Company sites, SEC filings, and public industrial wikis (e.g. GEM.wiki for steel/cement
  plants). **[PROVEN]**
- City economic-development / "major employers" history pages double as anchor lists and
  often name employee counts and facility scale. **[PROVEN]**
- **Cap this layer.** Anchors are the seed for Layer 3 relationship hunting, not the goal.

## Layer 2 — Trade-registry sweep (richest for small shippers)
Productive, accessible veins:
- **Industry/­trade producer rosters published as government PDFs** — e.g. a state DOT's
  approved-producer list for precast concrete pipe and box culvert is a clean,
  address-tagged roster. Pull the whole PDF, don't search it piecemeal. **[PROVEN — richest
  single precast/pipe source in test]**
- **The Blue Book (thebluebook.com)** — construction-industry directory; strong for steel
  fabricators, rebar fabricators, structural. **[PROVEN]**
- **Procore network (procore.com/network)** — "structural steel" and "reinforcing steel"
  company listings. **[PROVEN]**
- **Yellow Pages** — steel service centers, steel fabricators by city. Workmanlike but
  productive. **[PROVEN]**
- **Niche metals directories** (steelservicecenters.com, metalservicecenters.net,
  metalservicecenters-style listings). **[PROVEN]**
- **Open association supplier directories** that publish addresses — e.g. a regional
  precast association's state supplier page. **[PROVEN]**

High-value but **[GATED]** — priority targets to penetrate (membership or one-time
directory purchase converts these thin layers into dense ones):
- **MSCI** — Metals Service Center Institute member directory.
- **CRSI** — Concrete Reinforcing Steel Institute fabricator/member listings.
- **NASPD** — National Association of Steel Pipe Distributors.
- **NPCA / PCI** — precast producer member directories (full rolls).
- **Steel Joist Institute** member list.

## Layer 3 — Supplier-ring inference
- **Procore + Blue Book** filtered to structural steel fabricators and metal-building
  manufacturers (the buyers of mill steel who re-ship). **[PROVEN]**
- Query pattern: `"structural steel fabricator [city]"`, `"rebar fabricator [city]"`,
  `"metal building manufacturer [region]"`, plus an **"AISC certified [region]"** filter
  to find real fabricators. **[PROVEN]**
- AISC certified-member lookups (where accessible) for legitimate structural fabricators.
  **[UNTESTED — promising]**

## Layer 4 — Freight-footprint reversal (verification, not discovery)
- **TruckersReport (thetruckersreport.com)** — search by an ALREADY-KNOWN company name,
  e.g. `getting loaded at [company] [city]`. A "loading thread" hit is a strong signal the
  company ships flatbed volume. **[PROVEN as verification — one solid hit in test]**
- **Do NOT** cold-trawl Reddit (r/Truckers, r/flatbed, r/FreightBrokers) for unknown
  shipper names — it returns only generic load-finding/securement chatter. **[PROVEN DEAD
  END for discovery]**

## Confirmed dead ends (do not spend effort here for shipper discovery)
- **CarrierSource** and similar carrier-review sites — list carriers and brokers, not
  shippers. **[PROVEN DEAD END]**
- **Load boards** (DAT, Truckstop, 123Loadboard, Direct Freight, etc.) — surface
  carriers/brokers and transient loads, never a durable shipper roster. **[PROVEN DEAD END]**
- **Reddit cold-trawl** for discovery — see Layer 4. **[PROVEN DEAD END]**

## Note on retired Layer 5
City chamber pages and rail-park tenant lists, originally trialed as a "geospatial" layer,
are really just more Layer 2 directory sources and can be folded there if useful. The
actual satellite/overhead read is retired (human task, outside this skill).
