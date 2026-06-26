-- Carrier Onboarding backend — Phase 1 (applied to Supabase 2026-06-25 via MCP).
-- Tables are RLS-sealed (service_role only); the edge function db/functions/carrier-intake/ does all writes.

create table if not exists carrier_intake (
  id                   uuid primary key default gen_random_uuid(),
  created_at           timestamptz default now(),
  updated_at           timestamptz default now(),
  status               text default 'new',   -- new | docs_pending | complete | onboarded | declined
  legal_name           text not null,
  dba                  text,
  mc_number            text,
  dot_number           text,
  contact_name         text,
  phone                text,
  email                text,
  city                 text,
  state                text,
  equipment_types      text[],               -- flatbed | reefer | dry_van
  power_units          int,
  trailer_info         text,
  owner_operator       boolean,
  operating_areas      text,
  target_start_date    date,
  current_load_finding text,
  factoring_company    text,                 -- null = OTR / none
  weekly_revenue       text,
  sms_consent          boolean default false,
  sms_consent_method   text,
  sms_consent_date     timestamptz,
  tos_accepted         boolean default false,
  ip_address           text,
  user_agent           text,
  referral_source      text,
  hubspot_synced       boolean default false,
  hubspot_object_id    text,
  notes                text
);

create table if not exists carrier_documents (
  id                uuid primary key default gen_random_uuid(),
  carrier_intake_id uuid references carrier_intake(id) on delete cascade,
  doc_type          text,   -- mc_authority | coi | w9 | noa | eld | truck_trailer | other
  storage_path      text,
  file_name         text,
  content_type      text,
  size_bytes        int,
  uploaded_at       timestamptz default now()
);

create index if not exists carrier_intake_status  on carrier_intake (status);
create index if not exists carrier_intake_created on carrier_intake (created_at);
create index if not exists carrier_docs_intake    on carrier_documents (carrier_intake_id);

alter table carrier_intake    enable row level security;
alter table carrier_documents enable row level security;
grant all on carrier_intake    to service_role;
grant all on carrier_documents to service_role;

drop trigger if exists carrier_intake_touch on carrier_intake;
create trigger carrier_intake_touch before update on carrier_intake
  for each row execute function touch_updated_at();

-- private documents bucket
insert into storage.buckets (id, name, public)
values ('carrier-docs', 'carrier-docs', false)
on conflict (id) do nothing;
