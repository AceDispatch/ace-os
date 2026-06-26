-- Ace Shipper Database — schema.sql
-- Paste into Supabase Dashboard → SQL Editor → Run. Creates the single shippers table
-- (source of truth for the multi-vertical shipper DB) + indexes + the "ready to onboard" view.

create table if not exists shippers (
  shipper_id            text primary key,
  company_name          text not null,
  dba                   text,
  parent_company        text,
  address               text,
  city                  text,
  county                text,
  state                 text,
  zip                   text,
  naics                 text,
  equipment_class       text,   -- flatbed|van|reefer|dump|tanker|heavy-haul|hopper|mixed|unknown
  equipment_confidence  text,   -- high|med|low
  ftl_status            text,   -- CONFIRMED|LIKELY|UNCONFIRMED|LTL-ONLY|NO
  ftl_evidence          text,
  ships                 text,
  outbound_lanes        text,
  volume_signal         text,
  door_status           text,   -- GREEN|UNCONFIRMED
  door_type             text,
  onboarding_ease       text,   -- self-serve-portal|direct-contact|navigate-in|captive-only|none|unknown
  onboarding_url        text,
  effort_tier           int,
  phone                 text,
  email                 text,
  website               text,
  contact_grade         text,
  research_stage        text,   -- PROSPECTED|GRADED|RESEARCHED
  flags                 text,
  region                text,
  source                text,
  notes                 text,
  dedup_key             text,   -- normalized company_name+state+city (the upsert key)
  updated_at            timestamptz default now()
);

-- dedup_key is the upsert target so re-running a region updates rather than duplicates
create unique index if not exists shippers_dedup on shippers (dedup_key);
create index if not exists shippers_equip   on shippers (equipment_class);
create index if not exists shippers_ftl     on shippers (ftl_status);
create index if not exists shippers_region  on shippers (region);
create index if not exists shippers_door    on shippers (door_status);
create index if not exists shippers_stage   on shippers (research_stage);

-- keep updated_at fresh on every change
create or replace function touch_updated_at() returns trigger as $$
begin new.updated_at = now(); return new; end; $$ language plpgsql;
drop trigger if exists shippers_touch on shippers;
create trigger shippers_touch before update on shippers
  for each row execute function touch_updated_at();

-- THE dial-sheet view: FTL-confirmed/likely + a real onboarding door, researched
create or replace view v_ready_to_onboard as
  select company_name, equipment_class, ftl_status, door_status, door_type,
         onboarding_ease, onboarding_url, effort_tier, phone, email, website,
         city, state, region, outbound_lanes, ships
  from shippers
  where research_stage = 'RESEARCHED'
    and door_status = 'GREEN'
    and ftl_status in ('CONFIRMED','LIKELY')
  order by onboarding_ease, state, city;

-- Grant the secret/service_role key full access to the table + view.
-- anon/authenticated get NOTHING (RLS on + no grant = sealed from the public key).
grant all on public.shippers to service_role;
grant all on public.v_ready_to_onboard to service_role;
