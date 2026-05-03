# Blueprint: Morning Brief

A self-deploying, agent-native morning brief. Sources collapse into one short ping plus one full write-up. Built for a single Sunday afternoon.

The canonical command file `configs/commands/build-morning-brief.md` is the source of truth for what the slash command actually builds. This README mirrors that command. The runtime scaffold lives at `apps/morning-brief/` for students who choose the 8D web deploy path. If you change the JSON contract here, change it in `apps/morning-brief/src/lib/brief-contract.ts` too.

---

## Product promise

**The four-dimensional version (4D, accessible track).** Run `/build-morning-brief` in Claude Code. Pick your sources. The brief lands as a markdown file in your Obsidian vault (or local folder). Delivery is a short ping via Telegram bot (per the May 3 2026 spec lock), or a local macOS notification or email if no spec lock is active. No web infrastructure required for 4D. Done by 6pm Sunday.

**The eight-dimensional version (8D, builder track).** Same baseline plus the full Vercel + Supabase web surface, 2-3 additional sources, Slack or iMessage delivery alternates, scheduled cron runs, richer source status, and a custom connector if your business context supports it. The `apps/morning-brief/` scaffold is provided so 8D students can deploy a hosted brief view.

Both versions ship the same JSON contract and the same delivery ping. 4D writes the brief locally. 8D adds the web surface on top.

---

## Architecture

```
┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│ Sources      │ -> │ Claude Code    │ -> │ Supabase    │
│ (manual,     │    │ /build-morning-│    │ briefs      │
│  calendar,   │    │ brief skill    │    │ sources     │
│  gmail, etc) │    │                │    │ delivery_log│
└──────────────┘    └────────────────┘    └─────┬───────┘
                                                │
                          ┌─────────────────────┴───────────────────┐
                          │                                          │
                    ┌─────▼──────┐                          ┌────────▼──────┐
                    │ Vercel App │                          │ Telegram Bot  │
                    │ (full      │                          │ (short ping)  │
                    │  read view)│                          └───────────────┘
                    └────────────┘
```

The student's machine runs `/build-morning-brief` in Claude Code. That skill compiles sources into the JSON contract and POSTs to `apps/morning-brief/api/briefs`. The route writes to Supabase. The same skill, or the homepage, can then trigger `apps/morning-brief/api/deliver/telegram` to fire the ping. The homepage at the Vercel URL shows the latest brief, the source registry, and the delivery log.

---

## 4D vs 8D split

| Capability | 4D | 8D |
|---|---|---|
| Local markdown brief in Obsidian or folder | required | required |
| Telegram delivery ping (May 3 spec lock default) | required | required |
| Manual notes source | required | required |
| Calendar source | optional | required |
| Vercel deploy of `apps/morning-brief/` | skip | required |
| Supabase backend | skip | required |
| Gmail / Slack / YouTube source | skip | pick at least 2 |
| Scheduled cron run | skip | required |
| Slack or iMessage alternate delivery | skip | optional, recommended |
| Custom connector or repo scan | skip | optional, recommended |

---

## Test checklist

Run these in order. If any step fails, fix it before moving on.

**4D path (required):**

- [ ] `/build-morning-brief` ran end to end without scaffolding Vercel or Supabase.
- [ ] A dated brief markdown file exists in your Obsidian vault or chosen output folder.
- [ ] `POST /api/deliver/telegram` (or the equivalent local script) sends a ping that lands in the right Telegram chat.
- [ ] You know the one command to run the brief again manually.
- [ ] No secrets are sitting in plaintext.

**8D path (additional):**

- [ ] `supabase/0001_morning_brief.sql` applied. `briefs` table exists.
- [ ] Vercel deploy succeeds. Homepage loads at the Vercel URL.
- [ ] `POST /api/briefs` accepts a payload that matches `brief-contract.json` and returns `{ ok: true, brief: ... }`.
- [ ] The new brief shows up on the homepage on refresh.
- [ ] `delivery_logs` has a row for that ping.
- [ ] Refresh the homepage. The delivery log card shows the new entry.

If the 4D checks pass, you have a working capstone. The 8D checks layer on top.

---

## File index for this blueprint

- `README.md` (this file): product promise, architecture, 4D/8D split, test checklist.
- `QUICKSTART-4D.md`: step-by-step deploy for the accessible track.
- `EXTENSIONS-8D.md`: extra sources, alternate delivery channels, scheduling.
- `brief-contract.json`: canonical JSON shape. Source of truth.
- `supabase/0001_morning_brief.sql`: schema. Mirrors the copy at `apps/morning-brief/supabase/migrations/0001_morning_brief.sql`.

---

## Spec lock reference

The decision to ship Option A (one Vercel app, one Telegram adapter, one schema, one contract) is locked in `~/GitHub/agent-native-os-hq/launches/2026-04-28-summer-camp-and-lab/CAPSTONE-SPEC-LOCK-2026-05-02.md`. Read that doc before proposing changes to scope.
