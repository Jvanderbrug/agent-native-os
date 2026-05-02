# Component 9: Scheduling

> **⚠️ PROVISIONAL DRAFT — NOT FROM SARA'S WALKTHROUGH**
>
> This was written speculatively before Sara walked through scheduling as a student. It's a structural strawman based on Component 8's pattern, NOT lived experience. Real friction, real gotchas, and real decisions will replace it after Sara does the setup herself.
>
> Use it only as: (a) a checklist of what we *think* will come up, and (b) a structural skeleton to compare against once we have the real story.

## What you're about to build

Component 8 gave you a `/morning-brief` you can fire on demand. Component 9 makes it fire **without you** — at 6am, while you're still asleep, so the brief is waiting in your Obsidian vault when you sit down with coffee.

This is the moment Claude Code stops being something you open and starts being something that runs in the background of your life. You go from "tool you reach for" to "agent that's already done the work."

By the end of this component you'll have:
- A **scheduled job** on your Mac that runs `/morning-brief` automatically at the time you choose
- A **brief in your Obsidian vault** every morning before you wake up
- A way to **pause, change, or delete** the schedule whenever you want

> **Note:** This component is Mac-only. The tool we use (launchd) is the macOS native scheduler. Windows and Linux students should flag this — there's a different tool on each (Task Scheduler on Windows, cron on Linux). Same idea, different commands.

---

## The architecture (in one picture)

```
   YOUR MAC                          OBSIDIAN VAULT
   ────────                          ──────────────
   launchd                           daily-briefs/
       │                                │
       ↓ (at 6:00 AM)                   │
   Claude Code (headless)               │
       │                                │
       ├─ Reads briefing-config.md      │
       ├─ Pulls Gmail / Calendar / Exa  │
       ├─ Compiles the brief            │
       └─ Writes the markdown ─────────→  YYYY-MM-DD-brief.md
```

**launchd** is the part of macOS that runs jobs on a schedule. You give it a small config file describing *what to run* and *when*, and it handles the rest. It's what Apple uses internally to schedule everything — Time Machine backups, Spotlight indexing, the lot. It's been on every Mac for 20 years.

You're not going to write the config file by hand. You're going to **ask Claude to write it for you** — that's the whole point of agent-native work.

---

## Before you start

Make sure you've completed:
- **Component 8** — `/morning-brief` works when you run it manually
- **Component 2** — Obsidian vault set up, with a folder for your briefs
- Component 8's brief saves to your **Obsidian vault**, not to Google Drive

