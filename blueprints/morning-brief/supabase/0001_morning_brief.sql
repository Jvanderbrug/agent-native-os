-- Morning Brief schema. Run this once after creating your Supabase project.
-- Apply via: Supabase SQL Editor, or `supabase db push` if using the CLI.

-- briefs: one row per generated morning brief.
create table if not exists public.briefs (
  id uuid primary key default gen_random_uuid(),
  date date not null,
  title text not null,
  summary text not null,
  top_priority text not null,
  sections jsonb not null default '[]'::jsonb,
  source_status jsonb not null default '[]'::jsonb,
  delivery_status jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
create index if not exists briefs_date_idx on public.briefs (date desc);

-- sources: optional registry of input sources the user can toggle on or off.
create table if not exists public.sources (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  enabled boolean not null default false,
  config jsonb not null default '{}'::jsonb,
  last_pulled_at timestamptz,
  created_at timestamptz not null default now()
);

-- delivery_logs: every ping attempt (success or failure) lands here.
create table if not exists public.delivery_logs (
  id uuid primary key default gen_random_uuid(),
  channel text not null check (channel in ('telegram','slack','imessage','email','none')),
  brief_id uuid references public.briefs(id) on delete set null,
  ok boolean not null,
  error text,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
create index if not exists delivery_logs_created_idx on public.delivery_logs (created_at desc);

-- RLS posture: workshop default is open-read, service-role-only-write.
-- For multi-tenant production, switch this to user-scoped policies.
alter table public.briefs enable row level security;
alter table public.sources enable row level security;
alter table public.delivery_logs enable row level security;

-- Public read so the homepage can render via the anon key.
-- Writes happen from API routes using SUPABASE_SERVICE_ROLE_KEY which bypasses RLS.
drop policy if exists "briefs read" on public.briefs;
create policy "briefs read" on public.briefs for select using (true);

drop policy if exists "sources read" on public.sources;
create policy "sources read" on public.sources for select using (true);

drop policy if exists "delivery_logs read" on public.delivery_logs;
create policy "delivery_logs read" on public.delivery_logs for select using (true);
