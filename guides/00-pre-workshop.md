# Guide 00, Before the Workshop

**Do this before workshop day. It takes about 30 to 45 minutes.**

The goal here is simple: show up on workshop day with your machine ready, your repo cloned, and zero setup surprises. The day moves fast and we don't want to spend the first two hours troubleshooting installations.

---

## What You Need Before You Arrive

### The Non-Negotiables

**1. Claude Max Subscription**
Everything in this workshop runs on Claude Code. Sign in at **claude.ai** and upgrade to **Claude Max 5x ($100/month minimum)** or **Max 20x ($200/month, recommended)**. Pro ($20/month) technically has Claude Code but rate limits hit fast on workshop day. This is your AI engine.

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
- [ ] 1Password app installed AND CLI working. Run `op whoami` in your terminal. On Git Bash, `op whoami` or `op.exe whoami` should work. On WSL2/Ubuntu, run `op whoami` inside Ubuntu. Either path should show your account email, not an error.

### Step 2: Clone This Repo

If you're reading this on GitHub.com (not on your own machine), you need to clone the repo:

**Mac:**
```bash
cd ~/Documents
gh repo clone aibuild-lab/agent-native-os
cd agent-native-os
```

**Windows (inside WSL2/Ubuntu terminal):**
```bash
cd ~
gh repo clone aibuild-lab/agent-native-os
cd agent-native-os
```

**Windows (Git Bash):**
```bash
cd ~/Documents
gh repo clone aibuild-lab/agent-native-os
cd agent-native-os
```

### Step 3: Run the Verification Script

Inside the `agent-native-os` folder:
```bash
bash verify.sh
```

You want all green checkmarks. If something is red, the script will tell you exactly what to do to fix it.

### Step 4: Start Filling In Your CLAUDE.md

Open `CLAUDE.md` in any text editor (Notepad, TextEdit, VS Code, whatever you have). Fill in at least:
- Your name and what you do
- Your primary computer type
- Your goals for the workshop (at least one)

Don't worry about filling everything in. That's what the workshop is for. Just get started so Claude has something to work with.

---

## What to Bring on Workshop Day

- Your laptop (charged and with charger)
- Any external monitors you want to use (having more screen space is very helpful)
- Your GitHub username and password handy
- Your Claude.ai login handy
- A list of 2-3 real tasks or workflows from your actual job that you'd love to automate or improve

That last one is important. The workshop is most valuable when you apply it to your real work. Think now about what you'd actually use this for.

---

## The Workshop Day Schedule (Preview)

The workshop is a single Sunday, roughly seven hours, live on Zoom. All times shown in CDT (the Maven listing timezone) with EDT in parentheses.

| Time (CDT / EDT) | Block |
|------------------|-------|
| 10:00 AM / 11:00 AM | Welcome + Architecture |
| 10:20 AM / 11:20 AM | Lesson + Demo: Claude Code Is Not a Chatbot |
| 10:45 AM / 11:45 AM | Install Block One: CLAUDE.md (Brain of Your OS) |
| 11:45 AM / 12:45 PM | Lesson + Demo: Memory, Workspace, System Commands |
| 12:15 PM / 1:15 PM | Install Block Two: Custom Commands + Second Brain |
| 1:00 PM / 2:00 PM | Co-Working Block (lunch + open build time) |
| 1:45 PM / 2:45 PM | Lesson + Demo: Wiring Your OS Into the World |
| 2:15 PM / 3:15 PM | Install Block Three: Connect Data Sources + First Fleet Run |
| 2:45 PM / 3:45 PM | Install Block Four: Schedule the Fleet + First /build |
| 4:15 PM / 5:15 PM | Showcase + Surprise Magic Show + Bonus Blueprint |

The 10 numbered guides in `guides/` map to these blocks. We move through them live, then they're yours as reference.

---

## Questions Before Workshop Day?

Post in the community Slack. Include your platform (Mac or Windows) and what step you're on. Someone from the team checks Slack regularly in the days before the workshop.

See you Sunday at 10 AM CDT (11 AM EDT).
