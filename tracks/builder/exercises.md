# Builder Track — Exercises

You're in Builder track because you have some technical comfort, some tool experience, and you want to build real things — not just follow along. This track moves at a faster clip, gives you less hand-holding on the basics, and pushes you toward building things that solve real problems.

By Sunday afternoon, you should have a working agent OS that you'll actually use on Monday morning.

---

## Exercise Set 01 — Terminal Basics

**Time:** ~15 minutes (you probably know most of this)

### Exercise 1A: Verify Your Environment

Run these and confirm everything looks right:

```bash
which claude && claude --version
which node && node --version
which gh && gh auth status
which op && op whoami
```

All four should return version numbers or success messages. If any fail, fix them before moving on.

### Exercise 1B: Shell Configuration

Look at your shell config:

**Mac:**
```bash
cat ~/.zshrc | grep -E "(PATH|alias|export)"
```

**WSL2:**
```bash
cat ~/.bashrc | grep -E "(PATH|alias|export)"
```

What do you have in there? Any conflicts or missing paths that explain weird behavior?

### Exercise 1C: Create Useful Aliases

Add at least two aliases to your shell config that will speed up your agent OS workflow:

```bash
# Examples to customize
alias claude-morning='cd ~/Documents/agent-native-os && claude -p "/morning"'
alias claude-briefings='ls -lt ~/Documents/briefings/ | head -5'
```

Reload your config: `source ~/.zshrc` (or `.bashrc`)

---

## Exercise Set 02 — Claude Interfaces

**Time:** ~20 minutes

### Exercise 2A: Headless Mode

Claude Code's most powerful mode for automation is headless — running a prompt without entering interactive mode:

```bash
# Run a one-shot command
claude -p "What's the current state of my agent-native-os repo?"

# Pipe output to a file
claude -p "Generate a README outline for a project called 'Weekly Report Generator'" > ~/Desktop/outline.md

# Use it in a script
SUMMARY=$(claude -p "Summarize this: $(cat ~/Documents/notes.md)")
echo "$SUMMARY"
```

Practice: Run Claude headless on a real task you have right now.

### Exercise 2B: File Context

Pass a file to Claude Code for context:

```bash
# Pass a specific file
claude --file ~/Documents/agent-native-os/CLAUDE.md -p "Based on this context file, what MCP servers should I prioritize adding?"

# Pass multiple files
claude --file file1.md --file file2.md -p "Compare these two documents"
```

### Exercise 2C: VS Code Integration

If you haven't already, install the Claude Code VS Code extension and try:
- Highlighting a block of text in CLAUDE.md and asking Claude to improve it
- Using "Cmd+Shift+P > Claude: Explain" on a section you want to understand better

---

## Exercise Set 03 — Your First CLAUDE.md

**Time:** ~30 minutes

### Exercise 3A: A Real CLAUDE.md

Don't fill in the template with placeholder text. Fill it in with real, specific information:

- Your actual role with real detail
- Real current projects with real status
- Real people you work with and their context
- Real rules that match how you actually work

### Exercise 3B: Business Vocabulary

Add a section to your CLAUDE.md with domain-specific vocabulary:

```markdown
## Domain Context

Industry terms Claude should understand:
- [Term 1]: [what it means in your context]
- [Term 2]: ...

Common scenarios in my work:
- [Situation A]: [how I typically handle it]
- [Situation B]: ...
```

### Exercise 3C: Test Your Context Thoroughly

Simulate real work scenarios with Claude to verify your CLAUDE.md is working:

```bash
claude
> I just got a call from [real client name]. They want to [real type of request]. What would you recommend we do?
```

Does Claude's response reflect your industry knowledge, your company's context, your actual preferences? If not — what's missing from your CLAUDE.md?

### Exercise 3D: CLAUDE.md Versioning

Your CLAUDE.md should be in git so you can track changes over time. It's already in the repo — make sure you're committing updates:

```bash
cd ~/Documents/agent-native-os
git add CLAUDE.md
git commit -m "Updated CLAUDE.md with real project context"
git push
```

---

## Exercise Set 04 — MCP Servers

**Time:** ~40 minutes

### Exercise 4A: Multiple MCPs

Install at least three MCP servers today. Go beyond the basics:

**Priority tier:**
- Gmail or Outlook
- Google Calendar or Outlook Calendar
- Notion or Obsidian filesystem

**Second tier (pick one):**
- Slack
- GitHub
- Airtable, Postgres, or another database

