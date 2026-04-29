# Guide 09 — Autonomous Workflows

**When we cover this:** Install Block Four: Schedule the Fleet + First /build (2:45 PM CDT, 3:45 PM EDT). See the README for the full agenda.

---

## The Shift From Tool to System

Everything we've built so far requires you to start a session and ask for something. That's powerful. But there's a level beyond that: workflows that run on their own, on a schedule, without you doing anything.

This is the difference between an assistant and a **system.**

An assistant waits for you. A system runs while you sleep.

By the end of this session, you'll have at least one thing happening automatically on a schedule.

---

## The Concept: Scheduled Claude Sessions

On Mac and Windows, you can schedule any command to run automatically. When you schedule Claude Code to run a specific command, it executes your instructions without you touching anything.

The pattern is:
1. Write a command (like your `/morning` briefing)
2. Schedule it to run at a specific time
3. Have it deliver output somewhere you'll see it (Slack, email, Obsidian note)

---

## Mac: Using Launchd (or Cron)

Mac has two built-in schedulers. We'll use **cron** because it's simpler for what we're doing.

### What is Cron?

Cron is the Mac/Linux scheduler — it's been around for decades and it just works. You give it a command and a time pattern, and it runs that command on schedule.

Open your cron table:
```bash
crontab -e
```

This opens a text editor (probably nano or vim). A cron line looks like this:

```
0 8 * * 1-5 /path/to/command
```

The five numbers before the command mean: `minute hour day-of-month month day-of-week`

`0 8 * * 1-5` means: at 8:00 AM, every day that's Monday through Friday.

### Setting Up the Morning Briefing on Schedule

**Step 1: Create the scheduled script**

Create a file at `~/morning-briefing.sh`:

```bash
#!/bin/bash

# Load secrets (so op:// references work)
eval $(op signin --raw 2>/dev/null) 2>/dev/null || true

# Run Claude with the morning command and print output
/usr/local/bin/claude --no-color -p "/morning" 2>&1 | \
  tee ~/Documents/briefings/$(date +%Y-%m-%d).md
```

Make it executable:
```bash
chmod +x ~/morning-briefing.sh

# Create the briefings folder
mkdir -p ~/Documents/briefings
```

**Step 2: Add to cron**
```bash
crontab -e
```

Add this line (runs at 7:30 AM weekdays):
```
30 7 * * 1-5 /Users/yourname/morning-briefing.sh
```

**Step 3: Verify**
```bash
# Run the script manually first to make sure it works
~/morning-briefing.sh

# Check the output
cat ~/Documents/briefings/$(date +%Y-%m-%d).md
```

---

## Windows: Using Task Scheduler (or WSL2 Cron)

**Option 1: WSL2 Cron (Easiest)**

If your computer is always on (or you leave WSL2 running), you can use cron inside WSL2.

Start cron in WSL2:
```bash
# Make sure cron is installed
sudo apt install cron

# Start cron
sudo service cron start

# Add to cron (runs at 7:30 AM weekdays)
crontab -e
30 7 * * 1-5 /home/yourname/morning-briefing.sh
```

> Note: WSL2 cron only runs when WSL2 is actively running. If you close your terminal, it stops. For truly scheduled automation on Windows, use Task Scheduler.

**Option 2: Windows Task Scheduler**

1. Search for "Task Scheduler" in the Start menu
2. Click "Create Basic Task"
3. Name: "Morning Briefing"
4. Trigger: Daily, at 7:30 AM
5. Action: Start a program
6. Program: `C:\Windows\System32\wsl.exe`
7. Arguments: `-e bash /home/yourname/morning-briefing.sh`
8. Finish

This tells Windows Task Scheduler to start WSL2 and run your script every morning.

---

## Delivering Output Automatically

A morning briefing that writes to a file you have to remember to open is only half-useful. Better: have it deliver to you.

### Deliver to Slack

