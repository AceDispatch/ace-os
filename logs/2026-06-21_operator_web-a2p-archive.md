# Run Log — Operator Session: Web Self-Host + A2P Compliance + git Archive

- **Date/time:** 2026-06-21
- **Contract:** none — operator-initiated infrastructure/compliance work, not a pipeline agent run
- **Operator-initiated or scheduled:** Operator-initiated (Anthony)
- **Inputs:** Hostinger Horizons export of acedispatch.us (React+Vite); HubSpot (region NA2); Aircall (read-only, /v1/numbers); Termify-hosted privacy policy

## Outputs
- `web/acedispatch-site/` — website source, rebuilt off Horizons and made A2P-compliant; self-hosted on Hostinger Business (Custom PHP/HTML, `public_html`). **LIVE at acedispatch.us.**
- `compliance/a2p/` — A2P registration sheet, Terms of Service, Privacy edits, fill-in worksheet, README (governing model + status).
- HubSpot (operator created in UI): contact properties `sms_consent`, `sms_consent_method`, `sms_consent_date`; embedded form `924e9f4f-dfad-4d37-8da7-e526c2c8b60b` (portal 245837044).
- Site contact form wired to post into that HubSpot form (was a dead localStorage stub before).
- STATE.md → v0.3; ace-os placed under git.

## Result
- **Success.** Site is live, compliant, self-hosted; SMS consent capture verified end-to-end (2 test submissions: with-consent set `sms_consent=Yes`, without-consent still captured the lead).

## Anomalies / data-quality notes
- Original contact form sent nothing (localStorage stub + fake success toast) — replaced with real HubSpot submission.
- Generated (Termify) privacy policy shared data with "advertisers/marketing partners" — the #1 A2P rejection cause — replaced with a compliant `/privacy` page + SMS section.
- Windows `Compress-Archive` wrote backslash paths → Hostinger extracted assets as literal filenames (blank site); fixed by building the zip with forward-slash entries.
- `npm run build` fails on Windows (`|| true` not valid in cmd.exe) — build with `npx vite build`.
- 7-day CDN cache in the Horizons `.htaccess` served a stale blank page after first deploy; cleared via hard refresh. (Open item: relax HTML caching so future deploys show instantly.)
- Test contact `a2p-wiring-test@acedispatch.us` left in HubSpot — operator to archive (connected MCP cannot delete records).

## Proposed promotions / remaining work
- `compliance/a2p/README.md` is the durable record of the A2P model (cold=call, warm=text).
- REMAINING before A2P submission: (1) enable HubSpot form notification email so leads are seen; (2) archive the test contact; (3) screenshot the live consent checkbox (campaign CTA evidence); (4) submit the Aircall brand + campaign from the registration sheet.
- Optional site hardening: edit `.htaccess` so the CDN does not cache HTML (hashed `/assets/` stay cached) — removes the stale-blank-page risk on every future deploy.