### Exercise 4B: Test Each MCP With Real Requests

For each MCP you install, write a prompt that does something genuinely useful:

**Gmail:**
```
> Find all emails from clients I haven't responded to in the last 48 hours. List them with the sender, subject, and a one-line summary of what they need.
```

**Calendar:**
```
> Look at my calendar for the next two weeks. Flag any days where I have more than 5 hours of meetings. Suggest which meetings could be consolidated or moved.
```

**Notion:**
```
> Find all Notion pages that haven't been updated in more than 30 days. List them.
```

### Exercise 4C: Debug Mode

Look at what's happening inside MCP connections:

```bash
# Run Claude with verbose output to see MCP activity
CLAUDE_DEBUG=1 claude
```

This shows you the raw tool calls Claude is making to your MCP servers. Useful for understanding what's actually happening under the hood.

---

## Exercise Set 05 — Secrets Management

**Time:** ~20 minutes

### Exercise 5A: Full 1Password Integration

Migrate ALL your API keys into 1Password. Not one — all of them.

```bash
# Verify each op:// reference resolves correctly
op read "op://Personal/Brave Search API Key/credential"
```

### Exercise 5B: Pre-Resolved Cache (Advanced)

If you want Claude Code to start instantly without waiting for 1Password, create a pre-resolved secrets cache:

Create `~/.config/claude-mcp-secrets.env`:
```bash
#!/bin/bash
# Run this to regenerate: bash ~/.config/resolve-secrets.sh

export BRAVE_API_KEY=$(op read "op://Personal/Brave Search API Key/credential")
export NOTION_TOKEN=$(op read "op://Personal/Notion Claude Integration/credential")
# Add all your secrets here
```

Make a resolver script:
```bash
#!/bin/bash
# ~/.config/resolve-secrets.sh
eval $(op signin --raw)
source ~/.config/claude-mcp-secrets.sh
```

Add to `~/.zshrc`:
```bash
if [ -f ~/.config/claude-mcp-secrets.env ]; then
  source ~/.config/claude-mcp-secrets.env
fi
```

Now your secrets are pre-loaded every terminal session, fetched once on first `op signin`.

### Exercise 5C: Audit Your Settings

Check that your settings.json has zero plain-text API keys:

```bash
cat ~/.claude/settings.json | grep -v "op://" | grep -E "[A-Za-z0-9]{20,}"
```

Any output here is a potential exposed secret. Migrate it.

---

## Exercise Set 06 — Obsidian Second Brain

**Time:** ~35 minutes

### Exercise 6A: Comprehensive Vault Setup

Go beyond the basic PARA folders. Add:

```
Your Vault/
├── Inbox/
├── Areas/
│   ├── Business/
│   ├── Personal/
│   └── Health/
├── Projects/
│   └── [One folder per active project]
├── Resources/
│   ├── Industry/
│   ├── Tools/
│   └── People/
├── Archive/
├── Daily Notes/
└── Templates/
    ├── Daily Note.md
    ├── Meeting Note.md
    └── Project Brief.md
```

### Exercise 6B: Claude + Obsidian Deep Integration

Update your CLAUDE.md to specify Obsidian behavior in detail:

```markdown
## Obsidian Rules

- When capturing a meeting: create a note in Projects/[project]/Meetings/ with date and attendees
- When I say "note this" or "capture that": add to Inbox with today's date as title
- When researching a topic: first check Resources/, then search web, then create/update a Resources/ note
- Daily note format: use the template at Templates/Daily Note.md
```

### Exercise 6C: Build a Meeting Intelligence Workflow

Create a custom command `~/.claude/commands/meeting-capture.md`:

```markdown
# Meeting Capture

I just finished a meeting. Here's what happened: {notes}

Do all of this:
1. Create a structured meeting note in my Obsidian Projects/ folder with:
   - Date and attendees (ask me for this if not provided)
   - Key discussion points
   - Action items with owners and due dates
   - Decisions made
2. Extract all action items that are mine and add them to a "My Actions" note in Areas/
3. If a calendar event needs to be created for a follow-up, draft it for my approval
```

---

## Exercise Set 07 — Custom Commands

**Time:** ~30 minutes

### Exercise 7A: Five Commands

By end of this session, have at least five custom commands:

1. `/morning` — Daily briefing
2. `/eod` (end of day) — Capture what happened, prep for tomorrow
3. `/meeting-prep` — Research before a meeting
4. `/draft` — Draft an email, message, or document
5. `/decision` — Help think through a decision

