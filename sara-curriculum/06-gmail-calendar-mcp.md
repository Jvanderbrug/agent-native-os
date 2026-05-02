# Component 6: Gmail, Calendar + Drive MCPs

## What are these MCPs?

These are three connections that let Claude read (and optionally manage) your Gmail, Google Calendar, and Google Drive. Together, they're a big part of what makes the daily briefing possible -- Claude can check your inbox, look at your schedule, and save documents for you.

But here's what's new: **these are a different kind of MCP than Exa and Firecrawl.** The setup is simpler. No API key. No 1Password. No wrapper script.

Remember Component 0's "two kinds of MCP connections"? These are **Claude.ai-managed MCPs**. Anthropic built and hosts the connection for you. All you do is log in and grant permission.

| | Local MCPs (Exa, Firecrawl) | Claude.ai-managed MCPs (Gmail, Calendar, Drive) |
|--|----------------------------|--------------------------------------------------|
| **Setup complexity** | Wrapper script + API key + 1Password | Click "authenticate" and log in |
| **Where the tool runs** | On your computer | On Anthropic's servers |
| **What you secure** | Your API key | Nothing -- OAuth handles it |
| **How long setup takes** | 5-10 minutes per tool | About 1 minute per tool |

**The short version:** If you made it through Components 4 and 5, this will feel refreshingly easy. You're going to connect three services in about the same time it took to connect one Exa.

---

## Before you start

Make sure you've completed:
- **Component 0** -- specifically the "two kinds of MCP connections" section. Understanding why this setup is different matters here.
- **Google account ready** -- the account you want Claude to connect to (personal Gmail or Workspace, either works)

That's it. No API keys to create. No 1Password entries to prepare.

---

## Setting up all three

The flow is the same for each service. We'll do all three back-to-back.

### Step 1: Open the MCP menu

Inside Claude Code, type:

```
/mcp
```

A menu opens showing every MCP server you have installed. You'll see three that say **"Needs authentication"**:
- claude.ai Gmail
- claude.ai Google Calendar
- claude.ai Google Drive

### Step 2: Start with Gmail

Select **claude.ai Gmail** from the menu. Your browser opens automatically.

### Step 3: Log in with your Google account

Standard Google sign-in screen. Log in with the account you want Claude to access.

### Step 4: Review the permissions

This is the screen where most students freeze. Google shows you exactly what Claude is about to get access to. For Gmail, you'll see two checkboxes:

- **View your email messages and settings**
- **Manage drafts and send emails**

**What you should do:** Check both (the default).

