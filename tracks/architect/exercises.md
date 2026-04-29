# Architect Track — Exercises

Architect track is for people with technical backgrounds who want to build at the edges of what's possible with Claude Code. We assume terminal comfort, some coding experience, and a desire to understand systems rather than just use them.

The exercises here go deeper into configuration, extend Claude Code's defaults, and push toward production-grade reliability. You'll also spend time thinking about architecture — not just "does it work" but "is this the right way to build it."

---

## Exercise Set 01 — Terminal and Environment

**Time:** ~20 minutes

### Exercise 1A: Environment Audit

```bash
# Full environment audit
echo "=== Shell ===" && echo $SHELL && echo $0
echo "=== Node ===" && node --version && npm --version
echo "=== Git ===" && git --version && git config --global -l
echo "=== Claude ===" && claude --version
echo "=== GitHub CLI ===" && gh --version && gh auth status
echo "=== 1Password ===" && op --version && op whoami
echo "=== PATH ===" && echo $PATH | tr ':' '\n'
```

Any conflicts? Anything missing or outdated?

### Exercise 1B: Shell Profile Architecture

Review and clean up your shell profile. Architects should have a well-organized, commented shell config:

```bash
# ~/.zshrc structure (example)

# 1. PATH extensions
export PATH="/opt/homebrew/bin:$HOME/.local/bin:$PATH"

# 2. Environment variables
export EDITOR="code"

# 3. Secret loading (from pre-resolved cache or op)
[ -f "$HOME/.cache/claude-mcp-secrets.env" ] && source "$HOME/.cache/claude-mcp-secrets.env"

# 4. Tool initializations
eval "$(op completion zsh)" # 1Password CLI completion

# 5. Aliases
alias c='claude'
alias cm='claude -p "/morning"'

# 6. Functions
claude-run() {
  cd ~/Documents/agent-native-os && claude -p "$*"
}
```

### Exercise 1C: dotfiles Consideration

Should your agent OS configuration be in a dotfiles repo? Think through:
- What should be version-controlled? (CLAUDE.md, custom commands, settings.json structure)
- What shouldn't be? (Actual secrets, credentials)
- How would you sync this across multiple machines?

Draft a dotfiles strategy for your agent OS configuration.

---

## Exercise Set 02 — Claude Interfaces

**Time:** ~25 minutes

### Exercise 2A: Claude Code Architecture Deep Dive

Read through the Claude Code settings schema:

```bash
# See all available settings
claude --help

# Inspect your current settings
cat ~/.claude/settings.json | python3 -m json.tool
```

Questions to answer:
- What's the difference between `~/.claude/settings.json` and a project-level `CLAUDE.md`?
- How does Claude Code handle permission escalation?
- What hooks are available (pre/post tool call, session start/end)?

### Exercise 2B: Hooks System

Claude Code supports hooks that run at specific lifecycle events. Explore the hooks architecture:

```json
// In settings.json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Session ended' >> ~/logs/claude-sessions.log"
          }
        ]
      }
    ]
  }
}
```

Build at least one useful hook:
- Log all sessions to a file
- Notify via Slack or notification when a long task completes
- Auto-update CLAUDE.md modification date

### Exercise 2C: Multi-Instance Architecture

For Architects who have multiple machines: how would you run Claude Code across machines with shared configuration?

Design the architecture:
- What's in git (CLAUDE.md, commands, settings template)?
- What's machine-specific (actual credentials, local paths)?
- How do you bootstrap a new machine from your dotfiles?

---

## Exercise Set 03 — CLAUDE.md

**Time:** ~30 minutes

### Exercise 3A: Hierarchical CLAUDE.md

