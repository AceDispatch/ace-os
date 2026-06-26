import csv, sys, re, glob, os, html
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EQ = {"flatbed","van","reefer","dump","tanker","heavy-haul","hopper","mixed","unknown"}
def norm(s): return re.sub(r"[^a-z0-9]+","",(s or "").lower())

def equip_class(vertical, flatbed_fit):
    v=(vertical or "").strip().lower()
    if v in EQ and v!="unknown": return v
    for k in ("flatbed","reefer","tanker","dump","hopper"):
        if k in v: return k
    if "heavy" in v: return "heavy-haul"
    if "van" in v or "ltl" in v: return "van"
    if flatbed_fit in ("yes","unsure"): return "flatbed"
    return "unknown"

VOL=re.compile(r"\btruckload|\bTL\b|\d+\s*TL/|truckloads|tons?/yr|tons per year|loads?/(?:wk|week|day)|\d+\+?\s*truck",re.I)
def ftl(flatbed_fit, flag, ships, lanes, notes, stage):
    blob=" ".join([ships or "",lanes or "",notes or ""])
    f=(flag or "").upper()
    if "DEFUNCT" in f or "defunct" in (notes or "").lower(): return "NO","closed/defunct"
    if VOL.search(blob): return "CONFIRMED","explicit truckload/volume signal in research"
    if stage=="RESEARCHED" and flatbed_fit in ("yes",): return "LIKELY","manufacturer ships truckloads (equipment-confirmed)"
    return "UNCONFIRMED",""

def ease(door_status, door_type, effort_tier, flag):
    dt=(door_type or "").lower(); f=(flag or "").upper()
    if "CAPTIVE_ONLY" in f or "captive-only" in dt: return "captive-only"
    if door_status=="GREEN":
        if any(k in dt for k in ("portal","signup","sign-up","rmis","mycarrierpackets","cmp","carrier-setup","carrier setup","hired hauler","driver-application","application","online")): return "self-serve-portal"
        return "direct-contact"
    try: t=int(effort_tier)
    except: t=0
    return {1:"self-serve-portal",2:"direct-contact",3:"navigate-in",4:"none"}.get(t,"unknown")

def door_status_of(r):
    ds=(r.get("door_status") or "").strip().upper()
    if ds in ("GREEN","UNCONFIRMED"): return ds
    dt=(r.get("door_type") or "").strip()
    try: t=int(r.get("effort_tier") or 0)
    except: t=0
    if dt and dt.lower() not in ("","none","n/a") and t in (1,2): return "GREEN"
    return "UNCONFIRMED"

OUT_COLS=["shipper_id","company_name","parent_company","address","city","county","state","zip","naics",
"equipment_class","equipment_confidence","ftl_status","ftl_evidence","ships","outbound_lanes","volume_signal",
"door_status","door_type","onboarding_ease","onboarding_url","effort_tier","phone","email","website","contact_grade",
"research_stage","flags","region","source","notes"]

rows=[]
RESEARCHED=[
 ("outbox/ca_sacramento/2026-06-23_shipper_registry_sac_FULL_288.csv","sacramento-CA"),
 ("outbox/shreveport/2026-06-24_shipper_registry_shreveport.csv","shreveport-LA"),
 ("outbox/blytheville/2026-06-25_shipper_registry_blytheville.csv","blytheville-AR"),
 ("outbox/se_campaign/memphis/2026-06-25_shipper_registry_memphis.csv","memphis-TNMSAR"),
 ("outbox/2026-06-17_shipper_registry_LA-MS-AL.csv","la-ms-al-w1"),
 ("outbox/2026-06-17_shipper_registry_LA-MS-AL_batch2.csv","la-ms-al-w2"),
 ("outbox/research_campaign/results/shipper_registry.csv","ca-campaign"),
 ("outbox/2026-06-25_netx_memphis_lanehunt.csv","netx-lanehunt-TX"),
]
for f,region in RESEARCHED:
    if not os.path.exists(f): continue
    for r in csv.DictReader(open(f,encoding="utf-8",errors="replace")):
        r={k:(html.unescape(v) if isinstance(v,str) else v) for k,v in r.items()}
        ff=(r.get("flatbed_fit") or "").strip().lower()
        ec=equip_class(r.get("vertical"), ff)
        ds=door_status_of(r)
        fs,fe=ftl(ff, r.get("flag"), r.get("ships"), r.get("outbound_lanes"), r.get("notes"), "RESEARCHED")
        rows.append({
         "company_name":(r.get("company_name") or "").strip(),"parent_company":r.get("parent_company",""),
         "address":r.get("address",""),"city":r.get("city",""),"county":"","state":(r.get("state") or "").upper(),"zip":r.get("zip",""),
         "naics":r.get("naics",""),"equipment_class":ec,"equipment_confidence":"high" if ff=="yes" else "med",
         "ftl_status":fs,"ftl_evidence":fe,"ships":r.get("ships",""),"outbound_lanes":r.get("outbound_lanes",""),"volume_signal":"",
         "door_status":ds,"door_type":r.get("door_type",""),"onboarding_ease":ease(ds,r.get("door_type"),r.get("effort_tier"),r.get("flag")),
         "onboarding_url":r.get("onboarding_url",""),"effort_tier":r.get("effort_tier",""),"phone":r.get("phone",""),"email":r.get("email",""),
         "website":r.get("website",""),"contact_grade":r.get("contact_grade",""),"research_stage":"RESEARCHED","flags":r.get("flag",""),
         "region":region,"source":r.get("source","EPA_FRS"),"notes":(r.get("notes","") or "")[:400]})

