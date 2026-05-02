# 01: Your First n8n Workflow

Goal: in under 30 minutes, you'll have a live n8n Cloud account and a workflow that fires on a schedule, fetches data from an HTTP API, and sends a message to Slack.

This intentionally does NOT involve Claude. The point is to get comfortable with the n8n interface, credentials, and execution model before adding AI to the mix.

## Step 1: Sign Up for n8n Cloud

1. Go to https://n8n.io
2. Click "Get Started" and pick the Cloud free tier
3. Pick a workspace name — this becomes your subdomain, e.g. `yourname.app.n8n.cloud`
4. Confirm your email and log in

The free tier gives you 5 active workflows and 2.5k executions per month. Plenty for learning.

## Step 2: Get Your First Credential Set Up

Pick one channel where you want notifications. Easiest options:

**Option A: Slack (recommended if you have a workspace)**
1. In n8n, go to Credentials (left sidebar) > New Credential
2. Search "Slack"
3. Pick "Slack OAuth2 API" and click "Sign in with Slack"
4. Authorize the workspace and channel scope you want

**Option B: Gmail (if no Slack)**
1. Credentials > New Credential > "Gmail OAuth2"
2. Sign in with the Google account you want to send from
3. Grant the requested scopes

Save the credential. Name it something obvious like "My Slack" or "Personal Gmail".

## Step 3: Build the 3-Node Workflow

Click "Workflows" in the sidebar, then "+ Add workflow".

You'll be looking at an empty canvas with a "+" button.

### Node 1: Schedule Trigger

1. Click the "+" button
2. Search for "Schedule Trigger"
3. Set "Trigger Interval" to "Every X" minutes — pick 1 minute for testing (you can change it later)
4. Click "Back to canvas"

### Node 2: HTTP Request

1. Click the "+" to the right of the Schedule Trigger
2. Search for "HTTP Request"
3. Settings:
   - Method: GET
   - URL: `https://api.coindesk.com/v1/bpi/currentprice.json`
   - (No auth needed, this is a public Bitcoin price API)
4. Click "Test step" — you should see a JSON response with current BTC prices
5. Click "Back to canvas"

That URL was picked because it's public, free, requires no auth, and returns predictable data. Substitute any other public JSON API if you prefer.

### Node 3: Slack (or Gmail)

**For Slack:**
1. Click "+" after HTTP Request
2. Search "Slack"
3. Resource: "Message"
4. Operation: "Send"
5. Select your credential
6. Channel: pick a test channel (`#test` or DM yourself)
7. Text: paste this expression
   ```
   Bitcoin is currently ${{ $json.bpi.USD.rate }} USD as of {{ $json.time.updated }}
   ```
8. Click "Test step" — you should get a Slack message

**For Gmail:**
1. Click "+" after HTTP Request
2. Search "Gmail" → Resource: Message → Operation: Send
3. To: your own email address
4. Subject: `BTC update`
5. Message: same expression as above
6. Test step

## Step 4: Activate It

1. Click the "Inactive" toggle in the top right to switch to "Active"
2. The workflow now runs on the schedule you set

If you set it to every 1 minute for testing, change it to something less spammy (every hour, every day) before walking away.

## Step 5: Watch It Execute

1. Click "Executions" in the left sidebar
2. You'll see a log of every run, with status (success/error) and the data each node produced
3. Click into any execution to see the full input/output of each node

This is the n8n "what just happened" view. You'll come here every time something breaks.

## What You Just Learned

- Credentials live separately from workflows (so you can swap accounts without rebuilding)
- Triggers start workflows (Schedule, Webhook, Email Read, etc.)
- Most nodes do one specific thing (HTTP request, send Slack, query database)
- Expressions use `{{ }}` to reference data from previous nodes
- Executions log every run with full data — invaluable for debugging

## Common Beginner Gotchas

- **"My credential isn't showing up"** — make sure you saved it. The Credentials list will confirm.
- **"My expression returns `[object Object]`"** — you forgot to drill into the field. Use `{{ $json.fieldName }}`, not `{{ $json }}`.
- **"My workflow won't activate"** — at least one node has an error. Hover over node icons to see red badges.
- **"Schedule Trigger fires immediately when I save"** — that's by design for testing. After it fires once, it runs on schedule.

## Next

You now know the n8n surface. Next stop: `02-n8n-cli.md` for the terminal-based way to manage all this once you have more than 3 workflows.
