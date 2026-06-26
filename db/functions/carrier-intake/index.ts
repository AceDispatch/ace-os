// Supabase Edge Function: carrier-intake
// Public carrier onboarding endpoint for acedispatch.us. Validates the submission, inserts a
// structured carrier_intake row, issues signed upload URLs for declared documents (returned to
// the browser, which uploads directly to the private carrier-docs bucket).
// Deployed to Supabase with verify_jwt=true. The service-role key is used server-side only.
//
// Deploy:  via the Supabase MCP deploy_edge_function, or `supabase functions deploy carrier-intake`.
import { createClient } from "jsr:@supabase/supabase-js@2";

const cors = {
  "Access-Control-Allow-Origin": "*", // TODO: tighten to https://www.acedispatch.us at launch
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(obj: unknown, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { ...cors, "content-type": "application/json" } });
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);

  let body: any;
  try { body = await req.json(); } catch { return json({ error: "invalid json" }, 400); }

  // honeypot — silently accept-and-drop bots
  if (body.website_hp) return json({ ok: true, intake_id: null });

  if (!body.legal_name || (!body.mc_number && !body.dot_number) || !body.contact_name) {
    return json({ error: "missing required: legal_name, mc_number or dot_number, contact_name" }, 400);
  }

  // Cloudflare Turnstile — enforced only once TURNSTILE_SECRET_KEY is set on the function (fail-open
  // until then, so the form keeps working between shipping the widget frontend and adding the secret).
  const turnstileSecret = Deno.env.get("TURNSTILE_SECRET_KEY");
  if (turnstileSecret) {
    if (!body.turnstile_token) return json({ error: "verification required" }, 403);
    const vForm = new FormData();
    vForm.append("secret", turnstileSecret);
    vForm.append("response", String(body.turnstile_token));
    const ip = req.headers.get("x-forwarded-for")?.split(",")[0]?.trim();
    if (ip) vForm.append("remoteip", ip);
    try {
      const vRes = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: vForm });
      const outcome = await vRes.json();
      if (!outcome.success) return json({ error: "verification failed" }, 403);
    } catch {
      return json({ error: "verification error" }, 502);
    }
  }

  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const docs = Array.isArray(body.documents) ? body.documents : [];

  const intake = {
    status: docs.length ? "docs_pending" : "new",
    legal_name: body.legal_name, dba: body.dba ?? null,
    mc_number: body.mc_number ?? null, dot_number: body.dot_number ?? null,
    contact_name: body.contact_name, phone: body.phone ?? null, email: body.email ?? null,
    city: body.city ?? null, state: body.state ?? null,
    equipment_types: body.equipment_types ?? null, power_units: body.power_units ?? null,
    trailer_info: body.trailer_info ?? null, owner_operator: body.owner_operator ?? null,
    operating_areas: body.operating_areas ?? null, target_start_date: body.target_start_date ?? null,
    current_load_finding: body.current_load_finding ?? null, factoring_company: body.factoring_company ?? null,
    weekly_revenue: body.weekly_revenue ?? null,
    sms_consent: !!body.sms_consent,
    sms_consent_method: body.sms_consent ? "website_form" : null,
    sms_consent_date: body.sms_consent ? new Date().toISOString() : null,
    tos_accepted: !!body.tos_accepted,
    ip_address: req.headers.get("x-forwarded-for"), user_agent: req.headers.get("user-agent"),
    referral_source: body.referral_source ?? "acedispatch.us",
  };

  const { data: row, error } = await supabase.from("carrier_intake").insert(intake).select("id").single();
  if (error) return json({ error: "insert failed", detail: error.message }, 500);
  const intakeId = row.id;

  const uploads: any[] = [];
  for (const d of docs) {
    const safe = String(d.file_name ?? "file").replace(/[^a-zA-Z0-9._-]/g, "_");
    const path = `${intakeId}/${d.doc_type ?? "other"}-${safe}`;
    const { data: signed, error: sErr } = await supabase.storage.from("carrier-docs").createSignedUploadUrl(path);
    if (sErr || !signed) continue;
    await supabase.from("carrier_documents").insert({
      carrier_intake_id: intakeId, doc_type: d.doc_type ?? "other", storage_path: path,
      file_name: d.file_name ?? null, content_type: d.content_type ?? null,
    });
    uploads.push({ doc_type: d.doc_type ?? "other", path, signed_url: signed.signedUrl, token: signed.token });
  }

  // TODO (v2, operator-gated): mirror to HubSpot here. Structure is ready; not wired per decision 1.
  return json({ ok: true, intake_id: intakeId, uploads });
});
