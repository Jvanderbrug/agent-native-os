# Guide 07 — Custom Commands (Slash Commands)

**When we cover this:** Install Block Two: Custom Commands + Second Brain (12:15 PM CDT, 1:15 PM EDT, right before the co-working block). See the README for the full agenda.

---

## What Are Custom Commands?

When you type `/exit` in Claude Code, something happens immediately. That's a built-in slash command.

You can build your own.

Custom commands are reusable instructions you give Claude once and then trigger with a short `/name` command. Instead of typing the same detailed prompt over and over, you write it once and invoke it with one word.

---

## Slash Command vs Skill (Important Distinction)

Claude Code has two related but distinct concepts that often get confused. You should know which one you're building.

| | Slash Command | Skill |
|---|---|---|
| **Lives at** | `~/.claude/commands/foo.md` | `~/.claude/skills/foo/SKILL.md` (or `~/.claude/skills/foo.md`) |
| **Triggered by** | You type `/foo` explicitly | Claude auto-invokes when your request matches the skill's `description` |
| **Format** | Plain markdown, no frontmatter required | YAML frontmatter required (`name`, `description`) |
| **Use when** | You want a named shortcut you remember and run on demand | You want Claude to *automatically* reach for this capability when the situation calls for it |

### Slash Command Example

`~/.claude/commands/morning.md`:

```markdown
# Morning Briefing

Pull today's calendar from Google Calendar, my Gmail since 5pm yesterday,
and my Obsidian inbox. Give me a one-page brief with my top 3 priorities.
```

You invoke it by typing `/morning` in Claude Code.

### Skill Example

`~/.claude/skills/meeting-prep/SKILL.md`:

```markdown
---
name: meeting-prep
description: Research a person or company before a meeting. Use when the user mentions an upcoming call, meeting, intro, or first conversation with someone, or asks "what should I know about X before we meet."
---

When invoked:
1. Search Obsidian for any prior notes on this person or their company.
2. Search Gmail for the last 30 days of threads with them.
3. Pull the relevant calendar event for context (attendees, agenda).
4. Draft 3 good questions to ask, grounded in what you found.
```

You don't type `/meeting-prep`. You just say "I have a call with David at Summit Capital tomorrow, prep me." Claude reads the skill's `description`, recognizes the match, and invokes the skill automatically.

### Which to Use When

- **Pick a slash command** when *you* want to be the trigger. Daily briefings, weekly reviews, "draft an email reply to this," "summarize this." Anything where you'll deliberately type `/name`.
- **Pick a skill** when you want Claude to *notice the situation* and reach for the capability without being told. Meeting prep, research-before-pitching, "always lint before committing," "always cite sources when answering factual questions."

The rest of this guide focuses on slash commands because they're the simpler starting point. We'll touch skills again in later guides.

**Before custom commands:**
```
> Check my email inbox for anything urgent, look at my calendar for today, check my Obsidian inbox for any unprocessed items, and give me a morning briefing with priorities
```
(Type this every single morning)

**After custom commands:**
```
> /morning
```
Same result. One word.

---

## How Custom Commands Work

Custom commands are stored as `.md` files in a specific folder: `~/.claude/commands/`

Each file is one command. The filename becomes the slash command.

A file named `morning.md` → triggers with `/morning`
A file named `weekly-review.md` → triggers with `/weekly-review`

The content of the file is the prompt Claude runs when you trigger the command. It can be as simple or complex as you want — and it has full access to all your MCP servers, your CLAUDE.md, everything Claude Code normally has access to.

---

## Creating Your First Custom Command

Let's build the morning briefing command together.

### Step 1: Create the Commands Folder

```bash
mkdir -p ~/.claude/commands
```

### Step 2: Create the Command File

```bash
# Mac
open ~/.claude/commands/

# Windows (WSL2)
code ~/.claude/commands/
```

Create a new file called `morning.md` with this content:

```markdown
# Morning Briefing

Run my morning briefing. Here's what to include:

1. **Today's date and day of week**

2. **Calendar** — Pull today's events from Google Calendar (via MCP). List them in time order with start times. Flag any conflicts.

3. **Email Triage** — Check Gmail for anything that arrived since yesterday at 5 PM. Categorize as:
   - Urgent (needs response today)
   - Important (response this week)
   - FYI (no response needed)
   List only the urgent and important ones with a one-sentence summary.

4. **Obsidian Inbox** — Check my Obsidian inbox folder. List any unprocessed notes.

5. **Today's Top 3** — Based on everything above, suggest my top 3 priorities for the day. Be specific and actionable.

Format: Use headers and bullets. Keep it scannable. Total length should be under one page.
```

