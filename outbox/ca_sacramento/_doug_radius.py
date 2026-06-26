import csv, sys, math
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DOUG = (33.1901, -94.3496)
def hav(a, b):
    R = 3958.8
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    d = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(d))

C = {
("LA","Shreveport"):(32.51,-93.75),("LA","Bossier City"):(32.52,-93.66),("LA","Haughton"):(32.53,-93.50),
("LA","Keithville"):(32.36,-93.86),("LA","Belcher"):(32.75,-93.84),("LA","Minden"):(32.62,-93.29),
("LA","Mansfield"):(32.04,-93.70),("LA","Coushatta"):(32.02,-93.34),("LA","Monroe"):(32.51,-92.12),
("LA","West Monroe"):(32.52,-92.15),("LA","Ruston"):(32.52,-92.64),("LA","Delhi"):(32.46,-91.49),
("LA","Oak Grove"):(32.86,-91.39),("LA","Winnfield"):(31.93,-92.64),("LA","Urania"):(31.86,-92.30),
("LA","Alexandria"):(31.31,-92.44),("LA","Leesville"):(31.14,-93.26),("LA","Forest Hill"):(31.04,-92.41),
("LA","Taylor"):(32.30,-92.55),("LA","Mansura"):(31.06,-92.05),("LA","Lemoyen"):(30.62,-91.86),
("LA","Baton Rouge"):(30.45,-91.19),("LA","New Orleans"):(29.95,-90.07),("LA","Houma"):(29.60,-90.72),
("LA","Lafayette"):(30.22,-92.02),("LA","Lake Charles"):(30.23,-93.22),("LA","Sulphur"):(30.24,-93.38),
("LA","New Iberia"):(30.00,-91.82),("LA","Thibodaux"):(29.79,-90.82),("LA","Morgan City"):(29.70,-91.21),
("LA","Hammond"):(30.50,-90.46),("LA","Slidell"):(30.28,-89.78),("LA","Mandeville"):(30.36,-90.07),
("LA","Kenner"):(30.00,-90.24),("LA","Metairie"):(30.00,-90.18),("LA","Harvey"):(29.90,-90.08),
("LA","Westwego"):(29.91,-90.14),("LA","Chalmette"):(29.94,-89.96),("LA","Belle Chasse"):(29.85,-89.99),
("LA","Violet"):(29.90,-89.90),("LA","St Bernard"):(29.86,-89.83),("LA","Reserve"):(30.05,-90.55),
("LA","Laplace"):(30.07,-90.48),("LA","Convent"):(30.02,-90.84),("LA","Gonzales"):(30.24,-90.92),
("LA","Donaldsonville"):(30.10,-90.99),("LA","Plaquemine"):(30.29,-91.24),("LA","Port Allen"):(30.45,-91.21),
("LA","Brusly"):(30.39,-91.25),("LA","Prairieville"):(30.30,-90.98),("LA","Saint Amant"):(30.21,-90.86),
("LA","Walker"):(30.49,-90.86),("LA","Denham Springs"):(30.49,-90.96),("LA","Greenwell Springs"):(30.55,-90.99),
("LA","Ponchatoula"):(30.44,-90.44),("LA","Saint Francisville"):(30.78,-91.38),("LA","Clinton"):(30.87,-91.01),
("LA","Greensburg"):(30.83,-90.68),("LA","Franklinton"):(30.85,-90.14),("LA","Amelia"):(29.67,-91.10),
("LA","Baldwin"):(29.84,-91.54),("LA","Centerville"):(29.76,-91.43),("LA","Breaux Bridge"):(30.27,-91.90),
("LA","Broussard"):(30.15,-91.96),("LA","Scott"):(30.24,-92.09),("LA","Church Point"):(30.40,-92.21),
("LA","Saint Martinville"):(30.13,-91.83),("LA","Bourg"):(29.55,-90.61),("LA","Lockport"):(29.65,-90.54),
("LA","Dequincy"):(30.45,-93.43),("LA","Harahan"):(29.94,-90.20),("LA","Jefferson"):(29.96,-90.15),
("MS","Greenville"):(33.41,-91.06),("MS","Rolling Fork"):(32.91,-90.88),("MS","Vicksburg"):(32.35,-90.88),
("MS","Natchez"):(31.56,-91.40),("MS","Indianola"):(33.45,-90.66),("MS","Hermanville"):(31.97,-90.83),
("MS","Yazoo"):(32.85,-90.41),("MS","Gloster"):(31.20,-91.01),("MS","Hazlehurst"):(31.86,-90.40),
("MS","Crystal Springs"):(31.99,-90.36),("MS","Brookhaven"):(31.58,-90.44),("MS","Magnolia"):(31.14,-90.46),
("MS","Mccomb"):(31.24,-90.45),("MS","Jackson"):(32.30,-90.18),("MS","Liberty"):(31.16,-90.81),
("TX","Texarkana"):(33.44,-94.04),("TX","Nash"):(33.44,-94.13),("TX","New Boston"):(33.46,-94.42),
("TX","Atlanta"):(33.11,-94.16),("TX","Avinger"):(32.90,-94.56),("TX","Hughes Springs"):(32.99,-94.62),
("TX","Daingerfield"):(33.03,-94.72),("TX","Lone Star"):(32.94,-94.71),("TX","Clarksville"):(33.61,-95.05),
("TX","Paris"):(33.66,-95.56),("TX","Mount Pleasant"):(33.16,-94.97),("TX","Saltillo"):(33.16,-95.37),
("TX","Sulphur Springs"):(33.14,-95.60),("TX","Jefferson"):(32.76,-94.35),("TX","Marshall"):(32.54,-94.37),
("TX","Scottsville"):(32.54,-94.25),("TX","Longview"):(32.50,-94.74),("TX","White Oak"):(32.53,-94.86),
("TX","Kilgore"):(32.39,-94.87),("TX","Henderson"):(32.15,-94.80),("TX","Tyler"):(32.35,-95.30),
("TX","Whitehouse"):(32.22,-95.22),("TX","Van"):(32.52,-95.64),("TX","Center"):(31.80,-94.18),
("TX","Timpson"):(31.90,-94.40),("TX","Nacogdoches"):(31.60,-94.65),("TX","Lufkin"):(31.34,-94.73),
("TX","Diboll"):(31.19,-94.78),("TX","San Augustine"):(31.53,-94.11),("TX","Hemphill"):(31.34,-93.85),
("TX","Pineland"):(31.25,-93.97),("TX","Woden"):(31.74,-94.55),("TX","Pollok"):(31.42,-94.83),
("TX","Jacksonville"):(31.96,-95.27),("TX","Mount Enterprise"):(31.92,-94.69),("TX","Palestine"):(31.76,-95.63),
("TX","Crockett"):(31.32,-95.46),("TX","Trinity"):(30.95,-95.37),("TX","Livingston"):(30.71,-94.93),
("TX","Athens"):(32.20,-95.86),("TX","Mabank"):(32.36,-96.10),("TX","Buffalo"):(31.46,-96.06),
("TX","Jewett"):(31.36,-96.14),("TX","Corsicana"):(32.10,-96.47),("TX","Ennis"):(32.33,-96.63),
("TX","Waxahachie"):(32.39,-96.85),("TX","Kaufman"):(32.59,-96.31),("TX","Terrell"):(32.74,-96.27),
("TX","Mesquite"):(32.77,-96.60),("TX","Dallas"):(32.78,-96.80),("TX","Garland"):(32.91,-96.64),
("TX","Rockwall"):(32.93,-96.46),("TX","Greenville"):(33.14,-96.11),("TX","Caddo Mills"):(33.07,-96.22),
("TX","Wylie"):(33.02,-96.54),("TX","Melissa"):(33.29,-96.57),("TX","Anna"):(33.35,-96.55),
("TX","Farmersville"):(33.16,-96.36),("TX","Trenton"):(33.43,-96.34),("TX","Sherman"):(33.64,-96.61),
("TX","Denison"):(33.76,-96.54),("TX","Whitesboro"):(33.66,-96.91),("TX","Gainesville"):(33.63,-97.13),
("TX","Muenster"):(33.65,-97.37),("TX","Lancaster"):(32.59,-96.76),("TX","Cedar Hill"):(32.59,-96.96),
("TX","Midlothian"):(32.48,-96.99),("TX","Grand Prairie"):(32.75,-96.99),("TX","Arlington"):(32.74,-97.11),
("TX","Irving"):(32.81,-96.95),("TX","Carrollton"):(32.99,-96.90),("TX","Farmers Branch"):(32.93,-96.89),
("TX","Richardson"):(32.95,-96.73),("TX","Allen"):(33.10,-96.67),("TX","Frisco"):(33.15,-96.82),
("TX","Lewisville"):(33.05,-96.99),("TX","Denton"):(33.21,-97.13),("TX","Roanoke"):(33.00,-97.23),
("TX","Keller"):(32.93,-97.25),("TX","Southlake"):(32.94,-97.13),("TX","Haslet"):(32.97,-97.35),
("TX","Haltom City"):(32.80,-97.27),("TX","North Richland Hills"):(32.83,-97.23),("TX","Hurst"):(32.82,-97.18),
("TX","Euless"):(32.84,-97.08),("TX","Fort Worth"):(32.76,-97.33),("TX","Saginaw"):(32.86,-97.36),
("TX","Rhome"):(33.05,-97.47),("TX","Newark"):(33.00,-97.48),("TX","Bridgeport"):(33.21,-97.76),
("TX","Burleson"):(32.54,-97.32),("TX","Crowley"):(32.58,-97.36),("TX","Cleburne"):(32.35,-97.39),
("TX","Grandview"):(32.27,-97.18),("TX","Alvarado"):(32.41,-97.21),("TX","Mansfield"):(32.56,-97.14),
("TX","Palmer"):(32.43,-96.67),("TX","Hillsboro"):(32.01,-97.13),("TX","Hewitt"):(31.46,-97.20),
("TX","Waco"):(31.55,-97.13),("TX","Mexia"):(31.68,-96.48),("TX","Huntsville"):(30.72,-95.55),
("TX","Willis"):(30.42,-95.48),("TX","Conroe"):(30.31,-95.46),("TX","Splendora"):(30.23,-95.16),
("TX","Cleveland"):(30.34,-95.09),("TX","Weatherford"):(32.76,-97.80),
}
def dist(st, ci):
    p = C.get((st, ci.strip().title()))
    return hav(DOUG, p) if p else None

