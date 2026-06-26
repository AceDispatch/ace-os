#!/usr/bin/env python3
"""pipeline/classify.py — the CLASSIFY stage: sort EVERY company by equipment (multi-vertical).
Mechanical, no web. Sort-don't-discard. Supersedes the flatbed-only grader for the Supabase era.
Includes the Memphis 'sheet-metal van-trap' fix (332321/332322 + HVAC/vent/duct -> van).

Usage: python pipeline/classify.py --in roster.csv --out classified.csv
"""
import csv, sys, re, argparse
from collections import Counter

TIER1 = set("331110 331221 331222 331210 332312 332311 332313 332321 332322 332323 332420 332910 332911 332919 332996 327320 327331 327332 327390 327991 321113 321114 321214 321920 333120 333132 336611 332111".split())
TIER2 = set("331318 331511 331513 332439 332618 327992 327120 327310 321211 321212 321912 321918 321991 321992 333111 333131 333922 333923 333924 336212 336510 332112 332119 332510 332999 332410".split())
FB_STRONG = ["STEEL","IRON WORK","IRONWORK","FABRICAT","STRUCTURAL","REBAR","PIPE","TUBE","PRECAST","CULVERT","BEAM","TRUSS","LUMBER","FOUNDRY","FORGING","EXTRUSION","METAL BUILDING","BUILDING SYSTEMS","TANK","BRICK","CONCRETE PRODUCT","MILLWORK","WIRE PRODUCTS","COIL"]
FB_MED = ["MANUFACTURING","MFG","METAL","WELDING","FENCE","PANEL","PALLET","WOODWORK","MOULDING","MOLDING","INDUSTRIES","PRODUCTS","SUPPLY","MACHINE","EQUIPMENT","CASTING"]
VANTRAP_NAICS = {"332321","332322"}
VANTRAP_NAME = re.compile(r"BLOW PIPE|\bLOUVER|\bDUCT\b|\bHVAC\b|AIR HANDL|\bDAMPER\b|VENTILAT|\bVENT\b|SPRAY BOOTH", re.I)
VANTRAP_SOFT = ["SHEET METAL", "PLASTIC"]
DUMP = ["AGGREGATE","SAND","GRAVEL","READY MIX","READY-MIX","READYMIX","CRUSHED STONE","QUARRY","CEMENT","CEMEX"]
PRECAST_RESCUE = ["PRECAST","PIPE","CULVERT","PRODUCT","BLOCK","VAULT","BARRIER","SEPTIC","PAVER","BRICK","TILE"]
TANKER = ["CHEMICAL","LIQUID","PROPANE"," FUEL","ASPHALT"," LPG"," LNG","PETROLEUM"]
TANK_MAKER = ["TANK MANUFACTUR","TANK & MANUFACTUR","TANK FAB","TANK WORKS","TANK SYSTEM","TANK CO","TANK LINING","TANK & EQUIP","TANK AND EQUIP","VESSEL","BOILER"]
HEAVY = ["CRANE","TRANSFORMER","TURBINE"]
VAN = ["POWDER","ATOMIZED","PACKAGING"," DRUM","TOTE","ENCLOSURE","CABINET","CORRUGAT","FOOD CONTAINER","LABEL","PRINTING"]
EXTRACT_NAICS = {"211111","211120"}
EXTRACT = re.compile(r"\bWELL\b|TANK BATTER|PIPELINE|COMPRESSOR STATION|PRODUCTION FACILITY|WELLSITE|DEHYDRAT|GATHERING|\bDRILLING\b|^SCHLUMBERGER|\bFRAC\b|FLOWBACK|GAS PROCESSING|CENTRAL FACILITY", re.I)
DISCARD = re.compile(r"PLATING|ANODIZ|GALVANIZ|POWDER COAT|ELECTROPLAT|MACHINE SHOP|TOOL & DIE|TOOL AND DIE|\bREPAIR\b|HEAT TREAT|LABORATOR|\bTESTING\b|INSPECTION|DENTAL|JEWELR|RECYCL|SALVAGE|\bSCRAP\b|\bWASTE\b|DISPOSAL|CAR WASH|AUTO BODY|AUTO SALES|\bFUNERAL\b", re.I)

