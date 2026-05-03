# Blueprint: Morning Brief

A self-deploying, agent-native morning brief. Sources collapse into one short ping plus one full write-up. Built for a single Sunday afternoon.

This is the canonical product spec. The runtime scaffold lives at `apps/morning-brief/`. Both halves of this blueprint should stay in sync. If you change the contract here, change it in `apps/morning-brief/src/lib/brief-contract.ts` too.

---

## Product promise

**The four-dimensional version (4D, accessible track).** Fork this repo, paste secrets into Vercel + Supabase + Telegram, deploy, and see your live morning brief at a Vercel URL. One delivery channel (Telegram). One schema (Supabase). One contract (JSON). One deploy path. Done by 6pm Sunday.

**The eight-dimensional version (8D, builder track).** Same baseline plus 2-3 additional sources, Slack or iMessage delivery alternates, scheduled cron runs, richer source status, and a custom connector if their business context supports it.

Both versions ship the same schema, the same JSON contract, and the same Vercel app surface. The only difference is how many knobs the student turns.

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
| Vercel deploy | required | required |
| Supabase backend | required | required |
| Telegram delivery | required | required |
| Manual notes source | required | required |
| Calendar source | optional | required |
| Gmail / Slack / YouTube source | skip | pick at least 2 |
| Scheduled cron run | skip | required |
| Slack or iMessage alternate delivery | skip | optional, recommended |
| Custom connector or repo scan | skip | optional, recommended |

---

## Test checklist

Run these in order. If any step fails, fix it before moving on.

- [ ] `supabase/0001_morning_brief.sql` applied. `briefs` table exists.
- [ ] Vercel deploy succeeds. Homepage loads at the Vercel URL.
- [ ] `POST /api/briefs` accepts a payload that matches `brief-contract.json` and returns `{ ok: true, brief: ... }`.
- [ ] The new brief shows up on the homepage on refresh.
- [ ] `POST /api/deliver/telegram` with a known brief id returns `{ ok: true }`.
- [ ] The Telegram message lands in the right chat.
- [ ] `delivery_logs` has a row for that ping.
- [ ] Refresh the homepage. The delivery log card shows the new entry.

If all eight pass, you have a working capstone.

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
