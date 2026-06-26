import React, { useState } from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Truck, FileText, ShieldCheck, CheckCircle2, Upload, ArrowLeft, ArrowRight, Loader2 } from 'lucide-react';
import Section from '@/components/Section';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { useToast } from '@/hooks/use-toast';

// Supabase carrier-intake endpoint. URL is public; anon key is public (safe in frontend) and set at build.
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || 'https://hsrzysvihamlaupgthrz.supabase.co';
const ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';
const INTAKE_URL = `${SUPABASE_URL}/functions/v1/carrier-intake`;

const EQUIPMENT = [
  { key: 'flatbed', label: 'Flatbed' },
  { key: 'reefer', label: 'Reefer' },
  { key: 'dry_van', label: 'Dry Van' },
];
const DOCS = [
  { key: 'mc_authority', label: 'MC Authority Letter' },
  { key: 'coi', label: 'Certificate of Insurance (COI)' },
  { key: 'w9', label: 'W-9' },
  { key: 'noa', label: 'Notice of Assignment (factoring)' },
  { key: 'eld', label: 'ELD / truck & trailer info' },
];
const STEPS = ['Authority', 'Operation', 'Documents', 'Review'];

const inp = (err) =>
  `w-full px-4 py-3 bg-white text-darkGray border ${err ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-dispatchRed focus:border-transparent transition-all duration-300 disabled:opacity-50`;

