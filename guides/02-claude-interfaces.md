# Guide 02 - The Three Ways to Use Claude

**When we cover this:** Lesson + Demo: Claude Code Is Not a Chatbot (10:20 AM CDT, 11:20 AM EDT). See the README for the full agenda.

> **Installer-flow students:** If your installer put you on native Windows Git Bash instead of WSL2/Ubuntu, use the Git Bash notes below. Start Claude with `claude`; use `winpty claude` only when an interactive command has TTY trouble.

---

## Three Doors, Same Room

Claude Code has three main entry points. You don't have to choose one forever. They complement each other. But knowing which one to reach for and when will make you dramatically more effective.

| Interface | Best For | Power Level |
|-----------|---------|-------------|
| **Claude Code CLI** (terminal) | Complex tasks, file work, automation | Highest |
| **Claude Desktop App** | Conversations, quick tasks, visual context | High |
| **VS Code Extension** | Working alongside your files visually | High |

Let's set each one up and understand when to use it.

---

## Interface 1 - Claude Code CLI (Terminal)

This is the one we focus on all day. It's the most powerful because:

- It can read, write, and edit files directly on your computer
- It can run commands on your behalf
- It can connect to MCP servers (your external tools)
- It has access to your full `CLAUDE.md` context
- It can run autonomously without you watching

**Think of it as:** Your AI team member that can actually do things, not just talk about them.

### Setting Up Claude Code CLI

You should have done this in prerequisites, but let's verify:

**Mac and Windows (WSL2/Ubuntu):**
```bash
# Check if it's installed
claude --version

# If not installed
npm install -g @anthropic-ai/claude-code

# Log in (opens browser)
claude
```

**Windows (native Git Bash):**
```bash
# Check if Claude Code is visible on the Windows PATH
claude --version

# Start Claude Code
claude

# If an interactive session has TTY/input trouble
winpty claude
```

On native Git Bash, launch with `claude`. If a TTY-sensitive command misbehaves, use the installer alias `winpty claude` for that command or session. If `claude` works in WSL2/Ubuntu but not Git Bash, it was probably installed only inside WSL2. Use the terminal your installer selected.

When you type `claude` and press Enter, Claude Code opens in your terminal. You'll see a welcome screen and a `>` prompt where you type your requests.

### How to Use It

```bash
# Start a session
claude

# You're now talking to Claude Code
# Type naturally, like you'd text someone
> Read my CLAUDE.md and tell me what you know about me

# Claude will read the file and respond
# Ask it to do something
> Create a folder called "projects" and add a README.md inside it

# Claude will execute the commands and show you what it did
```

To exit: type `/exit` or press `Ctrl + C`.

### Useful CLI Flags

```bash
# Start with a specific file in context
claude --file CLAUDE.md

# Run a one-shot command without entering interactive mode
claude -p "Summarize the contents of my README.md"

# Continue the last conversation
claude --continue
```

---

## Interface 2 - Claude Desktop App

The Claude desktop app recently gained built-in Claude Code support. This is the friendliest interface. It looks like a chat application, but it can access your files and run Claude Code under the hood.

**Think of it as:** The visual, point-and-click version of Claude Code. Great for things you want to see on screen while you work.

### Setting Up Claude Desktop App

**Mac:**
1. Download from **claude.ai/download**
2. Open the .dmg file and drag Claude to Applications
3. Open Claude and sign in with your Claude.ai account
4. In the app, go to Settings > Claude Code to enable it

**Windows:**
1. Download the Windows installer from **claude.ai/download**
2. Run the installer
3. Sign in with your Claude.ai account
4. In Settings, enable Claude Code

### Enabling File Access

For Claude Desktop App to access your files, you need to tell it where to look:

1. Open Claude Desktop App
2. Start a new conversation
3. Click the paperclip icon (attach). You can drag files directly into the chat
4. Or in Settings, you can configure a workspace folder Claude has persistent access to

### When to Use the Desktop App

