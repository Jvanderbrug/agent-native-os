# Guide 00 — Before the Workshop

**Do this before Saturday morning. It takes about 30–45 minutes.**

The goal here is simple: show up to Day 1 with your machine ready, your repo cloned, and zero setup surprises. The weekend will move fast and we don't want to spend the first two hours troubleshooting installations.

---

## What You Need Before You Arrive

### The Non-Negotiables

**1. Claude Max Subscription**
Everything in this workshop runs on Claude Max. Go to **claude.ai**, sign in or create an account, and upgrade to Max (~$100/month). This is your AI engine.

**2. A GitHub Account**
Free at **github.com**. GitHub is where your workshop files live, and we use it throughout. If you already have one, you're set.

**3. A Mac or Windows PC**
Not an iPad, not a Chromebook. You need a real computer. See your platform setup guide:
- Mac: `setup/mac/prerequisites.md`
- Windows: `setup/windows/prerequisites.md`

---

## Your Pre-Workshop Checklist

Work through your platform setup guide first, then come back and verify everything here.

### Step 1: Complete the Setup Guide for Your Platform
- [ ] Mac: Completed `setup/mac/prerequisites.md` top to bottom
- [ ] Windows: Completed `setup/windows/prerequisites.md` top to bottom

### Step 2: Clone This Repo

If you're reading this on GitHub.com (not on your own machine), you need to clone the repo:

**Mac:**
```bash
cd ~/Documents
gh repo clone 8Dvibes/agent-native-os
cd agent-native-os
```

**Windows (inside WSL2/Ubuntu terminal):**
```bash
cd ~
gh repo clone 8Dvibes/agent-native-os
cd agent-native-os
```

### Step 3: Run the Verification Script

Inside the `agent-native-os` folder:
```bash
bash verify.sh
```

You want all green checkmarks. If something is red, the script will tell you exactly what to do to fix it.

### Step 4: Start Filling In Your CLAUDE.md

Open `CLAUDE.md` in any text editor (Notepad, TextEdit, VS Code — whatever you have). Fill in at least:
- Your name and what you do
- Your primary computer type
- Your goals for the workshop (at least one)

Don't worry about filling everything in — that's what Day 1 is for. Just get started so Claude has something to work with.

---

## What to Bring on Day 1

- Your laptop (charged and with charger)
- Any external monitors you want to use (having more screen space is very helpful)
- Your GitHub username and password handy
- Your Claude.ai login handy
- A list of 2–3 real tasks or workflows from your actual job that you'd love to automate or improve

That last one is important. The workshop is most valuable when you apply it to your real work. Think now about what you'd actually use this for.

---

## The Day 1 Schedule (Preview)

| Time (EDT) | Session |
|-----------|---------|
| 11:00 AM | Welcome + What We're Building |
| 11:30 AM | Guide 01: Terminal Basics |
| 12:30 PM | Guide 02: Claude Interfaces |
| 1:15 PM | Lunch Break |
| 2:00 PM | Guide 03: Your First CLAUDE.md |
| 3:15 PM | Guide 04: MCP Servers |
| 4:15 PM | Guide 05: Secrets Management |
| 5:00 PM | Day 1 Wrap-Up + What's Coming Sunday |
| 5:15 PM | Done |

---

## The Day 2 Schedule (Preview)

| Time (EDT) | Session |
|-----------|---------|
| 11:00 AM | Day 1 Recap + Warm-Up |
| 11:30 AM | Guide 06: Obsidian Second Brain |
| 12:30 PM | Guide 07: Custom Commands |
| 1:15 PM | Lunch Break |
| 2:00 PM | Guide 08: Connecting Your World |
| 3:15 PM | Guide 09: Autonomous Workflows |
| 4:15 PM | Guide 10: Your Agent OS |
| 5:00 PM | Demo Day + Next Steps |
| 5:15 PM | Done |

---

## Questions Before Saturday?

Post in the community Slack. Include your platform (Mac or Windows) and what step you're on. Someone from the team checks Slack regularly in the days before the workshop.

See you Saturday at 11 AM EDT.
