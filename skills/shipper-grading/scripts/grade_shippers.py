#!/usr/bin/env python3
"""
grade_shippers.py — Refiner Job 1 (the GRADER), Ace Dispatch shipper pipeline.

Mechanical grading of a raw EPA candidate roster. NO WEB. Runs on the whole pile.
Reads the NAICS tiers + name signals from the skill reference, scores
flatbed-plausibility, sorts into FLATBED-YES / FLATBED-UNSURE / OTHER-VERTICAL
(dump|van|heavy-haul|tanker) / DISCARD, dedupes to company, and ranks flatbed-yes.

Input : an EPA roster CSV (the Prospector's output, or a raw EPA FRS export).
        Required columns: name, naics. Optional: address, city, zip, source.
Output: <outbox>/YYYY-MM-DD_grader_flatbed_ranked.csv   (the map for the Researcher)
        <outbox>/YYYY-MM-DD_grader_other_vertical.csv    (seed for future verticals)
        <outbox>/YYYY-MM-DD_grader_summary.md             (counts, tiers, preview)
        <outbox>/YYYY-MM-DD_grader_discard_log.csv        (audit, not silent delete)

Usage:
  python skills/shipper-grading/scripts/grade_shippers.py --in inbox/epa_roster_TX.csv
  python skills/shipper-grading/scripts/grade_shippers.py --in <file> --outdir outbox
"""

import argparse, csv, os, re, sys, datetime

# ---- NAICS tiers (mirror references/NAICS_TIERS.md) ----
TIER1 = set("""331110 331221 331222 331210 332312 332311 332313 332321 332322 332323
332420 332910 332911 332919 332996 327320 327331 327332 327390 327991 321113 321114
321214 321920 333120 333132 336611 332111""".split())
TIER2 = set("""331318 331511 331513 332439 332618 327992 327120 327310 321211 321212
321912 321918 321991 321992 333111 333131 333922 333923 333924 336212 336510 332112
332119 332510 332999 332410""".split())

FLATBED_NAME_STRONG = ["STEEL","IRON WORK","IRONWORK","FABRICAT","STRUCTURAL","REBAR","PIPE",
 "TUBE","PRECAST","CULVERT","BEAM","TRUSS","LUMBER","FOUNDRY","FORGING","EXTRUSION",
 "METAL BUILDING","BUILDING SYSTEMS","TANK","BRICK","CONCRETE PRODUCT","MILLWORK"]
FLATBED_NAME_MED = ["MANUFACTURING","MFG","METAL","WELDING","FENCE","PANEL","PALLET",
 "WOODWORK","MOULDING","MOLDING","INDUSTRIES","PRODUCTS","SUPPLY","MACHINE","EQUIPMENT"]

DISCARD_SIGNALS = ["PLATING","COATING","ANODIZ","POLISH","GALVANIZ","POWDER COAT","PAINT",
 "RECYCL","SALVAGE","SCRAP","WASTE","DISPOSAL","ENVIRONMENTAL SERVICES","ENERGY SERVICES",
 "OILFIELD SERVICE","MACHINE SHOP","TOOL & DIE","TOOL AND DIE","REPAIR","HEAT TREAT",
 "ELECTROPLAT","LABORATOR","TESTING","INSPECTION","DENTAL","JEWELR"]

# ---- equipment-type overrides (route to OTHER-VERTICAL) ----
DUMP_SIG = ["AGGREGATE","SAND","GRAVEL","READY MIX","READY-MIX","CRUSHED STONE","QUARRY"]
DUMP_CEMENT = ["CEMEX","CEMENT"]  # cement = dump UNLESS clearly making precast products
VAN_SIG = ["POWDER","ATOMIZED","PACKAGING"," DRUM","TOTE","ENCLOSURE","CABINET"]
TANKER_SIG = ["CHEMICAL","LIQUID","PROPANE"," FUEL","ASPHALT"]
HEAVYHAUL_SIG = ["CRANE","TRANSFORMER","TURBINE"]

PRECAST_RESCUE = ["PRECAST","PIPE","CULVERT","PRODUCT","BLOCK","VAULT","BARRIER","SEPTIC"]


