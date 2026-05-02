---
title: Free morning-brief delivery - 4 paths that don't add another paid tool
status: workshop-ready
audience: Cohort 1 students who don't want to pay for Vercel + Supabase
prereqs: Component 8 (Daily Briefing skill), Component 10 (Delivery Channels)
---

# Free morning-brief delivery - 4 paths that don't add another paid tool

The Sunday capstone path is a morning brief surface built with Vercel and Supabase. Both have free tiers that are enough for a personal morning brief, so this does not need to add another bill for most students.

This guide is the fallback menu. Use it if you want the short ping and full brief without setting up a hosted dashboard during the workshop.

Here are 4 paths that get the same outcome (your morning brief delivered somewhere you'll actually read it) without adding another bill.

Pick the one that matches your existing stack. Some require no new accounts.

---

## Path 1 — Slack DM only (zero infrastructure)

**Best for:** anyone who's already in Slack hourly. The default for most people.

**What you do:**

1. Your daily-briefing skill (Component 8) writes the brief to a markdown file at `~/Documents/second-brain/daily-briefs/<YYYY-MM-DD>.md` (you do this already)
2. Same skill, last step: `slack-cli chat post <YOUR_DM_CHANNEL_ID> "$(cat <brief-file>)"` posts it to your own DM channel in Slack

**Cost:** $0. Slack free tier is fine.

**How to find your DM channel ID:**

```bash
slack-cli conv list --json | jq -r '.[] | select(.is_im == true and .user == "<your-user-id>") | .id'
```

Pin the post each morning so it's at the top of the conversation.

**Limitation:** Slack free tier hides messages older than 90 days. If you want a permanent archive, ALSO write to the local file (which you're doing already).

---

## Path 2 — Telegram bot to your own channel (5 min setup, free forever)

**Best for:** anyone who's not in Slack. Works on iOS / Android / desktop. Push notifications are first-class.

**What you do:**

1. **One-time setup:** DM `@BotFather` on Telegram, type `/newbot`, follow the prompts. You get a bot token. Save it to 1Password or a `.env`.
2. Find your own Telegram chat ID by DMing `@userinfobot` on Telegram (returns your numeric ID).
3. Your daily-briefing skill last step:

   ```bash
   curl -s -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
     -d "chat_id=<YOUR_CHAT_ID>" \
     -d "parse_mode=Markdown" \
     --data-urlencode "text@$(cat <brief-file>)"
   ```

**Cost:** $0. Telegram bot tier is unlimited.

**Bonus:** Telegram supports Markdown rendering, so your brief actually looks like a brief. Inline links work. Code blocks work.

**Limitation:** No web view (it's a chat thread, not a dashboard). If you want a dashboard, see Path 3 or 4.

---

## Path 3 — Cloudflare Tunnel + local SQLite + a static HTML brief (1 hour setup, $0/month)

**Best for:** people who want a real dashboard URL but don't want a paid hosting bill. You serve the brief from your own Mac.

**What you do:**

1. **One-time setup:**

   ```bash
   brew install cloudflared
   cloudflared tunnel login                    # opens browser, auth your CF account
   cloudflared tunnel create my-brief          # creates tunnel
   cloudflared tunnel route dns my-brief brief.<your-domain>.com
   ```

   You need a Cloudflare account (free) and one domain you own. If you don't have a domain, register one for $10/yr at Cloudflare Registrar (cheapest TLD is `.com` at ~$10/yr; `.click` and similar are <$5/yr).

2. **Local server:** Use Python's built-in HTTP server, or a tiny Node script, or `http-server` from npm. Simplest:

   ```bash
   cd ~/Documents/second-brain/daily-briefs/
   python3 -m http.server 8080
   ```

3. **Render the brief as HTML:** Your daily-briefing skill does the markdown → HTML conversion, writes `index.html` next to the markdown. Use `pandoc` or `marked` from npm.

4. **Wire the tunnel to the local server:**

   ```bash
   cloudflared tunnel run my-brief --url http://localhost:8080
   ```

   Add it as a launchd job so it runs at login.

5. Visit `https://brief.<your-domain>.com` from anywhere on the internet.

**Cost:** $0/month (Cloudflare Tunnel free tier is generous). Possibly $10/year if you don't already own a domain.

**Limitation:** Your Mac has to be running for the URL to work. If your Mac is off or asleep, the URL is dead. Acceptable trade-off if your Mac is on most of the time.

**Bonus:** SQLite layer optional. If you want a queryable brief history, add a tiny Python script that reads the markdown files and serves them as a JSON API on `localhost:8080/api/briefs`. Then your HTML can be a real dashboard with filters.

---

## Path 4 — PocketBase on your Mac + Tailscale Funnel (the "real backend" path, $0/month)

**Best for:** people who want a real database + auth + REST API + admin UI but refuse to pay Supabase.

**What is PocketBase:** Single-binary backend (Go-based, ~30MB), gives you SQLite + REST API + admin UI + auth + file uploads in one process. https://pocketbase.io

**What you do:**

1. **One-time setup:**

   ```bash
   # Download for your platform from https://pocketbase.io
   ./pocketbase serve --http=0.0.0.0:8090
   ```

2. **Schema:** Create a "briefs" collection in the admin UI at `http://localhost:8090/_/`. Fields: `date` (date), `markdown` (text), `html` (text), `summary` (text).

3. **Your daily-briefing skill** POSTs to `http://localhost:8090/api/collections/briefs/records` with the day's brief.

4. **Expose via Tailscale Funnel** (you have Tailscale running already if you took Component 11):

   ```bash
   tailscale funnel --bg --https=443 --set-path=/ http://localhost:8090
   ```

   Now `https://<your-machine>.tailc3e7f5.ts.net/` serves your PocketBase UI to the internet.

5. **Build a static HTML reader** that consumes the PocketBase REST API. Or skip it and just bookmark the admin UI at `https://<your-machine>.tailc3e7f5.ts.net/_/`.

**Cost:** $0/month.

**Limitation:** Same as Path 3 — your Mac has to be running. Plus Tailscale Funnel has a 100GB/month bandwidth limit on the free tier (you will not hit this with text briefs).

**Bonus:** Real backend. Real database. Real auth. Add more collections as you grow your second brain (decisions, ideas, projects, daily reviews, etc.). When you outgrow the Mac, lift PocketBase to any $5/mo VPS unchanged.

---

## Comparison table

| Path | Setup time | Monthly cost | Phone notifications | Web dashboard | Database | Survives Mac off |
|---|---|---|---|---|---|---|
| 1. Slack DM only | 5 min | $0 | Yes (Slack app) | No | No | Yes (Slack hosts) |
| 2. Telegram bot | 5 min | $0 | Yes (Telegram) | No | No | Yes (Telegram hosts) |
| 3. Cloudflare Tunnel + static HTML | 1 hour | $0 (or $10/yr domain) | No | Yes | Optional SQLite | No (Mac must be on) |
| 4. PocketBase + Tailscale Funnel | 1 hour | $0 | No | Yes | Yes | No (Mac must be on) |

---

## What we recommend by user type

| You are... | Use Path |
|---|---|
| In Slack all day | 1 (Slack DM) |
| Phone-first | 2 (Telegram bot) |
| Want a real URL to share | 3 (Cloudflare Tunnel) |
| Building toward a real personal app | 4 (PocketBase) |
| Just want to start | 1, then upgrade later |

---

## Tyler's setup (for reference, not prescription)

Tyler runs **The Lookout** at `the-lookout.vercel.app` (Vercel + Supabase, paid). It's the right answer for him because:

- The brief is shared with Sara + Wade + the team
- It needs to be reliably up 24/7 (Mac Studio reboots happen)
- The Vercel hobby tier was free when he started, then he upgraded as the team grew

For a single user (you), Paths 1-4 are all better trade-offs than what Tyler runs. The Lookout is a team tool. You probably don't need a team tool yet.

---

## How to upgrade later

You can move between paths without losing anything because the source-of-truth is always the local markdown file at `~/Documents/second-brain/daily-briefs/<YYYY-MM-DD>.md`. The delivery layer is interchangeable.

Common upgrade paths people take:

- Path 1 → Path 2 (when you stop opening Slack on weekends)
- Path 2 → Path 3 (when you want to share a URL with a friend)
- Path 3 → Path 4 (when you want to add other collections beyond the brief)
- Path 4 → Hosted Vercel + Supabase (when you have a team that needs it)

Each upgrade is "add the new path, keep the old one running, move when ready, retire the old one." No flag day.

---

## What this guide does NOT cover

- **Email-only delivery.** We didn't include a Path 5 because most people who want a brief don't want one more email. If you do, the gws CLI from Component 6 can send it to yourself.
- **iCloud Notes / Apple Notes delivery.** Possible via AppleScript but Apple Notes is a poor reading experience for daily briefs.
- **Custom mobile push.** Possible via Pushover, ntfy.sh, or a custom iOS Shortcut hitting an HTTP endpoint. Out of scope for v1; ask in cohort Slack if you want help.

---

*Pick one path. Set it up tonight. Tomorrow morning your brief lands in the place you actually look. That's the win.*
