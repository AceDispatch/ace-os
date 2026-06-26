import requests, os
def load_env(p=".env"):
    e = {}
    for line in open(p, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1); e[k.strip()] = v.strip().strip('"').strip("'")
    return e
env = load_env(); URL = env["SUPABASE_URL"].rstrip("/")
KEY = env.get("SUPABASE_SECRET_KEY") or env.get("SUPABASE_SERVICE_KEY")
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
def count(q):
    r = requests.get(f"{URL}/rest/v1/{q}", headers={**H, "Prefer": "count=exact", "Range": "0-0"}, timeout=30)
    return r.headers.get("content-range", "?").split("/")[-1]
print("TOTAL shippers:", count("shippers?select=shipper_id"))
print("by equipment_class:")
for ec in ("flatbed", "van", "dump", "tanker", "heavy-haul"):
    print(f"   {ec:11}", count(f"shippers?select=shipper_id&equipment_class=eq.{ec}"))
print("RESEARCHED:", count("shippers?select=shipper_id&research_stage=eq.RESEARCHED"))
print("v_ready_to_onboard (FTL + GREEN door):", count("v_ready_to_onboard?select=company_name"))
print("\nSample of the live 'ready to onboard' view:")
r = requests.get(f"{URL}/rest/v1/v_ready_to_onboard?select=company_name,equipment_class,onboarding_ease,state,region&limit=8", headers=H, timeout=30)
for row in r.json():
    print(f"   - {row.get('company_name','')[:34]:34} | {row.get('equipment_class','')} | {row.get('onboarding_ease','')} | {row.get('state','')}")
