# 04 — Using The Dashboard (Day 2 Power User)

**Goal:** Stop thinking of Langfuse as "the place traces land" and start using it as the actual operations console for your fleet.

This guide assumes you have traces flowing in from Guide 03. Open your dashboard and follow along.

---

## The Mental Model

Langfuse organizes data in a hierarchy:

```
Project
  └─ Session (one Claude Code conversation, end to end)
       └─ Trace (one user turn → assistant response)
            ├─ Generation (the LLM call itself, with model/cost/tokens)
            └─ Span (each tool call: Bash, Read, Edit, Web, etc.)
```

You can navigate at any level. The most common day-2 moves are at the Session and Trace level.

---

## Move 1: Find A Specific Session

You ran something an hour ago and want to see what happened.

**Tracing → Sessions** in the left sidebar. You see a list of every session, newest first. Each row shows:

- Session ID (the Claude Code session ID)
- Number of traces
- Total tokens
- Total cost
- Tags
- First timestamp

Click into any session to see all the turns inline. Each turn shows the user message at the top, assistant response below, tool calls expandable.

---

## Move 2: Filter By Tag

The tags you set up in Guide 03 (machine, agent source, project) are the main filtering tool.

In the Sessions or Traces view, click **Filters** at the top. Add filters like:

- `Tags contains mac-studio` — only sessions from your Mac Studio
- `Tags contains mention-listener` — only sessions kicked off by the autonomous responder
- `Tags contains client-acme` — only sessions for one project

Combine filters: "show me everything mention-listener did on m1-max in the last 24 hours." This is the killer feature for multi-machine fleets.

---

## Move 3: Compare Costs Across Models

You want to know: am I burning more on Sonnet or Opus this week? Should I downshift some workloads to Haiku?

**Dashboards → Usage** (or build a custom dashboard). Group by model name, time-bucket by day. You'll see a bar chart of token usage and dollar cost per model per day.

Look for:
- One model dominating cost — candidate for downshifting on routine work
- A spike on one specific day — drill into that day's sessions to find what burned the budget
- A model you forgot you were using — sometimes a script defaults to Opus for tiny tasks

---

## Move 4: Find The Slowest Tool Calls

Long sessions are usually long because of one or two tool calls. Find them.

**Tracing → Observations**, filter by `Type = SPAN`, sort by **Latency** descending. The slowest spans float to the top.

Common offenders:
- WebFetch with a large page (multi-second download + LLM summarization)
- Bash commands that wait for a long-running process
- File reads of huge JSONL transcripts
- Tool calls that hit slow third-party APIs

Once you know which tool is slow on which input, you can fix the workflow — paginate, cache, or split the call.

---

## Move 5: Catch Errors Before They Cascade

Filter Traces by **Level = ERROR** or look for traces with very short outputs (often a sign the assistant errored out early).

Better: set up an alert.

**Settings → Webhooks → Add webhook.** Configure:
- Trigger: trace created with `level = error`
- Endpoint: a Slack incoming webhook URL, or your n8n webhook, or a generic monitoring endpoint
- Payload: trace ID, session ID, tags

Now any agent error pings you instantly. You don't have to remember to check the dashboard.

---

## Move 6: Cost Spike Alerting

Same pattern, different trigger. Use webhooks (or schedule a daily summary job) to flag when:

- Daily cost exceeds a threshold (e.g., $20/day)
- A single session exceeds a threshold (e.g., $5/session)
- A specific tag's cost trends up week-over-week

If your provider doesn't support this in webhooks directly, write a small n8n workflow that hits the Langfuse Public API on a schedule, sums the costs, and alerts via Slack/email when over budget.

---

## Move 7: Compare Two Sessions Side By Side

You changed a prompt or a CLAUDE.md file and want to know if it helped.

Open two browser tabs, one for each session. Look at:
- Total tokens (did the new version use more or less?)
- Tool call count (did it need fewer steps?)
- Final assistant text (did it get to a better answer?)
- Duration

For more rigor, set up **Evaluations** — Langfuse has a built-in framework for scoring traces against criteria, including LLM-as-judge. Out of scope for this guide but worth exploring once you outgrow eyeballing.

---

## Move 8: Export Traces For Offline Analysis

Sometimes you want raw data — to feed into a notebook, train a fine-tune, or audit a specific period.

**Public API:**

```bash
curl -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces?limit=100&fromTimestamp=2026-01-01T00:00:00Z" \
  | jq .
```

You get JSON with full trace data. Pipe to a file, load in pandas or DuckDB, do whatever you want.

**Bulk export:** for very large pulls, the API supports pagination via `page` and `limit`. Loop until you've drained everything.

---

## Move 9: Share A Trace With A Teammate

Debugging together. Hit the share button on any trace — Langfuse generates a public URL valid for as long as you want it (or revocable).

Send the link in Slack. Your teammate sees the exact same trace view, no login required. Great for "look at what my agent did at 3 AM and tell me where it went wrong."

If you're on self-hosted, your share links are on your domain. If you're on Cloud, they're on `cloud.langfuse.com`. Both work the same way.

---

## Move 10: Build A Custom Dashboard

The default dashboards are good. Custom ones are better.

**Dashboards → New dashboard.** Add widgets:

- Top 10 most expensive sessions this week
- Tool call distribution (which tools fire most often)
- Error rate trend
- Agent source breakdown (interactive vs autonomous traffic)
- Daily cost per machine

Pin the dashboard, bookmark it in your browser, glance at it once a day. The point is to make the state of your fleet visible at a glance instead of having to dig.

---

## Antipatterns To Avoid

- **Tracing every experimental session.** You'll bloat the dashboard with noise. Only enable `TRACE_TO_LANGFUSE=true` when you want to keep the data.
- **Treating redacted traces as fully safe to share publicly.** They're safer, not safe. Default to private share links.
- **Ignoring the queue file.** If `~/.claude/state/pending_traces.jsonl` keeps growing, your hooks can't reach Langfuse — fix the connection rather than letting the queue swell.
- **Putting different agents in the same project with no tags.** You'll never be able to filter. Tag everything.
- **Skipping the cost dashboard.** This is the single biggest reason to have observability. Look at it weekly.

---

## You're Done

You now have:
- A working Langfuse instance (Cloud or self-hosted)
- Claude Code wired to send traces automatically with secret redaction
- Tags letting you filter by machine, agent, project
- A dashboard you actually look at

Loop back to `README.md` if you want to share this module with someone else, or move on to the next guide in your track.
