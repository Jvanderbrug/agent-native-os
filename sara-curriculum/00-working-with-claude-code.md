# Component 0: Working with Claude Code

*This is a living document. As we go through each workshop component, new concepts that students need to understand beforehand get added here.*

---

## What is Claude Code?

Claude Code is an AI agent that lives in your terminal. It's not a website you visit (like ChatGPT) and it's not an autocomplete tool inside a code editor (like Copilot). It's an agent that can see your files, edit them, run commands, search the web, and connect to other tools -- all from your terminal.

### Why "agent" and not "assistant"?

An assistant waits for you to tell it exactly what to do, step by step. An agent is different. You give it a goal, and it figures out the steps on its own, does them, and checks its own work.

For example:
- **Assistant behavior:** "Read this file." *reads file.* "Now find the error." *finds error.* "Now fix it." *fixes it.* "Now test it." *tests it.*
- **Agent behavior:** "There's a bug in the login page -- fix it." *reads the relevant files, identifies the problem, fixes it, runs the tests to make sure it works, and tells you what it did.*

You're still in control -- Claude asks your permission before making changes -- but you're directing the work at a higher level instead of giving one instruction at a time.

---

## The basics of talking to Claude

When you open Claude Code, you're in a conversation. You type, Claude responds. It's as simple as texting.

