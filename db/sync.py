#!/usr/bin/env python3
"""
db/sync.py — push the master shipper DB into Supabase via the REST API (service key).
Reads SUPABASE_URL + SUPABASE_SECRET_KEY from .env at runtime (never printed/logged).
Idempotent: upserts on dedup_key, so re-running a region updates rather than duplicates.

Usage: python db/sync.py            (loads outbox/shipper_db/shippers_master.csv)
       python db/sync.py <csv>      (loads a specific file with the master schema)
"""
import csv, os, sys, re, json
try:
    import requests
except ImportError:
    sys.exit("Missing 'requests' — run: pip install requests")

def load_env(path=".env"):
    env = {}
    if not os.path.exists(path): return env
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env

env = load_env()
URL = env.get("SUPABASE_URL")
KEY = env.get("SUPABASE_SECRET_KEY") or env.get("SUPABASE_SERVICE_KEY")
if not URL or not KEY:
    sys.exit("Missing SUPABASE_URL or SUPABASE_SECRET_KEY in .env")
URL = URL.rstrip("/")
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

def norm(s): return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

# 1) connection + table check
try:
    r = requests.get(f"{URL}/rest/v1/shippers?select=shipper_id&limit=1", headers=H, timeout=30)
except Exception as e:
    sys.exit(f"Could not reach Supabase ({URL}): {e}")
if r.status_code == 404 or 'relation "public.shippers" does not exist' in r.text or "Could not find the table" in r.text:
    sys.exit("CONNECTED OK, but the 'shippers' table does not exist yet.\n"
             "-> In Supabase: SQL Editor -> paste db/schema.sql -> Run, then re-run this.")
if r.status_code not in (200, 206):
    sys.exit(f"Table check failed ({r.status_code}): {r.text[:300]}")
print(f"connected to {URL} | shippers table present")

# 2) load master + compute dedup_key
src = sys.argv[1] if len(sys.argv) > 1 else "outbox/shipper_db/shippers_master.csv"
rows = list(csv.DictReader(open(src, encoding="utf-8", errors="replace")))
INT = {"effort_tier"}
def clean(rec):
    out = {}
    for k, v in rec.items():
        if k == "updated_at": continue
        if k in INT:
            out[k] = int(v) if str(v).strip().isdigit() else None
        else:
            out[k] = v if (v is not None and v != "") else None
    out["dedup_key"] = f"{norm(rec.get('company_name'))}|{(rec.get('state') or '').upper()}|{norm(rec.get('city'))}"
    return out
recs = [clean(r) for r in rows if (r.get("company_name") or "").strip()]
print(f"loading {len(recs)} records from {src}")

# 3) upsert in batches on dedup_key
HU = dict(H); HU["Prefer"] = "resolution=merge-duplicates,return=minimal"
B, done, errs = 500, 0, 0
for i in range(0, len(recs), B):
    batch = recs[i:i+B]
    rr = requests.post(f"{URL}/rest/v1/shippers?on_conflict=dedup_key", headers=HU,
                       data=json.dumps(batch), timeout=120)
    if rr.status_code in (200, 201, 204):
        done += len(batch)
    else:
        errs += 1
        print(f"  batch @{i}: {rr.status_code} {rr.text[:200]}")
print(f"upserted {done}/{len(recs)} (batch errors: {errs})")

# 4) verify total + a quick breakdown
rc = requests.get(f"{URL}/rest/v1/shippers?select=shipper_id", headers={**H, "Prefer": "count=exact", "Range": "0-0"}, timeout=30)
print("rows now in DB:", rc.headers.get("content-range", "?"))
