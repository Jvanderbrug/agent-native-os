# Guide 03 — Your First CLAUDE.md

**Session time:** 2:00 PM – 3:15 PM (Day 1)
**This is the AHA moment of the whole workshop.**

---

## The Problem With Starting From Zero Every Time

Think about the last time you hired a new assistant, brought in a consultant, or asked a new colleague for help. How much time did you spend just... explaining context?

"Here's how we work. Here's what I care about. Here's the background on this project. Here's how I like things formatted. Here are the people involved."

That's exhausting. And you do it every time with Claude — every new chat starts completely blank. Claude has no idea who you are, what you do, what you've already tried, or what you care about.

`CLAUDE.md` fixes this.

---

## What CLAUDE.md Actually Is

`CLAUDE.md` is a plain text file that lives in your project folder. When Claude Code starts, it automatically reads this file. Every interaction you have in that session starts with Claude already knowing everything in it.

It's your **persistent context**. Your briefing document. Your "here's who I am and what I need" memo that Claude reads before every session.

**Before CLAUDE.md:**
> "I need help writing an email to a client."
> Claude: "Sure! What's the context? Who's the client? What's the project? What's your tone?"

**After CLAUDE.md:**
> "I need help writing an email to Sarah at Pinnacle."
> Claude: "On it. I'll use your formal-but-warm tone, reference the Q3 proposal we discussed, and flag that she prefers bullet points over long paragraphs."

Same request. Completely different starting point.

---

## What Makes a Great CLAUDE.md

The difference between a mediocre CLAUDE.md and a great one comes down to specificity. Vague context produces vague help. Specific context produces specific, useful help.

**Vague:** "I'm a business owner."
**Specific:** "I run a 7-person marketing agency in Nashville. We do brand strategy and content for mid-market B2B companies. My biggest challenge is managing client expectations around timelines."

**Vague:** "I want Claude to be helpful."
**Specific:** "Always confirm before sending any external message. Give me options when I ask for creative direction, not just one answer. Never use jargon I'd have to explain to a client."

Think of it like writing a job description for an assistant you're bringing on full-time. What would they need to know on day one to do their job well?

---

## The Seven Sections of Your CLAUDE.md

Your template (in the root of this repo) has all of these. Let's walk through each one.

### 1. Who I Am

This is the foundation. Your name, role, company, and a real description of what you actually do — not your job title, but what your days look like.

Claude will use this to calibrate everything. An accountant at a law firm and a product manager at a startup need very different kinds of help.

```markdown
## Who I Am

Name: Alex Rivera
Role: Operations Director
Company: Meridian Property Group
What I do: I manage everything that happens after a property goes under contract —
inspections, contractors, timelines, client communication. I oversee a team of 4
coordinators and handle the complex deals personally.
```

### 2. My Machines

What computer you're on, what OS, any relevant specs. This helps Claude give you the right commands — Mac commands differ from Windows commands.

### 3. My Goals

Why are you here? What do you actually want to be able to do? Be specific. The more concrete your goals, the better Claude can help you achieve them.

### 4. Autonomy Level

This is important. It tells Claude how independently to act.

**Safe Mode / Director's Cut** (recommended for beginners): Claude tells you before it does anything. Always asks for confirmation. You're in full control.

**Co-Pilot**: Claude acts on clear requests without asking, but checks in on anything ambiguous.

**Autopilot**: Claude takes action unless something seems risky or irreversible.

Start at Safe Mode. Move to Co-Pilot once you trust the system. You can always change it.

### 5. Communication Preferences

How do you want Claude to talk to you? Be direct about this. Claude will match your preferences.

- Do you want bullet points or paragraphs?
- Do you want options or just the best answer?
- Do you hate long preambles? Say so.
- Do you want it to explain its reasoning? Or just do the thing?

### 6. Tools and Accounts

What software do you use? Once you connect MCP servers, you'll list those here too. This helps Claude know what resources it has access to.

### 7. Rules

The things Claude should always do (or never do). This is where you encode your non-negotiables.

```markdown
## Rules for This Agent

1. Always confirm before sending any external communication
2. When I ask for writing help, match my voice — don't make it sound like AI wrote it
3. If I give you a vague request, ask one clarifying question before proceeding
4. Never include client names in example outputs
```

---

## Filling In Your CLAUDE.md Right Now

Open `CLAUDE.md` in your text editor. We're going to fill it in together.

**Work through these in order:**

**Step 1 — Who I Am**
Write 2–3 sentences describing what you actually do. Not your official title — what does your day look like? What are you responsible for?

**Step 2 — Autonomy Level**
Leave it at "Safe Mode" for now. You can adjust after the workshop.

**Step 3 — Communication Preferences**
How do you like to receive information? Think about a coworker who communicates well with you. What do they do that others don't?

**Step 4 — Goals**
Write at least two specific goals. "Learn Claude Code" is too vague. "Set up Gmail integration so I can draft client responses in under 2 minutes" is specific.

**Step 5 — Rules**
What are your non-negotiables? Start with at least two.

Leave the other sections partially blank for now — we'll fill in tools and accounts as we add them through the day.

---

## Watching CLAUDE.md Work

Let's see the difference immediately. Do this exercise:

**Without CLAUDE.md:**
```bash
# Start claude in a temporary folder with no CLAUDE.md
mkdir /tmp/test-no-context && cd /tmp/test-no-context
claude
```
Type: `Help me write a follow-up email to a client.`
Notice how Claude asks a bunch of questions.
Type `/exit`

**With CLAUDE.md:**
```bash
# Now start claude from your workshop folder (which has your CLAUDE.md)
cd ~/Documents/agent-native-os
claude
```
Type: `Help me write a follow-up email to a client.`
Notice how Claude's response uses what it learned about you from CLAUDE.md.
Type `/exit`

The difference is dramatic once your CLAUDE.md has real context in it.

---

## Keeping CLAUDE.md Current

Here's the thing about CLAUDE.md: it's only as good as what's in it. The best users update it regularly.

**Good times to update:**
- When you finish a big project
- When you start a new one
- When your role or priorities change
- When you add a new tool or integration
- When you realize Claude keeps misunderstanding something about you

**Quick way to update:**
You can even ask Claude to help you update it:
```
> I just finished the website relaunch project. Update my CLAUDE.md to reflect that it's complete and that I'm now focused on the email campaign.
```

Claude will suggest the update, and if you approve it, it'll write it directly to the file.

---

## The Bigger Picture

You're building something that compounds. Every piece of context you add to CLAUDE.md makes every future interaction better. It's like training a long-term assistant — the investment you make early pays dividends every day after.

Some of our most successful students from previous workshops tell us that six months later, their CLAUDE.md is one of the most valuable documents they own. It's a living record of their role, their priorities, their working style, and everything their AI OS needs to serve them well.

Start it now. Keep it current. It will pay for itself.

---

## Track Exercises

See `tracks/[your-track]/exercises.md` — Exercise Set 03.

---

*Next up: Guide 04 — MCP Servers (Connecting Your World)*
