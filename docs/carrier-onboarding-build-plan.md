# Ace Carrier Onboarding — Build Plan

**Status:** DRAFT for operator ratification · **Created:** 2026-06-25
**Goal:** Replace the email-to-admin@ document scramble (§13 "won't scale past ~15 trucks") with a real,
structured carrier onboarding flow on **acedispatch.us** — capturing the §6 sales qualifiers + the
required documents into **Supabase** (the unified backend), securely, while reading as the first taste of
the Ace Standard. This realizes §17 step 2 (carrier-intake polish — "protects live demand").

## Architecture (the shape)
Static React/Vite site on **Hostinger** (unchanged host) → talks to a **Supabase Edge Function** →
writes to **Postgres** + **Storage**, sealed by **RLS**. The browser never holds a secret key; the
Edge Function does all privileged writes. Optional mirror into HubSpot (operator-sanctioned, see below).

```
[acedispatch.us /carriers/onboard]  --POST fields-->  [Edge Fn: carrier-intake]
        |                                                   |-- insert -> carrier_intake (Postgres)
        |  <--signed upload URLs--                          |-- (return signed upload URLs)
        |--PUT docs--> [Supabase Storage: carrier-docs]     |-- (optional) mirror -> HubSpot
```

---

## BACKEND

### 1. Data model (Postgres, in the existing Supabase project)
**`carrier_intake`** — one row per submission:
- `id uuid pk`, `created_at`, `updated_at`, `status text default 'new'` (new | docs_pending | complete | onboarded | declined)
- Identity: `legal_name`, `dba`, `mc_number`, `dot_number`, `contact_name`, `phone`, `email`, `city`, `state`
- Operation (§6 qualifiers): `equipment_types text[]` (flatbed/reefer/dry_van), `power_units int`, `trailer_info`,
  `owner_operator bool`, `operating_areas`, `target_start_date date`, `current_load_finding`,
  `factoring_company` (null = OTR/none), `weekly_revenue` (optional range)
- Consent/compliance: `sms_consent bool`, `sms_consent_method`, `sms_consent_date`, `tos_accepted bool`,
  `ip_address`, `user_agent`
- Ops: `referral_source`, `hubspot_synced bool default false`, `hubspot_object_id`, `notes`

**`carrier_documents`** — one-to-many (the docs §13 requires):
- `id uuid pk`, `carrier_intake_id uuid fk`, `doc_type` (mc_authority | coi | w9 | noa | eld | truck_trailer | other),
  `storage_path`, `file_name`, `content_type`, `size_bytes`, `uploaded_at`
- Required at onboarding: **MC authority cert · COI (Ace named as cert holder) · W-9 · NOA (factoring) · ELD ID**

### 2. Storage
- Private bucket **`carrier-docs`** (no public/anon read or list).
- Path convention: `carrier-docs/{carrier_intake_id}/{doc_type}-{filename}`.
- Uploads via **signed upload URLs** the Edge Function issues (bucket stays fully sealed; service key never leaves the server).

### 3. Security (RLS)
- `carrier_intake` + `carrier_documents`: **RLS ON, no anon policies** — sealed exactly like `shippers`.
  All writes go through the Edge Function (service role). Browser gets *no* direct DB access.
- Storage bucket: private; access only via service role / signed URLs.
- Run `get_advisors(security)` after the migration (we keep the DB advisor-clean).