# ---- NAME PENALTIES (discipline, not a flat word list — added 2026-06-13, refined) ----
# Three distinct mechanisms, each with judgment about the word IN CONTEXT:
#
#  (1) DISQUALIFYING PHRASES — specific PAIRS that name a known non-shipper operation.
#      Matched as phrases, not tokens. "paint shop" sinks; "wood shop" / "fab shop" do NOT.
#      The pairing is the signal — the word "shop" alone is not.
#  (2) STANDALONE DISQUALIFIERS — words with NO dual reading: a plating company plates,
#      it doesn't ship truckloads. These penalize on their own.
#  (3) SIZE NUDGE — a bare "shop" (not in a disqualifying pair) leans SMALL, so a gentle
#      downweight, not a sink. Plenty of real shippers are a "shop."
#
# Penalties REORDER, never delete (the Grader ranks, doesn't gate) — so a mis-penalized
# real shipper just waits lower in line. NOT penalized: welding, fabrication, steel, etc.
# (welding is a plausible real fabricator — it belongs with positives, not penalties).

DISQUALIFYING_PHRASES = {   # -35: known non-shipper operations (the PAIR is the signal)
    "PAINT SHOP": -35, "PAINT BOOTH": -35, "MACHINE SHOP": -35, "BODY SHOP": -35,
    "REPAIR SHOP": -35, "WELD SHOP": -35, "WELDING SHOP": -35, "FAB SHOP": -20,
    "SIGN SHOP": -35, "PRINT SHOP": -35, "CHROME SHOP": -35, "MUFFLER SHOP": -35,
}
# NOTE: "WOOD SHOP", "STEEL SHOP", "PIPE SHOP" intentionally NOT here — those can be real
# producers. Only shops that name a finishing/jobbing/service trade are disqualified.

STANDALONE_DISQUALIFIERS = {  # -35: no dual reading — the business IS the finish/service
    "PLATING": -35, "ANODIZ": -35, "ELECTROPLAT": -35, "POWDER COAT": -35,
    "GALVANIZ": -35, "HEAT TREAT": -35, "POLISHING": -35, "CHROME PLAT": -35,
    "MACHINE & TOOL": -30, "TOOL & DIE": -30, "CALIBRAT": -35, "NDT": -30,
    "RENTAL": -30, "RENTALS": -30, "TESTING LAB": -35, "INSPECTION SERVICE": -30,
}
STANDALONE_MED = {  # -18: service/finishing/jobbing leaning, but some ship
    "COATING": -18, "FINISHING": -18, "REMANUFACTUR": -18, "RECONDITION": -18,
    "MAINTENANCE": -18, "INSTALLATION": -15, "ERECTION": -15, "ERECTORS": -15,
}
SIZE_NUDGE_SHOP = -6   # a bare "shop" not in a disqualifying pair: leans small, gentle nudge

# ---- OILFIELD/EXTRACTION/TANKER discipline (added 2026-06-13) ----
# The distinction is the company's ROLE IN THE FREIGHT, not its industry:
#   - SERVICES / EXTRACTION / TANKER  -> not a flatbed product shipper -> SINK
#   - MANUFACTURED PRODUCT (even oil-adjacent: motor oil, auto parts) -> GREAT -> spare
# Principle: catch the CLEAR false-positives; let genuinely ambiguous names pass to the
# Researcher (a plausible-but-wrong target costs one check; a wrongly-sunk real shipper
# may never get looked at — asymmetry favors letting plausible things through).

OILFIELD_SERVICE_NAMES = {   # -40: named services/extraction majors — recognizable, not shippers
    "SCHLUMBERGER": -40, "HALLIBURTON": -40, "BAKER HUGHES": -40, "WEATHERFORD": -40,
    "ANADRILL": -40, "HELMERICH": -40, "NABORS": -40, "PATTERSON-UTI": -40,
    "CONOCO": -40, "CHEVRON": -40, "EXXON": -40, "MARATHON OIL": -40, "OCCIDENTAL": -40,
    "APACHE CORP": -40, "DEVON ENERGY": -40, "PIONEER NATURAL": -40, "EOG RESOURCES": -40,
}
EXTRACTION_SERVICE_SIGNALS = {  # -35: role = service or extraction, not product shipping
    "OILFIELD SERVICE": -35, "OIL FIELD SERVICE": -35, "WELL SERVICE": -35,
    "WIRELINE": -35, "WELL SERVICING": -35, "DRILLING": -35, "FRAC ": -35,
    "FRACKING": -35, "FLOWBACK": -35, "PRODUCTION SERVICES": -35, "WELL LOGGING": -35,
    "EXPLORATION": -35, " E&P": -35, "OIL & GAS": -30, "OIL AND GAS": -30,
    "RESOURCES": -28, "PETROLEUM CORP": -30, "ENERGY SERVICES": -30, "ENERGY LLC": -22,
    "OPERATING COMPANY": -22, "OPERATING LLC": -22, "PRODUCTION COMPANY": -25,
}
TANKER_GAS_SIGNALS = {  # -35: liquid/gas = wrong trailer (also routed to other-vertical)
    "AIR PRODUCTS": -35, "PRAXAIR": -35, "LINDE ": -35, "AIRGAS": -35, "MATHESON": -35,
    "CRUDE": -35, "REFINING": -30, "REFINERY": -30, " LNG": -35, " LPG": -35,
}
# PRODUCT-MANUFACTURER RESCUE — if any of these appear, the name is a product shipper;
# do NOT apply the oilfield/extraction penalty (spares motor oil, auto parts, etc.)
PRODUCT_RESCUE = ["MOTOR OIL", "LUBRICANT", "AUTO PART", "AUTOMOTIVE", "PARTS",
    " FILTER", "BATTERY", "BATTERIES", "BRAKE", "GASKET", "BEARING", "PISTON",
    "PACKAGING", "BLENDING", "GREASE", "ADDITIVE", "PRODUCTS CORP", "PRODUCTS INC",
    "PRODUCTS LLC", "PRODUCTS CO", "MANUFACTURING", "FABRICAT", "STEEL", "PIPE & SUPPLY"]