res = ["outbox/2026-06-17_shipper_registry_LA-MS-AL.csv", "outbox/2026-06-17_shipper_registry_LA-MS-AL_batch2.csv"]
inr = []; uncoded = Counter()
for f in res:
    for r in csv.DictReader(open(f, encoding="utf-8", errors="replace")):
        st = (r.get("state") or "").strip().upper(); ci = (r.get("city") or "").strip().title()
        if st == "AL": continue
        d = dist(st, ci)
        if d is None: uncoded[(st, ci)] += 1; continue
        if d <= 200: r["_mi"] = round(d); inr.append(r)
def door(r):
    dt = (r.get("door_type") or "").strip()
    return dt and dt.lower() not in ("", "none", "n/a")
print(f"=== RESEARCHED (LA/MS) shippers within 200 mi: {len(inr)}  (GREEN doors: {sum(1 for r in inr if door(r))}) ===")
inr.sort(key=lambda r: r["_mi"])
for r in inr:
    g = "GREEN" if door(r) else "  -  "
    print(f"  {r['_mi']:>3}mi {r['state']} {r['city']:<13} T{r.get('effort_tier','?')} {g} {r['company_name'][:40]:40} | {r.get('phone','')}")
if uncoded:
    print("  [uncoded LA/MS cities -> treated OUT]:", dict(uncoded))