const OnboardingPage = () => {
  const { toast } = useToast();
  const [step, setStep] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(null); // { intake_id, docCount }
  const [errors, setErrors] = useState({});
  const [files, setFiles] = useState({}); // { doc_type: File }
  const [form, setForm] = useState({
    legal_name: '', dba: '', mc_number: '', dot_number: '', contact_name: '', phone: '', email: '',
    city: '', state: '', equipment_types: [], power_units: '', owner_operator: '', operating_areas: '',
    target_start_date: '', current_load_finding: '', factoring_company: '', weekly_revenue: '',
    sms_consent: false, tos_accepted: false, website_hp: '',
  });

  const set = (k, v) => { setForm((p) => ({ ...p, [k]: v })); if (errors[k]) setErrors((e) => ({ ...e, [k]: '' })); };
  const toggleEquip = (key) =>
    setForm((p) => ({ ...p, equipment_types: p.equipment_types.includes(key) ? p.equipment_types.filter((x) => x !== key) : [...p.equipment_types, key] }));

  const validate = (s) => {
    const e = {};
    if (s === 0) {
      if (!form.legal_name.trim()) e.legal_name = 'Company legal name is required';
      if (!form.mc_number.trim() && !form.dot_number.trim()) e.mc_number = 'Enter your MC# or DOT#';
      if (!form.contact_name.trim()) e.contact_name = 'Contact name is required';
      if (!form.phone.trim()) e.phone = 'Phone is required';
      if (form.email.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) e.email = 'Enter a valid email';
    }
    if (s === 3) {
      if (!form.tos_accepted) e.tos_accepted = 'Please accept the Terms & Privacy Policy to continue';
    }
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const next = () => { if (validate(step)) setStep((s) => Math.min(s + 1, STEPS.length - 1)); else toast({ title: 'Please check the highlighted fields', variant: 'destructive' }); };
  const back = () => setStep((s) => Math.max(s - 1, 0));

  const submit = async () => {
    if (submitting) return;
    if (!validate(3)) return;
    if (form.website_hp) return; // honeypot
    if (!ANON_KEY) { toast({ title: 'Form not configured', description: 'Please call (631) 807-3088 to onboard.', variant: 'destructive' }); return; }
    setSubmitting(true);
    try {
      const documents = DOCS.filter((d) => files[d.key]).map((d) => ({ doc_type: d.key, file_name: files[d.key].name, content_type: files[d.key].type || 'application/octet-stream' }));
      const payload = { ...form, power_units: form.power_units ? Number(form.power_units) : null, owner_operator: form.owner_operator === '' ? null : form.owner_operator === 'yes', target_start_date: form.target_start_date || null, documents };
      const res = await fetch(INTAKE_URL, { method: 'POST', headers: { 'content-type': 'application/json', Authorization: `Bearer ${ANON_KEY}`, apikey: ANON_KEY }, body: JSON.stringify(payload) });
      const data = await res.json();
      if (!res.ok || !data.ok) throw new Error(data.error || `status ${res.status}`);
      // best-effort document uploads via the signed URLs (docs are optional — never block the lead)
      let uploaded = 0;
      for (const up of data.uploads || []) {
        const f = files[up.doc_type];
        if (!f) continue;
        try {
          const r = await fetch(up.signed_url, { method: 'PUT', headers: { 'content-type': f.type || 'application/octet-stream', 'x-upsert': 'true' }, body: f });
          if (r.ok) uploaded += 1;
        } catch (_) { /* best effort */ }
      }
      setDone({ intake_id: data.intake_id, docCount: uploaded });
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      toast({ title: 'Something went wrong', description: 'Please try again or call (631) 807-3088.', variant: 'destructive' });
    } finally {
      setSubmitting(false);
    }
  };

  if (done) {
    return (
      <Section className="bg-gradient-to-br from-gray-50 to-gray-100 min-h-[80vh] flex items-center">
        <div className="max-w-2xl mx-auto w-full">
          <Card className="bg-white text-center">
            <div className="flex justify-center mb-6"><div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center"><CheckCircle2 className="w-10 h-10 text-green-600" /></div></div>
            <h1 className="text-3xl md:text-4xl font-bold text-darkGray mb-3">You're in. Welcome to the Ace Standard.</h1>
            <p className="text-lg text-gray-600 mb-6">We've got your information{done.docCount ? ` and ${done.docCount} document${done.docCount > 1 ? 's' : ''}` : ''}. A dispatcher will reach out shortly to finish onboarding{done.docCount ? '' : ' and collect any remaining documents'}.</p>
            <p className="text-sm text-gray-500">Questions now? Call <a href="tel:6318073088" className="text-dispatchRed hover:underline">(631) 807-3088</a> or email <a href="mailto:admin@acedispatch.us" className="text-dispatchRed hover:underline">admin@acedispatch.us</a>.</p>
          </Card>
        </div>
      </Section>
    );
  }

  return (
    <>
      <Helmet>
        <title>Carrier Onboarding - Ace Dispatch</title>
        <meta name="description" content="Onboard your authority with Ace Dispatch. Quick, secure carrier intake to start running profitable, well-planned freight." />
      </Helmet>

      <Section className="bg-gradient-to-br from-gray-50 to-gray-100 py-16">
        <div className="max-w-3xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-darkGray mb-3">Carrier Onboarding</h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">~90% of new carriers fail in year one. Ace's job is to put you in the 10% that survive and grow. Let's get you set up.</p>
          </motion.div>

          {/* Step indicator */}
          <div className="flex items-center justify-center gap-2 mb-8" aria-hidden="true">
            {STEPS.map((label, i) => (
              <div key={label} className="flex items-center gap-2">
                <div className={`flex items-center justify-center w-9 h-9 rounded-full text-sm font-semibold ${i < step ? 'bg-green-600 text-white' : i === step ? 'bg-dispatchRed text-white' : 'bg-gray-200 text-gray-500'}`}>{i < step ? '✓' : i + 1}</div>
                <span className={`hidden sm:inline text-sm ${i === step ? 'text-darkGray font-medium' : 'text-gray-400'}`}>{label}</span>
                {i < STEPS.length - 1 && <div className="w-6 sm:w-10 h-0.5 bg-gray-200" />}
              </div>
            ))}
          </div>

          <Card className="bg-white">
            {/* honeypot */}
            <input type="text" tabIndex="-1" autoComplete="off" value={form.website_hp} onChange={(e) => set('website_hp', e.target.value)} className="hidden" aria-hidden="true" />

            {step === 0 && (
              <div className="space-y-5">
                <div className="flex items-center gap-3 mb-2"><Truck className="w-6 h-6 text-dispatchRed" /><h2 className="text-2xl font-bold text-darkGray">You &amp; your authority</h2></div>
                <Field label="Company legal name *" err={errors.legal_name}><input className={inp(errors.legal_name)} value={form.legal_name} onChange={(e) => set('legal_name', e.target.value)} placeholder="Acme Trucking LLC" /></Field>
                <Field label="DBA (if different)"><input className={inp()} value={form.dba} onChange={(e) => set('dba', e.target.value)} /></Field>
                <div className="grid sm:grid-cols-2 gap-4">
                  <Field label="MC number" err={errors.mc_number}><input className={inp(errors.mc_number)} value={form.mc_number} onChange={(e) => set('mc_number', e.target.value)} placeholder="MC-123456" /></Field>
                  <Field label="DOT number"><input className={inp()} value={form.dot_number} onChange={(e) => set('dot_number', e.target.value)} placeholder="3999999" /></Field>
                </div>
                <Field label="Your name *" err={errors.contact_name}><input className={inp(errors.contact_name)} value={form.contact_name} onChange={(e) => set('contact_name', e.target.value)} /></Field>
                <div className="grid sm:grid-cols-2 gap-4">
                  <Field label="Phone *" err={errors.phone}><input type="tel" className={inp(errors.phone)} value={form.phone} onChange={(e) => set('phone', e.target.value)} placeholder="(555) 123-4567" /></Field>
                  <Field label="Email" err={errors.email}><input type="email" className={inp(errors.email)} value={form.email} onChange={(e) => set('email', e.target.value)} /></Field>
                </div>
              </div>
            )}

            {step === 1 && (
              <div className="space-y-5">
                <div className="flex items-center gap-3 mb-2"><Truck className="w-6 h-6 text-dispatchRed" /><h2 className="text-2xl font-bold text-darkGray">Your operation</h2></div>
                <Field label="Equipment (select all that apply)">
                  <div className="flex flex-wrap gap-3">
                    {EQUIPMENT.map((eq) => (
                      <button type="button" key={eq.key} onClick={() => toggleEquip(eq.key)} className={`px-4 py-2 rounded-lg border text-sm font-medium transition-all ${form.equipment_types.includes(eq.key) ? 'bg-dispatchRed text-white border-dispatchRed' : 'bg-white text-darkGray border-gray-300 hover:border-dispatchRed'}`}>{eq.label}</button>
                    ))}
                  </div>
                </Field>
                <div className="grid sm:grid-cols-2 gap-4">
                  <Field label="Number of trucks"><input type="number" min="0" className={inp()} value={form.power_units} onChange={(e) => set('power_units', e.target.value)} placeholder="1" /></Field>
                  <Field label="Owner-operator?">
                    <div className="flex gap-3">
                      {['yes', 'no'].map((v) => (
                        <button type="button" key={v} onClick={() => set('owner_operator', v)} className={`flex-1 px-4 py-3 rounded-lg border text-sm font-medium capitalize transition-all ${form.owner_operator === v ? 'bg-dispatchRed text-white border-dispatchRed' : 'bg-white text-darkGray border-gray-300 hover:border-dispatchRed'}`}>{v}</button>
                      ))}
                    </div>
                  </Field>
                </div>
                <Field label="Operating areas / preferred lanes"><input className={inp()} value={form.operating_areas} onChange={(e) => set('operating_areas', e.target.value)} placeholder="e.g. OTR, TX-Southeast, home weekends" /></Field>
                <div className="grid sm:grid-cols-2 gap-4">
                  <Field label="Target start date"><input type="date" className={inp()} value={form.target_start_date} onChange={(e) => set('target_start_date', e.target.value)} /></Field>
                  <Field label="Factoring company (if any)"><input className={inp()} value={form.factoring_company} onChange={(e) => set('factoring_company', e.target.value)} placeholder="None / OTR Solutions / ..." /></Field>
                </div>
                <Field label="How are you finding loads today?"><input className={inp()} value={form.current_load_finding} onChange={(e) => set('current_load_finding', e.target.value)} placeholder="DAT, broker calls, another dispatcher..." /></Field>
              </div>
            )}

            {step === 2 && (
              <div className="space-y-5">
                <div className="flex items-center gap-3 mb-1"><FileText className="w-6 h-6 text-dispatchRed" /><h2 className="text-2xl font-bold text-darkGray">Documents</h2></div>
                <p className="text-sm text-gray-500 -mt-2">Optional now — upload what you have and your dispatcher will collect the rest. Nothing here blocks getting you started.</p>
                <div className="space-y-3">
                  {DOCS.map((d) => (
                    <label key={d.key} className="flex items-center justify-between gap-4 p-3 border border-gray-200 rounded-lg hover:border-dispatchRed transition-colors cursor-pointer">
                      <span className="text-sm font-medium text-darkGray flex items-center gap-2"><Upload className="w-4 h-4 text-gray-400" />{d.label}</span>
                      <span className="text-xs text-gray-500 truncate max-w-[45%]">{files[d.key] ? files[d.key].name : 'Choose file'}</span>
                      <input type="file" accept=".pdf,.jpg,.jpeg,.png" className="hidden" onChange={(e) => setFiles((p) => ({ ...p, [d.key]: e.target.files[0] }))} />
                    </label>
                  ))}
                </div>
              </div>
            )}

            {step === 3 && (
              <div className="space-y-5">
                <div className="flex items-center gap-3 mb-2"><ShieldCheck className="w-6 h-6 text-dispatchRed" /><h2 className="text-2xl font-bold text-darkGray">Review &amp; submit</h2></div>
                <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-700 space-y-1">
                  <p><span className="text-gray-500">Carrier:</span> {form.legal_name || '—'} {form.mc_number && `(${form.mc_number})`}</p>
                  <p><span className="text-gray-500">Contact:</span> {form.contact_name || '—'} · {form.phone || '—'}</p>
                  <p><span className="text-gray-500">Equipment:</span> {form.equipment_types.length ? form.equipment_types.map((k) => EQUIPMENT.find((e) => e.key === k)?.label).join(', ') : '—'}</p>
                  <p><span className="text-gray-500">Documents:</span> {DOCS.filter((d) => files[d.key]).length || 0} attached</p>
                </div>
                <label className="flex items-start gap-3">
                  <input type="checkbox" checked={form.sms_consent} onChange={(e) => set('sms_consent', e.target.checked)} className="mt-1 h-4 w-4 flex-shrink-0 rounded border-gray-300 text-dispatchRed focus:ring-dispatchRed" />
                  <span className="text-xs text-gray-600 leading-relaxed">I agree to receive text messages from Ace Dispatch at the number provided about my onboarding and services. Msg &amp; data rates may apply. Msg frequency varies. Reply STOP to opt out, HELP for help. Consent is not a condition of any service.</span>
                </label>
                <label className="flex items-start gap-3">
                  <input type="checkbox" checked={form.tos_accepted} onChange={(e) => set('tos_accepted', e.target.checked)} className="mt-1 h-4 w-4 flex-shrink-0 rounded border-gray-300 text-dispatchRed focus:ring-dispatchRed" />
                  <span className="text-xs text-gray-600 leading-relaxed">I agree to the <Link to="/terms" className="text-dispatchRed hover:underline">Terms</Link> and <Link to="/privacy" className="text-dispatchRed hover:underline">Privacy Policy</Link>. *</span>
                </label>
                {errors.tos_accepted && <p className="text-sm text-red-500">{errors.tos_accepted}</p>}
              </div>
            )}

            {/* Nav */}
            <div className="flex items-center justify-between mt-8 pt-6 border-t border-gray-100">
              <button type="button" onClick={back} disabled={step === 0 || submitting} className={`inline-flex items-center gap-2 text-sm font-medium ${step === 0 ? 'invisible' : 'text-gray-500 hover:text-darkGray'}`}><ArrowLeft className="w-4 h-4" /> Back</button>
              {step < STEPS.length - 1 ? (
                <Button onClick={next} size="lg">Next <ArrowRight className="w-4 h-4 ml-2" /></Button>
              ) : (
                <Button onClick={submit} size="lg" className={submitting ? 'opacity-70 pointer-events-none' : ''}>{submitting ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Submitting...</> : 'Submit onboarding'}</Button>
              )}
            </div>
          </Card>

          <p className="text-center text-xs text-gray-400 mt-4">Secure intake. Your information goes only to Ace Dispatch. Prefer a call? <a href="tel:6318073088" className="text-dispatchRed hover:underline">(631) 807-3088</a></p>
        </div>
      </Section>
    </>
  );
};

const Field = ({ label, err, children }) => (
  <div>
    <label className="block text-sm font-medium text-darkGray mb-2">{label}</label>
    {children}
    {err && <p className="mt-1 text-sm text-red-500">{err}</p>}
  </div>
);

export default OnboardingPage;