> **If your Component 8 brief saves to Drive, change it to Obsidian first.** Cloud destinations require valid OAuth tokens at run time, which can fail silently when the brief runs at 6am with no one watching. Local Obsidian writes are bulletproof. (You can still send the brief to Drive *after* it's written — that's Component 10's territory.)

You'll also need:
- Your Mac plugged in or on battery overnight (the schedule won't run if the Mac is fully shut down)
- About 5 minutes of "Allow Full Disk Access" setup — explained in Step 2

---

## Step 1: Decide when you want the brief to run

Pick a time the brief should be ready. Most students pick somewhere between **5:30 AM and 7:00 AM** — early enough that it's done before you wake up, late enough that overnight news has settled.

Two questions to answer:

1. **What time?** (e.g., 6:00 AM)
2. **Which days?** (every day, or weekdays only?)

Write your answer down. You're about to tell Claude.

---

## Step 2: Grant Claude Code "Full Disk Access"

This is a one-time macOS security step. Without it, scheduled jobs can't write to protected folders (which includes most of your Obsidian vault locations).

1. Open **System Settings → Privacy & Security → Full Disk Access**
2. Click the **+** button
3. Navigate to **Applications → Utilities → Terminal** and add it
4. Also add **Claude Code** if it appears in the list
5. Restart Terminal after granting access

> **Why this is needed:** macOS treats scheduled jobs as a security risk by default. Full Disk Access tells the OS "yes, I really do want this scheduled job to write files for me." You only do this once.

---

## Step 3: Tell Claude to set up the schedule

This is the agent-native part. You don't write the config — you describe what you want.

In a Claude Code session, type:

> "Set up a launchd job on my Mac to run my /morning-brief command every weekday at 6:00 AM. Save the plist file to ~/Library/LaunchAgents/ with a name like com.aibuildlab.morning-brief.plist. The job should call Claude Code in headless mode and run the same prompt that's in ~/.claude/commands/morning-brief.md. Make sure the brief output lands in my Obsidian vault at [your vault path]/daily-briefs/. After you create the plist, give me the exact `launchctl` command to load it, and a separate command to unload it later if I want to change anything."

Claude will:
- Write the plist file (an XML config that launchd reads)
- Tell you the load command (something like `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.aibuildlab.morning-brief.plist`)
- Tell you the unload command for later
- Confirm the schedule when you run the load command

**Run the load command Claude gave you.** That activates the schedule.

---

## Step 4: Test the schedule (don't wait until tomorrow)

You don't want to wait until 6am to find out if it works. Two ways to test now:

### Option A — Force a run right now

Ask Claude:

> "Run the launchd job for com.aibuildlab.morning-brief.plist immediately so I can verify it works."

Claude will give you the command (`launchctl kickstart gui/$(id -u)/com.aibuildlab.morning-brief`). Run it. Wait 30-60 seconds. Then check your Obsidian vault — a brief should appear with today's date.

### Option B — Schedule it 2 minutes out

If you'd rather see the actual scheduling fire, ask Claude to temporarily change the schedule to 2 minutes from now, reload, watch it fire, then change it back to 6am.

Either way: **don't trust the schedule until you've seen it actually produce a brief.**

---

## Step 5: Verify it ran tomorrow morning

Tomorrow at 6:00 AM your brief should appear automatically. When you wake up:

1. Open Obsidian
2. Navigate to your `daily-briefs/` folder
3. Look for a file with today's date

If it's there, you're done. The agent ran while you slept.

If it's not there, jump to "Common issues and fixes" below.

---

## Step 6: Iterate (this is where it actually becomes useful)

The schedule is the easy part. The brief itself will keep getting better. After a week of automatic runs, you'll notice patterns:

- "I never read the topic updates section" → tune the config to drop that topic
- "I wish it included tomorrow's calendar too" → edit the slash command to pull the next 24 hours
- "The brief is too long to read at 6am" → add a length constraint
- "I want it 30 minutes earlier on Mondays" → edit the plist (or ask Claude to edit it)

**Schedule once, tune forever.** The brief is alive because you keep tuning it.

---

## Common issues and fixes

| Problem | Fix |
|---------|-----|
| Brief didn't appear in Obsidian this morning | Check `launchctl print gui/$(id -u)/com.aibuildlab.morning-brief` for the last exit status. If it failed, the error message will tell you what broke. |
| "Operation not permitted" error in the log | You skipped Step 2 (Full Disk Access). Add Terminal and Claude Code to Full Disk Access, restart Terminal, reload the plist. |
| Brief ran but is empty / says "no data" | Your MCP OAuth tokens expired. Open Claude Code, run `/mcp`, re-authenticate any service showing red. The schedule will work again next run. |
| Mac was asleep at 6am — nothing ran | launchd doesn't wake your Mac. Either leave it awake overnight, OR set System Settings → Battery → Schedule to wake at 5:55 AM. |
| Brief ran twice | You loaded the plist twice. Run the unload command once, then load again. |
| I want to pause the schedule for a week | Run the unload command. The plist file stays on disk; reload it when you're ready. |
| I want to delete the schedule entirely | Unload the plist, then delete the file from `~/Library/LaunchAgents/`. |
| I changed the plist file but the new schedule isn't taking effect | launchd reads the plist when you load it. After editing, run unload then load again. |
| I want a second briefing on a different schedule | Build a second plist file with a different name (e.g., `com.aibuildlab.evening-brief.plist`) pointing to a different slash command. They run independently. |

---

## What's next

- **Component 10 (Delivery channels):** sends the brief somewhere besides your vault — Slack DM, email, voice/TTS, even a NotebookLM-style podcast
- **Component 11 (Remote control):** lets you trigger or modify the brief from your phone
- **Component 12 (Progressive autonomy):** scales the agent's permissions safely as you trust it more

---

## Quick reference

| Question | Answer |
|----------|--------|
| Where does the schedule config live? | `~/Library/LaunchAgents/com.aibuildlab.morning-brief.plist` |
| Where does the brief land? | Your Obsidian vault → `daily-briefs/` folder |
| What if I want to change the time? | Ask Claude to edit the plist, then run unload + load |
| What if my Mac is asleep at run time? | launchd won't wake it. Set System Settings → Battery → Schedule to auto-wake before the run, or leave the Mac awake. |
| Does the schedule survive a restart? | Yes. launchd auto-loads `LaunchAgents/` on login. |
| Can I have weekday-only schedules? | Yes — the plist supports day-of-week filters. Tell Claude what days you want. |
| How do I see the last run's logs? | Ask Claude for the exact `launchctl print` command for your job. |
| Does this cost extra Claude API tokens? | Yes — each run uses your normal Claude Code session quota. Pro/Max plans cover this. |

---

## Glossary (Component 9)

| Term | What it means |
|------|---------------|
| **launchd** | The macOS native scheduler. Runs jobs at specific times, on a schedule, or in response to events. Apple uses it for everything from Time Machine to Spotlight. |
| **plist** | A small XML config file (Property List). It tells launchd what to run and when. You don't write these by hand — Claude does. |
| **Headless mode** | Running Claude Code without a terminal window — it does its work, writes the output, and exits. That's how scheduled jobs work. |
| **launchctl** | The command you use to load, unload, or trigger a launchd job. Three commands you'll use: `bootstrap` (load), `bootout` (unload), `kickstart` (force a run now). |
| **LaunchAgents folder** | `~/Library/LaunchAgents/` — where personal scheduled jobs live. Anything in this folder loads automatically when you log in. |
| **Full Disk Access** | A macOS security setting that lets a program read/write protected folders. Scheduled jobs need it to write to your Obsidian vault. |
| **OAuth token** | The "logged-in" credential that lets Claude Code talk to Gmail, Calendar, Drive, etc. Tokens can expire silently — re-authenticate via `/mcp` if your scheduled brief comes back empty. |

---

*Status: DRAFT v1 — Mac-native launchd path per Tyler's Playbook. Scheduling fork (cloud Routines vs. local launchd) captured in [TYLER-ALIGNMENT-scheduling.md](../sara-teaching-prep/TYLER-ALIGNMENT-scheduling.md). Windows/Linux paths and the Routines alternative not yet drafted.*
