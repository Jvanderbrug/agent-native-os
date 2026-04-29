# Beginner Track — Exercises

Welcome, Beginner track. This is the right place for you if the terminal felt unfamiliar this morning or if most of this is new. You're going to be totally fine. We go slower here, we explain more, and we don't assume anything.

The goal isn't to keep up with anyone else. It's to leave Sunday with something actually working.

---

## Exercise Set 01 — Terminal Basics

**Time:** ~30 minutes during Guide 01

### Exercise 1A: Navigate and Explore

Open your terminal. Run each of these commands one at a time. After each one, look at what the output tells you.

```bash
pwd
ls
ls -la
cd ~/Documents
pwd
ls
```

Questions to answer before moving on:
- What does the `~` symbol mean?
- What's the difference between `ls` and `ls -la`?
- What directory are you in right now?

### Exercise 1B: Create a Sandbox

```bash
# Go to your Documents folder
cd ~/Documents

# Create a practice folder
mkdir workshop-sandbox

# Go into it
cd workshop-sandbox

# Confirm you're there
pwd

# Create a text file
echo "Hello from the terminal" > my-first-file.txt

# Read it
cat my-first-file.txt
```

You just created a file from the terminal. That's what Claude does for you — but automatically and at scale.

### Exercise 1C: Tab Completion Practice

Type `cd Doc` and then press Tab before pressing Enter. Did it complete to `Documents`?

Try it with a few other things. Tab completion is going to save you a lot of typos.

### Beginner Checkpoint 01

Before moving on, you should be able to:
- [ ] Open your terminal confidently
- [ ] Know what folder you're in at any time (pwd)
- [ ] List files in a folder (ls)
- [ ] Move between folders (cd)
- [ ] Use Tab to autocomplete

If any of these feel shaky, practice a bit more or ask a neighbor or the facilitator.

---

## Exercise Set 02 — Claude Interfaces

**Time:** ~20 minutes during Guide 02

### Exercise 2A: First Claude Code Session

```bash
# Navigate to your workshop repo
cd ~/Documents/agent-native-os

# Start Claude Code
claude
```

When the Claude prompt appears, type:
```
Hello! I'm a new Claude Code user in a workshop. Tell me one thing that would be useful to know.
```

Wait for the response. Notice how it looks different from the Claude website — this is the CLI version.

Type `/exit` to close.

### Exercise 2B: Claude Looking at Your Files

```bash
claude
```

Type:
```
What files are in my current directory?
```

Claude will look around your filesystem and tell you what it sees. This is Claude Code's "file access" in action.

Type `/exit`.

### Exercise 2C: Desktop App vs. CLI

Open the Claude Desktop App (if installed). Ask it the same question: "What files are in my current directory?"

Notice what happens. The Desktop App doesn't have file system access by default — it responds differently than the CLI.

This is the key difference between the interfaces.

---

## Exercise Set 03 — Your First CLAUDE.md

**Time:** ~45 minutes during Guide 03

### Exercise 3A: Fill In the Basics

Open `CLAUDE.md` (in the `agent-native-os` folder) in any text editor. Fill in at minimum:

- [ ] Your name
- [ ] What you do (2–3 sentences — be real and specific)
- [ ] Your autonomy level (leave it at Safe Mode)
- [ ] One communication preference
- [ ] Two goals for the workshop
- [ ] Two rules for the agent

Don't overthink it. Just be honest. You can always change it later.

### Exercise 3B: The Before/After Test

**Before (no context):**
```bash
mkdir /tmp/no-context-test && cd /tmp/no-context-test
claude
```
Ask: `Write me a short professional bio.`
Note the output. Type `/exit`.

**After (with your CLAUDE.md):**
```bash
cd ~/Documents/agent-native-os
claude
```
Ask: `Write me a short professional bio.`
Compare the output.

The second one should feel more like *you.* That's the power of CLAUDE.md.

### Exercise 3C: Teach Claude About a Real Project

Add a "Current Projects" section to your CLAUDE.md. Describe one real thing you're working on right now — a project, a challenge, a goal.

Then ask Claude:
```
Based on my CLAUDE.md, what are the most important things you know about me?
```

Does Claude's answer match what you intended? If something's missing or wrong, update your CLAUDE.md.

---

## Exercise Set 04 — MCP Servers

**Time:** ~30 minutes during Guide 04

### Exercise 4A: Install Brave Search

Follow the steps in Guide 04 to install the Brave Search MCP server.

- [ ] Got a Brave Search API key
- [ ] Added it to 1Password (or settings.json for now)
- [ ] Updated settings.json with the MCP configuration
- [ ] Tested with a real question that requires current info

