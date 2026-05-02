# Example n8n Workflows

These are importable n8n workflow JSON files you can drop into your own instance and customize. They are intentionally minimal — start here, then graduate to more complex patterns from `~/GitHub/n8n-workflows/` (Tyler's workflow library, 186+ workflows tagged by node type).

## How to Import

**Via the web UI:**
1. Open your n8n instance
2. Workflows → Import from File
3. Select one of the JSON files in this directory
4. Set up any credentials the workflow needs
5. Activate

**Via n8n-cli:**
```bash
n8n-cli workflows import 01-hello-hackernews.json
n8n-cli workflows import 04-schedule-http-slack.json --activate
```

See `../../guides/n8n/02-n8n-cli.md` for n8n-cli setup.

## What's Here

| File | Trigger | What it does | Credentials needed |
|------|---------|--------------|--------------------|
| `01-hello-hackernews.json` | Manual | Fetches the latest Hacker News stories. The simplest possible n8n workflow — a trigger and one node. Use this to verify your instance works. | None |
| `02-rss-fetcher.json` | Manual | Reads an RSS feed and outputs the items. Swap the URL to any feed you care about. | None |
| `03-datetime-parse.json` | Manual | Demonstrates the DateTime node parsing a custom format. Trivial, but useful as a reference for date handling. | None |
| `04-schedule-http-slack.json` | Schedule (hourly) | The canonical "first real workflow" from `01-getting-started.md`. Hits a public Bitcoin price API on a schedule and posts to Slack. | Slack OAuth2 |

## After You Import

Each of these is a starting point, not a finished workflow. After importing:

1. **Open it in the editor** — click around, see how the nodes connect
2. **Run it manually first** — click "Test workflow" to see the data flow before activating
3. **Wire your own credentials** — the Slack workflow needs your Slack credential set up
4. **Customize** — change the URL, the channel, the schedule interval

## Adding More

This directory will grow as the workshop curriculum expands. Future additions will pull from Tyler's `~/GitHub/n8n-workflows/` collection (186+ workflows by node type) and from cohort student submissions, after stripping any credentials, instance IDs, or sensitive endpoint URLs.

## Safety Note

If you find a workflow JSON file anywhere (Reddit, Discord, a tutorial repo) and want to import it: **always inspect it first**. Look for:

- Hardcoded API keys (`sk-...`, `xoxb-...`, `ghp_...`, `Bearer <token>`)
- Webhook URLs that point to someone else's instance
- Database connection strings
- Email addresses or phone numbers

n8n-cli ships a `/n8n-cli-import` skill that walks Claude Code through credential mapping safely. Use it for unknown workflows.

## Source

The three Manual-triggered examples (01, 02, 03) are sourced from the public n8n workflow library at https://github.com/Zie619/n8n-workflows (a community-maintained collection of 2,000+ workflows). They have been audited for sensitive content before inclusion here.

The Schedule+HTTP+Slack example (04) is a clean reference implementation matching the tutorial in `../../guides/n8n/01-getting-started.md`.
