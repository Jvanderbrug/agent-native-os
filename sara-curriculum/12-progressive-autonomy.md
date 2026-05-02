# Component 12: Progressive Autonomy

> **This is Block 12: Progressive Autonomy.**
>
> **What you'll have:** A trust policy in your CLAUDE.md that tells your agent exactly what it's cleared to do without asking — and what it must always check first. Your agent stops being cautious by default and starts being decisive within the boundaries you've set.
>
> **How this stacks toward the Capstone:** `/build` writes files, creates slash commands, and modifies your agent setup. Without a trust policy, Claude stops and asks about every action. With it, Claude knows what it's authorized to do and moves. The Capstone only works if your agent trusts itself to act.
>
> **Why now:** You have a fleet that runs scheduled tasks and responds to remote commands. Before Component 13 expands what it can do, you need an explicit answer to "what is this thing allowed to do on its own?" Without that answer in writing, every session starts from scratch.

---

## The concept: three tiers

Think of this like employee authorization levels at a company.

- **Tier 1 — Cleared:** Low-risk, reversible actions that are explicitly part of your OS. Claude just does these. No interruption, no confirmation prompt.
- **Tier 2 — Ask First:** Actions that change something external or are harder to undo. Claude asks once — you say yes or no — then acts.
- **Tier 3 — Never Without Instruction:** Things that require you to say it explicitly. No ambiguity, no implied consent.

You write this policy once in your CLAUDE.md. Every session — interactive or scheduled — operates from it.

---

## What you're building

A new `# Autonomy Configuration` section in your CLAUDE.md. That's the entire install. No scripts, no plists, no restarts.

---

## The install

Open your CLAUDE.md:

```bash
open ~/.claude/CLAUDE.md
```

Add this section before `# My Voice`:

```markdown
# Autonomy Configuration

Three tiers. Every action falls into one of them.

## Tier 1 — Cleared (just do it)
These are low-risk, reversible, or explicitly part of my agent-native OS. No confirmation needed.

- Read any file in `~/Documents/second-brain/`, `~/GitHub/`, or `~/.claude/`
- Write daily briefs to `~/Documents/second-brain/daily-briefings/`
- Write notes or logs to `~/Documents/second-brain/`
- Send iMessage to my own number (+1XXXXXXXXXX)
- Read email (read-only — looking, not touching)
- Read calendar events
- Search the web (Exa, Firecrawl)
- Run any existing slash command in `~/.claude/commands/`
- Drop files into `~/.claude/remote-queue/`

## Tier 2 — Ask First
These actions change something external or are harder to reverse. One confirmation is enough — don't ask again mid-task.

- Create or modify calendar events
- Draft or send any email
- Write to any folder outside `~/Documents/second-brain/` or `~/GitHub/`
- Decline or accept meeting invitations
- Create new slash commands in `~/.claude/commands/`
- Install or modify launchd jobs

## Tier 3 — Never Without Explicit Instruction
These require me to say it clearly, not just imply it.

- Send email to anyone other than myself
- Delete any file (moving to Trash is OK; permanent deletion is not)
- Share or publish anything publicly
- Modify system settings or security preferences
- Purchase anything

## Connection to scheduled runs
The morning brief launcher uses `--permission-mode bypassPermissions`. That flag is the programmatic equivalent of Tier 1 for an unattended session — the same actions you've already cleared here, running without you present. Before adding any new scheduled task, check that every action it takes is on the Tier 1 list above.
```

Replace `+1XXXXXXXXXX` with your own phone number.

---

## Why `--permission-mode bypassPermissions` now makes sense

Before Component 12, that flag in the morning brief launcher might have felt like a workaround — something that "skips" a safety check. It's not.

`bypassPermissions` tells Claude: "Run this session as if the human has pre-approved everything." That's exactly what Tier 1 is: your explicit pre-approval list. The flag doesn't bypass your judgment — it *executes* your judgment, applied in advance.

If a future scheduled task tries to do something not on Tier 1, you should NOT use `bypassPermissions`. You'd need to either add it to Tier 1 (if you've decided it's safe) or redesign the task to not need that action unattended.

---

## Verification

After adding the section, start a new Claude Code session (⌘R or close and reopen). Ask Claude:

> "What actions are you cleared to take without asking me first?"

Claude should read from your CLAUDE.md and accurately describe Tier 1. If it does — the policy is loaded and working.

Then test a Tier 2 action:

> "Add a reminder to my calendar for tomorrow morning."

Claude should ask before acting. If it does — the tiers are working correctly.

---

## Beginner vs. Advanced track

| | Beginner | Advanced |
|---|---|---|
| **Starting point** | Use Sara's tier template verbatim, edit only the phone number | Author tiers from scratch based on your own installed components |
| **Tier 1 scope** | Conservative — only items from the template | Expansive — may include Slack, Notion, databases you've wired in |
| **Updating tiers** | Manual CLAUDE.md edit when you install new components | Standing Rule that prompts Claude to suggest tier placement after any new install |
| **Scheduled runs** | bypassPermissions only for morning brief (already configured) | Separate autonomy profiles per scheduled job |

---

## What this unlocks

Your agent now has a rulebook. It knows what it's cleared for. It knows what to ask about. It knows what to never touch.

Component 13 installs the first institutional capability on top of this foundation — a skill that your agent can call on demand, operating within the trust boundaries you just defined.

---

## Gotchas

**"Claude is still asking about things I put in Tier 1"**
CLAUDE.md changes take effect at the start of the next session. Close Claude Code and reopen it (⌘R) — don't just start a new conversation in the same window.

**"I'm not sure whether to put X in Tier 1 or Tier 2"**
Default to Tier 2. You can always promote something to Tier 1 after you've seen Claude handle it correctly a few times. It's easier to loosen trust than to tighten it after something goes wrong.

**"My morning brief uses bypassPermissions — does that override my tiers?"**
No. `bypassPermissions` tells Claude to skip interactive permission prompts — it doesn't tell Claude to ignore CLAUDE.md. Your tiers still apply as guidelines. The difference is Claude won't stop and ask mid-run; it uses your pre-stated tiers as its decision framework.