### Step 3: Use It

```bash
claude
```

```
> /morning
```

Claude will run through each step, pulling from your real calendar and email (via MCP servers), and deliver your briefing.

---

## Building a Second Command: Weekly Review

Create `~/.claude/commands/weekly-review.md`:

```markdown
# Weekly Review

Run my weekly review. Today is {date}.

**Step 1 — Capture Loose Ends**
Check my Obsidian inbox for anything unprocessed. List what's there.

**Step 2 — Review Last Week**
Look at my Google Calendar for last week (Mon–Fri). What was I actually doing? Note any patterns.

**Step 3 — Projects Status**
Read my Obsidian Projects folder. For each active project, give me a one-sentence status.

**Step 4 — Email Backlog**
Are there any emails in my Gmail that I've left unresponded for more than 3 days? List them.

**Step 5 — Plan Next Week**
Based on everything above, suggest 3–5 priorities for the coming week. Don't just echo my calendar — tell me what actually needs attention.

**Format:** Present this as a structured review I can read in 5 minutes. Use headers. Be concise.
```

---

## Command Variables

Commands can include dynamic elements. Claude handles these naturally — just write your command using plain language that refers to things Claude has access to.

**Date references work automatically:**
```markdown
Check my calendar for this coming {weekday}...
```

**You can ask for input:**
```markdown
# Meeting Prep

I'm about to meet with {name}. Before we start:
1. Search my Obsidian for any notes about this person or their company
2. Check my email for any recent threads with them
3. Pull up my calendar to show what we've talked about before
4. Give me 3 good questions to ask based on what you find
```

When you trigger this with `/meeting-prep`, Claude will prompt you for `{name}` and then run the research.

---

## Command Ideas for Common Business Roles

**For anyone:**
- `/morning` — Daily briefing
- `/weekly-review` — Weekly review
- `/draft-email` — Draft a reply to the email I'm about to paste
- `/summarize` — Summarize the content I'm about to paste

**For operators/managers:**
- `/team-update` — Pull info and draft weekly team update
- `/project-status` — Status report on all active projects
- `/decision` — Help me think through a decision (paste the situation)

**For sales/BD:**
- `/meeting-prep` — Research a person before a call
- `/follow-up` — Draft a follow-up email after a meeting I'll describe
- `/proposal-outline` — Build a proposal outline for an opportunity I'll describe

**For content creators:**
- `/content-brief` — Create a brief for a piece I describe
- `/repurpose` — Take this content and repurpose it for [format]
- `/post-week` — Plan this week's content calendar

---

## Tips for Great Commands

**Be specific about the output format.**
Don't just say "give me a summary." Say "give me a bullet-point summary, 5 bullets max, each one a single sentence."

**Include what NOT to do.**
"Do not include pleasantries or preambles. Start directly with the content."

**Reference your CLAUDE.md.**
Claude already has your context, but you can reinforce key things in the command: "Remember I prefer options over recommendations for decisions like this."

**Iterate.**
Your first version of a command probably won't be perfect. Use it a few times, notice what's missing or annoying, edit the file. The file is just text — tweak it anytime.

---

## Organizing Multiple Commands

As you build more commands, keep a note in your CLAUDE.md about what commands you have:

```markdown
## My Custom Commands

| Command | What It Does |
|---------|-------------|
| /morning | Daily briefing: calendar + email + Obsidian inbox |
| /weekly-review | Weekly review across all my tools |
| /meeting-prep | Research a person/company before a call |
| /draft-email | Draft an email reply |
```

You can also ask Claude to list your commands:
```
> What custom commands do I have set up?
```
Claude will look in `~/.claude/commands/` and list them.

---

## What You Just Built

- A `~/.claude/commands/` folder with your reusable commands
- At least one command (`/morning`) that actually does something useful
- The pattern for building more commands for any repetitive task you have

---

## Track Exercises

See `tracks/[your-track]/exercises.md` — Exercise Set 07.

---

*Lunch break — back at 2:00 PM EDT*

*Next up: Guide 08 — Connecting Your World*