# graded seed bank (other-vertical) -> stage GRADED
SEED=[f for f in glob.glob("outbox/**/*_grader_other_vertical.csv",recursive=True) if "test_AL" not in f]
seedn=0
for f in SEED:
    for r in csv.DictReader(open(f,encoding="utf-8",errors="replace")):
        sv=(r.get("suspected_vertical") or "").strip().lower()
        ec=sv if sv in EQ else (equip_class(sv,"") )
        rows.append({"company_name":(r.get("company") or "").strip(),"parent_company":"","address":"","city":r.get("city",""),
         "county":"","state":"","zip":"","naics":r.get("naics",""),"equipment_class":ec or "unknown","equipment_confidence":"low",
         "ftl_status":"UNCONFIRMED","ftl_evidence":"","ships":"","outbound_lanes":"","volume_signal":"","door_status":"","door_type":"",
         "onboarding_ease":"unknown","onboarding_url":"","effort_tier":"","phone":"","email":"","website":"","contact_grade":"",
         "research_stage":"GRADED","flags":"","region":os.path.basename(f).split("_grader")[0],"source":r.get("source","EPA_FRS"),"notes":""})
        seedn+=1

# dedup: RESEARCHED beats GRADED; key normalized name+state(+city)
rows.sort(key=lambda r:0 if r["research_stage"]=="RESEARCHED" else 1)
seen={}; out=[]
for r in rows:
    k=(norm(r["company_name"]), (r["state"] or "").upper(), norm(r["city"]))
    if not r["company_name"]: continue
    if k in seen: continue
    seen[k]=1; out.append(r)
for i,r in enumerate(out,1): r["shipper_id"]=f"S{i:06d}"

dst="outbox/shipper_db/shippers_master.csv"
with open(dst,"w",encoding="utf-8",newline="") as g:
    w=csv.DictWriter(g,fieldnames=OUT_COLS); w.writeheader()
    for r in out: w.writerow({c:r.get(c,"") for c in OUT_COLS})

R=[r for r in out if r["research_stage"]=="RESEARCHED"]; G=[r for r in out if r["research_stage"]=="GRADED"]
print(f"MASTER DB: {dst}  ({len(out)} unique shippers; researched={len(R)}, graded-seed={len(G)})")
print("\nBy equipment_class:",dict(Counter(r['equipment_class'] for r in out).most_common()))
print("\n=== RESEARCHED tier ===")
print("  equipment_class:",dict(Counter(r['equipment_class'] for r in R).most_common()))
print("  ftl_status:",dict(Counter(r['ftl_status'] for r in R)))
print("  door_status:",dict(Counter(r['door_status'] for r in R)))
print("  onboarding_ease:",dict(Counter(r['onboarding_ease'] for r in R).most_common()))
print("\n*** THE TARGET LIST: FTL(confirmed/likely) + GREEN door, researched ***")
tgt=[r for r in R if r['door_status']=="GREEN" and r['ftl_status'] in ("CONFIRMED","LIKELY")]
print(f"  {len(tgt)} shippers meet the bar right now. By ease:",dict(Counter(r['onboarding_ease'] for r in tgt)))
PYEOF=None
