# Extensions: 8D Track

If your 4D capstone is live and the smoke test passed, you can pick from any of these. Each is independent. Pick what fits your business.

---

## Extension A. Wire 2-3 real sources

The scaffold ships with a single "manual-notes" source. Real value comes from automated pulls.

### Calendar

- Pull events for the next 24 hours from Google Calendar via the `gws` CLI or the Calendar MCP.
- Drop them into `source_status` as `{"name":"calendar","enabled":true,"last_pulled_at":"...","item_count":N}`.
- Surface the top 3 events in a `sections` block titled "Today's calendar".

### Gmail

- Pull unread emails from priority threads (label or starred).
- Summarize each in one sentence. Add to a "Inbox top" section.
- Be careful with PII. Don't log email bodies into Supabase unless you're scoping access.

### YouTube transcripts

- Pull from the YouTube transcript pipeline at `automations/youtube-pipeline/` (if you have it set up).
- Summarize new transcripts that landed since the last brief.
- Add a "What I should watch" section.

### Slack channels you read every morning

- Use `slack-cli conversations.history` to pull recent messages from one or two channels.
- Summarize the last 12 hours.
- Add a "Slack temperature" section.

---

## Extension B. Alternate delivery channels

The default is Telegram. You can add (not replace) other channels.

### Slack incoming webhook

- Create a Slack app, add an Incoming Webhook to your target channel.
- Add a route at `apps/morning-brief/src/app/api/deliver/slack/route.ts` that mirrors the Telegram one.
- Store `SLACK_WEBHOOK_URL` in Vercel env.

### iMessage (Mac-only)

- Requires a Mac that's always on and authenticated. Not Vercel-friendly.
- Pattern: Vercel cron triggers a webhook on your Mac (via Tailscale or ngrok), the Mac runs an AppleScript to send the iMessage.
- See `~/CLAUDE.md` for the AppleScript template AIBL uses.

### Email

- Use Resend, Postmark, or Supabase's Edge Functions + an SMTP provider.
- Add a route at `apps/morning-brief/src/app/api/deliver/email/route.ts`.
- Requires a verified sender domain.

---

## Extension C. Scheduled runs

Make the brief generate itself every morning.

### Vercel Cron (simplest)

- Add a `crons` block to `vercel.json`:
  ```json
  "crons": [{ "path": "/api/cron/build-brief", "schedule": "0 11 * * *" }]
  ```
- Create `apps/morning-brief/src/app/api/cron/build-brief/route.ts` that:
  1. Compiles sources (calls your source pulls).
  2. Calls Claude (via the Anthropic API) to generate the JSON brief.
  3. POSTs it to `/api/briefs`.
  4. Calls `/api/deliver/telegram` with the new brief id.

### GitHub Actions (more control)

- A scheduled workflow at `.github/workflows/morning-brief.yml`.
- Runs the same compile-then-POST flow, but on GitHub's runners.
- Useful if your sources require credentials Vercel can't hold.

---

## Extension D. Richer source status

The minimum scaffold ships a flat list. Upgrade it.

- Add a `last_error` field per source. Surface failed sources in red on the homepage.
- Add a `next_pull_at` so students can see when the next sync runs.
- Add a `count_delta` (today vs yesterday) so they spot dead sources fast.

---

## Extension E. Custom connectors / existing-repo scan

If you have a repo or a database that defines your morning, build a connector for it.

- Pattern: a single file at `apps/morning-brief/src/lib/sources/<name>.ts` that exports `pull(): Promise<{ items, lastPulledAt }>`.
- Wire it into your cron handler.
- Examples worth building: a Linear pull, a Notion database query, a custom CRM scan, a git-log-of-yesterday reader for solo developers.

---

## Extension F. Auth and multi-tenant

The 4D scaffold has open-read on briefs. That's fine for a single user. If you ship to a team:

- Enable Supabase Auth.
- Replace the open-read RLS policies with `auth.uid() = owner_id` patterns.
- Add an `owner_id` column to `briefs` and `delivery_logs`.
- Update `lib/supabase.ts` to use a per-user JWT instead of the service role key.

---

## When to stop

These are extensions, not requirements. Pick one or two that solve a real morning problem you have. Ship those. Don't build all six. The 4D capstone is already a working product.
