# QUICKSTART: 4D Track

> Goal: live Vercel URL + Supabase-backed brief + working Telegram ping by 6pm Sunday.
> Estimated time: 35 minutes if accounts are ready, 60 minutes if you're starting cold.

Each step has a checkbox, an estimated duration, and a recovery line. Follow in order.

---

## [ ] Step 1. Fork the repo (3 min)

- Go to `github.com/aibuild-lab/agent-native-os` and click Fork.
- Clone your fork locally: `git clone <your-fork-url> && cd agent-native-os/apps/morning-brief`.
- Copy the env template: `cp .env.example .env.local`. Leave it open.

**If this fails:** make sure you're logged into the right GitHub account. Workshop students often have personal and work accounts crossed.

---

## [ ] Step 2. Create the Supabase project (8 min)

- Sign up at supabase.com if you haven't.
- Click New Project. Name it `morning-brief`. Pick the closest region. Set a strong DB password (you won't need to type it, but save it in 1Password).
- Wait for the project to provision (about 90 seconds).
- Open the SQL Editor. Paste the contents of `apps/morning-brief/supabase/migrations/0001_morning_brief.sql`. Click Run. You should see "Success. No rows returned."
- Optional: paste `apps/morning-brief/supabase/seed.sql` and Run, so the homepage shows demo briefs on first deploy.
- Settings -> API. Copy:
  - Project URL -> `SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_URL` in `.env.local`
  - anon public key -> `SUPABASE_ANON_KEY` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - service_role secret key -> `SUPABASE_SERVICE_ROLE_KEY`

**If this fails:** the SQL Editor returns errors when the database is still provisioning. Wait two minutes and retry.

---

## [ ] Step 3. Create the Telegram bot (5 min)

- Open Telegram. Search `@BotFather`. Tap Start.
- Send `/newbot`. Pick a display name. Pick a username ending in `bot` (e.g., `tyler_morning_brief_bot`).
- BotFather replies with your token. It looks like `123456789:ABCdef...`. Copy it into `.env.local` as `TELEGRAM_BOT_TOKEN`.

### [ ] Step 3a. Message your bot first (CRITICAL, 1 min)

- **Telegram bots cannot start a conversation. You must message the bot first.**
- Tap the link BotFather gave you, or search the bot username in Telegram.
- Send the bot any message. `hi` is fine.

### [ ] Step 3b. Get your chat id (2 min)

- In a browser, open: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
- Replace `<YOUR_BOT_TOKEN>` with the token from Step 3.
- You should see JSON. Find the path: `result[0].message.chat.id`. That number is your chat id.
- Copy it into `.env.local` as `TELEGRAM_CHAT_ID`.

**If `getUpdates` returns `{"ok":true,"result":[]}`:** you didn't actually send the bot a message. Go back to Step 3a.

**If you want the bot to post to a group chat:** add the bot to the group, send a message in the group with `@your_bot_name` mentioned, then re-run getUpdates. The chat id will start with a minus sign. That's normal for groups.

---

## [ ] Step 4. Deploy to Vercel (10 min)

- Push your fork: `git add .env.example && git commit -m "set up" && git push` (your `.env.local` is gitignored, so it stays local).
- Go to vercel.com/new. Import your fork.
- **Important: set the Project Root to `apps/morning-brief`.** Vercel asks during import. If you skip this, the build will fail.
- Framework preset should auto-detect as Next.js.
- Expand Environment Variables. Add every line from your `.env.local`:
  - `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
  - `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
  - For each variable, check Production, Preview, and Development.
- Click Deploy. Wait ~2 minutes.

**If the build fails with "Missing SUPABASE_URL":** you forgot to add the env vars. Project Settings -> Environment Variables. Add them, then click Redeploy.

---

## [ ] Step 5. Smoke test (5 min)

- Open your Vercel URL. The homepage should load with the field-manual aesthetic (paper background, 46px grid, lime accents).
- If you ran the seed, you should see a demo brief. If not, you should see "No briefs yet."

### Test the Telegram delivery:

```bash
curl -X POST https://<YOUR_VERCEL_URL>/api/deliver/telegram \
  -H "Content-Type: application/json" \
  -d '{"date":"2026-05-04","title":"hello from my morning brief","top_priority":"ship it"}'
```

- You should see `{"ok":true,"message_id":N}` in the response.
- Check Telegram. The bot should have sent you the ping.
- In Supabase, open the `delivery_logs` table. You should see one row with `ok=true`.

### Test the brief write:

```bash
curl -X POST https://<YOUR_VERCEL_URL>/api/briefs \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-05-04",
    "title": "my first real brief",
    "summary": "test summary",
    "top_priority": "ship the capstone",
    "sections": [{"heading": "Notes", "body": "It works."}],
    "source_status": [{"name": "manual-notes", "enabled": true, "last_pulled_at": null, "item_count": 1}],
    "delivery_status": {"channel": "telegram", "delivered_at": null, "recipient": null, "ok": false}
  }'
```

- You should see `{"ok":true,"brief":{...}}`.
- Refresh the homepage. The new brief should be at the top.

**If you got all five checkboxes:** your capstone is shipped. Take a screenshot of the live URL and post it in the workshop Slack.

---

## After Sunday

The slash command `/build-morning-brief` (when merged from its worker branch) walks Claude Code through compiling sources into the canonical JSON contract and posting it to your Vercel URL. Until then, hand-craft briefs using the shape in `brief-contract.json`.

For the 8D extensions (extra sources, scheduled runs, Slack alternate), see `EXTENSIONS-8D.md`.
