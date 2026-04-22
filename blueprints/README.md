# Blueprints — Ready-to-Deploy Agent OS Workflows

Blueprints are complete, documented workflows you can deploy into your agent OS without building from scratch. Each one has been tested and comes with setup instructions, custom commands, and notes on how to adapt it for your situation.

Think of them like recipes: you follow the steps, adjust for your taste, and you have something working.

---

## How to Use a Blueprint

1. Read the blueprint description to make sure it fits your situation
2. Check the prerequisites — what MCP servers you need, what tools must be connected
3. Copy any files into the right locations (commands go to `~/.claude/commands/`, templates go to your Obsidian vault)
4. Follow the setup steps
5. Test it manually before scheduling or automating

Blueprints are starting points. Customize them to fit how you actually work.

---

## The 10 Blueprints

### Blueprint 01 — Morning Executive Briefing
**What it does:** Every weekday morning, automatically pulls your calendar, email, Obsidian inbox, and Notion project boards. Delivers a prioritized briefing — calendar events, urgent emails, key actions — by 8 AM.

**Prerequisites:** Google Calendar MCP, Gmail MCP, Obsidian vault configured, Notion MCP (optional)
**Delivery:** Saves to Obsidian Daily Notes + optional Slack post
**Effort to deploy:** ~30 minutes

---

### Blueprint 02 — Client Email Follow-Up System
**What it does:** Monitors your Gmail for client emails you haven't responded to within your defined window (default: 48 hours). Drafts context-aware responses based on your relationship history with each client.

**Prerequisites:** Gmail MCP, Notion CRM database (optional but recommended)
**Delivery:** Drafts emails in Gmail for your review before sending
**Effort to deploy:** ~45 minutes

---

### Blueprint 03 — Content Calendar Manager
**What it does:** Maintains a weekly content calendar in Notion or Obsidian. Every Monday, generates a content plan based on your focus areas. Creates writing prompts and drafts when you're ready to create.

**Prerequisites:** Notion MCP or Obsidian, Brave Search MCP (for trend research)
**Delivery:** Notion database entries or Obsidian notes
**Effort to deploy:** ~1 hour

---

### Blueprint 04 — Meeting Intelligence
**What it does:** After each meeting, processes your rough notes into a structured meeting document: attendees, key discussion, decisions made, action items with owners and due dates. Automatically adds your action items to your task system.

**Prerequisites:** Obsidian vault, Notion MCP (optional), Google Calendar MCP
**Delivery:** Obsidian meeting notes, Notion task entries
**Effort to deploy:** ~45 minutes

---

### Blueprint 05 — CRM Enrichment from Email
**What it does:** Monitors incoming email from new contacts. Automatically creates or updates CRM entries in Notion with contact details, company info (via web search), and conversation history.

**Prerequisites:** Gmail MCP, Notion MCP, Brave Search or Exa MCP
**Delivery:** Notion database entries
**Effort to deploy:** ~1 hour

---

### Blueprint 06 — Weekly Team Update Generator
**What it does:** Every Friday afternoon, compiles a team update from your week's calendar, Notion project boards, and any completed action items. Drafts a Slack message or email summary ready for your review.

**Prerequisites:** Google Calendar MCP, Notion MCP, Slack MCP or Gmail MCP
**Delivery:** Draft in Slack or Gmail for your approval
**Effort to deploy:** ~30 minutes

---

### Blueprint 07 — Invoice and Payment Tracker
**What it does:** Monitors your email for invoice-related messages. Maintains a simple payment tracker in Notion. Flags overdue invoices and drafts follow-up messages when payment is late.

**Prerequisites:** Gmail MCP, Notion MCP
**Delivery:** Notion database, draft follow-up emails
**Effort to deploy:** ~1 hour

---

### Blueprint 08 — Recruitment Pipeline Assistant
**What it does:** When you receive a candidate email or resume, parses the key information, creates a Notion entry in your candidate pipeline, and drafts a standardized response. Tracks interview stages and follow-up timing.

**Prerequisites:** Gmail MCP, Notion MCP
**Delivery:** Notion database entries, draft emails
**Effort to deploy:** ~1.5 hours

---

### Blueprint 09 — Social Media Scheduler
**What it does:** Given a content brief or rough idea, drafts platform-specific posts (LinkedIn, Twitter/X, Instagram caption). Optionally schedules them via Buffer or another scheduler's API.

**Prerequisites:** Brave Search MCP (for trend context), Buffer API (optional, for scheduling)
**Delivery:** Draft posts for your review, then scheduled or posted on approval
**Effort to deploy:** ~1 hour

---

### Blueprint 10 — Customer Support Triage
**What it does:** Monitors a support email inbox. Categorizes incoming requests by type and urgency. Drafts responses for common questions. Escalates complex issues with a summary for human review.

**Prerequisites:** Gmail MCP, Notion or Airtable MCP (for tracking), Brave Search (for researching issues)
**Delivery:** Draft responses in Gmail, tracking entries in Notion
**Effort to deploy:** ~2 hours

---

## Coming Soon

We're building more blueprints based on what workshop participants are asking for. Voted most-wanted for the next batch:

- Contractor/freelancer SOW generator
- Board meeting prep assistant
- Competitive intelligence monitor
- Podcast episode prep system
- Performance review writer

Have a blueprint idea? Share it in the community Slack (#blueprint-requests).

---

## Building Your Own Blueprint

The best blueprints come from real problems you have every week. If you've built a workflow that saves you meaningful time, consider documenting it as a blueprint to share with the community.

A good blueprint includes:
1. What it does (clear, specific description)
2. Prerequisites (MCP servers, tools, accounts)
3. Files to create (commands, templates, scripts)
4. Setup steps (in order, tested)
5. Customization notes (what to change for different situations)
6. Known limitations

Submit via the community Slack or as a pull request to this repo.
