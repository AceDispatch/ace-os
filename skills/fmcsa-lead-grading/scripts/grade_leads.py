#!/usr/bin/env python3
"""
FMCSA Lead Grading Engine v4 - Ace Dispatch ("Perfect-Only" edition)
Philosophy: carrier supply is effectively unlimited; rep time is scarce.
PRECISION over recall. When in doubt, DISCARD. Import only perfect leads.

v4 changes (2026-06-19) — proven out against the live FMCSA datasets:

  1. VEHICLE-TYPE GATE (new HARD gate). A lead must operate a TRACTOR
     (OWNTRACT / TRMTRACT / TRPTRACT > 0). This concretely rules out
     straight/box trucks (OWNTRUCK), hotshots (light pickups, never a Class-8
     tractor), sprinter/cargo vans, and passenger vans/buses. The CRGO_* cargo
     flags do NOT catch these: ~28-29% of "general freight" interstate 1x1
     carriers are actually box trucks. FMCSA never records trailer BODY type, so
     the cargo flags are only an *inference* of flatbed/reefer/dry-van (reefer
     strong, flatbed moderate, dry-van ambiguous) and are kept ONLY for scoring.
     The gate is enforced when census vehicle-count columns are present in the CSV.

  2. TRUE AUTHORITY AGE. If the input carries TRUE_AUTHORITY_AGE_DAYS (or
     TRUE_AUTHORITY_GRANT_DATE) from the AuthHist enrichment (scripts/extract_leads.py),
     age is computed from the real operating-authority grant date. ADD_DATE is a
     FALLBACK only: it mis-ages ~37% of verifiable leads because an MCS-150 update
     resets it (a 26-year-old carrier can look 46 days old). Enrichment is upstream
     by design — this grader stays offline.

  3. ACTIVE OPERATING AUTHORITY. DOCKET1_STATUS_CODE must be 'A' when present.
     A carrier RECORD being active (STATUS_CODE='A') is not the same as the
     operating AUTHORITY being active.
"""
import csv, argparse
from datetime import date
AS_OF = date.today()

STRONG_TRUCKING = ['trucking','truck','truckline','truckin','transport','transportation','freight','freightways','freighting','logistics','logistic','hauling','haul','carrier','carriers','carrying','express','expedite','expediting','dispatch','distribution','cartage','intermodal','drayage','flatbed','reefer','refrigerated','overland','linehaul','otr']
MODERATE_TRUCKING = ['transit','shipping','delivery','deliveries','movers','moving','fleet','lines','line','forwarding','logix','trans','xpress','cargo']
# SOFT_NEGATIVE = ambiguous holding-co names, or real-but-off-profile freight niches
# (tanker / drayage / car-hauling). Post-tractor-gate these DOWN-RANK (apply SOFT_PENALTY);
# they do NOT discard. Keep tokens specific enough that they rarely co-occur with a real
# trucking word, since the penalty now stacks on top of any Strong/Moderate signal.
SOFT_NEGATIVE = ['storage','warehouse','auto','autos','motors','salvage','scrap','recycling','rental','leasing','sales','mechanic','repair',
    # 2026-06-24 — name-gap leads from the FL/VA/LA import: verified tractors but off-profile/ambiguous
    # names. Soft = down-rank (the tractor gate already proved equipment), not a kill.
    'auto transport','auto hauling','car hauling','car hauler','car carrier','petroleum','container','environmental',
    'consultation','consulting','trading','products','shopping','technologies',' tech ','charging','import export','heavy equipment','equips','energy']
SOFT_PENALTY = -15   # down-rank only — the tractor gate already removed the equipment risk
# HARD_NEGATIVE = a DIFFERENT-INDUSTRY business that happens to own a tractor (will never buy
# managed dispatch). This is the ONLY thing we hard-negate on name; reject overrides any trucking word.
HARD_NEGATIVE = ['construction','contracting','contractor','builders','building','landscaping','landscape','lawn','grounds','tree service','nursery','farming','farm','farms','ranch','agriculture','agri','dairy','plumbing','electric','electrical','hvac','mechanical','roofing','concrete','paving','asphalt','painting','welding','fencing','drilling','excavat','demolition','masonry','flooring','remodel','church','ministry','ministries','mission','temple','parish','school','academy','university','college','education','daycare','government','county of','city of','municipal','township','district','cleaning','janitorial','maid','catering','restaurant','cafe','mining','quarry','oilfield','oil field','towing','wrecker','medical','hospital','clinic','pharmacy','dental','funeral','disposal','septic','hauloff',
    # 2026-06-19 — non-freight trades found auditing Anthony Smart's book (roof/coatings et al.).
    'roof','coating',' coat ','sealcoat','seal coat',
    'automotive','motorsport','powersport','dealership',
    'handyman','remodeling','renovation','restoration','drywall','stucco','insulation','glazing','gutter','siding','cabinet','countertop',
    'detailing','car wash','carwash','pressure wash','power wash',
    'salon','realty','realtor','mortgage','feedlot','pest control','exterminat',
    # 2026-06-24 — other-industry businesses with a tractor, found in the FL/VA/LA import.
    'appliance','tile']

