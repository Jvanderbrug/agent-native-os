# 02: n8n-cli for Power Users

The n8n web UI is great for building. It is bad at:

- Managing 50+ workflows across two instances
- Bulk operations (activate everything tagged `production`, export everything tagged `archive`)
- Diffing workflows between cloud and self-hosted
- Searching "which workflow uses Slack credential X?"
- Anything you want to script

That's what `n8n-cli` is for.

## What Is n8n-cli?

`n8n-cli` is a Python CLI for the n8n REST API. It is open-source, MIT-licensed, and has zero external dependencies (Python stdlib only). Built and maintained by AI Build Lab.

Repo: https://github.com/8Dvibes/n8n-cli

What it gives you:
- 80+ commands across workflows, executions, credentials, tags, variables, projects, users, packages, nodes, webhooks
- Auto-updating local catalog of all 543+ n8n nodes (searchable offline)
- Multi-instance profiles (cloud + self-hosted in one tool)
- 40 Claude Code skills that wrap common patterns
- `--json` flag on every command for piping to `jq` or other tools

## Install

```bash
# From PyPI (recommended)
pip install n8n-toolkit

# Or with pipx if you prefer isolation
pipx install n8n-toolkit

# Or from source if you want to hack on it
git clone https://github.com/8Dvibes/n8n-cli.git
cd n8n-cli && pip install .
```

Verify:
```bash
n8n-cli --help
```

## Configure Your First Profile

You need an n8n API key. In your n8n instance:

1. Click your profile icon (top right) → Settings → API
2. Click "Create new API key"
3. Copy the key (you won't see it again)

Then configure n8n-cli:

```bash
n8n-cli config set-profile cloud \
  --url "https://yourname.app.n8n.cloud/api/v1" \
  --key "your-api-key-here" \
  --default

n8n-cli health
```

`health` should print something like `OK · n8n 1.x.x · X workflows`.

## Add a Second Profile (Self-Hosted)

If you also have a self-hosted instance:

```bash
n8n-cli config set-profile selfhosted \
  --url "https://n8n.yourdomain.com/api/v1" \
  --key "your-selfhosted-key"

# Switch between them with --profile
n8n-cli --profile selfhosted workflows list
n8n-cli --profile cloud workflows list

# Or change your default
n8n-cli config use selfhosted
```

Profiles are stored in `~/.n8n-cli.json` (mode 600, so other users on the machine can't read your API keys).

## The 5 Commands You'll Use Constantly

```bash
# 1. List workflows (filter by active/tag/name)
n8n-cli workflows list --active
n8n-cli wf ls --tag "production"

# 2. Get full details of one workflow
n8n-cli workflows get <id>

# 3. Export a workflow to JSON (for git, backup, sharing)
n8n-cli workflows export <id> -o my-workflow.json

# 4. Import a workflow from JSON
n8n-cli workflows import my-workflow.json --activate

# 5. Tail recent failures
n8n-cli executions list --status error --limit 10
```

Add `--json` to any of these to get machine-readable output:

```bash
n8n-cli --json workflows list --active | jq '.[].name'
n8n-cli --json executions list --status error | jq length
```

## The Node Catalog (Offline, Searchable)

Without ever connecting to a live n8n instance:

```bash
# Search 543+ nodes by keyword
n8n-cli nodes search slack
n8n-cli nodes search openai
n8n-cli nodes search postgres

# Get full property schema for any node
n8n-cli nodes get slack --full
```

This is invaluable when you're writing workflow JSON by hand or in Claude Code — you can check the exact node type name and property structure without leaving the terminal.

## Claude Code Skills (40 of Them)

If you use Claude Code, install the bundled skills:

```bash
n8n-cli skills install
```

This drops 40 slash commands into `~/.claude/skills/`. Restart Claude Code and you can type these directly:

**Core 11:**
- `/n8n-cli-status` — health check + active workflows + recent errors in one view
- `/n8n-cli-debug` — analyze failed executions, suggest fixes
- `/n8n-cli-create` — describe a workflow in English, Claude builds and imports it
- `/n8n-cli-import` / `/n8n-cli-export` — guided import/export with credential mapping
- `/n8n-cli-monitor` — watch the execution stream from your terminal
- `/n8n-cli-migrate` — move workflows between cloud and self-hosted
- `/n8n-cli-backup` — full instance backup to a git directory
- `/n8n-cli-diff` — compare workflows between instances or against local files
- `/n8n-cli-webhook-test` — fire test payloads at webhook workflows
- `/n8n-cli-creds` — find missing credentials for a workflow

**Plus 29 more** for hygiene (`/n8n-cli-cleanup`, `/n8n-cli-cost`, `/n8n-cli-tag-governance`), authoring (`/n8n-cli-document`, `/n8n-cli-refactor`, `/n8n-cli-review`), dependency mapping (`/n8n-cli-deps`, `/n8n-cli-impact`), production ops (`/n8n-cli-meta-monitor`, `/n8n-cli-upgrade-preflight`, `/n8n-cli-bulk`), testing (`/n8n-cli-test-fixtures`, `/n8n-cli-replay`, `/n8n-cli-smoke`), and bridges (`/n8n-cli-from-cron`, `/n8n-cli-from-launchd`, `/n8n-cli-from-zapier`, `/n8n-cli-from-mcp`, `/n8n-cli-to-mcp`).

Full skill list and details: https://github.com/8Dvibes/n8n-cli#claude-code-skills

## Why This Beats the n8n Web UI at Scale

| Task | Web UI | n8n-cli |
|------|--------|---------|
| List all active workflows | Click through pages | One command |
| Find every workflow using credential X | Manually open each one | `n8n-cli skills install` then `/n8n-cli-node-usage` |
| Back up to git | Export each one by hand | `/n8n-cli-backup` (or `n8n-cli workflows export` in a loop) |
| Diff cloud vs self-hosted | Open both UIs side by side | `/n8n-cli-diff` |
| Bulk activate by tag | Click each toggle | `/n8n-cli-bulk` (with mandatory dry-run) |
| Find dead workflows | Eyeball "last execution" times | `/n8n-cli-cleanup` |

## Common Workflows

**Daily git backup of your whole instance:**
```bash
n8n-cli workflows list --json | jq -r '.[].id' | \
  xargs -I{} n8n-cli workflows export {} -o "backup/{}.json"
git add backup && git commit -m "n8n daily backup"
```

**Sanity check before a big change:**
```bash
n8n-cli health
n8n-cli workflows list --active
n8n-cli executions list --status error --limit 5
```

**Move one workflow from cloud to self-hosted:**
```bash
n8n-cli --profile cloud workflows export <id> -o /tmp/wf.json
n8n-cli --profile selfhosted workflows import /tmp/wf.json --activate
# (then use /n8n-cli-creds to remap credentials)
```

## When to Reach for n8n-cli vs the Web UI

- **Building or visually debugging a workflow** → web UI
- **Anything bulk, anything scripted, anything multi-instance** → n8n-cli
- **Inside a Claude Code session** → the slash commands (Claude calls n8n-cli for you)

Most workshop graduates end up using both, with n8n-cli growing share over time as their workflow library grows past ~10 workflows.

## Next

`03-claude-and-n8n.md` covers the three integration patterns for connecting Claude Code, the Claude API, and n8n in a working agent stack.
