# Component 13: Skills Library

> **This is Block 13: Skills Library.**
>
> **What you'll have:** Three reusable commands: `/prep-for-meeting`, `/end-of-day`, and `/log-decision`. Together they prep context, close loops, and write durable memory into your second brain.
>
> **How this stacks toward the Capstone:** The Capstone is a morning brief system. These skills give Claude reusable patterns for context gathering, memory writing, and decision logging. `/build` uses those patterns to execute a blueprint, not to improvise from a blank page.
>
> **Why now:** Trust tiers are set (Component 12). Your agent knows what it's cleared for. Component 13 gives it more things to be capable of within that clearance. The Capstone is one step away.

---

## What you're building

The same pattern you used in Component 7 (Slash Commands) and Component 8 (Daily Briefing) — markdown files in `~/.claude/commands/` — but now with your full MCP stack doing real work:

1. **`/prep-for-meeting`** — Finds your next meeting, pulls recent email threads with attendees, researches them via Exa, delivers a one-screen prep brief in under 3 minutes of reading. Saves to `~/Documents/second-brain/meeting-prep/`.

2. **`/end-of-day`** — Reviews what happened today via calendar and inbox, surfaces what's still open, names your top 3 priorities for tomorrow. Saves to `~/Documents/second-brain/daily-reviews/`.

3. **`/log-decision`** — Captures a decision, the reasoning, reversibility, review date, and affected projects. Saves to `~/Documents/second-brain/decisions/` and updates `~/Documents/second-brain/cairns/L1/decisions-in-flight.md` when the Cairns starter structure exists.

---

## The install

### Step 1 — Create `/prep-for-meeting`

Save this to `~/.claude/commands/prep-for-meeting.md`:

````markdown
---
description: Prep brief for your next upcoming meeting — who's coming, relevant email history, context on the topic, what to bring up.
---

You are preparing [YOUR NAME] for their next meeting. They're about to walk into a call and need to be sharp in under 3 minutes of reading.

## Step 1 — Find the next meeting

Use the Calendar MCP to list events from now through the next 8 hours. Pick the next upcoming event that has at least one other attendee (skip solo blocks, focus time, reminders).

Extract:
- Meeting title, start time
- Attendee names and email addresses (excluding your own)
- Any description or notes on the event

## Step 2 — Pull context (in parallel)

**Gmail MCP** — search threads involving attendee emails from the last 30 days:
- Most recent exchange with each attendee
- Any open asks or unresolved threads

**Exa MCP** — search for each attendee or their company:
- Recent news, role changes, company updates

## Step 3 — Compile the prep brief

```markdown
# Prep Brief — [Meeting Title]
**[Time] with [Attendees]**

## Who's coming
One line per attendee — role, how you know them.

## Last contact
Most recent exchange. Any open threads.

## What they need from you
Pending asks, commitments you made.

## What you might bring up
1–3 hooks based on recent context or Exa findings.

## Watch out for
Anything sensitive or worth knowing before you join.
```

## Step 4 — Save

Save to: `~/Documents/second-brain/meeting-prep/[YYYY-MM-DD]-[meeting-slug].md`

If no upcoming meetings in 8 hours, say so in one line.
````

### Step 2 — Create `/end-of-day`

Save this to `~/.claude/commands/end-of-day.md`:

````markdown
---
description: End-of-day review — what happened today, what's unresolved, top 3 for tomorrow. Saves to Obsidian.
---

You are writing [YOUR NAME]'s end-of-day review. Short, honest, actionable.

## Step 1 — Gather today's data (in parallel)

**Calendar MCP** — list events that occurred today (start time before now):
- Which meetings happened
- Any that were declined or moved

**Gmail MCP** — scan today's inbox:
- Threads that arrived and still need a reply
- Anything that moved from pending to done

## Step 2 — Compile the review

```markdown
# End of Day — [Date]

## What happened
3–5 bullets. Meetings held, decisions made, things shipped.

## Still open
Anything needing follow-up. Be specific — who owes what.

## Tomorrow's top 3
Ranked. Bold the #1.

## One thing to let go of
Something that doesn't need to carry into tomorrow.
```

Under 250 words. No padding.

## Step 3 — Save

Save to: `~/Documents/second-brain/daily-reviews/[YYYY-MM-DD]-end-of-day.md`
````

### Step 3 — Create `/log-decision`

If you cloned this repo, the command already exists at:

```bash
configs/commands/log-decision.md
```

Install it globally:

```bash
mkdir -p ~/.claude/commands
cp configs/commands/log-decision.md ~/.claude/commands/log-decision.md
```

This command is the bridge from "Claude did work" to "Claude remembers what we decided." It writes a structured decision file and, if present, updates the L1 Cairns waypoint file.

### Step 4 — Test the skills

```bash
/prep-for-meeting
```

You should get a one-screen brief on your next meeting within 2–3 minutes. Check that the file appeared in `~/Documents/second-brain/meeting-prep/`.

At end of your workday:
```bash
/end-of-day
```

Check `~/Documents/second-brain/daily-reviews/`.

Then test the memory bridge:

```bash
/log-decision We are using the 4D track for baseline setup and 8D for advanced customization because the cohort has mixed technical readiness.
```

Check:

```bash
ls ~/Documents/second-brain/decisions/
cat ~/Documents/second-brain/cairns/L1/decisions-in-flight.md
```

---

## Why this pattern matters for the Capstone

Every skill you've built follows the same structure:
1. Gather context
2. Ask only the follow-up questions needed
3. Compile structured output
4. Save to a specific second-brain path
5. Report back what was done

When you run `/build` in the Capstone, Claude reads a blueprint and turns it into a working setup. Your skills library gives it examples of the local patterns it should reuse: where to save files, when to ask follow-up questions, how to handle sources, and how to report back.

You're not just adding capabilities. You're teaching your agent what "a skill" looks like.

---

## 4D vs. 8D path

| | 4D | 8D |
|---|---|---|
| **Starting point** | Copy Sara's templates, replace name and paths | Author skills from scratch for your specific workflow |
| **MCP usage** | Calendar + Gmail as shown | Add Notion, Slack, or custom data sources |
| **Output location** | Sara's Obsidian vault structure | Your own vault or note-taking system |
| **Third skill** | Install `/log-decision` | Extend `/log-decision`, or build a companion capture skill for scratchpad ingestion |

---

## What this unlocks

Your agent now has a growing capability library. It can prepare you for meetings, close out your day, brief you every morning, log decisions into memory, and take remote commands from your phone, all operating within the trust tiers you defined.

One component left: the Capstone. You use `/build` to execute the morning brief blueprint and make the pieces work together.