Here's why:
- **This workshop is about agents that take action.** View-only means Claude can read your email but never draft a reply. That misses most of the point.
- **Claude Code asks your permission before every individual action.** Even with "send emails" granted, Claude will show you a prompt -- *"Claude wants to send this email. Allow?"* -- before anything actually goes out. Two layers of safety.
- **You can revoke access any time** at [google.com/security](https://google.com/security) → Third-party apps with account access.

After you click Allow, the browser redirects back and your `/mcp` menu will show a green check next to "claude.ai Gmail."

### Step 5: Repeat for Calendar and Drive

Go back to `/mcp` and do the same flow for Calendar, then Drive.

**Heads up: the permission screen is slightly different for each service.** Gmail gives you granular checkboxes ("view" and "send" as separate choices). Calendar and Drive are simpler -- basically read-only vs. edit access. Don't panic when the UI looks different. It's the same concept.

For both Calendar and Drive, choose the full/edit option for the same reasons as Gmail.

### Step 6: Verify all three are connected

Type `/mcp` again. All three should now show a green check.

Or run in your terminal:

```
claude mcp list
```

You should see:

```
claude.ai Gmail: https://gmail.mcp.claude.com/mcp - ✓ Connected
claude.ai Google Calendar: https://gcal.mcp.claude.com/mcp - ✓ Connected
claude.ai Google Drive: https://api.anthropic.com/mcp/gdrive/mcp - ✓ Connected
```

---

## A note on Calendar: other people can see what Claude does

Gmail is self-contained: Claude drafts an email, you approve, you send. One action, one outcome.

Calendar is different. **When Claude creates, moves, or deletes a shared event, every attendee gets auto-notified.** Your colleague who was already on that 3 PM call will get an email the moment Claude reschedules it.

For your first week using Calendar with Claude, read every permission prompt carefully before approving. Especially for update or delete actions. You're training your own judgment on what's safe to auto-approve.

---

## The payoff: your first mini-briefing

This is where the OAuth setup becomes worth it.

With all three connected, Claude can coordinate them to build a small version of the morning briefing you'll design in Block 3. Try this exact prompt:

> "Check my Gmail for emails I need to answer, check my Calendar for tomorrow, and write me a short daily brief. Save it to my Google Drive as a document."

Watch the tool calls in the output. Claude will:

1. Use **Gmail MCP** to search your unread inbox
2. Use **Calendar MCP** to list tomorrow's events
3. **Filter signal from noise** -- automated notifications get demoted, real emails surface
4. Notice things you didn't ask it to -- back-to-back conflicts, missing RSVPs
5. Use **Drive MCP** to create a Google Doc with the brief

~30 seconds end-to-end. When it's done, Claude gives you a link to the doc in your Drive.

**What to notice:**
- Claude made judgment calls you didn't ask for. *"This email is automated, no reply needed." "These two meetings are back-to-back, no buffer."*
- Three separate services coordinated through one prompt.
- The document is persistent -- it's in your Drive, you can read it from your phone, share it with anyone.

> **Tip:** This is a preview. In Block 3 you'll design your OWN daily briefing with your chosen sources, topics, and people. Right now the point is just to see the stack work end-to-end with real data.

---

## What you can do with each service

Now that all three are connected, here are practical things you can ask.

### Gmail

- "Search my inbox for emails from [person]"
- "Find any emails about [project name] from the last two weeks"
- "Draft a reply to that email declining the meeting"
- "Summarize my unread emails by topic"

### Calendar

- "What's on my calendar this week?"
- "Find me a free 30-minute slot tomorrow afternoon"
- "Schedule a 1-hour call with [email] next Tuesday morning"
- "Check if I have any conflicts for Friday 2 PM ET"

### Drive

- "Create a Google Doc called [title] with this content..."
- "Find my notes from the [client name] meeting"
- "Summarize the contents of [doc name] in my Drive"
- "Create a folder called [folder name] and move [file] into it"

### All three together (this is the agent-native pattern)

- "Check my inbox for meeting requests, cross-reference with my calendar, and draft replies for any conflicts"
- "Before my 10 AM, read my notes doc about [client] in Drive and summarize the key points"
- "Every Friday, draft a weekly summary combining my inbox, calendar, and recent Drive activity"

---

## Gmail vs. Calendar vs. Drive: what's each for

All three serve the daily briefing differently:

| MCP | What it contributes to the brief |
|-----|----------------------------------|
| **Gmail** | What needs your attention today -- signal cut from notification noise |
| **Calendar** | Your schedule, conflicts, prep time before meetings |
| **Drive** | Where the brief lands, and a searchable archive of all past briefs |

Combined, they give Claude what used to require a human assistant: awareness of your schedule, your inbox, and where to file things.

---

## Common issues and fixes

| Problem | Fix |
|---------|-----|
| `/mcp` menu shows "Needs authentication" after I just logged in | Close and reopen Claude Code. The menu refreshes on restart. |
| Browser opens but nothing happens after login | Make sure you don't have multiple Google accounts in the same browser. Use a fresh window if needed. |
| Claude says "Gmail isn't available" | Run `/mcp` -- if it's not green, re-authenticate |
| Claude can read my email but can't draft or send | You picked view-only during auth. Re-run `/mcp` → Gmail → authenticate again with Select all |
| Calendar created an event but didn't notify anyone | Claude didn't include attendees. Ask: "Add [email] as an attendee and send the invite." |
| Claude created a doc in Drive root but I want it in a folder | Tell Claude the folder: "Create it in my 'Daily Briefs' folder." Claude will create the folder if it doesn't exist. |
| I want to disconnect these completely | [google.com/security](https://google.com/security) → Third-party apps → revoke Claude |

---

## Quick reference

| Question | Answer |
|----------|--------|
| What does this set up? | Gmail, Calendar, Drive access for Claude |
| What's different from Exa/Firecrawl setup? | No wrapper script, no 1Password, no API key. OAuth only. |
| Does Claude see ALL my email? | It has access to your full mailbox. It only reads what a specific request asks for. |
| Can Claude send emails without my approval? | No. Claude Code prompts you before every send action, even with "send emails" permission granted. |
| Can I use the same Google account with my Teams Claude later? | Yes. You'll re-authenticate once on Teams -- each Claude account is a separate OAuth grant, no conflict. |
| Where do briefing documents land? | By default, your Drive root. You can specify a folder in the prompt. |
| How do I revoke? | [google.com/security](https://google.com/security) → Third-party apps → Claude |

---

## Glossary (Component 6)

| Term | What it means |
|------|---------------|
| **OAuth** | A way to grant an app access to your account without giving it your password. When you "sign in with Google" on some website, that's OAuth. Claude.ai-managed MCPs use it. |
| **Claude.ai-managed MCP** | An MCP hosted by Anthropic. You don't install anything -- you just authenticate. Gmail, Calendar, Drive, and Notion all work this way. |
| **Permission scope** | What an app is allowed to do with your account. "View emails" is one scope. "Send emails" is a separate scope. You grant each one individually. |
| **Token** | The credential OAuth creates after you authenticate. Claude uses the token to talk to Gmail, Calendar, and Drive. You never see it. |
| **Revoke** | Taking back access you previously granted. Anytime you want Claude to stop accessing your Google account, go to google.com/security and revoke it. |
| **`/mcp`** | A slash command in Claude Code that opens the MCP server menu -- where you authenticate Claude.ai-managed MCPs. |

---

*Status: DRAFT v1 -- based on Sara's live setup of Gmail + Calendar + Drive on 2026-04-16, including the mini-briefing demo that previews Block 3.*