Update your morning briefing command to end with:
```
After generating the briefing, post it to my Slack #daily-briefing channel.
```

Claude will use the Slack MCP to post it. You'll see it in Slack when you open your phone.

### Deliver via Email

```
After generating the briefing, send it to me at [your email] with subject "Morning Brief [date]".
```

### Deliver to Obsidian Daily Note

```
After generating the briefing, create or update today's daily note in Obsidian at:
~/Documents/My Second Brain/Daily Notes/[today's date].md
```

---

## More Scheduled Workflow Ideas

**End-of-week summary (Friday 5 PM):**
```
30 17 * * 5 ~/weekly-summary.sh
```

What it does: Looks at the week's calendar, emails, and Notion projects. Drafts a summary. Posts to Slack or writes to a weekly notes file.

**Inbox zero push (Tuesday and Thursday 4 PM):**
```
0 16 * * 2,4 ~/inbox-triage.sh
```

What it does: Checks email for anything unanswered more than 48 hours. Lists them. Drafts suggested responses for your review.

**Content calendar reminder (Monday 9 AM):**
```
0 9 * * 1 ~/content-check.sh
```

What it does: Looks at your content calendar in Notion. Lists what needs to be written this week. Creates placeholder notes in Obsidian.

---

## Using n8n for More Complex Automation

For workflows that involve multiple steps, conditions, or external webhooks, **n8n** is a better tool than cron.

n8n is a workflow automation platform — think Zapier but self-hosted and more powerful. You can run it for free on your own computer or on a cheap cloud server.

Claude + n8n is a powerful combination:
- **n8n** handles the triggers, conditions, and multi-step flows
- **Claude** handles the thinking, writing, and decisions inside those flows

**Example n8n + Claude flow:**

1. **Trigger:** New form submission on your website
2. **n8n step:** Fetch the submission data
3. **Claude step:** Write a personalized response email based on the form content
4. **n8n step:** Send the email via Gmail
5. **n8n step:** Add the contact to your Notion CRM
6. **Claude step:** Decide if this lead is qualified, add a note

This runs automatically for every new form submission. You never touch it.

Setting up n8n is a full session on its own — we'll point you to the blueprint in `blueprints/` that walks through a complete n8n + Claude setup.

---

## The Autonomy Ladder

Think of autonomous workflows as a ladder:

**Rung 1 — You ask, Claude does (interactive)**
You type a request, Claude responds.

**Rung 2 — You trigger, Claude executes (command)**
You type `/morning`, Claude does the full workflow.

**Rung 3 — Scheduled, Claude executes (automated)**
Cron or Task Scheduler runs the command, Claude executes, output delivered to you.

**Rung 4 — Event-triggered, Claude executes (reactive)**
Something happens (new email, form submission, webhook), n8n detects it, Claude responds.

**Rung 5 — Multi-agent, continuous (fully autonomous)**
Multiple agents working together on ongoing tasks, Claude directing and executing.

You're currently moving from Rung 1 to Rung 3. Rungs 4 and 5 are the next frontier — and they're more accessible than they sound.

---

## A Word on Trust and Review

When Claude runs autonomously, you're not there to review each action. This makes the autonomy level in your CLAUDE.md critically important.

For scheduled tasks:
- Set up the workflow in Safe Mode first and run it manually a few times
- Verify the output is what you expected
- Only then move it to a schedule

For any autonomous workflow that sends messages or makes changes to real systems, build in a review step:
- Write the output to a file first
- Review the file
- Have a second command that actually executes (sends the email, posts to Slack)

Over time, as you trust specific workflows, you can remove the review step. But start cautious.

---

## What You Just Built

- At least one scheduled workflow that runs without you touching it
- Output delivered to a place you'll actually see it
- The mental model for the autonomy ladder

---

## Track Exercises

See `tracks/[your-track]/exercises.md` — Exercise Set 09.

---

*Next up: Guide 10 — Your Agent OS (Putting It All Together)*
