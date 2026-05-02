# Component 8: Daily Briefing Config

## What you're about to build

The daily briefing is the workshop's capstone build. You've connected the tools (Components 4-6) and you know how to turn a prompt into a slash command (Component 7). Now you combine those into the thing that sold you on agent-native work in the first place: **a briefing that writes itself overnight and waits for you in the morning.**

By the end of this component you'll have:
- A **briefing config file** that describes what you care about (people, topics, sources)
- A **`/morning-brief` slash command** that reads your config, pulls fresh content from Gmail, Calendar, Exa, and anything else you've connected, and writes a clean brief to your Drive or Obsidian vault
- A brief you can run *manually right now* -- scheduling comes in Component 9

> **Note:** In this component the brief is manual -- you type `/morning-brief` and it runs. Component 9 schedules it to run overnight. Component 10 adds fancy delivery (Slack, email, voice). Build the brains first, schedule and deliver later.

---

## The architecture (in one picture)

Every briefing follows the same shape:

```
   SOURCES          →     COMPILE          →     DELIVER
   ────────                ───────                ───────
   Gmail                   Executive summary       Google Doc in Drive
   Calendar                Priority actions        Markdown file locally
   Exa (web)               Calendar prep           Obsidian vault
   Firecrawl               Interesting finds       (later: Slack, email, voice)
   (your choices)
```

Three stages: **pull the raw inputs**, **make sense of them**, **drop the result somewhere you'll actually read it.**

Component 8 teaches you how to design all three for your own life.

---

## Before you start

Make sure you've completed:
- **Component 6** -- Gmail, Calendar, Drive MCPs connected (minimum)
- **Component 7** -- you know how to build a custom slash command
- **Optional but recommended:** Component 4 (Exa) for web research, Component 5 (Firecrawl) for specific sites you watch, Component 2 (Obsidian) if you want your briefs filed in your vault

The more MCPs you have connected, the richer your briefing can be. But don't hold up Component 8 waiting to connect more -- you can build a great brief with just Gmail + Calendar + Exa.

---

## Step 1: Design your briefing (the questionnaire)

Before you write any code or prompt, answer these five questions about *your* work. This is the config -- the thing that makes your brief different from anyone else's.

Create a file at `~/briefing-config.md` (or inside your Obsidian vault if you set one up) and fill it in. Use this template:

```markdown
# My Briefing Config

## People I Follow
- [name or @handle] -- [why they matter to you]
- [name] -- [why]

## Topics I Track
- [topic] -- [why]
- [competitor or industry signal] -- [why]

## Websites I Watch
- [URL] -- [what you look for there]

## Email Priorities
- **Flag immediately:** emails from [client/investor/key contact]
- **Summarize:** newsletters, receipts, scheduling noise
- **Ignore:** [automated sources you don't care about]

## Calendar Intelligence
- Flag meetings with new people (Claude preps context)
- Flag back-to-back conflicts and missing RSVPs
- Remind me about [specific deadlines or recurring prep]

## Output Format
- Length: [short / medium / full]
- Tone: [professional / casual / punchy]
- Where to save: [Google Drive folder / Obsidian vault / local file]
```

**Tips for filling it in:**
- Be specific. "Startup news" is too vague. "Funding announcements for competitors in my industry" is actionable.
- List real names, handles, URLs, and keywords -- not categories. Claude can't filter for "important people" without knowing who they are.
- Keep the config under one page. If you're writing an essay, you're overdesigning.

This file is your briefing's brain. Every time the brief runs, Claude reads it to know what matters to you.

---

## Step 2: Build the `/morning-brief` slash command

This is where Component 7's skill pays off. You're going to write a slash command that reads your config, pulls from your MCPs, and writes a brief.

Ask Claude:

> "Create a custom slash command called `/morning-brief` at `~/.claude/commands/morning-brief.md`. It should read my briefing config at `~/briefing-config.md`, then use Gmail, Calendar, and Exa to generate a daily brief that matches the format in the config. Save the brief to my Google Drive with today's date in the title."

Claude will create the file. It'll look something like this (the exact wording will vary):

```markdown
---
description: Generate today's daily brief based on ~/briefing-config.md and save to Drive.
---

You are writing Sara's daily brief for today.

## Step 1 -- Read the config
Read `~/briefing-config.md`. This defines the people, topics, and sources Sara cares about.

## Step 2 -- Pull sources
Based on the config, in parallel:
- Use Gmail MCP to check the inbox -- flag items matching "email priorities"
- Use Calendar MCP to list today's events + flag issues (conflicts, missing RSVPs, meetings with new people)
- Use Exa MCP to search for fresh news on the "topics I track"

## Step 3 -- Compile the brief
Structure as:
- Executive summary (5 bullets, what matters most today)
- Priority actions (what needs a response or decision)
- Calendar prep (meetings + context)
- Topic updates (news/research from Exa)
- Interesting finds (anything surprising)

## Step 4 -- Save to Drive
Create a Google Doc titled "Daily Brief -- YYYY-MM-DD" in the Drive root.
```

### Restart Claude Code

Quit completely (Cmd+Q) and relaunch. Custom commands only load on startup.

---

## Step 3: Run it for real

Type:

```
/morning-brief
```

Watch the tool calls. You'll see Claude hit Gmail, Calendar, Exa, and Drive in sequence. The first run usually takes 30-60 seconds.