- When you want to **see Claude's output** formatted nicely (it renders markdown)
- When you want to **drag and drop files** into the conversation
- When you're doing **research or brainstorming** that's less about running commands
- When you want to work while looking at other windows (the app floats beside your work)
- Good for **beginners** who want a familiar chat interface while learning

---

## Interface 3 - VS Code Extension

If you're comfortable with a code editor, the VS Code extension puts Claude directly inside your editor. You can see your files, make selections, and have Claude work on specific parts of documents.

**Think of it as:** Claude looking over your shoulder while you work in your editor, and able to touch what you're looking at.

### Installing the VS Code Extension

**Mac and Windows:**
1. Open VS Code (install from code.visualstudio.com if you haven't)
2. Press `Cmd/Ctrl + Shift + X` to open the Extensions panel
3. Search for "Claude" and install the official Anthropic extension
4. Sign in with your Claude.ai account when prompted

### How to Use It

- Press `Cmd/Ctrl + Shift + P` and type "Claude" to see available commands
- Highlight any code or text, right-click, and look for Claude options in the menu
- The Claude panel appears in the sidebar. Click it to open a conversation
- Ask Claude to work on selected text, explain something, or modify the current file

### When to Use VS Code

- When you're working on **files or documents** and want to see them while Claude edits
- When you want to **reference specific parts** of a file in your request
- When you're doing **longer editing sessions** on a specific document
- For **Architects** who are comfortable in editors and want the visual context

---

## How They Work Together

You don't pick one and ignore the others. Here's how a typical workflow might look:

1. **Morning briefing:** Open Claude Desktop App, paste your schedule and ask for priorities
2. **File work:** Switch to CLI: `claude` in the terminal, have it update your project notes
3. **Document editing:** Open in VS Code with the extension, have Claude help draft a proposal
4. **Automation:** Back to CLI: set up a scheduled task to run every morning

---

## The Key Difference: MCP Servers

Here's something important: **MCP servers (your tool integrations) primarily work through the CLI.**

When you connect Gmail, Calendar, Notion, or Slack, those connections live in your Claude Code configuration file. The CLI has access to all of them. The desktop app has some MCP support but it's more limited. The VS Code extension is focused on file editing.

This is why we spend so much time in the terminal. It's where the full power lives.

---

## Hands-On: Try All Three

**1. CLI:**
```bash
claude
```
Type: `Tell me what files are in my current directory`
Watch Claude use the terminal to look around.
Type `/exit` when done.

**2. Desktop App:**
Open the Claude desktop app. Start a new chat.
Type: `Summarize what the Agent Native OS workshop is teaching me` (paste in your README.md)
Notice how it formats the response differently than the terminal.

**3. VS Code (if installed):**
Open VS Code. Open your `agent-native-os` folder (File > Open Folder).
Open `CLAUDE.md`. Highlight a section.
Open the Claude panel and ask it to help you expand that section.

---

## Mac vs. Windows: Interface Notes

| Interface | Mac | Windows (WSL2/Ubuntu) | Windows (Git Bash) |
|-----------|-----|------------------------|--------------------|
| CLI | `claude` in any terminal | `claude` inside WSL2/Ubuntu terminal | `claude` in Git Bash; `winpty claude` for TTY-sensitive sessions |
| Desktop App | Native Mac app (.dmg) | Windows installer (.exe), runs on Windows side | Windows installer (.exe), runs on Windows side |
| VS Code | Mac native | Windows native, can connect to WSL2 | Windows native, opens Windows-side files |

> **Windows note:** When using VS Code on Windows with files in WSL2, install the "WSL" extension in VS Code. This lets VS Code work with your Linux files as if they're local.

---

## What You Just Learned

- Three interfaces: CLI (most powerful), Desktop App (friendliest), VS Code (best for files)
- The CLI is the foundation. MCP servers and full automation live here
- Desktop App and VS Code complement the CLI for different kinds of work
- You'll use all three. Pick the right tool for the moment

---

## Track Exercises

See `tracks/[your-track]/exercises.md` - Exercise Set 02.

---

*Next up: Guide 03 - Your First CLAUDE.md (The AHA Moment)*