**Things to know:**
- Type your message and press **Enter** to send
- If you want to write multiple lines before sending, press **Shift+Enter** to go to a new line (or type `\` then Enter)
- Press **Up/Down arrows** to scroll through your previous messages
- Press **Ctrl+C** to stop Claude mid-response if it's going in the wrong direction

> **Tip:** You don't need to write perfect prompts. Talk to Claude the way you'd talk to a colleague. "Can you help me write an email to my client about the project delay?" works just as well as a carefully structured prompt.

---

## Permission modes: how much freedom you give Claude

Claude Code has different modes that control how much it can do without asking you first. Think of it like supervision levels -- you choose how much independence Claude gets.

### The three main modes

| Mode | What Claude can do without asking | Best for | How it feels |
|------|----------------------------------|----------|--------------|
| **Default** | Read files only. Asks before editing or running commands. | Beginners, sensitive work | Like a new employee who checks with you before every action |
| **Auto-accept edits** | Edit files freely. Still asks before running commands. | When you trust Claude with file changes | Like a team member who edits docs freely but checks before running anything |
| **Plan mode** | Explore and plan only. No changes until you approve the plan. | Understanding a new project, complex changes | Like asking someone to research and propose a plan before doing anything |

**To switch between modes:** Press **Shift+Tab** to cycle through them.

> **Tip:** Start in Default mode. As you get comfortable, try auto-accept edits to speed things up. Use Plan mode when you want Claude to think through something complex before acting.

---

## What Claude can actually do on your computer

Claude Code isn't just a chatbot -- it has real tools it can use on your computer. Here's what it can do:

| Action | What it means | Example |
|--------|--------------|---------|
| **Read files** | Look at any file on your computer (in the current project) | "Read my notes from last week's meeting" |
| **Write files** | Create brand new files | "Create a new document called project-plan.md" |
| **Edit files** | Change specific parts of existing files | "Update the date in that document to today" |
| **Search files** | Find files by name or search inside files for specific words | "Find all files that mention 'budget'" |
| **Run commands** | Execute terminal commands on your computer | "Install this tool" or "Run the tests" |
| **Search the web** | Look things up online | "What's the latest pricing for Notion?" |
| **Connect to other tools** | Access Slack, Google Drive, Gmail, calendars, and more (via MCP) | "Check my calendar for next week" |

> **Tip:** You don't need to know the technical names for these tools. Just describe what you want in plain English and Claude will use the right tool. "Find that email draft I was working on" is a perfectly valid instruction.

---

## The permission prompt (don't panic)

When Claude wants to do something on your computer -- like edit a file or run a command -- it asks your permission first. You'll see a prompt that shows you exactly what Claude wants to do.

**Your options:**
- **Yes / Allow** -- go ahead and do it
- **No / Deny** -- don't do that
- **Always allow** -- do this and don't ask me again for this type of action

This is a safety feature. Claude can't change anything on your computer without your say-so (unless you've switched to a mode that auto-approves certain actions).

> **Tip:** If you see a permission prompt and you're not sure what it means, it's always safe to say no. Claude will suggest an alternative approach. You can't break anything by denying a permission.

---

## Slash commands: what they are and when to use them

A slash command is a shortcut. You type `/name` and Claude runs a pre-defined set of instructions instead of making you type them every time.

### What they actually are, under the hood

Two kinds of things can be a slash command:

| What it is | Example |
|------------|---------|
| **A saved prompt.** A markdown file with instructions. When you type `/thing`, Claude reads the file and acts like you'd typed those instructions yourself. Think template. | `/weekly-review` that always pulls your calendar and asks what you learned |
| **A packaged skill.** A folder with multiple files -- the prompt, reference material, sometimes scripts. More sophisticated, but feels the same to use. | `/build` (Tyler's meta-command that builds whole systems from a description) |

From where you sit, both feel identical -- you type `/name` and something happens. The difference is what's in the folder.

### The three kinds you'll encounter

| Kind | Example | Who made it |
|------|---------|-------------|
| **Built-in** | `/help`, `/clear`, `/mcp`, `/compact` | Ships with Claude Code (Anthropic) |
| **Installed skills** | `/build`, `/briefing` | Tyler (or another builder) made it, you install it |
| **Your custom commands** | `/morning-brief`, `/plan-my-day` | You build it yourself for YOUR workflow |

Component 7 teaches you to build your own.

### Built-in commands you'll use most

| Command | What it does |
|---------|-------------|
| `/clear` | Start a new conversation. Your previous one is saved. |
| `/help` | Get help and see what commands are available. |
| `/undo` | Undo the last thing Claude did. Like Ctrl+Z for Claude's actions. |
| `/compact` | Free up memory when your conversation gets long. |
| `/context` | See how much of Claude's memory you're using. |
| `/init` | Ask Claude to auto-create a CLAUDE.md for your project. |
| `/resume` | Pick up where you left off in a past conversation. |
| `/mcp` | Open the MCP server menu -- authenticate Google, Notion, etc. |

> **Tip:** You don't need to memorize these. Just remember `/help` exists and it will show you everything else.

### When to make a slash command -- and when not to

**Make one if:**
- You do the same thing more than twice a week
- The prompt is long and you don't want to retype it
- The task has a repeatable shape (same inputs, same outputs, same logic)

**Don't make one if:**
- It's a one-off task ("help me debug THIS specific thing")
- The workflow changes every time
- You need real back-and-forth conversation -- slash commands are single-shot

### The connection rule

A slash command is a prompt. If the prompt needs Gmail, Gmail has to be connected first. You can't build a command for tools you haven't installed.

This is why the workshop is ordered the way it is: connect your tools (Components 4-6), *then* build commands that use them (Component 7).

---

## The context window: Claude's working memory

Claude can only hold so much information at once during a conversation. Think of it like a desk -- there's only so much space for papers. This is called the **context window**.

**What this means for you:**
- Longer conversations use more space
- When the desk gets full, Claude automatically tidies up (summarizes older parts of the conversation to make room)
- Files Claude reads, commands it runs, and your messages all take up space
- This is one reason your CLAUDE.md should be short -- it takes up desk space every single time you start a conversation

**When you notice things getting slow or Claude seems to forget earlier instructions:**
- Type `/compact` to manually free up space
- Type `/context` to see how much space you're using
- Or just type `/clear` to start a fresh conversation (your previous one is saved)

> **Tip:** If you're working on something complex and the conversation is getting really long, it's often better to start a new conversation with `/clear` than to keep going. Claude reads your CLAUDE.md fresh each time, so your core context is never lost.

---

## How Claude Code is different from other AI tools

If you've used other AI tools before, here's how Claude Code compares:

| Tool | What it does | How you interact |
|------|-------------|-----------------|
| **ChatGPT** | Chat in a browser window | You copy and paste code, text, or files back and forth |
| **GitHub Copilot** | Autocomplete inside your code editor | It suggests code as you type, line by line |
| **Cursor** | AI embedded inside a code editor | It edits files within the editor interface |
| **Claude Code** | AI agent in your terminal | It sees your whole project, plans multi-step work, acts on its own, runs commands, creates and edits files, and checks its own work |

The key difference: most AI tools are **reactive** (you ask, they answer). Claude Code is **agentic** (you set a goal, it plans and executes). You're directing the work, not doing it step by step.

---

## Saving your work: what "commit" means and when to do it

When you work with Claude Code, it creates and edits files on your computer. Those changes are saved to the files immediately -- just like editing a Word document. But there's a second layer of saving that you'll encounter called **committing**.

### What is git?

Git is a tool that tracks the history of your files. Think of it like "Track Changes" in Google Docs, but for your entire project folder. Every time you save a snapshot of your work (called a **commit**), git remembers exactly what changed. If something goes wrong later, you can go back to any previous snapshot.

You don't need to understand git deeply for this workshop. You just need to know a few concepts:

### The key concepts

| Concept | What it means | Real-world analogy |
|---------|--------------|-------------------|
| **Commit** | Saving a snapshot of your work at a specific point in time | Like pressing "Save Version" in Google Docs -- you can always go back to this point |
| **Repository (repo)** | A project folder that git is tracking | Your project folder, but with version history built in |
| **Branch** | A separate copy of your project where you can experiment without affecting the original | Like making a copy of a document to try out changes before updating the original |
| **Push** | Sending your saved snapshots to the cloud (GitHub) so they're backed up and shareable | Like syncing a local folder to Google Drive |
| **Pull** | Downloading the latest changes from the cloud to your computer | Like syncing changes someone else made in a shared Google Drive folder |
| **Gitignore** | A list of files that git should NOT track or share | Like telling Google Drive "don't sync this folder" -- useful for private files, passwords, or files that are only relevant to your computer |

### When should you commit?

Think of committing like saving checkpoints in a video game. You want to save:

- **After completing something that works.** Got your CLAUDE.md set up and Claude is responding differently? Commit. Built a slash command and it works? Commit.
- **Before trying something risky.** About to make a big change? Commit first so you can go back if it doesn't work out.
- **At natural stopping points.** End of a work session? Commit so your progress is saved.

**How to do it:** You can ask Claude directly: "Commit my changes with a message describing what I did." Claude will handle the git commands for you. You don't need to memorize any commands.

> **Tip:** If you're not sure whether to commit, just ask Claude: "Should I commit what I have so far?" It will tell you whether there are changes worth saving.

### The three states of your work

When you're working in a project folder, your files can be in one of three states. People mix these up constantly -- worth getting straight early.

| State | What it means | Who can see it |
|-------|--------------|---------------|
| **Uncommitted** | Files exist in your folder, but git isn't tracking them yet | Only you, on your computer |
| **Committed** | You've saved a snapshot in git | Only you -- still local, but now recoverable |
| **Pushed** | Your commits are sent to GitHub | You + anyone else with access to the repo |

**The Word doc analogy:**
- **Uncommitted** = you're typing in a Word doc but haven't hit "Save" yet. The file exists, but nothing is safely snapshotted.
- **Committed** = you hit "Save Version." The snapshot exists on your computer.
- **Pushed** = you uploaded the doc to Google Drive. Now your team can see it.

**Why this matters for collaboration:** If you're working alongside someone and they don't see your changes, you probably haven't pushed yet. Work can be saved (committed) and still invisible to your team until you push.

> **Tip:** You can work on something for a long time -- write files, edit them, even commit your progress -- without ever pushing. Useful when you want to polish something before your team sees it. Just ask Claude: "I want to keep working on this locally. Let me know when I've got something worth pushing."

**How to do each one:**
- "Commit my changes" -- saves a snapshot locally
- "Push to GitHub" -- sends your commits to the cloud (your team can now see them)

You can commit many times before pushing. Think of it as saving multiple drafts on your computer, then uploading them all at once when you're ready to share.

---

### Archiving vs. deleting vs. committing: three different actions

These look similar but they're not:

| Action | What it does | When to use it |
|--------|-------------|--------------|
| **Archive** | Move a folder aside so you know it's old, but keep the files | Finished a project and want it out of the way, but not lost |
| **Delete** | Remove the files entirely | You're sure you'll never need them |
| **Commit** | Save a snapshot in git | Checkpoint your current work |

Archiving is not a git concept -- git doesn't know or care whether a folder is "archived." It's just a human convention: you rename a folder with something like `-ARCHIVED-20260414` so you know at a glance that it's not the active version.

> **Tip:** If you see a folder with `ARCHIVED` in the name, don't work in it -- there's probably a newer, active version somewhere else. Ask Claude: "Find the active version of this project folder."

### What about gitignore?

Some files shouldn't be tracked or shared. For example:
- **API keys and passwords** -- you don't want these shared with anyone
- **Personal settings** -- your Local CLAUDE.md (`CLAUDE.local.md`) is meant to stay private
- **Claude Code's settings file** -- this contains your MCP configurations, which include API keys
- **Temporary files** -- files that your computer generates automatically

A `.gitignore` file tells git to skip these files. Claude Code knows about this and will usually handle it for you. If you're creating something that should be private, just tell Claude: "Add this to the gitignore."

### Keeping API keys safe

When you connect Claude Code to external tools (like web search, email, or calendar), those tools need API keys -- think of them like passwords that let Claude access the service on your behalf.

Here's how the security works:

1. **1Password** is where you store and manage your keys. It's the secure vault -- like a safe for your passwords. You save your API key here first.
2. **Claude Code's settings file** is where the tool actually reads the key from. Claude pulls it from 1Password and saves it here so the tool can use it.
3. **Gitignore** makes sure that settings file never gets shared with anyone.

**What this protects against:**
- Your key appearing in a conversation (where it could be logged or seen by others)
- Your key getting committed to git and shared publicly
- Losing track of where your keys are (1Password keeps them all in one place)

**What to understand:**
- The key does live on your computer in the settings file -- it has to, so the tool can read it
- That's okay, as long as the settings file is gitignored (not shared)
- 1Password is the source of truth -- if you ever need to find, change, or revoke a key, go to 1Password

> **Tip:** Never paste an API key directly into the chat. Instead, save it in 1Password first, then tell Claude: "Pull my [tool name] API key from 1Password and configure it." The key goes from 1Password to the settings file without ever appearing in your conversation.

---

## The two kinds of MCP connections

When you connect Claude to external tools (web search, email, calendar, etc.), you'll encounter two different types of MCP connections. They work differently, and it's worth understanding the difference before you hit it in the workshop.

### Local MCPs

A local MCP is a tool that runs on **your computer**. You install it, configure it, and it runs in the background whenever Claude needs it.

**Examples in this workshop:** Exa (web search), Firecrawl (web scraping)

**How it works:**
- You sign up for the service and get an API key
- You store the key in 1Password
- You create a wrapper script that pulls the key from 1Password
- The tool runs on your machine whenever Claude uses it

**Why you have to do all that:** These are independent services that aren't built into Claude. You're essentially installing a tool, pointing it at your account, and giving Claude access to it.

### Claude.ai-managed MCPs

A Claude.ai-managed MCP is a tool that runs on **Anthropic's servers**, not yours. Anthropic built and hosts the connection for you. You don't install anything -- you just log in to authorize it.

**Examples in this workshop:** Gmail, Google Calendar, Google Drive, Notion

**How it works:**
- The connection is already set up in your Claude Code
- You click "authenticate" and log in with your Google (or Notion) account
- That's it -- no API key, no wrapper script, no 1Password

**Why this is easier:** Anthropic handled the setup. All you're doing is granting Claude permission to access your account, the same way you'd grant permission to a third-party app.

### How to tell which is which

When you run `claude mcp list` in your terminal, you can see the difference at a glance:

```
claude.ai Gmail: https://gmail.mcp.claude.com/mcp - ! Needs authentication
exa: /Users/saradavison/.claude/exa-wrapper.sh - ✓ Connected
```

- **Starts with `claude.ai`** and has a URL (like `gmail.mcp.claude.com`) = Claude.ai-managed
- **Has a file path** (like `/Users/.../exa-wrapper.sh`) or a command (like `npx ...`) = Local MCP

### Which type do you get for each tool?

| Tool | Type | Why |
|------|------|-----|
| Gmail | Claude.ai-managed | Google's OAuth login handles auth |
| Google Calendar | Claude.ai-managed | Same -- OAuth with Google |
| Google Drive | Claude.ai-managed | Same -- OAuth with Google |
| Notion | Claude.ai-managed | OAuth with Notion |
| Exa | Local | Exa provides API keys directly, no OAuth |
| Firecrawl | Local | Same as Exa |
| Slack | Local (usually) | Depends on setup |

### Why this matters for security

The 1Password wrapper pattern (Component 3) only applies to **local MCPs** -- those are the ones where you manage an API key.

For **Claude.ai-managed MCPs**, there's no API key to store. Authentication happens through a login flow (OAuth) -- you grant permission through your Google account, and Anthropic's servers handle the rest. Nothing for you to secure on your end.

> **Tip:** If a guide asks you to create a wrapper script and store an API key, it's a local MCP. If it just says "click authenticate and log in with your Google account," it's a Claude.ai-managed MCP. Both are legitimate -- they're just different setup patterns for different types of services.

---

## Workflow guidance: how to actually work with Claude

Knowing what Claude Code can do is one thing. Knowing *when* to do what is another. Here's a practical guide to the rhythm of working with Claude.

### Starting a work session

1. Open your terminal
2. Navigate to your project folder (or just type `claude` if you're already there)
3. Type `claude` to start
4. Claude reads your CLAUDE.md and is ready to go

> **Tip:** If you were working on something before, type `/resume` to pick up where you left off instead of starting fresh.

### During your work

**When to keep going in the same conversation:**
- You're working on related tasks (setting up your CLAUDE.md, then testing it, then tweaking it)
- Claude has context it needs from earlier in the conversation
- Things are flowing well

**When to start a new conversation (`/clear`):**
- You're switching to a completely different task
- The conversation is getting long and Claude seems to be forgetting things
- You've finished one piece of work and want a clean start for the next

**When to use Plan mode (Shift+Tab):**
- You want Claude to research or explore before making changes
- The task is complex and you want to see the plan before Claude acts
- You're not sure what approach to take and want options

**When to undo (`/undo`):**
- Claude made a change you don't like
- Something broke after the last edit
- You want to try a different approach

### Ending a work session

1. Review what Claude has done -- ask "What changes did we make today?" if you need a summary
2. Commit your work -- ask Claude: "Commit my changes"
3. Close Claude Code (Ctrl+D or just close the terminal)

Your conversation is saved automatically. Pick it up anytime with `/resume`.

### Common workflow patterns

**"Build something"** (most common in this workshop):
1. Tell Claude what you want to build
2. Let it create files and make edits (review the permission prompts)
3. Test the result
4. Ask Claude to adjust if needed
5. Commit when it works

**"Fix something":**
1. Tell Claude what's wrong
2. It will read files, investigate, and suggest a fix
3. Review and approve the fix
4. Test to make sure it works
5. Commit

**"Explore and learn":**
1. Switch to Plan mode (Shift+Tab)
2. Ask Claude to explain something or research options
3. Review the information
4. Switch back to default mode when you're ready to act

> **Tip:** You can always ask Claude "What should I do next?" It will suggest the logical next step based on where you are in your work.

---

## Sessions: your conversations are saved

Every conversation with Claude Code is automatically saved on your computer. This means:

- You can close Claude Code and come back later
- Type `/resume` to see your previous conversations and pick one up
- Each project folder keeps its own conversation history
- Starting a new conversation with `/clear` doesn't delete the old one -- it's still there

> **Tip:** If you were working on something yesterday and want to pick up where you left off, just type `/resume` when you open Claude Code.

---

## When you need to restart Claude Code

Sometimes you'll install a new tool or change a setting, and Claude needs to restart to pick it up. This happens because Claude reads its configuration at the start of a session, not mid-conversation.

**How to restart:**
- **In VS Code:** Type `/clear` in the Claude Code chat panel to start a fresh session. Or open the Command Palette (Cmd + Shift + P) and look for "Claude Code: New Session."
- **In the Terminal app:** Close the current session (Ctrl + D), then type `claude` again.

**How to know it worked:** After restarting, test the new tool with a specific prompt. Throughout this workshop, we'll give you a test prompt for every tool we set up so you can verify it's working.

> **Tip:** If you install something new and it doesn't seem to work, the first thing to try is restarting Claude Code. Nine times out of ten, that's the fix -- Claude just needs to reload its settings.

---

## Glossary (Component 0)

| Term | What it means |
|------|---------------|
| **Agent** | An AI that can plan and take actions on its own, not just answer questions. Claude Code is an agent -- you give it a goal and it figures out the steps, does them, and checks its work. |
| **Terminal** | The application where you type commands to your computer (and where Claude Code runs). On Mac, it's called Terminal. Think of it as a text-based way to interact with your computer instead of clicking around. |
| **Permission prompt** | A popup in Claude Code that asks your permission before it edits a file or runs a command. A safety feature -- Claude can't change anything without your approval (unless you've changed the mode). |
| **Slash command** | A shortcut that starts with `/` that you type in Claude Code to do common things quickly. Like `/clear` to start a new conversation or `/help` to see what's available. |
| **Context window** | Claude's working memory during a conversation. It can only hold so much at once. When it fills up, Claude summarizes older content to make room. This is why short, focused CLAUDE.md files work better than long ones. |
| **Session** | A single conversation with Claude Code. Sessions are saved automatically and can be resumed later. Each project folder has its own conversation history. |
| **MCP (Model Context Protocol)** | A way to connect Claude Code to other tools and services like Slack, Google Drive, Gmail, and more. Covered in detail in later components. |
| **Local MCP** | An MCP tool that runs on your computer. You install it, provide an API key, and manage it yourself. Examples: Exa, Firecrawl. |
| **Claude.ai-managed MCP** | An MCP tool hosted by Anthropic. The connection is built-in -- you just log in with your account (OAuth) to authorize it. No installation or API key needed. Examples: Gmail, Google Calendar, Google Drive, Notion. |
| **OAuth** | A secure login flow where you grant an app permission to access your account without giving it your password. When you "sign in with Google," that's OAuth. Claude.ai-managed MCPs use OAuth to connect to your accounts. |
| **Token** | The unit Claude uses to measure text. Roughly 4 characters = 1 token. Your context window has a limited number of tokens, which is why keeping things concise matters. |
| **Mode** | A setting that controls how much freedom Claude has to act without asking. Default mode asks before every change. Auto-accept lets Claude edit files freely. Plan mode is read-only until you approve. |
| **Git** | A tool that tracks the history of your project files. Like "Track Changes" for your entire project folder. It lets you save snapshots (commits) and go back to any previous version. |
| **Commit** | A saved snapshot of your project at a specific point in time. Like pressing "Save Version" so you can always go back to this point if something goes wrong later. |
| **Repository (repo)** | A project folder that git is tracking. Your project folder with version history built in. |
| **Push** | Sending your saved snapshots (commits) to the cloud (usually GitHub) so they're backed up and can be shared with others. |
| **Pull** | Downloading the latest changes from the cloud to your computer. The opposite of push. |
| **Branch** | A separate copy of your project where you can experiment without affecting the original version. |
| **Gitignore (.gitignore)** | A file that tells git which files to skip -- not track, not share. Used for private files like API keys, personal settings, or temporary files. |
| **API key** | A password-like code that gives Claude Code permission to use an external service (like web search or email). You store these in 1Password and Claude pulls them when needed. |
| **1Password** | A secure app for storing passwords and API keys. Think of it as a safe for all your secret codes. Claude Code can pull keys from 1Password without them ever appearing in your conversation. |
| **Settings file** | Claude Code's configuration file (`settings.json`) where tool connections and API keys are stored on your computer. This file is gitignored so it never gets shared. |

---

*Status: LIVING DOCUMENT -- will be updated as we go through each component*
