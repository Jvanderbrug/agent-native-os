# Observability Module — Knowing What Your Agents Did

**When we cover this:** This is a self-paced module. Work through it after Guide 09 (Autonomous Workflows) — once you have agents running while you sleep, you need a way to see what they did.

---

## The Problem We're Solving

Your fleet ran overnight. You wake up. Five things happened. Two went well, one silently failed, one cost more than it should have, and one is mid-flight on a long task.

Without observability, you find out by:
- Reading raw log files in `~/.claude/`
- Asking each agent "what did you do?" (and trusting the answer)
- Discovering the failure when something downstream breaks

With observability, you open a dashboard and see every session, every tool call, every prompt and response, every cost, every duration — sortable, searchable, filterable. Same way a developer reads server logs, except for AI agents.

This module installs that dashboard.

---

## Why Langfuse

There are several agent-observability tools. We recommend Langfuse for the AI Build Lab stack for four reasons:

1. **Open source.** You can read the code, fork it, run it forever even if the company disappears.
2. **Self-hostable.** Your prompts and responses can stay on your own server. No third party reads your work.
3. **Free at individual scale.** The cloud free tier is generous (50k events/month at the time of writing), and self-hosting is free forever.
4. **Built for LLMs.** Native concepts for trace, session, generation, tool span, cost, latency, model version. Not a generic logging tool repurposed.

It tracks:
- **Sessions** (a full Claude Code conversation, end to end)
- **Traces** (one user turn and the assistant response)
- **Generations** (the LLM call itself, with model + cost + latency)
- **Spans** (each tool call inside a turn)
- **Scores** (eval results, if you wire them up)

---

## Two Paths

You don't have to pick one forever. Most people start on Cloud and graduate to self-hosted later.

**Path A — Langfuse Cloud** (start here)
- Sign up at cloud.langfuse.com, create a project, copy two API keys, paste into your env. Done in ten minutes.
- Free tier covers a serious individual workload.
- Read `01-getting-started-cloud.md`.

**Path B — Self-hosted on a VPS** (graduate here)
- Spin up a $5-10/month Hostinger or DigitalOcean droplet, run docker-compose, point a domain at it.
- Your data, your hardware, no vendor lock-in.
- One of the AI Build Lab production fleets runs this way.
- Read `02-self-hosted.md` after you have Cloud working.

---

## What This Module Contains

| File | What it covers |
|---|---|
| `01-getting-started-cloud.md` | Langfuse Cloud signup, project creation, API keys, your first trace. The 10-minute path to "I can see my sessions in a dashboard." |
| `02-self-hosted.md` | Spinning up Langfuse on a VPS with docker-compose, DNS, SSL via Caddy. For when Cloud is no longer the right home. |
| `03-claude-code-integration.md` | The Stop and PostToolUse hooks pattern. How to wire Claude Code to send traces automatically, how to redact secrets, how to tag traces by machine and agent source. |
| `04-using-the-dashboard.md` | Day-2 power user moves. Filtering by session, comparing model costs, finding slow tools, alerting on errors, exporting traces. |

Read them in order. Each one builds on the previous.

---

## What You'll Be Able To Do After

- See every Claude Code session you've run, with full prompts and responses
- Know what each session cost in tokens and dollars
- Know which tool calls were slow
- Filter by machine (Mac Studio vs MBP vs your VPS), by agent source (interactive vs scheduled), by project
- Catch silent failures before they cause downstream damage
- Hand a teammate a link to a specific trace when debugging together

---

## A Note On Privacy

When you turn this on, your prompts and responses leave your machine and land in either Langfuse Cloud or your own server. Both options redact secrets before sending — see `03-claude-code-integration.md` for how that works — but you should still understand where your data goes before flipping the switch.

If you handle anything sensitive (client data, medical, legal, financial), default to self-hosting from the start.
