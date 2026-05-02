# Component 7: Custom Slash Commands

## What you're about to build

Until now, every time you want Claude to do something, you type the full prompt. That's fine for one-offs. But you've already noticed there are things you do the same way every time -- ending a session, planning your day, prepping for a meeting.

A custom slash command turns a repeated prompt into a shortcut. Type `/end-session`, and Claude runs the full instructions as if you'd typed them yourself. No retyping. No forgetting a step. Same output format every time.

In this component you'll build **`/end-session`** -- a command that writes a clean handover document at the end of any work session. By the end you'll understand the pattern well enough to build your own commands for anything.

> If you haven't read Component 0's "Slash commands: what they are and when to use them," go do that first. This guide assumes you know what a slash command *is* -- now you're going to build one.

---

## Why `/end-session` is the right first command

A few reasons this is the example we're using:

- **It doesn't need any MCPs.** Pure saved prompt -- just instructions to Claude. If Gmail or Exa aren't set up, `/end-session` still works. It reinforces "a slash command is a prompt, not a tool."
- **You'll use it every day.** Every work session ends somewhere. A clean handover means future-you (or Tyler, or a collaborator) can pick up without re-reading the whole conversation.
- **It's short.** One file, ~40 lines, no scripts, no configuration. You'll see the whole thing in one screen.
- **It teaches the shell injection trick** (that `!` thing you'll see in a minute) -- which is what separates a basic saved prompt from a command that actually pulls live context.

---

## Before you start

Make sure you've completed:
- **Component 0** -- specifically the slash commands section
- **Component 1 (CLAUDE.md)** -- not required, but your CLAUDE.md makes the output more personalized

That's it. No API keys. No MCPs. No 1Password.

---

## Where commands live

Custom slash commands are just markdown files in one of two folders:

| Location | Scope | When to use |
|----------|-------|-------------|
| `~/.claude/commands/` | **User-level** -- works in every project | Commands you'd use across all your work (end-session, plan-my-day, research) |
| `your-project/.claude/commands/` | **Project-level** -- works only in that project | Commands specific to one project (review-this-repo, run-deploy-checklist) |

Drop a markdown file into either folder, restart Claude Code, and the command is live.

For `/end-session`, we'll use the user-level location -- you want this command available everywhere, not just in one project.

---

## Building `/end-session`

### Step 1: Ask Claude to create the file

Open Claude Code in any project folder. Type this exact prompt:

> "Create a custom slash command called `/end-session` at `~/.claude/commands/end-session.md`. It should write a handover document for the current session so I can pick up where I left off tomorrow. The handover should include: what I accomplished, key decisions, open loops, next steps, and uncommitted git changes if any exist."

Claude will create the file and show you the contents.

### Step 2: Review what Claude wrote

The file will look something like this:

```markdown
---
description: Wrap up the current session -- create a clean handover doc with what was done, decisions made, open loops, and next steps.
---

You are writing a session handover for [your name]. They'll come back to this project tomorrow, next week, or hand it off to a collaborator -- and they need to pick up exactly where they stopped without re-reading the full conversation.

## Step 1 -- Gather context

In parallel:
- Run: !`git status --short` (if this is a git repo)
- Run: !`git log --oneline -5` (if this is a git repo)
- Review the current conversation for decisions, work done, and open questions

## Step 2 -- Write the handover

Save to `SESSION-HANDOVER-YYYY-MM-DD.md` in the current working directory...
```

Two things worth understanding here:

**The frontmatter** (the part between the `---` lines) is metadata. The `description` field is what shows up when you type `/` and browse your commands. Keep it short and clear.

**The `!` backtick syntax** (like `` !`git status --short` ``) is a live shell command. When you run the slash command, Claude runs those shell commands first and uses their output as context. Without this, Claude is guessing at your git state. With it, Claude has the actual current state. This is the move that makes slash commands useful instead of generic.

### Step 3: Restart Claude Code

This is required. Claude Code only loads custom commands when it starts up. If you skip this, your command won't appear.

Quit Claude Code completely (Cmd+Q, not just close the window) and relaunch it.

### Step 4: Verify the command loaded

In Claude Code, type `/` and start typing "end." You should see `/end-session` in the autocomplete menu with your description next to it.

If you don't see it:
- Check the file exists at `~/.claude/commands/end-session.md` (the filename becomes the command name)
- Make sure you actually quit and relaunched Claude Code
- Check the frontmatter -- if the `---` lines are broken, Claude Code skips the file

### Step 5: Test it

At the end of your next real work session, type:

```
/end-session
```

Claude will gather your git state, scan the conversation, and write a handover to a file called `SESSION-HANDOVER-YYYY-MM-DD.md` in whatever project folder you're in.

Open that file. Read it. If it's useful, you're done. If it's missing something important, edit the command file to add that section -- then restart Claude Code and run `/end-session` again.

**This is the rhythm: write it, test it, tune it. Every custom command gets better the second time.**

---

## How to read what you just built

The file at `~/.claude/commands/end-session.md` is just a markdown file with:

1. **Frontmatter** -- metadata Claude Code uses to display the command
2. **A prompt** -- plain English instructions for Claude, the same way you'd write them in chat
3. **Optional live context** -- shell commands wrapped in `` !`...` `` that run before Claude starts writing

That's it. No code. No configuration. No installation. You wrote a prompt and saved it as a file.

**The big idea:** every slash command is this. `/plan-my-day` is instructions for planning your day. `/prep-for-meeting` is instructions for prepping for a meeting. The mechanism is the same -- it's the prompt that changes.

---

## Other commands worth building

Once `/end-session` clicks, here are the next commands that pay for themselves fast. Each one takes 10-20 minutes to build.

| Command | What it does | What it'd pull in |
|---------|-------------|-------------------|
| `/plan-my-day` | Kicks off your morning -- reviews calendar, inbox priorities, yesterday's open loops | Gmail, Calendar MCPs (Component 6) |
| `/weekly-review` | Pulls your calendar, completed work, and open threads for a Friday reflection | Calendar, Drive MCPs |
| `/prep-for-meeting` | Takes a meeting name, finds related emails, prior notes, and attendee context | Gmail, Calendar, Drive MCPs |
| `/draft-reply` | Writes a first-draft response in your voice to an email you paste in | No MCPs -- works in any project |
| `/capture-idea` | Drops an idea into your Obsidian vault with a date, tags, and related links | Obsidian vault (Component 2) |
| `/log-decision` | Writes a decision record (what you decided, why, what you considered) | No MCPs -- pure structure |
| `/research` | Kicks off a research task with Exa, saves the findings to Drive as a doc | Exa, Drive MCPs |

**Which to build next:** The command you catch yourself wishing existed. Don't build speculatively -- build the one you'd use tomorrow morning.

---

## How to improve a command over time

The first version of a command is almost never the final version. The pattern:

1. **Use it for real.** Not a practice run -- an actual work session.
2. **Notice what's missing or noisy.** "It never includes my calendar." "It's too long." "I wish it asked me a question first."
3. **Edit the markdown file directly.** Open `~/.claude/commands/end-session.md` in any text editor. Add or remove sections. Save.
4. **Restart Claude Code.** Every change requires a restart to pick up.
5. **Use it again.** Repeat.

Keep commands short. A command that's too general tries to do everything and does nothing well. `/end-session` handles end-of-session. If you want a different flavor for different projects, build `/end-client-session` as a separate command -- don't overload one.

---

## The two patterns that make commands powerful

### Pattern 1: Injecting live context with `!`

As you saw in `/end-session`, wrapping a shell command in `` !`...` `` runs that command and injects its output before Claude starts. This is how you get current state into the command without asking the user to paste it.

Examples:
- `` !`git log --oneline -10` `` -- recent commits
- `` !`ls -la` `` -- files in the current directory
- `` !`date` `` -- today's date

### Pattern 2: Structured output format

Telling Claude *exactly* how to format the response is what makes commands feel consistent. In `/end-session`, the prompt says "Structure exactly as follows" and lists the sections. Without that, Claude will improvise every time.

> **Tip:** When you find yourself fixing the output format every time you use a command, that's a sign to tighten the prompt. Specify the sections, the length, the tone. The more you specify, the less you'll correct.

---

## Common issues and fixes

| Problem | Fix |
|---------|-----|
| I typed `/` but my command isn't in the list | You didn't restart Claude Code. Quit completely (Cmd+Q) and relaunch. |
| The command runs but ignores my instructions | Check the frontmatter. Broken `---` lines cause Claude Code to skip the file silently. |
| The shell command in `!` didn't work | Run the same command directly in Terminal. If it fails there, it'll fail inside the slash command too. |
| My command works in one project but not another | You saved it to `.claude/commands/` in one project. Move it to `~/.claude/commands/` for global use. |
| I want to delete a command | Delete the markdown file. Restart Claude Code. Gone. |
| The output is too long every time | Add "Keep under 300 words" or "Be concise, no preamble" to the prompt. Restart to reload. |
| Claude keeps asking me clarifying questions instead of just running | Your prompt is too open-ended. Tell Claude exactly what to do, in what order, with what output. |

---

## Quick reference

| Question | Answer |
|----------|--------|
| Where do user-level commands live? | `~/.claude/commands/` |
| Where do project-level commands live? | `your-project/.claude/commands/` |
| Does the filename matter? | Yes -- `end-session.md` becomes `/end-session` |
| Do I need to restart Claude Code after adding a command? | Yes, every time you add or edit a command file |
| Can a command run shell commands? | Yes, wrap them in `` !`...` `` backticks |
| Do commands need MCPs? | No -- a command is just a prompt. MCPs are only needed if the command's instructions reference them. |
| Can I share a command with someone else? | Yes -- it's just a markdown file. Email it, drop it in a repo, or check it into your project's `.claude/commands/` folder. |

---

## Glossary (Component 7)

| Term | What it means |
|------|---------------|
| **Slash command** | A shortcut -- type `/name` and Claude runs a saved prompt. |
| **Custom slash command** | A command *you* built (vs. built-in like `/help` or installed skills like `/build`). |
| **Frontmatter** | The metadata block at the top of a markdown file, between the `---` lines. Claude Code reads the description from here. |
| **Shell injection** | The `` !`command` `` syntax that runs a shell command and injects its output into the prompt before Claude starts. |
| **User-level command** | A command in `~/.claude/commands/` -- works in every project on your computer. |
| **Project-level command** | A command in `.claude/commands/` inside a specific project -- only works when Claude Code is running in that project. |
| **Saved prompt** | The simplest kind of slash command -- just a markdown file with instructions, no scripts or helpers. |

---

*Status: DRAFT v1 -- based on Sara building `/end-session` live on 2026-04-16 as her first custom slash command.*
