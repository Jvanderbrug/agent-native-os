---
description: Build the morning brief system — the Sunday capstone. Compiles a daily briefing from your sources, sends a short ping, and parks a full write-up where you can read it. Plain-language entry point; /build is the generic blueprint executor.
argument-hint: "[sources: gmail,calendar,slack,obsidian]"
---

You are running the Sunday capstone build: the user's morning brief system.

This command is the Sunday-facing, plain-language entry point. It is opinionated about *what* gets built (the morning brief) and unopinionated about *which sources* the user has wired up. The generic blueprint executor lives at `/build`.

## What this command builds

A morning brief system with three pieces:

1. **Sources** — pulled from whatever the user has connected (Gmail, Calendar, Slack, Obsidian, plus any others wired in later).
2. **Compile step** — a script or command that reads the sources, runs them through Claude, and writes a dated brief to disk.
3. **Delivery** — a short ping the user actually sees, plus a full write-up surface they can come back to.

The scaffold path for the generated app is:

```text
apps/morning-brief/
```

This is a placeholder. The Worker #5 build pass owns populating it. Do not scaffold Vercel, Supabase, or any web infrastructure here — that is out of scope for this command.

## Step 0: Read $ARGUMENTS

If the user passed arguments, treat them as a comma-separated source list. Valid sources:

- `gmail`
- `calendar`
- `slack`
- `obsidian`

Examples:

```text
/build-morning-brief gmail,calendar
/build-morning-brief gmail,calendar,slack,obsidian
/build-morning-brief
```

If no arguments are passed, ask the user which sources to enable. Do not assume all four.

If an unknown source is passed, list the valid ones and ask the user to choose.

## Step 1: Pick the path

Ask the user which path they are on:

- **4D path** — Obsidian-only output. No web deploy. The brief is a markdown file in the user's vault. Delivery is a local notification or email. Simplest possible build.
- **8D path** — Full web deploy. Brief is rendered on a hosted page (handled by a later worker). Delivery includes a link to the hosted brief.

If the user does not say, default to 4D.

Do not build any web infrastructure in either path inside this command. The 8D path simply records the intent so a later worker can pick it up.

## Step 2: Pick the delivery adapter

Check whether the capstone spec lock file exists:

```text
/Users/tyfisk/GitHub/agent-native-os-hq/launches/2026-04-28-summer-camp-and-lab/CAPSTONE-SPEC-LOCK-2026-05-02.md
```

- **If the file exists**, read it and use the delivery adapter it specifies. The spec lock is the source of truth — if it conflicts with the defaults below, the spec lock wins.

For the May 3 2026 Sunday cohort, the spec lock specifies Telegram bot as the delivery adapter. The defaults below apply only if the spec lock is removed.

- **If the file does not exist**, default to:
  - Primary delivery: **local macOS notification** (via `osascript -e 'display notification ...'` or `terminal-notifier`)
  - Alternate delivery: **email** (via the user's already-wired Gmail/SMTP setup, or a `mailto:` fallback if nothing is wired)

Do not require Slack, iMessage, or Telegram. Those are optional add-ons, not the default.

## Step 3: Confirm the build plan

Before writing any files, return a short plan in this shape:

```markdown
## Morning Brief Build Plan
- Path: 4D (Obsidian-only) or 8D (web deploy intent recorded)
- Sources enabled: <list>
- Compile script: <path inside apps/morning-brief/>
- Output location: <Obsidian vault path or apps/morning-brief/output/YYYY-MM-DD.md>
- Delivery: <macOS notification | email | spec-lock-defined>
- Auth the user must handle: <list, or "none">
- How we will test it: <one manual run command>
- Rollback: <one sentence>
```

Wait for approval before making changes unless the user explicitly says to proceed.

## Step 4: Execute in checkpoints

Build in this order. Stop at each checkpoint and confirm before moving on.

1. Create `apps/morning-brief/` and the minimal config files for the chosen sources.
2. Create the compile script that reads sources and writes a dated brief.
3. Wire the delivery adapter (notification or email).
4. Run the compile + deliver flow once, manually, end to end.
5. Only after the manual run succeeds, discuss scheduling with the user. Do not schedule inside this command.

Never schedule the brief before the manual test passes. Never write API keys in plaintext.

## Step 5: 4D vs 8D divergence

After the core build is working:

- **4D path:** Stop. The brief lands in Obsidian. The user opens it manually or via the notification. Done.
- **8D path:** Record the intent for the web deploy in `apps/morning-brief/README.md` so the next worker can pick it up. Do not scaffold the app, the database, or the deploy here.

## Step 6: Verify

A morning brief build is done only when:

- A brief file was generated and the user can open it.
- The delivery ping fired and the user saw or received it.
- The user knows the one command to run it again manually.
- No secrets are sitting in plaintext.

## Step 7: Hand off

Tell the user:

```text
Run /verify after to check your setup.
```

If `/log-decision` is installed, optionally offer to log the chosen path (4D vs 8D), source list, and delivery adapter.