# TANK is rescued ONLY as a manufacturer (tank MAKER ships product) — NOT bare "tank",
# which also matches "tank farm" / "crude oil storage tank" (pure storage/tanker).
TANK_MAKER_RESCUE = ["TANK MANUFACTUR", "TANK & MANUFACTUR", "TANK AND MANUFACTUR",
    "TANK FAB", "TANK WORKS", "TANK CO", "TANK INC", "TANK LLC", "TANK SYSTEMS",
    "STORAGE TANK MANUFACTUR", "TANK SALES"]
TANK_STORAGE_BLOCK = ["TANK FARM", "STORAGE FACILITY", "CRUDE OIL STORAGE", "TANK BATTERY",
    "TERMINAL", "TANK STORAGE"]


def oilfield_penalty(name):
    """Sink clear services/extraction/tanker names — but SPARE product manufacturers."""
    u = " " + name.upper() + " "
    # tank STORAGE/farm is a hard block — never rescued (pure storage/tanker, not a shipper)
    if any(b in u for b in TANK_STORAGE_BLOCK):
        return -35
    # product-manufacturer rescue wins outright
    if any(r in u for r in PRODUCT_RESCUE):
        return 0
    # tank rescue ONLY for tank makers (not bare "tank")
    if any(r in u for r in TANK_MAKER_RESCUE):
        return 0
    pen = 0
    svc_named = [v for k, v in OILFIELD_SERVICE_NAMES.items() if k in u]
    svc_sig = [v for k, v in EXTRACTION_SERVICE_SIGNALS.items() if k in u]
    tanker = [v for k, v in TANKER_GAS_SIGNALS.items() if k in u]
    if svc_named: pen += min(svc_named)
    if svc_sig: pen += min(svc_sig)
    if tanker: pen += min(tanker)
    return pen


def name_penalty(name):
    """Apply the three mechanisms. Phrase-aware, not a flat token scan."""
    u = " " + name.upper() + " "
    pen = 0

    # (1) disqualifying phrases — take the single worst phrase hit
    phrase_hits = [v for k, v in DISQUALIFYING_PHRASES.items() if k in u]
    if phrase_hits:
        pen += min(phrase_hits)

    # (2) standalone disqualifiers (heavy, then med — additive across the two tiers)
    sd_heavy = [v for k, v in STANDALONE_DISQUALIFIERS.items() if k in u]
    sd_med = [v for k, v in STANDALONE_MED.items() if k in u]
    if sd_heavy: pen += min(sd_heavy)
    if sd_med: pen += min(sd_med)

    # (3) size nudge: a bare " SHOP " that did NOT already trigger a disqualifying phrase
    if " SHOP " in u and not phrase_hits:
        pen += SIZE_NUDGE_SHOP

    # (4) oilfield-services / extraction / tanker sink (spares product manufacturers)
    pen += oilfield_penalty(name)

    return pen


def has(name, terms):
    u = name.upper()
    return any(t in u for t in terms)