def naics_list(s): return [n.strip()[:6] for n in (s or "").replace(";", ",").split(",") if n.strip()]
def has(name, sigs): return any(s in name for s in sigs)

def classify_one(name, naics):
    u = (name or "").upper()
    nl = naics_list(naics); fbset = set(nl); p = nl[0] if nl else ""
    # 1. extraction / non-shipper (spare oilfield EQUIPMENT makers)
    if p in EXTRACT_NAICS or EXTRACT.search(u):
        maker = p == "333132" and has(u, ["MANUFACTUR", "MFG", "EQUIPMENT", "WELLHEAD", "VALVE", "PUMP", "FABRICAT"]) and not EXTRACT.search(u)
        if not maker:
            return ("unknown", "low", 0, "extraction/non-shipper")
    # 2. service / finishing (no flatbed signal)
    if DISCARD.search(u) and not has(u, FB_STRONG):
        return ("unknown", "low", 0, "service/finishing")
    # 3. van-trap (the Memphis fix): unambiguous HVAC/duct NAME -> van regardless of NAICS;
    #    sheet-metal/plastic NAICS + softer name -> van.
    if VANTRAP_NAME.search(u):
        return ("van", "high", 0, "van(hvac/duct)")
    if (fbset & VANTRAP_NAICS) and has(u, VANTRAP_SOFT):
        return ("van", "med", 0, "van-trap(sheet-metal)")
    # 4. dump: loose material — precast PRODUCTS spared
    if (has(u, DUMP) or p == "327320") and not has(u, PRECAST_RESCUE):
        return ("dump", "high" if has(u, DUMP) else "med", 0, "")
    # 5. van: light goods
    if has(u, VAN):
        return ("van", "med", 0, "")
    # 6. tanker: liquids — tank MAKERS spared
    if has(u, TANKER) and not has(u, TANK_MAKER):
        return ("tanker", "med", 0, "")
    # 7. heavy-haul
    if has(u, HEAVY):
        return ("heavy-haul", "med", 0, "")
    # 8. flatbed: NAICS tier + name signal
    base = 30 if (fbset & TIER1) else (20 if (fbset & TIER2) else 8)
    score = base + (20 if has(u, FB_STRONG) else (10 if has(u, FB_MED) else 0))
    if (fbset & TIER1) or (fbset & TIER2) or has(u, FB_STRONG):
        conf = "high" if ((fbset & TIER1) and has(u, FB_STRONG)) else "med"
        return ("flatbed", conf, score, "")
    # 9. unknown remainder
    return ("unknown", "low", score, "")

def classify_rows(rows):
    seen = {}; out = []
    for r in rows:
        name = (r.get("name") or r.get("company") or "").strip()
        if not name: continue
        key = (re.sub(r"[^a-z0-9]+", "", name.lower()), (r.get("state") or "").upper(), (r.get("city") or "").strip().lower())
        if key in seen: continue
        seen[key] = 1
        ec, conf, score, flags = classify_one(name, r.get("naics"))
        out.append({"company": name, "naics": r.get("naics", ""), "city": (r.get("city") or "").title(),
                    "state": (r.get("state") or "").upper(), "address": r.get("address", ""), "zip": r.get("zip", ""),
                    "equipment_class": ec, "equipment_confidence": conf, "flatbed_score": score,
                    "ftl_signal": "unknown" if ec == "unknown" else "likely", "flags": flags,
                    "source": r.get("source", "EPA_FRS")})
    out.sort(key=lambda x: (x["equipment_class"] != "flatbed", -x["flatbed_score"]))
    return out

COLS = ["company", "naics", "city", "state", "address", "zip", "equipment_class", "equipment_confidence", "flatbed_score", "ftl_signal", "flags", "source"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.inp, encoding="utf-8", errors="replace")))
    cl = classify_rows(rows)
    with open(a.out, "w", encoding="utf-8", newline="") as g:
        w = csv.DictWriter(g, fieldnames=COLS); w.writeheader()
        for r in cl: w.writerow(r)
    print(f"classified {len(cl)} -> {a.out}")
    print("by equipment_class:", dict(Counter(r["equipment_class"] for r in cl).most_common()))