### 4. Edge Function `carrier-intake` (Deno/TypeScript, deployed via MCP)
Responsibilities:
1. Accept `POST` (JSON form fields). Validate required fields (MC#, DOT#, equipment, contact, consent), formats.
2. Anti-spam: honeypot field check + (phase 2) Cloudflare Turnstile token verify.
3. Insert `carrier_intake` row → get `id`.
4. Generate **signed upload URLs** for each declared document; insert `carrier_documents` rows (pending).
5. Return `{ ok, intake_id, upload_urls }` to the browser, which PUTs files directly to Storage.
6. (Optional, operator-gated) mirror a Contact/Company into HubSpot.
- Holds `SUPABASE_SERVICE_ROLE_KEY` from the function's env (server-side only).

### 5. HubSpot sync — the compliance nuance
CLAUDE.md makes *agent-driven* CRM writes propose-only. This is different: the **carrier submitting their own
consented data via a form** is the same sanctioned pattern as the existing contact form (which already posts to
HubSpot). **Decision for operator:** (a) Supabase-only for v1 (cleanest), or (b) also mirror to HubSpot now.
Supabase is always the source of truth either way.

---

## FRONTEND (`web/acedispatch-site/`)

### 6. Page & flow
- New route **`/carriers/onboard`** (linked from the carrier-facing CTAs). Reads as Ace Standard, not a DMV form.
- **Multi-step wizard** (reduces overwhelm, higher completion):
  1. **You & your authority** — legal name, DBA, MC#, DOT#, contact, phone, email
  2. **Your operation** — equipment, # trucks, owner-operator?, operating areas, target start, current load-finding, factoring, weekly revenue (optional)
  3. **Documents** — upload MC authority, COI, W-9, NOA, ELD (drag-drop; PDF/JPG/PNG; size cap ~10MB; clear what each is + why)
  4. **Consent & review** — SMS-consent checkbox (A2P language, optional), TOS/Privacy accept, review summary, Submit
- Confirmation screen ("We've got it — here's what happens next"), graceful error handling, progress indicator.

### 7. Copy/brand (§4, §6, §7)
- Lead with the survival promise: "~90% of new carriers fail year one. Ace's job is to put you in the 10%."
- Brand: charcoal/near-black + Ace red `#FE353B`; tagline "The Ace Standard in Dispatching."

### 8. Validation, anti-spam, config
- Client-side validation (required, MC# format, file type/size) + server-side mirror in the Edge Function.
- Honeypot field; Turnstile in phase 2.
- Vite env (public, safe in frontend): `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_INTAKE_FN_URL`.
- Submits via `fetch` to the Edge Function; uploads via returned signed URLs.

---

## DEPLOYMENT
- **Backend (me, via MCP):** apply migration; create bucket; write + `deploy_edge_function`; advisor check.
- **Frontend (me, in repo):** build the wizard; `npx vite build` (NOT `npm run build`).
- **Operator (§15 — creds never through Claude):**
  - Set the Edge Function secrets in Supabase (service key is auto-provided; add HubSpot token if used).
  - Add the `VITE_*` values for the build.
  - Upload `dist/` to Hostinger `public_html` (zip with forward-slash paths per STATE.md).
- **Together:** end-to-end test — real submission lands in `carrier_intake` + docs in Storage.
- **Always-on:** a public form needs the DB awake → **upgrade Supabase to Pro ($25/mo)** before launch (free tier auto-pauses after 7 idle days).

## COMPLIANCE & SECURITY CHECKLIST
- A2P: SMS consent optional + captured (method/date); model stays cold=call, warm=text after opt-in.
- PII: carrier data + docs are sensitive → RLS sealed, private Storage, HTTPS, never in git.
- Inbound/consented submission = the "warm" path (TCPA-safe); no agent sends outbound messages.
- DB stays advisor-clean (run `get_advisors` post-DDL).

## PHASED SEQUENCE (~3–4 working days)
- **Phase 1 — Backend (me):** schema migration + bucket + RLS + Edge Function deployed & test-posted.
- **Phase 2 — Frontend (me):** the 4-step wizard wired to the function; build.
- **Phase 3 — Deploy (operator + me):** env + Hostinger upload + live end-to-end test.
- **Phase 4 — Ops:** submissions view (manager's inbox) + status workflow; HubSpot mirror (if chosen); go Pro.
- **Phase 5 — Polish:** Turnstile, FMCSA cross-ref on submit (enrich vs known leads — data flywheel), notifications.

## DECISIONS (resolved 2026-06-25)
1. **Supabase-only for v1**; build the function so the HubSpot mirror bolts on later (structure for it, don't wire it now).
2. **Documents optional at submit** — allow "send later" (status=docs_pending); encourage full upload, dispatcher can collect the rest. Never block the lead on paperwork.
3. **No CTAs yet.** Current contact form lives at `acedispatch.us/contact`. New onboarding page route + linking decided at deploy time.
4. **Supabase Pro** — operator upgrading within 24h.
5. **Turnstile anti-spam REQUIRED before launch** (moved from phase 5 into the pre-launch set).

> Build is QUEUED behind the ace-os standardization/housekeeping (see below). Execute that first, then this.

## FUTURE ENHANCEMENTS
- FMCSA cross-ref on submit (auto-verify authority age / tractor vs the lead-grading data).
- Internal authed admin view (the network-MVP seed; Supabase Auth + RLS).
- Auto-status progression + manager realtime alerts.
- Reuse the same backend pattern for the Shipper Direct portal (§13 phase two).
