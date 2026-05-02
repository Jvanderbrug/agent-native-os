# Guide 08 — Connecting Your World

**When we cover this:** Lesson + Demo: Wiring Your OS Into the World (1:45 PM CDT, 2:45 PM EDT) and Install Block Three: Connect Data Sources + First Fleet Run (2:15 PM CDT, 3:15 PM EDT). See the README for the full agenda.

---

## From Islands to an Ecosystem

Right now you might have:
- Email in Gmail
- Schedule in Google Calendar
- Notes in Obsidian
- Communication in Slack
- Projects in Notion or Airtable

These tools don't know about each other. You're the connective tissue — manually copying information between them, context-switching constantly, losing things in the cracks.

**Your agent OS changes this.** When Claude is connected to all your tools, it becomes the connective tissue. It can pull from all of them at once, synthesize across them, and take action in any of them on your behalf.

This guide is about adding the remaining connections.

---

## What We're Connecting

By the end of this session, you'll have at least 3 of these connected. Pick the ones that match your actual tools. Each one installs with a single `claude mcp add` command.

| Tool | Install Command | What You Get |
|------|-----------------|--------------|
| Gmail | `claude mcp add gmail` | Read, draft, search email |
| Google Calendar | `claude mcp add google-calendar` | Read/create events, find availability |
| Notion | `claude mcp add notion` | Read/write pages and databases |
| Slack | `claude mcp add slack` | Read channels, post messages |
| GitHub | `claude mcp add github` | Repos, issues, PRs |
| Airtable | `claude mcp add airtable` | Read/write your bases |
| n8n | Custom (see Guide 09) | Trigger your automation workflows |

> **Legacy note:** Older docs (and the templates in `templates/settings/`) show a hand-rolled `mcpServers: { ... command: "npx", args: ["-y", "@modelcontextprotocol/server-X"] ... }` block in `~/.claude/settings.json`. That format still works, but `claude mcp add` is the recommended path now and handles the credentials/env wiring for you.

---

## Google Calendar

If you already did Gmail, Calendar is similar.

### Setup

1. Enable the **Google Calendar API** in your Google Cloud project (console.cloud.google.com)
2. Your existing OAuth credentials from Gmail should cover it. Just add the Calendar scope.
3. Install the MCP server:

```bash
claude mcp add google-calendar
```

When prompted, point it at the same OAuth credentials JSON you used for Gmail.

### Test it:
```
> What's on my calendar for the rest of this week?
```
```
> Do I have any conflicts between 2 PM and 5 PM on Friday?
```
```
> Schedule a 30-minute block called "Deep Work" tomorrow morning at 9 AM
```

---

## Notion

Notion is powerful for teams and personal PKM. The MCP integration lets Claude read any page you give it access to.

### Setup

1. Go to **notion.so/my-integrations**
2. Click "+ New integration"
3. Name it "Claude MCP"
4. Copy the integration token
5. Add the integration to each Notion page or database you want Claude to access (in Notion: click ... > Add connections > your integration)

Store the token in 1Password, then install the MCP server:

```bash
claude mcp add notion
```

When prompted, paste your Notion integration token (or the 1Password reference, e.g. `op://Personal/Notion Claude Integration/credential`).

### Test it:
```
> Find my Notion page about [something you have in Notion]
```
```
> Add a new item to my [database name] in Notion with title "[something]"
```

---

## Slack

If your team uses Slack, this is a high-value connection.

### Setup

1. Go to **api.slack.com/apps**
2. Create a new app > From scratch
3. Name: "Claude MCP"
4. Workspace: your Slack workspace
5. Under "OAuth & Permissions", add these scopes:
   - `channels:read`
   - `channels:history`
   - `chat:write`
   - `users:read`
6. Install to workspace
7. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

Store in 1Password, then install the MCP server:

```bash
claude mcp add slack
```

When prompted, paste the bot token (or the 1Password reference, e.g. `op://Personal/Slack Claude Bot/credential`).

### Test it:
```
> What are the most recent messages in my #general channel?
```
```
> Post a message to #updates: "Testing my new Claude integration — it works!"
```

> Note: Be careful with Slack posting — in Safe Mode, Claude will show you the message before sending. Always review before it posts.

---

## Cross-Tool Workflows

Here's where things get genuinely powerful. With multiple tools connected, you can do things that would have required jumping between 4 apps:

**Example: Meeting follow-up in one command**
```
> I just finished my call with David at Summit Capital. He wants us to send a proposal by Friday.
> 
> Do all of these:
> 1. Create a Notion page in my Projects database: "Summit Capital Proposal" with due date Friday
> 2. Add an event to my calendar Wednesday 2 PM: "Work on Summit Proposal" (2 hours)
> 3. Draft a follow-up email to David thanking him for his time and confirming we'll send the proposal by Friday
> 4. Create a note in my Obsidian Projects/Summit Capital/ folder capturing what he said about their needs
```

Claude will do all four. You review and approve (in Safe Mode).

**Example: Weekly team update**
```
> Look at my calendar from this past week and my Notion project boards. 
> Draft a Slack message to #team-updates summarizing what was accomplished, 
> what's in progress, and what's coming next week. Keep it under 10 bullet points.
```

**Example: Smart inbox triage**
```
> Go through my Gmail inbox. For every email that's been sitting unanswered for more than 48 hours:
> 1. Categorize it (urgent/important/FYI)
> 2. Check if there's a related Notion project
> 3. Draft a brief response
> 
> Present them one at a time so I can review and approve each response before you draft the next.
```

---

## Adding Your n8n Connection

n8n is a workflow automation tool (think: a more powerful Zapier). If you're using it (or we set it up later today), Claude can trigger your n8n workflows.

This creates a powerful pattern: Claude handles the thinking and decisions, n8n handles the automated execution.

```
> Trigger my "New Client Onboarding" n8n workflow with client name: Pinnacle Group, contact: sarah@pinnaclegroup.com
```

We'll cover this more in Guide 09.

---

## Updating Your CLAUDE.md

Add your new connections:

```markdown
## Connected Tools (MCP Servers)

- Gmail — read inbox, draft replies, search
- Google Calendar — full read/write
- Notion — Projects and Resources databases connected
- Slack — #team-updates, #general, #projects channels
```

Also add any patterns you want Claude to follow with these tools:

```markdown
## Tool Rules

- Always show me a Slack message before posting
- When creating calendar events, add a description with context
- When adding to Notion, follow my existing page structure
- Never delete emails or calendar events without explicit confirmation
```

---

## What You Just Built

- At least 3 real tools connected and working
- Cross-tool workflows where Claude bridges between your apps
- Patterns in your CLAUDE.md for how Claude should use each tool

---

## Track Exercises

See `tracks/[your-track]/exercises.md` — Exercise Set 08.

---

*Next up: Guide 09 — Autonomous Workflows*
