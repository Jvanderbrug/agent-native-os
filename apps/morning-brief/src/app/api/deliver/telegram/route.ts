import { NextResponse } from "next/server";
import { sendTelegramMessage, formatBriefPing } from "@/lib/telegram";
import { supabaseAdmin } from "@/lib/supabase";

// POST /api/deliver/telegram
// Body: { brief_id: string } OR { date, title, top_priority, url? }
// Sends the short ping to TELEGRAM_CHAT_ID via the Bot API and logs to delivery_logs.
export async function POST(req: Request) {
  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "invalid json" }, { status: 400 });
  }

  let payload: { date: string; title: string; top_priority: string; url?: string; brief_id?: string };

  if (typeof body.brief_id === "string") {
    try {
      const sb = supabaseAdmin();
      const { data, error } = await sb.from("briefs").select("*").eq("id", body.brief_id).single();
      if (error || !data) return NextResponse.json({ error: error?.message ?? "brief not found" }, { status: 404 });
      payload = {
        brief_id: data.id,
        date: data.date,
        title: data.title,
        top_priority: data.top_priority,
        url: typeof body.url === "string" ? body.url : undefined,
      };
    } catch (err) {
      return NextResponse.json({ error: err instanceof Error ? err.message : "lookup failed" }, { status: 500 });
    }
  } else {
    if (!body.date || !body.title || !body.top_priority) {
      return NextResponse.json({ error: "missing date, title, or top_priority" }, { status: 422 });
    }
    payload = {
      date: String(body.date),
      title: String(body.title),
      top_priority: String(body.top_priority),
      url: typeof body.url === "string" ? body.url : undefined,
    };
  }

  const text = formatBriefPing(payload);
  const result = await sendTelegramMessage(text);

  // Best-effort log. Do not fail the request if logging fails.
  try {
    const sb = supabaseAdmin();
    await sb.from("delivery_logs").insert({
      channel: "telegram",
      brief_id: payload.brief_id ?? null,
      ok: result.ok,
      error: result.error ?? null,
      payload: { text, message_id: result.message_id },
    });
  } catch {
    /* swallow log errors */
  }

  if (!result.ok) return NextResponse.json({ error: result.error }, { status: 502 });
  return NextResponse.json({ ok: true, message_id: result.message_id });
}