def normalize_company(name):
    """Aggressive normalization so facility variants of one company collapse to a single
    record. 'Dixie Iron Works' / 'Dixie Iron Works Ltd' / 'Dixie Ironworks - Commerce St'
    must all reduce to the same key. Dedup only REORDERS the pile (removes repeats), so
    over-collapsing slightly is safer than leaving 15 copies of Hanson Pipe for the
    Researcher to chew through."""
    u = name.upper()
    # cut everything after a facility/location delimiter
    for cut in [" DBA ", " - ", " #", " PLANT", " PLT", " FACILITY", " LOCATION"]:
        u = u.split(cut)[0]
    # strip trailing corporate suffixes (NOT 'works' — that's part of the company name)
    u = re.sub(r"\b(INC|LLC|LP|LTD|LLP|CORP|CORPORATION|COMPANY|CO|PLLC|INCORPORATED|"
               r"LIMITED|HOLDINGS|USA)\b", " ", u)
    # collapse common spelling variants (iron works / ironworks etc.)
    u = u.replace("IRONWORKS", "IRON WORKS").replace("STEELWORKS", "STEEL WORKS")
    # remove all non-alphanumerics and collapse whitespace
    u = re.sub(r"[^A-Z0-9 ]", " ", u)
    u = re.sub(r"\s+", " ", u).strip()
    # key on the first 3 significant tokens (kills suffix/address-tail variants while
    # keeping genuinely different companies apart)
    toks = u.split()
    return " ".join(toks[:3]) if len(toks) >= 3 else u


