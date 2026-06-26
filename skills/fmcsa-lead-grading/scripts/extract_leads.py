#!/usr/bin/env python3
"""
FMCSA lead EXTRACTION + ENRICHMENT — Ace Dispatch (the upstream step for grade_leads.py)

This is "option 3": the grader stays OFFLINE. This script does the live work and
writes a grade-ready CSV that already carries:
  - the census VEHICLE-TYPE columns (OWNTRACT/TRMTRACT/TRPTRACT/OWNTRUCK) so the
    grader's tractor gate can fire, and
  - TRUE_AUTHORITY_AGE_DAYS / TRUE_AUTHORITY_GRANT_DATE from the AuthHist join,
    so the grader uses the real operating-authority grant date, not the ADD_DATE proxy.

Datasets (data.transportation.gov / Socrata, no auth required; an app token in
$SOCRATA_APP_TOKEN just lifts rate-throttling):
  - Company Census ............ az4n-8mr2   (identity, contact, cargo, vehicle counts)
  - AuthHist (authority grants) 9mw4-x3tu   (orig_served_date of GRANTED actions = true grant date)

Gotchas baked in (learned the hard way):
  - AuthHist orig_served_date is TEXT 'MM/DD/YYYY' -> cannot $where range-filter or
    sort it server-side; pull GRANTED rows by year via like '%/YYYY' and parse locally.
  - AuthHist DOT is zero-padded to 8 chars; census DOT is unpadded -> normalize.
  - AuthHist lags real-time ~6-8 weeks, so carriers granted in the last ~6 weeks may
    have no AuthHist row yet (TRUE_AUTHORITY_AGE_DAYS blank -> grader falls back to ADD_DATE).

Usage:
  python extract_leads.py --out leads_enriched.csv [--states TX,GA,TN] \
         [--power-units 1] [--years 2024,2025,2026] [--as-of 2026-06-18]
Then:
  python grade_leads.py leads_enriched.csv --out graded.csv --top 25
"""
import argparse, csv, json, os, sys, urllib.parse, urllib.request
from datetime import date, datetime

BASE='https://data.transportation.gov/resource'
CENSUS='az4n-8mr2'; AUTHHIST='9mw4-x3tu'
TOKEN=os.environ.get('SOCRATA_APP_TOKEN','')

# Census columns the grader reads (lowercase Socrata fieldnames -> emitted UPPERCASE).
CENSUS_COLS=['dot_number','legal_name','dba_name','carrier_operation','classdef','status_code',
  'prior_revoke_flag','docket1prefix','docket1','docket1_status_code','add_date','mcs150_date',
  'power_units','total_drivers','phone','cell_phone','email_address','phy_street','phy_city',
  'phy_state','phy_zip','company_officer_1','interstate_beyond_100_miles','interstate_within_100_miles',
  'driver_inter_total','owntruck','owntract','owntrail','trmtract','trptract','trptruck','trmtruck',
  'crgo_genfreight','crgo_paperprod','crgo_drybulk','crgo_farmsupp','crgo_metalsheet','crgo_bldgmat',
  'crgo_machlrg','crgo_logpole','crgo_construct','crgo_coldfood','crgo_produce','crgo_meat','crgo_beverages',
  'crgo_passengers','crgo_liqgas','crgo_chem','crgo_oilfield','crgo_livestock','crgo_garbage','crgo_usmail',
  'crgo_drivetow','crgo_mobilehome','crgo_coalcoke','crgo_waterwell']

def fetch(dataset, select, where, limit=50000, order='dot_number'):
    """Paginated Socrata JSON fetch -> list of dict rows."""
    rows=[]; offset=0
    while True:
        qs=urllib.parse.urlencode({'$select':select,'$where':where,'$order':order,
                                   '$limit':limit,'$offset':offset})
        req=urllib.request.Request(f'{BASE}/{dataset}.json?{qs}',
                                   headers={'X-App-Token':TOKEN} if TOKEN else {})
        page=json.load(urllib.request.urlopen(req, timeout=180))
        rows.extend(page)
        if len(page)<limit: break
        offset+=limit
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    ap.add_argument('--states',default='',help='comma list of phy_state codes, e.g. TX,GA')
    ap.add_argument('--power-units',default='',help="exact power_units, e.g. 1 (blank = any)")
    ap.add_argument('--years',default='',help='AuthHist grant years to pull (default: this + 2 prior)')
    ap.add_argument('--as-of',default='',help='YYYY-MM-DD reference date (default: today)')
    a=ap.parse_args()
    as_of=datetime.strptime(a.as_of,'%Y-%m-%d').date() if a.as_of else date.today()
    years=a.years.split(',') if a.years else [str(as_of.year-2),str(as_of.year-1),str(as_of.year)]

    # --- 1. census: interstate for-hire, active carrier AND active operating authority, never revoked
    where=("carrier_operation='A' AND classdef like '%AUTHORIZED FOR HIRE%' AND status_code='A' "
           "AND docket1_status_code='A' AND (prior_revoke_flag IS NULL OR prior_revoke_flag!='Y')")
    if a.power_units: where+=f" AND power_units='{a.power_units}'"
    if a.states:
        inlist=','.join("'%s'"%s.strip().upper() for s in a.states.split(','))
        where+=f" AND phy_state in({inlist})"
    print(f'Pulling census ({CENSUS}) ...', file=sys.stderr)
    census=fetch(CENSUS, ','.join(CENSUS_COLS), where)
    print(f'  {len(census)} carriers', file=sys.stderr)

    # --- 2. AuthHist: latest GRANTED orig_served_date per DOT (= true authority grant date)
    print(f'Pulling AuthHist ({AUTHHIST}) grants for {years} ...', file=sys.stderr)
    grant={}
    for yr in years:
        ah=fetch(AUTHHIST,'dot_number,orig_served_date',
                 f"original_action_desc='GRANTED' AND orig_served_date like '%/{yr}'")
        for r in ah:
            k=r.get('dot_number','').lstrip('0')
            if not k: continue
            try: d=datetime.strptime(r['orig_served_date'],'%m/%d/%Y').date()
            except (KeyError,ValueError): continue
            if k not in grant or d>grant[k]: grant[k]=d
    print(f'  {len(grant)} DOTs with a grant date', file=sys.stderr)

    # --- 3. write enriched, grade-ready CSV (UPPERCASE FMCSA-style headers)
    out_cols=[c.upper() for c in CENSUS_COLS]+['TRUE_AUTHORITY_GRANT_DATE','TRUE_AUTHORITY_AGE_DAYS']
    n=trued=0
    with open(a.out,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(out_cols)
        for r in census:
            dot=r.get('dot_number','')
            g=grant.get(dot.lstrip('0'))
            tg=g.isoformat() if g else ''
            ta=str((as_of-g).days) if g else ''
            if g: trued+=1
            w.writerow([r.get(c,'') for c in CENSUS_COLS]+[tg,ta]); n+=1
    print(f'Wrote {n} rows ({trued} with TRUE authority age) -> {a.out}', file=sys.stderr)
    print('Next: python grade_leads.py %s --out graded.csv --top 25' % a.out, file=sys.stderr)

if __name__=='__main__': main()