def name_score(legal_name):
    n = ' ' + legal_name.lower().replace(',',' ').replace('.',' ') + ' '
    # HARD: a different-industry business that happens to own a tractor -> discard outright.
    for kw in HARD_NEGATIVE:
        if kw in n: return (-1000,'HARD NEGATIVE',kw)
    # Base trucking signal.
    base,sig,hit = 0,'Neutral',''
    for kw in STRONG_TRUCKING:
        if (' '+kw+' ') in n or n.strip().endswith(kw):
            base,sig,hit = 15,'Strong',kw; break
    if base==0:
        for kw in MODERATE_TRUCKING:
            if (' '+kw+' ') in n:
                base,sig,hit = 8,'Moderate',kw; break
    # SOFT: ambiguous / off-profile-but-real freight -> DOWN-RANK on top of the trucking
    # signal (never discard). Checked AFTER the base so a soft token penalizes even a name
    # that also carries a trucking word (e.g. "...TRUCK... REPAIR").
    for kw in SOFT_NEGATIVE:
        if kw in n:
            label = (sig+'+SoftNeg') if base else 'Soft-Neg'
            return (base+SOFT_PENALTY, label, (hit+'+'+kw.strip() if hit else kw.strip()))
    return (base,sig,hit)

EQUIP_DISCARD_FLAGS = {'CRGO_PASSENGERS':'Passengers','CRGO_LIQGAS':'Liquid/Gas (tanker)','CRGO_CHEM':'Chemicals','CRGO_OILFIELD':'Oilfield/Hotshot','CRGO_USMAIL':'US Mail','CRGO_LIVESTOCK':'Livestock','CRGO_GARBAGE':'Garbage','CRGO_DRIVETOW':'Drive/Tow-away','CRGO_MOBILEHOME':'Mobile Homes','CRGO_WATERWELL':'Water Well','CRGO_COALCOKE':'Coal/Coke'}
FLATBED_FLAGS = ['CRGO_METALSHEET','CRGO_BLDGMAT','CRGO_MACHLRG','CRGO_LOGPOLE','CRGO_CONSTRUCT']
REEFER_FLAGS  = ['CRGO_COLDFOOD','CRGO_PRODUCE','CRGO_MEAT','CRGO_BEVERAGES']
DRYVAN_FLAGS  = ['CRGO_GENFREIGHT','CRGO_PAPERPROD','CRGO_DRYBULK','CRGO_FARMSUPP']

# --- Vehicle TYPE (not commodity). Census owned/leased counts. ---
# A real tractor-trailer carrier owns or leases a TRACTOR. OWNTRUCK = straight/box
# truck. (*VAN / *COACH / *BUS / *LIMO = passenger and are excluded upstream.)
TRACTOR_FLAGS = ['OWNTRACT','TRMTRACT','TRPTRACT']
VEHICLE_COLS  = TRACTOR_FLAGS + ['OWNTRUCK','TRMTRUCK','TRPTRUCK']

def flag(row,name): return row.get(name,'').strip().upper()=='X'

def has_tractor(row):
    for f in TRACTOR_FLAGS:
        v = row.get(f,'').strip()
        if v and v not in ('0','0.0'): return True
    return False

def classify_equipment(row):
    """Cargo-INFERRED body type, used for SCORING only (FMCSA does not record
    trailer body type; this is commodity inference, not equipment truth)."""
    for fld,reason in EQUIP_DISCARD_FLAGS.items():
        if flag(row,fld): return ('DISCARD',0,reason)
    has_flat=any(flag(row,f) for f in FLATBED_FLAGS)
    has_reef=any(flag(row,f) for f in REEFER_FLAGS)
    has_van =any(flag(row,f) for f in DRYVAN_FLAGS)
    types=[]
    if has_flat: types.append('Flatbed')
    if has_reef: types.append('Reefer')
    if has_van:  types.append('Dry Van')
    if not types: return ('DISCARD',0,'no cargo flagged')
    if has_flat and has_reef: score=40
    elif has_flat or has_reef: score=35 if has_van else 32
    else: score=12
    return (', '.join(types),score,None)