Claude Code reads CLAUDE.md files hierarchically — project-level files supplement (don't replace) your global one. Design a hierarchy:

```
~/.claude/CLAUDE.md           ← Global: who you are, always true
~/work/CLAUDE.md              ← Work context: work tools, work rules
~/work/project-x/CLAUDE.md   ← Project context: specific to project X
```

Create at least two levels and test that context compounds correctly.

### Exercise 3B: Dynamic CLAUDE.md

Your CLAUDE.md can be generated or updated programmatically. Build a script that:
1. Fetches your current Notion project list
2. Updates the "Current Projects" section of CLAUDE.md automatically
3. Runs weekly (via cron or n8n)

```bash
#!/bin/bash
# update-claude-context.sh

PROJECTS=$(claude -p "List my active Notion projects as a bullet list" 2>/dev/null)

# Update the CLAUDE.md projects section
# [implementation using sed or python]
```

### Exercise 3C: CLAUDE.md as Code

Consider your CLAUDE.md as infrastructure-as-code. What's the right approach?

- Version control with git (already doing this)
- Semantic versioning for major context changes?
- Changelog so you can see how your context has evolved?
- Testing: how do you verify CLAUDE.md changes don't break expected behavior?

Write a simple test suite for your CLAUDE.md:

```bash
#!/bin/bash
# test-claude-context.sh
# Run after CLAUDE.md changes to verify key context is still working

echo "Test 1: Does Claude know my industry?"
RESPONSE=$(claude -p "In one sentence, what industry do I work in?")
echo "$RESPONSE" | grep -i "[expected industry keyword]" && echo "PASS" || echo "FAIL: $RESPONSE"

echo "Test 2: Does Claude respect my tone preferences?"
# etc.
```

---

## Exercise Set 04 — MCP Servers

**Time:** ~45 minutes

### Exercise 4A: Full MCP Stack

By end of this session, have 5+ MCP servers running. Push beyond the common ones:

**Must have:**
- Gmail + Google Calendar (or Outlook equivalent)
- Notion or Airtable
- Brave Search or Exa

**Go further:**
- Postgres or SQLite (direct database access)
- Custom HTTP MCP (call any API)
- Filesystem MCP configured for specific directories
- GitHub (repos, issues, PRs)

### Exercise 4B: Build a Custom MCP Server

The real power is building your own. Let's build a simple MCP server that exposes a custom capability.

Example: A "Business Data" MCP that reads from a CSV file and answers questions about your client list:

```javascript
// business-data-mcp/index.js
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');

const server = new Server({
  name: 'business-data',
  version: '1.0.0',
}, {
  capabilities: { tools: {} }
});

// Register a tool
server.setRequestHandler('tools/list', async () => ({
  tools: [{
    name: 'get_client_data',
    description: 'Get data about a specific client',
    inputSchema: {
      type: 'object',
      properties: {
        client_name: { type: 'string' }
      },
      required: ['client_name']
    }
  }]
}));

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'get_client_data') {
    const clientName = request.params.arguments.client_name;
    // Read from your CSV/database/wherever
    return {
      content: [{ type: 'text', text: JSON.stringify({ /* your data */ }) }]
    };
  }
});

const transport = new StdioServerTransport();
server.connect(transport);
```

Add it to settings.json:
```json
"business-data": {
  "command": "node",
  "args": ["/path/to/business-data-mcp/index.js"]
}
```

### Exercise 4C: MCP Performance and Reliability

MCP servers can fail. Design for reliability:

- What happens when an MCP server crashes? (Claude gracefully degrades, but you lose that capability)
- How do you know when an MCP is silently failing?
- Build a health check script that tests each MCP:

```bash
#!/bin/bash
# mcp-health-check.sh

check_mcp() {
  local name=$1
  local test_prompt=$2
  
  RESULT=$(timeout 15 claude -p "$test_prompt" 2>&1)
  if [ $? -eq 0 ]; then
    echo "✓ $name MCP: OK"
  else
    echo "✗ $name MCP: FAILED"
    echo "  $RESULT"
  fi
}

check_mcp "Brave Search" "Use Brave Search to tell me what year it is"
check_mcp "Gmail" "List my 3 most recent emails"
check_mcp "Calendar" "What's on my calendar today?"
# Add all your MCPs
```

---

## Exercise Set 05 — Secrets Management

**Time:** ~20 minutes

### Exercise 5A: Keychain Integration (Mac)

Architect-grade secret storage on Mac: the 1Password service account token in Keychain (not a file).

```bash
# Store the SA token in Keychain
security add-generic-password \
  -a "claude-mcp" \
  -s "op-service-account" \
  -w "your-service-account-token"

# Retrieve it
security find-generic-password -a "claude-mcp" -s "op-service-account" -w
```

Create a wrapper script that pulls from Keychain:
```bash
#!/bin/bash
# op-with-keychain.sh
SA_TOKEN=$(security find-generic-password -a "claude-mcp" -s "op-service-account" -w 2>/dev/null)
if [ -z "$SA_TOKEN" ]; then
  exec op "$@"
else
  OP_SERVICE_ACCOUNT_TOKEN="$SA_TOKEN" exec op "$@"
fi
```

### Exercise 5B: Secret Rotation Strategy

Design a rotation strategy:
- Which secrets expire? (OAuth tokens, API keys with expiration)
- How do you track when they expire?
- How do you automate rotation reminders or the rotation itself?

Build a simple rotation tracker in Obsidian or Notion:

| Secret | Location in 1Password | Last Rotated | Expires | Next Rotation |
|--------|----------------------|-------------|---------|--------------|
| Gmail OAuth | Personal/Gmail Credentials | 2026-04-22 | Never | — |
| Brave Search | Personal/Brave API | 2026-04-22 | ? | 2026-10-22 |

---

## Exercise Set 06 — Obsidian Second Brain

**Time:** ~30 minutes

### Exercise 6A: Obsidian + Git

Put your Obsidian vault in git for version history and backup:

```bash
cd ~/Documents/My\ Second\ Brain
git init
echo ".obsidian/workspace*" > .gitignore
echo ".obsidian/cache" >> .gitignore
git add .
git commit -m "Initial vault commit"
gh repo create my-second-brain --private
git push -u origin main
```

Add to cron to auto-commit daily:
```
0 22 * * * cd ~/Documents/My\ Second\ Brain && git add -A && git commit -m "Daily auto-commit $(date +%Y-%m-%d)" && git push
```

### Exercise 6B: Obsidian Dataview Queries

With the Dataview plugin, your vault becomes a queryable database:

```dataview
TABLE file.mtime AS "Modified", status AS "Status"
FROM "Projects"
WHERE status != "Done"
SORT file.mtime DESC
```

Build at least two useful Dataview queries:
1. Active projects sorted by last modified
2. All notes with `#followup` tag created this week

### Exercise 6C: Claude as Vault Curator

Build a weekly vault maintenance command:

`~/.claude/commands/vault-maintenance.md`:
```markdown
# Vault Maintenance

Run my weekly Obsidian vault maintenance:

1. **Inbox processing**: Read all files in my Obsidian Inbox/. For each one:
   - Suggest the correct PARA destination (Area, Project, or Resource)
   - Suggest any tags to add
   - Flag if it should be archived
   Present findings as a table for my review.

2. **Dead links**: Check for any Obsidian notes that link to non-existent files. List them.

3. **Orphaned notes**: Find notes with no incoming links and no tags. Are they worth keeping?

4. **Project health**: For each active project in Projects/:
   - When was it last modified?
   - Are there action items that look overdue?

Output as a structured vault maintenance report. Save to Daily Notes/[date]-vault-review.md
```

---

## Exercise Set 07 — Custom Commands

**Time:** ~25 minutes

### Exercise 7A: Command Architecture

Design your command namespace thoughtfully. Avoid conflicts with Claude Code built-in commands. Consider:

- Prefix conventions (e.g., `/my-` prefix for all your commands)
- Documentation: each command file should have a clear header explaining what it does and what context it needs
- Composability: commands that call sub-behaviors

### Exercise 7B: Conditional Commands

Build a command that adapts based on context:

`~/.claude/commands/status-update.md`:
```markdown
# Status Update Generator

Generate a status update. Adapt based on context:

- If it's Monday: focus on weekly plan
- If it's Friday: focus on week recap and next week preview  
- If it's end of month: include month summary

Check my calendar for the last week, my Notion project boards, and my Obsidian daily notes from this week.

Output:
- A Slack message for #team-updates (casual, bullet points)
- A more formal email version for stakeholders

Ask me which version I want to send before posting anything.
```

### Exercise 7C: Command Testing

Build a test harness for your custom commands:

```bash
#!/bin/bash
# test-commands.sh

echo "Testing /morning command..."
OUTPUT=$(claude -p "/morning" 2>&1)
[ ${#OUTPUT} -gt 100 ] && echo "✓ /morning: produced output" || echo "✗ /morning: no output"

echo "Testing /weekly-review command..."
OUTPUT=$(claude -p "/weekly-review" 2>&1)
[ ${#OUTPUT} -gt 100 ] && echo "✓ /weekly-review: produced output" || echo "✗ /weekly-review: no output"

# Add all your commands
```

---

## Exercise Set 08 — Connecting Your World

**Time:** ~45 minutes

### Exercise 8A: Full Integration Map

Map every tool in your work life. For each one:
- Do you have an MCP for it?
- If not, does one exist?
- If not, could you build one? (It's a REST API call away for most tools)
- What would you do with the integration?

### Exercise 8B: n8n as Orchestration Layer

Deploy n8n and build at minimum one workflow that:
1. Triggers on an external event (webhook, schedule, email)
2. Calls Claude Code (via subprocess or webhook)
3. Takes action based on Claude's output

Example architecture:
```
New Typeform submission
  → n8n webhook trigger
  → Extract form data
  → Call Claude: "Based on this form submission, write a personalized onboarding email"
  → Claude returns email text
  → n8n sends via Gmail
  → n8n logs to Notion CRM
```

### Exercise 8C: Bi-directional Integrations

Most MCP integrations are read/write — Claude can both fetch and update. Build a workflow that reads from one tool and writes to another:

```
Read from: Gmail (incoming client inquiry)
Process: Claude extracts key info, categorizes the request
Write to: Notion CRM (new client record)
Write to: Google Calendar (follow-up call scheduled)
Write to: Gmail (acknowledgment sent to client)
```

This runs manually via a command first. Then automate it.

---

## Exercise Set 09 — Autonomous Workflows

**Time:** ~35 minutes

### Exercise 9A: Production-Grade Scheduled Tasks

Your scheduled tasks should have:
- Logging to dated log files
- Error handling and alerts
- Idempotency (safe to run twice without duplicating output)
- A manual trigger option (for testing/debugging)

```bash
#!/bin/bash
# Template for a production-grade Claude scheduled task

TASK_NAME="morning-briefing"
LOG_DIR="$HOME/logs/claude"
LOG_FILE="$LOG_DIR/$TASK_NAME-$(date +%Y-%m-%d).log"

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

run_task() {
  log "Starting $TASK_NAME"
  
  # Verify Claude is accessible
  if ! claude -p "ping" --timeout 10 &>/dev/null; then
    log "ERROR: Claude unavailable"
    return 1
  fi
  
  # Run the actual task
  RESULT=$(claude -p "/morning" 2>&1)
  if [ $? -ne 0 ]; then
    log "ERROR: Task failed"
    log "Output: $RESULT"
    return 1
  fi
  
  log "Task completed successfully"
  echo "$RESULT" >> "$LOG_FILE"
  
  # Deliver output
  # [your delivery mechanism here]
}

run_task || {
  # Alert on failure
  # [your alerting mechanism here]
  exit 1
}
```

### Exercise 9B: Multi-Agent Orchestration

Claude Code instances can be orchestrated — one Claude can launch another with specific instructions. Design (and if possible, implement) a multi-agent workflow:

**Example: Research + Writing pipeline**

1. "Researcher" agent: searches web and Obsidian for info on a topic, writes findings to a temp file
2. "Writer" agent: reads the research file, writes a structured document
3. "Editor" agent: reads the draft, suggests improvements, writes final version

```bash
#!/bin/bash
# multi-agent-pipeline.sh

TOPIC="$1"
WORK_DIR="/tmp/research-$(date +%s)"
mkdir -p "$WORK_DIR"

# Agent 1: Research
claude -p "Research '$TOPIC'. Use Brave Search and my Obsidian vault. Write findings to $WORK_DIR/research.md" 

# Agent 2: Write
claude -p "Read $WORK_DIR/research.md and write a structured 500-word article about '$TOPIC'. Save to $WORK_DIR/draft.md"

# Agent 3: Edit
claude -p "Read $WORK_DIR/draft.md. Improve clarity, flow, and accuracy. Save final version to $WORK_DIR/final.md"

echo "Pipeline complete. Final output at: $WORK_DIR/final.md"
```

---

## Exercise Set 10 — Your Agent OS

### Exercise 10A: System Architecture Document

Write a technical architecture document for your agent OS. Include:

- Infrastructure diagram (what connects to what)
- Configuration inventory (what config files exist and what they control)
- Secret management approach
- Backup and recovery strategy
- Upgrade path (when Claude Code releases a new version, how do you update?)

### Exercise 10B: Make It Portable

Could you rebuild your agent OS on a new machine from scratch in under 30 minutes? Design a bootstrap script:

```bash
#!/bin/bash
# bootstrap-agent-os.sh
# Run on a fresh Mac to set up my full agent OS

# 1. Install Homebrew
# 2. Install tools (node, git, gh, op, claude)
# 3. Clone dotfiles repo (includes settings.json, commands/)
# 4. Clone agent-native-os repo
# 5. Configure git
# 6. Set up 1Password and sign in
# 7. Run verify.sh

echo "Bootstrap complete. Run 'claude' to start."
```

### Exercise 10C: Contribute Back

The most interesting thing you built today, document it clearly and consider contributing to the blueprints library or sharing in the community.

What would be genuinely useful for other people to have?

---

*You came in technical. You're leaving with a system.*

*The next frontier: multi-agent systems, custom MCP servers, and agent networks that scale across teams. See you in the community.*
