# 03: Claude + n8n — Three Integration Patterns

Once you have Claude Code running interactively and n8n running triggered work, you'll want to connect them. There are three patterns. Each has tradeoffs. Pick the one that fits the shape of the work.

## Pattern A: Claude Code Calls n8n via Webhook (Push)

**You are sitting in Claude Code. Claude needs to trigger something to happen out in the world (send a Slack message, write to a database, kick off a long-running process). Instead of Claude doing it directly, it POSTs to an n8n webhook and lets n8n handle the side effect.**

### When to use it

- The side effect is something n8n already does well (Slack post, Notion update, Airtable write)
- You want one canonical place that talks to that service (so you don't scatter Slack tokens across 15 Claude sessions)
- The work might take longer than Claude wants to wait

### Skeleton

n8n side: a workflow with two nodes:

```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "post-to-slack",
        "httpMethod": "POST",
        "responseMode": "lastNode"
      },
      "typeVersion": 1
    },
    {
      "name": "Slack",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "resource": "message",
        "operation": "post",
        "channel": "={{ $json.body.channel }}",
        "text": "={{ $json.body.text }}"
      },
      "typeVersion": 2
    }
  ]
}
```

Claude Code side (just bash):
```bash
curl -X POST https://yourname.app.n8n.cloud/webhook/post-to-slack \
  -H "Content-Type: application/json" \
  -d '{"channel": "#general", "text": "Hello from Claude"}'
```

### Tradeoffs

- Cost: near-zero (one n8n execution, no Claude tokens)
- Latency: ~500ms-2s
- Debuggability: high — you see the full execution in n8n's Executions log
- Caveat: webhook URLs are essentially passwords. Use n8n's "Header Auth" or "Basic Auth" on the webhook node for anything sensitive.

## Pattern B: n8n Triggers Run a Claude Code Task via API

**An n8n workflow needs Claude to do something hard (summarize a document, classify customer feedback, write a draft). The n8n Schedule Trigger or Webhook fires, n8n preps the data, then it calls the Claude API directly from an HTTP Request node.**

### When to use it

- You want Claude's reasoning inside a triggered, scheduled workflow
- The output needs to flow back into the rest of the n8n workflow
- You don't want a human in the loop

### Skeleton

```json
{
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": { "interval": [{ "field": "hours", "hoursInterval": 1 }] }
      },
      "typeVersion": 1
    },
    {
      "name": "Get Recent Tickets",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://your-helpdesk.com/api/tickets?status=new"
      },
      "typeVersion": 4
    },
    {
      "name": "Classify with Claude",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://api.anthropic.com/v1/messages",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "anthropicApi",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            { "name": "anthropic-version", "value": "2023-06-01" }
          ]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            { "name": "model", "value": "claude-sonnet-4-5" },
            { "name": "max_tokens", "value": "1024" },
            { "name": "messages", "value": "=[{\"role\":\"user\",\"content\":\"Classify this ticket as urgent/normal/spam: {{ $json.body }}\"}]" }
          ]
        }
      },
      "typeVersion": 4
    }
  ]
}
```

n8n now has a built-in "Anthropic" node (search `n8n-cli nodes search anthropic`) so you can skip the raw HTTP Request boilerplate if you prefer. The HTTP Request version is shown here because it works on every n8n version and makes the API call obvious.

### Tradeoffs

- Cost: Claude API tokens per execution (cheap, but multiplies with frequency)
- Latency: 2-30 seconds depending on prompt and model
- Debuggability: medium — n8n shows the request and response, but the prompt itself can get hard to edit inline
- Use prompt caching (`cache_control: { type: "ephemeral" }` on the system prompt) when the same prompt fires repeatedly

## Pattern C: n8n + Claude API in Custom Code (No Claude Code at All)

**You've outgrown the "n8n calls Claude" pattern and want full control: streaming, tool use, multi-turn conversations, custom retry logic. You build a small Node or Python service that wraps the Claude API, deploy it somewhere (Vercel, Cloud Run, your VPS), and have n8n call your service via HTTP Request.**

### When to use it

- Your prompt is long enough or complex enough that maintaining it inside an n8n HTTP Request body is painful
- You need streaming, tool use, or computer use
- You want one canonical Claude wrapper that multiple n8n workflows (and other apps) can call

### Skeleton

Tiny wrapper service (Node, deployed to Vercel as a serverless function):

```js
// api/classify.js
import Anthropic from "@anthropic-ai/sdk";
const anthropic = new Anthropic();

export default async function handler(req, res) {
  const { ticket_body } = req.body;

  const result = await anthropic.messages.create({
    model: "claude-sonnet-4-5",
    max_tokens: 1024,
    system: [{
      type: "text",
      text: "You are a ticket classifier. Return JSON: {category, urgency, summary}.",
      cache_control: { type: "ephemeral" }
    }],
    messages: [{ role: "user", content: ticket_body }]
  });

  res.json(JSON.parse(result.content[0].text));
}
```

n8n side: HTTP Request to `https://your-app.vercel.app/api/classify` with `{ticket_body: "..."}`.

### Tradeoffs

- Cost: Claude API tokens + tiny serverless cost (often free tier)
- Latency: Same as Pattern B (one extra hop, usually <100ms)
- Debuggability: highest — you control logging, error handling, retries
- Maintenance: highest — you now own a deployed service

## Decision Matrix

| Need | Pattern |
|------|---------|
| Claude Code wants to trigger a Slack post | A (push) |
| Daily cron that summarizes yesterday's tickets | B (n8n + Claude API node) |
| Customer-facing webhook that needs <2s response with cached prompts and tool use | C (custom service) |
| One-off "Claude, please do X" | Just Claude Code, skip n8n |
| Same exact transformation on 10k records | Just n8n, skip Claude |

## Cost / Latency / Debuggability Cheat Sheet

| Pattern | Cost | Latency | Debug | Maintenance |
|---------|------|---------|-------|-------------|
| A: Claude → n8n webhook | $ | low | high | low |
| B: n8n → Claude API node | $$ | medium | medium | low |
| C: n8n → custom service → Claude API | $$ | medium | highest | high |

Start with A. Graduate to B when you need scheduled AI. Move to C only when B's prompt-in-JSON gets unwieldy.

## What NOT to Do

- **Do not run Claude Code as the long-running service.** It's interactive by design. Use the Claude API directly when you need 24/7 work.
- **Do not put Claude API keys in n8n workflow JSON.** Always use n8n credentials so the key isn't in the export.
- **Do not skip the dry-run when n8n is calling expensive Claude prompts on a schedule.** Test once, watch the Execution log, then activate.
- **Do not chain three Claude API calls in one workflow when one with prompt caching would do.** Cost adds up fast.

## Examples

See `../../examples/n8n-workflows/` for importable JSON files demonstrating these patterns.

## Next

You now have the three patterns. Build something small with one of them this week — a daily summary, a classifier, a Slack notifier. The point is reps, not the perfect first workflow.