txin = []; txunc = Counter()
for r in csv.DictReader(open("outbox/2026-06-14_grader_flatbed_ranked.csv", encoding="utf-8", errors="replace")):
    ci = r["city"].strip().title(); d = dist("TX", ci)
    if d is None: txunc[ci] += 1; continue
    if d <= 200: r["_mi"] = round(d); txin.append(r)
print(f"\n=== TX GRADED candidates within 200 mi (NOT door-researched): {len(txin)} ===")
print("  by score:", dict(sorted(Counter(r["score"] for r in txin).items(), key=lambda x: -int(x[0]))))
print("  --- score-50 in range (strongest graded; doors unverified) ---")
for r in sorted([x for x in txin if x["score"] == "50"], key=lambda x: x["_mi"]):
    print(f"    {r['_mi']:>3}mi {r['company'][:38]:38} | {r['naics']:<12} | {r['city']}")

# write combined in-range CSV (researched LA/MS + TX graded)
out = "outbox/ca_sacramento/2026-06-23_within200mi_douglassville.csv"
cols = ["miles","data","state","city","company","score_or_tier","door_type","onboarding_url","phone","naics","notes"]
with open(out, "w", encoding="utf-8", newline="") as g:
    w = csv.writer(g); w.writerow(cols)
    for r in sorted(inr, key=lambda r: r["_mi"]):
        w.writerow([r["_mi"],"researched",r["state"],r["city"],r["company_name"],"T"+str(r.get("effort_tier","")),
                    r.get("door_type",""),r.get("onboarding_url",""),r.get("phone",""),r.get("naics",""),(r.get("notes","") or "")[:200]])
    for r in sorted(txin, key=lambda r: r["_mi"]):
        w.writerow([r["_mi"],"TX-graded-only","TX",r["city"],r["company"],"score "+r["score"],"","","",r["naics"],""])
print(f"\nWritten: {out}  ({len(inr)} researched + {len(txin)} TX graded rows)")