def parse_date(s):
    # Accepts YYYYMMDD, "YYYYMMDD HHMM", or YYYY-MM-DD (digits extracted).
    digs=''.join(ch for ch in s.strip().split(' ')[0] if ch.isdigit())
    if len(digs)<8: return None
    try: return date(int(digs[:4]),int(digs[4:6]),int(digs[6:8]))
    except ValueError: return None

def days_old(row):
    """(age_days, source). Prefer TRUE authority age (AuthHist); fall back to ADD_DATE proxy."""
    v=row.get('TRUE_AUTHORITY_AGE_DAYS','').strip()
    if v:
        try: return max(int(float(v)),0),'AuthHist (true)'
        except ValueError: pass
    g=parse_date(row.get('TRUE_AUTHORITY_GRANT_DATE',''))
    if g:
        d=(AS_OF-g).days; return (0 if d<0 else d),'AuthHist (true)'
    a=parse_date(row.get('ADD_DATE',''))
    if a:
        d=(AS_OF-a).days; return (0 if d<0 else d),'ADD_DATE (proxy)'
    return None,'none'

def to_int(v):
    try: return int(float(v))
    except (ValueError,TypeError): return 0

def age_score(d):
    if d<=30: return 15
    if d<=60: return 24
    if d<=105: return 30
    if d<=135: return 22
    if d<=180: return 12
    return 0

def fleet_score(pu):
    if 1<=pu<=3: return 10
    if 4<=pu<=6: return 5
    if 7<=pu<=15: return 2
    return 0

def interstate_intensity_score(row):
    s=0
    if to_int(row.get('INTERSTATE_BEYOND_100_MILES','0'))>0: s+=3
    if to_int(row.get('DRIVER_INTER_TOTAL','0'))>0: s+=2
    return min(s,5)

def tier_for(s):
    if s>=85: return 'P1'
    if s>=70: return 'P2'
    if s>=55: return 'P3'
    return 'P4'

def completeness_failures(row,add_ok,pu):
    m=[]
    if not (row.get('PHONE','').strip() or row.get('CELL_PHONE','').strip()): m.append('phone')
    if not add_ok: m.append('authority date')
    if pu<=0: m.append('power units')
    if not row.get('COMPANY_OFFICER_1','').strip(): m.append('officer')
    if not row.get('PHY_CITY','').strip(): m.append('city')
    if not row.get('PHY_STATE','').strip(): m.append('state')
    if not row.get('CLASSDEF','').strip(): m.append('classification')
    if not row.get('DOT_NUMBER','').strip(): m.append('DOT number')
    if not row.get('DOCKET1','').strip(): m.append('MC docket')
    return m

