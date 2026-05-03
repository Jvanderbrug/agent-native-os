// Minimal Telegram Bot API client. Sends a single text message.
// Ref: https://core.telegram.org/bots/api#sendmessage

export type TelegramSendResult = {
  ok: boolean;
  message_id?: number;
  error?: string;
};

export async function sendTelegramMessage(text: string, opts?: { parseMode?: "Markdown" | "HTML" }): Promise<TelegramSendResult> {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) {
    return { ok: false, error: "telegram: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing" };
  }

  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  const body = {
    chat_id: chatId,
    text,
    parse_mode: opts?.parseMode,
    disable_web_page_preview: true,
  };

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const json = (await res.json()) as { ok: boolean; result?: { message_id: number }; description?: string };
    if (!json.ok) return { ok: false, error: json.description ?? "telegram: unknown error" };
    return { ok: true, message_id: json.result?.message_id };
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err.message : String(err) };
  }
}

// Format a brief as a short Telegram ping. Keep under 4096 chars.
export function formatBriefPing(input: { date: string; title: string; top_priority: string; url?: string }): string {
  const lines = [
    `🗞️ MORNING BRIEF / ${input.date}`,
    "",
    input.title,
    "",
    `⚡ Top priority: ${input.top_priority}`,
  ];
  if (input.url) lines.push("", `Read full: ${input.url}`);
  return lines.join("\n");
}