### Exercise 7B: Parameterized Commands

Make your commands dynamic using placeholders:

`~/.claude/commands/research.md`:
```markdown
# Research

Research topic: {topic}

Use Brave Search to find current, authoritative information about {topic}.

Deliver:
1. A 3-paragraph summary of the current state
2. Key players or perspectives
3. 3 questions I should be asking about this topic
4. Sources cited

Save the research to a new note in my Obsidian Resources/Research/ folder titled "{topic} — [date]".
```

Trigger: `/research AI regulation` — Claude inserts "AI regulation" as the topic.

### Exercise 7C: Chain Commands

Build a command that calls another command as a sub-step:

`~/.claude/commands/client-kickoff.md`:
```markdown
# Client Kickoff Prep

Client name: {client}
Meeting time: {time}

Steps:
1. Run /research on {client} to find background info
2. Check my email for any prior correspondence with {client}
3. Check my Obsidian Projects/ for any existing notes on {client}
4. Prepare a briefing with: company background, our relationship history, and 5 smart questions to ask
5. Create a meeting note template in Projects/{client}/Meetings/ for me to fill in during the call
```

---

## Exercise Set 08 — Connecting Your World

**Time:** ~40 minutes

### Exercise 8A: Build a Cross-Tool Workflow

Design and build a workflow that touches at least 3 tools. Examples:

**New client intake:**
- Email arrives from new client inquiry
- Claude reads the email (Gmail)
- Creates a Notion page in your CRM database
- Creates a project folder in Obsidian
- Drafts a response email
- Adds an initial call to your calendar

**Weekly planning:**
- Pull last week from Calendar
- Pull open items from Notion projects
- Pull unprocessed Obsidian inbox items
- Generate a prioritized plan for the week
- Create the week's daily notes with pre-populated structure

### Exercise 8B: Webhooks with n8n

Set up n8n (if not already done) and create one workflow that sends a webhook when a trigger event occurs:

- New form submission → webhook → Claude drafts a response
- New Notion entry → webhook → Claude enriches the data
- Calendar event created → webhook → Claude creates prep notes

---

## Exercise Set 09 — Autonomous Workflows

**Time:** ~30 minutes

### Exercise 9A: Multiple Scheduled Tasks

Schedule at least two separate automated tasks:

1. Morning briefing (7:30 AM weekdays)
2. End-of-day capture (5:30 PM weekdays — or whenever your day typically ends)

For the end-of-day: have it review what was on your calendar, what emails you sent (Gmail Sent), and write a brief day-end summary to your Obsidian daily note.

### Exercise 9B: Error Handling

Real scheduled tasks fail sometimes. Build in basic error handling:

```bash
#!/bin/bash
# morning-briefing.sh with error handling

set -e

LOG_FILE=~/logs/morning-briefing-$(date +%Y-%m-%d).log
mkdir -p ~/logs

{
  echo "=== Morning Briefing Started: $(date) ==="
  
  # Run Claude
  claude -p "/morning" 2>&1
  
  echo "=== Completed: $(date) ==="
} | tee "$LOG_FILE"

# Alert if it fails
if [ $? -ne 0 ]; then
  echo "Morning briefing failed at $(date)" | mail -s "Claude Briefing Failed" you@youremail.com
fi
```

### Exercise 9C: Make It Resilient

What happens if your internet is down? If 1Password is locked? If Claude's API is temporarily unavailable?

Add a health check to your scheduled script:

```bash
# Check if Claude is accessible before running
if ! claude -p "test" --timeout 10 &>/dev/null; then
  echo "Claude unavailable at $(date), skipping briefing"
  exit 0
fi
```

---

## Exercise Set 10 — Your Agent OS

### Exercise 10A: Full System Documentation

Create a document (in Obsidian or as a README) that fully describes your agent OS:

- All connected MCP servers and what you use them for
- All custom commands with what they do
- All scheduled tasks with their schedule
- Key CLAUDE.md sections and why they matter
- Next 30 days plan

### Exercise 10B: Teach Someone Else

Find a workshop participant (probably a Beginner track person) and explain:
1. What you built
2. How your morning workflow works
3. One thing that surprised you about what's possible

Teaching is the best way to solidify what you know.

### Exercise 10C: Build Something You'll Actually Use Monday

Before you leave today, pick the one thing that will save you the most time or frustration next week and make sure it's working. Not theoretical — actually working.

What is that one thing?

---

*See you in the community. Post what you built.*
