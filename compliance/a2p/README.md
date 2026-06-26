# A2P 10DLC / SMS Compliance — Ace Dispatch

Compliance artifacts for Ace Dispatch's A2P 10DLC registration (Aircall SMS).
The governing decision, entity facts, and current status live here so the folder
is self-documenting.

## The compliant model (cold = call, warm = text)
- **Cold outreach is by phone only.** No first-touch SMS to FMCSA/lead lists
  (TCPA $500–1,500/text + carrier-block risk).
- **SMS only to leads who have opted in**, via one of three channels:
  1. Verbal consent on a call (rep logs it in HubSpot).
  2. Inbound text (the carrier texts us first).
  3. Website consent checkbox on acedispatch.us/contact.
- Registered use case: **Low Volume Mixed** (conversational / customer-care), NOT Marketing.
- Verbal consent covers conversational/transactional texts only; promotional
  blasts require the written (website) opt-in.

## Entity & numbers
- Legal entity (brand): **A&C Consulting Group LLC** d/b/a Ace Dispatch
- EIN: 88-2003940 · Address: 236 Via D Este, Apt 1402, Delray Beach, FL 33445
  (IRS spelling — no apostrophe; the public site uses "236 Via D' Este #1402")
- Aircall numbers: **Sales +1 561-291-8209** (SMS line) · **Main +1 561-231-2023**
- Both numbers registered to the campaign.

## HubSpot consent capture
- Contact properties: `sms_consent` (Yes/No) · `sms_consent_method`
  (Verbal / Inbound Text / Website Form) · `sms_consent_date`.
- The website contact form posts into HubSpot form `924e9f4f-dfad-4d37-8da7-e526c2c8b60b`
  (portal 245837044, region na2) and sets `sms_consent = Yes` when the optional
  checkbox is ticked. Aircall↔HubSpot integration already logs SMS to contacts.

## Files
- `Aircall_A2P_Registration_Sheet.md` — paste-ready brand + campaign answers.
- `Terms_of_Service.md` — Terms (also published at acedispatch.us/terms).
- `Privacy_Policy_Edits.md` — the policy fixes (now built into the site's /privacy page).
- `FILL_THESE_IN.md` — source-of-truth worksheet (entity details filled in).

## Status (2026-06-21)
- Website rebuilt compliant + self-hosted off Horizons (see `../../web/acedispatch-site`).
- Privacy + Terms pages live; consent checkbox live; contact form → HubSpot verified.
- **REMAINING:** enable HubSpot form notification email; archive test contact
  `a2p-wiring-test@acedispatch.us`; screenshot the live consent checkbox (CTA
  evidence); submit the Aircall brand + campaign from the registration sheet.