Open the brief in your Drive. **Read it the way you'd read a human assistant's work** -- not the way you'd read your own draft. Is it what you needed? Missing anything? Too long? Irrelevant sections?

---

## Step 4: Iterate (this is the most important step)

The first brief is almost never right. Your config and prompt both need tuning. Don't skip this.

Three things to tune, in this order:

### 1. The config
If the brief is focused on the wrong things, the config is wrong. Add the topic that's missing. Remove the one that never matters. Be more specific about who counts as a "priority" sender.

### 2. The prompt (slash command)
If the *structure* is wrong -- too long, missing a section, bad format -- edit `~/.claude/commands/morning-brief.md` directly. Add specifics:
- "Keep the executive summary to 5 bullets, max 15 words each"
- "For calendar prep, list each meeting with attendee name + one-sentence context"
- "Skip the 'interesting finds' section if nothing stands out"

### 3. The sources
If the brief is missing useful context, you may need more sources. Connect Firecrawl for specific blogs. Connect social data if you care about X/Twitter. Then edit the prompt to pull from them.

**Rule of thumb:** if you find yourself manually editing the brief every morning the same way, that's a tuning opportunity. Tune the config or prompt, not the output.

---

## The three-question test for a working brief

A good brief answers these three questions in under 2 minutes of reading:

1. **What do I need to do today?** (priorities, flagged emails, meeting prep)
2. **What changed overnight that I care about?** (news, inbox, calendar updates)
3. **Anything surprising?** (the one thing that's *new* -- a trend, a company move, an unexpected email)

If your brief doesn't answer all three, tune until it does.

---

## Choose Your Own Adventure: briefing patterns by role

Different roles want different briefings. Some starting points:

| Role | Heavy on | Light on |
|------|----------|----------|
| **Founder / CEO** | Competitor news, investor emails, team calendar | Internal process, industry trivia |
| **Operator / Ops lead** | Schedule, meeting prep, deadlines, team signals | External news |
| **Creator / Marketer** | Content trends, social signals (if connected), inbox | Internal calendar |
| **Consultant / Freelancer** | Client emails (flagged), upcoming meetings, project status | General news |
| **Investor** | Portfolio news, founder emails, fresh deal flow | Internal process |

Steal the pattern closest to your role, then tune for yourself.

---

## Common issues and fixes

| Problem | Fix |
|---------|-----|
| Brief is too generic -- doesn't feel like me | Config is too vague. Add real names, real URLs, real keywords. |
| Claude pulled irrelevant Exa results | Make topics in the config more specific. "AI" → "AI agents in legal ops." |
| Email section missed an obvious priority | Add the sender explicitly to "Flag immediately" in the config. |
| Brief is too long | Add length limits to the prompt. "Under 500 words. Executive summary max 5 bullets." |
| Brief missing calendar prep for a new-person meeting | Tell the prompt to flag meetings with attendees not in past calendar history. |
| `/morning-brief` doesn't appear | You didn't restart Claude Code after creating it. Cmd+Q and relaunch. |
| Brief didn't save to Drive | Check the `/mcp` menu -- Drive may need re-authentication. Or tell the prompt the exact folder path in Drive. |
| Brief is great but I want it in Obsidian instead | Change the save destination in the prompt. Obsidian files are just `.md` files in your vault folder. |

---

## What's next

- **Component 9 (Scheduling):** runs `/morning-brief` overnight without you, so the brief is waiting when you wake up
- **Component 10 (Delivery):** adds fancier channels -- Slack, email, voice/TTS, even a NotebookLM-style podcast version
- **Component 13 (`/build` skill):** shows you how to use the same pattern inside the morning brief capstone

---

## Quick reference

| Question | Answer |
|----------|--------|
| Where does the briefing config live? | `~/briefing-config.md` or in your Obsidian vault -- your choice |
| Where does the slash command live? | `~/.claude/commands/morning-brief.md` (user-level -- works in every project) |
| Can I have multiple briefings? | Yes. Build `/end-of-day-brief`, `/weekly-review`, `/client-brief` -- each with its own config and command |
| Does the brief need all the MCPs? | No. Start with Gmail + Calendar. Add Exa, Firecrawl, Obsidian when you want more signal. |
| What if I don't want it in Drive? | Save to local markdown file, or into your Obsidian vault. Any markdown destination works. |
| How often do I update the config? | Every couple of weeks. As your work changes, your config should change. |
| Can I share my briefing config? | Yes -- it's just a markdown file. Share with a teammate as a starting template. |

---

## Glossary (Component 8)

| Term | What it means |
|------|---------------|
| **Briefing config** | A markdown file describing what you care about -- people, topics, sources, format. The briefing reads this to know what to include. |
| **Agent-native briefing** | A briefing compiled by an agent coordinating multiple tools (Gmail, Calendar, Exa, Drive) from one prompt -- rather than you checking each source manually. |
| **Source** | Anywhere Claude pulls raw material from -- Gmail, Calendar, Exa, Firecrawl, etc. |
| **Compile** | The step where Claude turns raw source material into a structured brief. |
| **Deliver** | Where the brief ends up -- Drive, Obsidian, local file (or Slack/email/voice in Component 10). |
| **Tuning** | Iterating on the config and the prompt until the brief actually answers the three-question test. This is the most important part of the build. |

---

*Status: DRAFT v1 -- built on the Playbook's Daily Briefing Blueprint (Section 4). Manual trigger only; scheduling is Component 9, advanced delivery is Component 10.*
