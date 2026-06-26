import requests, json
def load_env(p=".env"):
    e = {}
    for line in open(p, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1); e[k.strip()] = v.strip().strip('"').strip("'")
    return e
env = load_env(); URL = env["SUPABASE_URL"].rstrip("/")
KEY = env.get("SUPABASE_SECRET_KEY") or env.get("SUPABASE_SERVICE_KEY")
payload = {
    "legal_name": "TEST Flatbed Carrier LLC", "mc_number": "MC-1234567", "dot_number": "3999999",
    "contact_name": "Test Driver", "phone": "555-0100", "email": "test@example.com", "state": "TX",
    "equipment_types": ["flatbed"], "power_units": 1, "owner_operator": True, "operating_areas": "OTR",
    "sms_consent": True, "tos_accepted": True,
    "documents": [{"doc_type": "coi", "file_name": "coi.pdf", "content_type": "application/pdf"}],
}
r = requests.post(f"{URL}/functions/v1/carrier-intake",
                  headers={"Authorization": f"Bearer {KEY}", "apikey": KEY, "content-type": "application/json"},
                  data=json.dumps(payload), timeout=30)
print("HTTP", r.status_code)
try:
    d = r.json()
    print("ok:", d.get("ok"), "| intake_id:", d.get("intake_id"))
    for u in d.get("uploads", []):
        print("  upload:", u.get("doc_type"), "->", u.get("path"), "| signed_url:", "yes" if u.get("signed_url") else "no")
except Exception:
    print(r.text[:600])
