# Guide 04 — MCP Servers

**Session time:** 3:15 PM – 4:15 PM (Day 1)

---

## What's an MCP Server?

Think of Claude Code as an extremely capable person who's been locked in a room with just a computer. They can read and write files, run commands, and think brilliantly — but they can't reach out and touch anything in the outside world.

**MCP servers are the doors out of that room.**

MCP stands for Model Context Protocol. It's a standard way for Claude to connect to external tools and services. When you install an MCP server, you're giving Claude a new capability — a new door it can walk through.

| MCP Server | What Claude Gains |
|------------|------------------|
| Gmail | Read emails, draft replies, search inbox |
| Google Calendar | See your schedule, create events, find conflicts |
| Notion | Read and write your notes, databases, wikis |
| Slack | Read messages, post to channels, search conversations |
| GitHub | Read repos, create issues, review pull requests |
| Brave Search / Exa | Search the web with real-time results |

Without MCPs: Claude knows what you tell it.
With MCPs: Claude knows what you tell it *plus* everything in your connected tools.

---

## How MCP Servers Work

Under the hood, an MCP server is a small program that runs on your computer and acts as a translator between Claude and an external service. Claude sends requests to the MCP server; the server talks to Gmail or Notion or whatever; the server brings the response back to Claude.

You don't need to understand the internals. What matters is:

1. You install an MCP server once
2. You tell Claude Code about it (via a config file)
3. Claude can now use that service in any session

---

## Installing Your First MCP Server

We're going to install the **Brave Search** MCP server. It's the simplest one — no authentication required, just install and go. We'll use it to verify that MCPs work before we move to the authenticated ones.

### Step 1: Get a Brave Search API Key

1. Go to **brave.com/search/api/**
2. Click "Get Started for Free"
3. Create an account
4. Create an API key — the free tier gives you 2,000 queries/month, which is plenty for this workshop
5. Copy the API key

### Step 2: Add It to Your Claude Code Settings

Claude Code keeps its MCP configuration in a file called `settings.json`. Let's open it.

**Mac:**
```bash
# Open the settings file in your default editor
open ~/.claude/settings.json
```

If the file doesn't exist yet:
```bash
mkdir -p ~/.claude && touch ~/.claude/settings.json
open ~/.claude/settings.json
```

**Windows (WSL2):**
```bash
# Create the directory if needed
mkdir -p ~/.claude

# Open in VS Code (if installed)
code ~/.claude/settings.json

# Or open with the default text editor
notepad.exe $(wslpath -w ~/.claude/settings.json)
```

The file should contain (or you should create it with):

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Replace `YOUR_API_KEY_HERE` with the key you copied from Brave.

### Step 3: Verify It Works

```bash
# Restart Claude Code (or start fresh)
claude
```

Type:
```
> What's the weather like in Nashville today?
```

If you see Claude actually searching the web and returning current results — your first MCP server is working.

---

## Installing the Gmail MCP Server

The Gmail integration is one of the most valuable. Here's how to set it up.

### What You'll Need

- A Google account (Gmail)
- A Google Cloud project (free) with the Gmail API enabled
- OAuth credentials

### Step 1: Set Up Google Cloud

1. Go to **console.cloud.google.com**
2. Create a new project (call it "Claude MCP" or whatever you like)
3. In the search bar, search for "Gmail API"
4. Click "Enable"
5. Go to "Credentials" (left sidebar)
6. Click "Create Credentials" > "OAuth client ID"
7. Choose "Desktop app"
8. Download the JSON file — save it somewhere safe (like `~/.claude/credentials/gmail.json`)

### Step 2: Install the Gmail MCP Server

```bash
npm install -g @modelcontextprotocol/server-gmail
```

### Step 3: Add to settings.json

Add this to your `mcpServers` section in `~/.claude/settings.json`:

```json
"gmail": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-gmail"],
  "env": {
    "GMAIL_CREDENTIALS_FILE": "/Users/yourname/.claude/credentials/gmail.json"
  }
}
```

Replace the path with wherever you saved your credentials file.

### Step 4: Authenticate

Start Claude Code: `claude`

The first time you reference Gmail, it will open a browser for you to authorize access. Follow the prompts and grant the permissions.

Test it:
```
> What are my 5 most recent emails?
```

---

## Choosing Which MCPs to Install

You don't need to install all of them today. During the workshop, pick the ones that match what you actually use:

**High value for most people:**
- Gmail or Outlook (email)
- Google Calendar or Outlook Calendar (scheduling)
- Notion, Obsidian, or your note tool

**High value depending on your work:**
- Slack (if your team uses it)
- GitHub (if you work with code or repos)
- Airtable or Postgres (if you have a database)

**Nice to have:**
- Brave Search or Exa (web search)
- YouTube transcript fetcher
- Weather

The principle: **connect the tools you already use every day**. Don't add MCPs for tools you barely touch — the value comes from Claude being embedded in your actual workflow.

---

## Updating Your CLAUDE.md

Once you have MCPs installed, add them to your CLAUDE.md so Claude knows what it has access to:

```markdown
## MCP Servers I've Installed

- Gmail — full email access (read, draft, search)
- Google Calendar — read/write access to my main calendar
- Brave Search — web search for current information
```

This is especially useful because it helps Claude know to use these tools proactively, not just when you explicitly mention them.

---

## MCP Server Troubleshooting

**"MCP server failed to start"**
Usually means the npm package didn't install correctly. Try: `npm install -g @modelcontextprotocol/server-[name]` manually.

**"Authentication failed" on Gmail or Calendar**
Delete the cached credentials and reauthenticate. Look in `~/.claude/` for any credential files from the affected service and delete them, then restart Claude.

**"I can see the MCP server in settings but Claude doesn't seem to use it"**
Make sure the JSON in your settings.json is valid (no missing commas, no extra curly braces). Use an online JSON validator if you're not sure.

**Claude says it can't access Gmail when I ask about emails**
Try being more explicit: "Use the Gmail MCP server to show me my recent emails."

---

## What You Just Built

- An understanding of what MCP servers are and why they matter
- At least one MCP server connected and working
- The framework for adding more as you need them

---

## Track Exercises

See `tracks/[your-track]/exercises.md` — Exercise Set 04.

---

*Next up: Guide 05 — Secrets Management (Keeping Your Keys Safe)*
