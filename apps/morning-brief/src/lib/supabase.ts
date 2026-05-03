import { createClient, SupabaseClient } from "@supabase/supabase-js";

// Server-side Supabase client. Uses service role for writes, falls back to anon for reads.
// Never import this from a client component. Browser code should use the public anon client.

let cachedAdmin: SupabaseClient | null = null;

export function supabaseAdmin(): SupabaseClient {
  if (cachedAdmin) return cachedAdmin;
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? process.env.SUPABASE_ANON_KEY;
  if (!url || !key) {
    throw new Error("supabase: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY/ANON_KEY missing");
  }
  cachedAdmin = createClient(url, key, {
    auth: { persistSession: false },
  });
  return cachedAdmin;
}

// Public anon client for read-only browser usage. Optional, page.tsx uses server fetch.
export function supabasePublic(): SupabaseClient {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !key) throw new Error("supabase: NEXT_PUBLIC_* env vars missing");
  return createClient(url, key, { auth: { persistSession: false } });
}
