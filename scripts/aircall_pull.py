#!/usr/bin/env python3
"""
aircall_pull.py — shared read-only part for ACE-OS agents.

Pulls call records from the Aircall API for a date range and writes them to a
CSV. Used by Contract 02 (Connect Reconciliation) and Contract 03 (Morning
Sales Brief). READ ONLY by constitution: this script must never POST/PUT/DELETE.

Setup:
  1. Aircall Dashboard -> Integrations & API -> API keys -> generate.
  2. Put credentials in ace-os/.env :
       AIRCALL_API_ID=xxxxx
       AIRCALL_API_TOKEN=xxxxx
  3. pip install requests python-dotenv

Usage:
  python scripts/aircall_pull.py --from 2026-06-01 --to 2026-06-05 \
      --out outbox/aircall_calls.csv
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # .env loading is a convenience; env vars may be set directly

BASE = "https://api.aircall.io/v1"


def auth():
    api_id = os.getenv("AIRCALL_API_ID")
    token = os.getenv("AIRCALL_API_TOKEN")
    if not api_id or not token:
        sys.exit("Missing AIRCALL_API_ID / AIRCALL_API_TOKEN in environment (.env).")
    return (api_id, token)


def to_unix(datestr: str, end_of_day: bool = False) -> int:
    dt = datetime.strptime(datestr, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    if end_of_day:
        dt = dt.replace(hour=23, minute=59, second=59)
    return int(dt.timestamp())


def pull_calls(start: str, end: str):
    """Yield call dicts from /calls, paginated. Read-only GETs only."""
    session = requests.Session()
    session.auth = auth()
    params = {
        "from": to_unix(start),
        "to": to_unix(end, end_of_day=True),
        "per_page": 50,
        "order": "asc",
    }
    url = f"{BASE}/calls"
    page = 1
    while url:
        resp = session.get(url, params=params if page == 1 else None, timeout=30)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", 5)))
            continue
        resp.raise_for_status()
        data = resp.json()
        for call in data.get("calls", []):
            yield call
        url = (data.get("meta") or {}).get("next_page_link")
        page += 1


FIELDS = [
    "id", "direction", "status", "started_at", "answered_at", "ended_at",
    "duration", "raw_digits", "user_name", "missed_call_reason",
]


def flatten(call: dict) -> dict:
    user = call.get("user") or {}
    return {
        "id": call.get("id"),
        "direction": call.get("direction"),
        "status": call.get("status"),
        "started_at": call.get("started_at"),
        "answered_at": call.get("answered_at"),
        "ended_at": call.get("ended_at"),
        "duration": call.get("duration"),
        "raw_digits": call.get("raw_digits"),
        "user_name": user.get("name"),
        "missed_call_reason": call.get("missed_call_reason"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", required=True, help="YYYY-MM-DD")
    ap.add_argument("--to", dest="end", required=True, help="YYYY-MM-DD")
    ap.add_argument("--out", default="outbox/aircall_calls.csv")
    args = ap.parse_args()

    rows = [flatten(c) for c in pull_calls(args.start, args.end)]
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} calls written to {args.out}")


if __name__ == "__main__":
    main()