### Exercise 4B: Test Your First MCP

With Brave Search installed:
```bash
claude
```

Ask something that requires current, real-world information:
```
What are the top tech news stories right now?
```

If Claude searches the web and returns current results — your MCP is working.

### Beginner Note on MCPs

Don't worry about installing all of them today. Brave Search is enough to understand the concept. Gmail, Calendar, and Notion we'll tackle in Guide 08 if you haven't done them yet.

---

## Exercise Set 05 — Secrets Management

**Time:** ~20 minutes during Guide 05

### Exercise 5A: Your First Secure Secret

1. Open 1Password
2. Create a new API Credential item
3. Name it "Test Secret"
4. Add a field called "credential" with value: `test-value-12345`
5. Copy the op:// reference

In your settings.json, update one of your MCP entries to use the op:// reference instead of a plain value.

### Exercise 5B: Verify It Works

Restart Claude Code (`claude`) and verify the MCP that uses your op:// reference still works.

If it works: your secrets are now secure.

### Beginner Checkpoint 05

Before the next install block:
- [ ] At least one secret stored in 1Password
- [ ] At least one op:// reference in your settings.json
- [ ] Your CLAUDE.md has real content about who you are

---

## Exercise Set 06 — Obsidian

**Time:** ~30 minutes during Guide 06

### Exercise 6A: Set Up Your Vault

Install Obsidian. Create a vault. Set up the PARA folders:
- [ ] Inbox/
- [ ] Areas/
- [ ] Projects/
- [ ] Resources/
- [ ] Archive/

### Exercise 6B: Create Your First Notes

Create three notes in Obsidian:
1. In `Inbox/`: "Workshop Thoughts", write down 2 to 3 things that clicked for you today
2. In `Projects/`: A note about a real current project
3. In `Resources/`: A note about something you want to remember

### Exercise 6C: Point Claude at Your Vault

Add your vault location to CLAUDE.md (Guide 06 shows the format).

Then test:
```
> Read my Obsidian Inbox and tell me what's there
```

---

## Exercise Set 07 — Custom Commands

**Time:** ~25 minutes during Guide 07

### Exercise 7A: Create the Morning Command

Follow Guide 07 to create `~/.claude/commands/morning.md`.

Keep it simple for your first version:
```markdown
# Morning Briefing

Give me a quick morning briefing:
1. Today's date and day of week
2. Three things to focus on today (ask me what they are)
3. One encouraging thought to start the day
```

Test it:
```bash
claude
> /morning
```

### Exercise 7B: Create One More Command

Think of something you do often and would like to shortcut. Create a command for it.

Ideas for beginners:
- `/summarize` — Summarize what I'm about to paste
- `/feedback` — Give me honest feedback on what I'm about to share
- `/simplify` — Rewrite what I'm about to paste in simpler language

---

## Exercise Set 08 — Connecting Your World

**Time:** ~45 minutes during Guide 08

### Exercise 8A: Add One More MCP

Pick one MCP from this list to add today:
- Google Calendar (if you use Google)
- Notion (if you use Notion)
- Slack (if your team uses Slack)

Follow the instructions in Guide 08 for your chosen tool.

### Exercise 8B: Cross-Tool Request

Once you have 2+ tools connected, try asking Claude something that requires both:

```
What's on my calendar today, and are there any emails related to those events?
```

---

## Exercise Set 09 — Autonomous Workflows

**Time:** ~30 minutes during Guide 09

### Exercise 9A: Manual Version First

Before scheduling anything, run your morning briefing manually and make sure the output is good:

```bash
claude -p "/morning"
```

Does it produce something useful? If not, improve the command first.

### Exercise 9B: Schedule Something Small

Schedule your morning command to run at 8 AM on weekdays (Mac: crontab, Windows: WSL2 cron or Task Scheduler).

Start with output to a file. Verify it runs correctly before adding any external delivery.

---

## Exercise Set 10 — Your Agent OS

### Exercise 10A: Map Your OS

Draw (or type out) what you've built. List:
- What tools are connected
- What commands you have
- What runs on a schedule
- What's in your CLAUDE.md

### Exercise 10B: The One-Sentence Pitch

Finish this sentence: "My agent OS automatically _______ so I don't have to."

That's your day's work in one sentence.

### Exercise 10C: What's Next?

Write down one thing you want to add or improve in the next 30 days. Keep it specific and achievable.

---

## You Did It

You came in not knowing the terminal. You're leaving with a working agent OS.

That's a real transformation. Don't underestimate what you've built today.

*See you in the community Slack.*
