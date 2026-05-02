# n8n in Your Agent-Native OS

This module covers n8n, the visual workflow tool that handles the "always-on triggered work" half of your agent stack. Claude Code is interactive (you sit down and ask it for something). n8n runs in the background on schedules and webhooks (it does work for you while you sleep).

You need both.

## What is n8n?

n8n (pronounced "n-eight-n", short for "nodemation") is an open-source workflow automation tool. Think Zapier, but:

- You can self-host it (no per-zap pricing)
- It has a visual node editor AND a full REST API
- Workflows are JSON files you can version control
- 543+ nodes for popular services (Slack, Gmail, Notion, OpenAI, HTTP, Postgres, etc.)
- It runs custom JavaScript or Python in Code nodes when you outgrow the built-in nodes

It's the "if this then that" layer of your agent stack, but with way more power than IFTTT or Zapier.

## Why It Matters in the Agent-Native OS Stack

Your agent stack has three runtime modes:

| Mode | Tool | When it runs |
|------|------|--------------|
| Interactive | Claude Code in a terminal | When you start it |
| Triggered | n8n workflows | When a webhook hits, a schedule fires, or an event happens |
| API-direct | Claude API in your own code | When your code calls it |

Claude Code is brilliant for one-off thinking work. But you do not want to leave a Claude Code session running 24/7 just to "watch for new emails". That is what n8n is for.

The pattern most graduates settle on:

1. Claude Code drafts the workflow logic during a build session
2. n8n runs it on a schedule or webhook in production
3. Claude Code reviews failures and refactors when something breaks

## The Two-Instance Reality

Most teams end up running n8n in two places:

**n8n Cloud** (`yourname.app.n8n.cloud`)
- Free tier: 5 active workflows, 2.5k executions/month
- Paid plans start around $20/mo
- Zero ops burden, n8n team handles uptime
- Best for: getting started, low-volume personal automation, customer-facing webhooks

**Self-hosted** (Docker on a VPS, or n8n's Hostinger one-click install)
- ~$5-15/mo for a small VPS
- Unlimited workflows and executions
- You manage updates, backups, SSL
- Best for: anything sensitive, high-volume work, or workflows that need to talk to your local network

You can run both. The `n8n-cli` tool (covered in `02-n8n-cli.md`) supports profile switching so you can manage both from one terminal.

Tyler's setup: cloud instance for customer-facing work + a Hostinger self-hosted instance for internal automation. ~$20/mo total.

## When to Use n8n vs Claude Code vs Both

**Use n8n alone when:**
- The work is fully repeatable (same steps, different data)
- It needs to run on a schedule or react to a webhook
- You can describe the logic as a flowchart
- Cost matters (a triggered n8n workflow costs cents; a Claude Code session costs tokens)

**Use Claude Code alone when:**
- The work is exploratory or one-off
- You need judgment, not just transformation
- You want to see and adjust the work as it happens

**Use both when:**
- n8n handles the trigger + data prep + final delivery
- Claude does the "hard thinking" middle step (summarize, classify, draft, decide)
- Three patterns for connecting them are covered in `03-claude-and-n8n.md`

## Module Files

| File | What it covers |
|------|----------------|
| `01-getting-started.md` | Sign up for n8n Cloud and build your first 3-node workflow |
| `02-n8n-cli.md` | Install `n8n-cli` for terminal-based workflow management |
| `03-claude-and-n8n.md` | Three patterns for combining Claude and n8n |
| `../../examples/n8n-workflows/` | Importable example workflow JSON files |

## What This Module Is NOT

- Not a deep tutorial on every n8n node — n8n's docs at https://docs.n8n.io are excellent for that
- Not a guide to building production workflows at scale — start small, then graduate to `n8n-cli` and the workflow patterns library
- Not a Zapier migration guide — but if you need one, the `n8n-cli` ships a `/n8n-cli-from-zapier` skill that does it for you

## Pointers Before You Start

- n8n docs: https://docs.n8n.io
- n8n-cli (Tyler's open-source CLI): https://github.com/8Dvibes/n8n-cli
- n8n community forum: https://community.n8n.io (very active, very helpful)
- The 543+ node catalog: searchable via `n8n-cli nodes search <keyword>` once installed

Move on to `01-getting-started.md` when you're ready.