def classify(name, codes):
    """Return (bucket, score, vertical) — bucket in yes/unsure/other/discard."""
    u = name.upper()

    # equipment-type overrides FIRST (route out of flatbed)
    # cement/aggregate = dump, UNLESS it's clearly precast products
    if has(name, DUMP_SIG) and not has(name, PRECAST_RESCUE):
        return ("other", 0, "dump")
    if has(name, DUMP_CEMENT) and not has(name, PRECAST_RESCUE):
        return ("other", 0, "dump")
    if has(name, VAN_SIG):
        return ("other", 0, "van")
    if has(name, TANKER_SIG):
        return ("other", 0, "tanker")
    if has(name, HEAVYHAUL_SIG):
        return ("other", 0, "heavy-haul")

    # discard: non-shipper service/finishing with no flatbed signal
    if has(name, DISCARD_SIGNALS) and not has(name, FLATBED_NAME_STRONG):
        return ("discard", 0, "")

    # flatbed score
    in_t1 = any(c in TIER1 for c in codes)
    in_t2 = any(c in TIER2 for c in codes)
    strong = has(name, FLATBED_NAME_STRONG)
    med = has(name, FLATBED_NAME_MED)

    s = 0
    if in_t1: s += 30
    elif in_t2: s += 20
    else: s += 8
    if strong: s += 20
    elif med: s += 10

    # SELF-PROTECTION: no flatbed NAICS AND no flatbed name = not flatbed ore.
    if not in_t1 and not in_t2 and not strong and not med:
        return ("discard", 0, "")

    # NAME PENALTY — heavy deductions for facility/service signals (paint shop, repair,
    # plating, machine shop, etc.). The name discriminates HARD, like the FMCSA grader.
    pen = name_penalty(name)
    s += pen  # net score: a flatbed NAICS with a "paint shop" name nets low

    # Clamp floor at 1 (never negative; the Grader ranks, doesn't delete).
    if s < 1: s = 1

    # BUCKETING with the penalty applied:
    # A heavy penalty knocks a name out of "confident yes" even with a tier-1 NAICS —
    # because the name is telling us this facility doesn't ship truckloads. It drops to
    # UNSURE (still researched, just ranked far lower), not discarded.
    HEAVY_PENALIZED = pen <= -30

    if in_t1 and not HEAVY_PENALIZED:
        return ("yes", s, "flatbed")
    if strong and not HEAVY_PENALIZED:
        return ("yes", s, "flatbed")
    # tier-2, or medium-only name, or anything heavily penalized -> unsure (low rank)
    return ("unsure", s, "flatbed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--outdir", default="outbox")
    args = ap.parse_args()

    if not os.path.exists(args.infile):
        sys.exit(f"Input not found: {args.infile}")
    os.makedirs(args.outdir, exist_ok=True)
    today = datetime.date.today().isoformat()

    rows = list(csv.DictReader(open(args.infile, encoding="utf-8")))
    if not rows:
        sys.exit("Input is empty.")
    # locate columns case-insensitively
    cols = {c.lower(): c for c in rows[0].keys()}
    name_c = cols.get("name") or cols.get("company") or cols.get("company_name")
    naics_c = cols.get("naics") or cols.get("naics_codes")
    if not name_c or not naics_c:
        sys.exit(f"Need 'name' and 'naics' columns. Found: {list(rows[0].keys())}")
    city_c = cols.get("city"); addr_c = cols.get("address"); zip_c = cols.get("zip")
    src_c = cols.get("source")

    yes, unsure, other, discard = [], [], [], []
    seen = set()
    for r in rows:
        name = (r.get(name_c) or "").strip()
        if not name:
            continue
        codes = [c.strip() for c in (r.get(naics_c) or "").replace(",", ";").split(";") if c.strip()]
        norm = normalize_company(name)
        if norm in seen:
            continue
        seen.add(norm)
        bucket, score, vertical = classify(name, codes)
        rec = {
            "company": name,
            "naics": ";".join(codes),
            "city": (r.get(city_c) or "").strip() if city_c else "",
            "address": (r.get(addr_c) or "").strip() if addr_c else "",
            "zip": (r.get(zip_c) or "").strip() if zip_c else "",
            "source": (r.get(src_c) or "EPA_FRS").strip() if src_c else "EPA_FRS",
            "score": score,
            "vertical": vertical,
        }
        if bucket == "yes": yes.append(rec)
        elif bucket == "unsure": unsure.append(rec)
        elif bucket == "other": other.append(rec)
        else: discard.append(rec)

    # rank flatbed (yes first by score, then unsure)
    yes.sort(key=lambda x: x["score"], reverse=True)
    unsure.sort(key=lambda x: x["score"], reverse=True)
    flatbed = []
    rank = 1
    for r in yes:
        r["rank"] = rank; r["bucket"] = "yes"; flatbed.append(r); rank += 1
    for r in unsure:
        r["rank"] = rank; r["bucket"] = "unsure"; flatbed.append(r); rank += 1

    # write flatbed ranked
    fb_path = os.path.join(args.outdir, f"{today}_grader_flatbed_ranked.csv")
    with open(fb_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["rank","score","bucket","company","naics","city","address","zip","source"])
        w.writeheader()
        for r in flatbed:
            w.writerow({k: r.get(k, "") for k in ["rank","score","bucket","company","naics","city","address","zip","source"]})

    # write other-vertical
    ov_path = os.path.join(args.outdir, f"{today}_grader_other_vertical.csv")
    with open(ov_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["company","naics","city","suspected_vertical","source"])
        w.writeheader()
        for r in other:
            w.writerow({"company":r["company"],"naics":r["naics"],"city":r["city"],
                        "suspected_vertical":r["vertical"],"source":r["source"]})

    # discard log
    dl_path = os.path.join(args.outdir, f"{today}_grader_discard_log.csv")
    with open(dl_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["company","naics","city","source"])
        w.writeheader()
        for r in discard:
            w.writerow({"company":r["company"],"naics":r["naics"],"city":r["city"],"source":r["source"]})

    # other-vertical breakdown
    from collections import Counter
    ov_types = Counter(r["vertical"] for r in other)

    # summary
    sm_path = os.path.join(args.outdir, f"{today}_grader_summary.md")
    with open(sm_path, "w", encoding="utf-8") as f:
        f.write(f"# Grader Summary — {today}\n\n")
        f.write(f"- Input: `{args.infile}`\n")
        f.write(f"- Rows in (raw): {len(rows)}\n")
        f.write(f"- Distinct companies (after dedupe): {len(seen)}\n\n")
        f.write(f"## Flatbed pile (the map for the Researcher)\n")
        f.write(f"- FLATBED-YES: {len(yes)}\n")
        f.write(f"- FLATBED-UNSURE: {len(unsure)}\n")
        f.write(f"- Total flatbed (ranked): {len(flatbed)}\n\n")
        f.write(f"## Other-vertical (seed for future directories)\n")
        for v, n in ov_types.most_common():
            f.write(f"- {v}: {n}\n")
        f.write(f"- Total other-vertical: {len(other)}\n\n")
        f.write(f"## Discard (non-shippers, audit log)\n- DISCARD: {len(discard)}\n\n")
        f.write(f"## Top 25 flatbed-yes (Researcher's first slice candidates)\n")
        for r in flatbed[:25]:
            f.write(f"  {r['rank']:>3}. [{r['score']}] {r['company'][:48]}  ({r['naics'][:12]})\n")

    print(f"Grader complete. {len(rows)} rows -> {len(seen)} companies")
    print(f"  FLATBED-YES: {len(yes)} | UNSURE: {len(unsure)} | OTHER: {len(other)} | DISCARD: {len(discard)}")
    print(f"  Other-vertical breakdown: {dict(ov_types)}")
    print(f"\nOutputs in {args.outdir}/:")
    print(f"  {os.path.basename(fb_path)}  (ranked flatbed — the map)")
    print(f"  {os.path.basename(ov_path)}  (other-vertical seed)")
    print(f"  {os.path.basename(sm_path)}  (summary)")
    print(f"  {os.path.basename(dl_path)}  (discard audit)")
    print(f"\nNext: operator points the Researcher at a slice, e.g. ranks 1-50 or 100-150.")


if __name__ == "__main__":
    main()