def grade(row,max_age,vehicle_gate):
    if row.get('CARRIER_OPERATION','').strip().upper()!='A': return None,'not interstate'
    if 'AUTHORIZED FOR HIRE' not in row.get('CLASSDEF','').upper(): return None,'not for-hire'
    if row.get('STATUS_CODE','').strip().upper()!='A': return None,'inactive'
    d1s=row.get('DOCKET1_STATUS_CODE','').strip().upper()
    if d1s and d1s!='A': return None,'authority not active'
    if row.get('PRIOR_REVOKE_FLAG','').strip().upper()=='Y': return None,'prior revocation'
    # VEHICLE-TYPE GATE: must run a tractor (rules out box trucks, hotshots, sprinters, vans).
    if vehicle_gate and not has_tractor(row): return None,'no tractor (box truck/hotshot/sprinter)'
    days,age_src=days_old(row)
    add_ok=days is not None
    if add_ok and days>max_age: return None,f'older than {max_age}d'
    ns,name_signal,name_kw=name_score(row.get('LEGAL_NAME',''))
    if ns==-1000: return None,f'name reject ({name_kw})'
    equip_label,equip_pts,eq_reason=classify_equipment(row)
    if equip_label=='DISCARD': return None,f'equipment ({eq_reason})'
    pu=to_int(row.get('POWER_UNITS','0'))
    missing=completeness_failures(row,add_ok,pu)
    if missing: return None,'incomplete: '+', '.join(missing)
    total=equip_pts+age_score(days)+ns+fleet_score(pu)+interstate_intensity_score(row)
    return {
        'Legal Name':row.get('LEGAL_NAME','').strip(),'DBA Name':row.get('DBA_NAME','').strip(),
        'DOT Number':row.get('DOT_NUMBER','').strip(),'MC (Docket1)':row.get('DOCKET1','').strip(),
        'Phone':row.get('PHONE','').strip(),'Cell Phone':row.get('CELL_PHONE','').strip(),
        'Email':row.get('EMAIL_ADDRESS','').strip(),'Street':row.get('PHY_STREET','').strip(),
        'City':row.get('PHY_CITY','').strip(),'State':row.get('PHY_STATE','').strip(),
        'Zip':row.get('PHY_ZIP','').strip(),'Authority Age (days)':days,'Age Source':age_src,
        'Add Date':row.get('ADD_DATE','').strip().split(' ')[0],
        'Vehicle Type':'Tractor','Equipment Types':equip_label,
        'Power Units':pu,'Officer':row.get('COMPANY_OFFICER_1','').strip(),
        'Classification':row.get('CLASSDEF','').strip(),'Operation':'Interstate',
        'Name Signal':name_signal,'Name Keyword':name_kw,'Lead Score':total,
        'Priority Tier':tier_for(total),
        'Score Breakdown':f"equip:{equip_pts} age:{age_score(days)} name:{ns:+d} fleet:{fleet_score(pu)} interstate:{interstate_intensity_score(row)}",
        'Source':'FMCSA Census',
    },None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('input'); ap.add_argument('--out',default='/mnt/user-data/outputs/graded_leads.csv')
    ap.add_argument('--top',type=int,default=0); ap.add_argument('--max-age',type=int,default=180)
    a=ap.parse_args()
    with open(a.input,newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f); rows=list(reader); fields=reader.fieldnames or []
    vehicle_gate = any(c in fields for c in VEHICLE_COLS)
    has_trueage  = ('TRUE_AUTHORITY_AGE_DAYS' in fields) or ('TRUE_AUTHORITY_GRANT_DATE' in fields)
    results,reasons=[],{}
    for row in rows:
        res,why=grade(row,a.max_age,vehicle_gate)
        if res: results.append(res)
        else:
            key=why.split(':')[0] if why.startswith('incomplete') else why
            reasons[key]=reasons.get(key,0)+1
    results.sort(key=lambda x:(x['Lead Score'],-x['Authority Age (days)']),reverse=True)
    for i,r in enumerate(results,1): r['Rank']=i
    fn=['Rank','Legal Name','DBA Name','DOT Number','MC (Docket1)','Phone','Cell Phone','Email','Street','City','State','Zip','Authority Age (days)','Age Source','Add Date','Vehicle Type','Equipment Types','Power Units','Officer','Classification','Operation','Name Signal','Name Keyword','Lead Score','Priority Tier','Score Breakdown','Source']
    with open(a.out,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fn); w.writeheader()
        for r in results: w.writerow(r)
    print(f'Input rows:      {len(rows)}')
    print(f'KEPT (perfect):  {len(results)}  ({100*len(results)//max(len(rows),1)}%)')
    print(f'Discarded:       {len(rows)-len(results)}')
    print('Vehicle gate:    ' + ('ON  (tractor required)' if vehicle_gate else 'OFF !! input lacks OWNTRACT/TRMTRACT/TRPTRACT columns -- box trucks/hotshots NOT filtered; re-run scripts/extract_leads.py'))
    print('Authority age:   ' + ('TRUE (AuthHist)' if has_trueage else 'PROXY !! ADD_DATE only -- enrich via scripts/extract_leads.py for true authority age'))
    tiers={}
    for r in results: tiers[r['Priority Tier']]=tiers.get(r['Priority Tier'],0)+1
    print('Tiers:           '+', '.join(f'{k}:{tiers.get(k,0)}' for k in ['P1','P2','P3','P4']))
    print('\nWhy leads were discarded:')
    for why,n in sorted(reasons.items(),key=lambda x:-x[1]): print(f'  {n:5}  {why}')
    if a.top:
        print(f'\nTop {a.top}:')
        for r in results[:a.top]:
            print(f"  {r['Rank']:3}. {r['Legal Name'][:40]:40} {r['Lead Score']:3} {r['Priority Tier']} {r['Authority Age (days)']:3}d  {r['Equipment Types']}")
    print(f'\nWrote: {a.out}')

if __name__=='__main__': main()
