# Component 10: Delivery Channels

> **This is Block 10: Delivery Channels.**
>
> **What you'll have:** Your morning brief notifies you automatically in the place you already check. The notification is short. The full brief lives in Obsidian, a Vercel page, or another surface you choose.
>
> **How this stacks toward the Capstone:** The Capstone is a morning brief system. Delivery channels are how the system tells you "the brief is ready" without dumping a wall of text into your phone.
>
> **Why now:** You needed the scheduled brief first (Component 9). You can't forward a brief that doesn't exist yet. Component 11 (Remote Control) builds on this too — you can't receive a reply from your agent if you haven't established a channel first.

---

## What you're building

Right now your morning brief:
1. Runs automatically at 6 AM via launchd (Component 9)
2. Writes a markdown file to your Obsidian vault

After this component, it also:
3. **Sends you a short ping with the brief title, top priority, and where to read the full version**

One small change to the launcher script. That's it.

---

## Why the launcher, not the slash command

The brief already writes to Obsidian inside the slash command. We could try to add delivery there — but iMessage delivery doesn't belong in the brief itself. Delivery is infrastructure, not content. The slash command stays clean; the launcher handles the routing.

Think of it like this: the slash command is the journalist who writes the story. The launcher is the distribution system that decides where it goes. Content and delivery are separate concerns.

---

## The install

### Step 1 — Open the launcher

```bash
open ~/.claude/morning-brief-launcher.sh
```

Or open it in Claude Code directly.

### Step 2 — Remove `exec`, add the delivery block

Find this line at the bottom:

```bash
exec /opt/homebrew/bin/claude -p --permission-mode bypassPermissions "/morning-brief"
```

Replace it with:

```bash
/opt/homebrew/bin/claude -p --permission-mode bypassPermissions "/morning-brief"

# Delivery Channel: iMessage short ping
TODAY=$(date +%Y-%m-%d)
BRIEF_FILE="$HOME/Documents/second-brain/daily-briefings/${TODAY}-brief.md"

if [[ -f "$BRIEF_FILE" ]]; then
    BRIEF_PREVIEW=$(head -20 "$BRIEF_FILE" | sed '/^$/d' | head -5)
    osascript <<APPLESCRIPT
tell application "Messages"
    set targetService to 1st account whose service type = iMessage
    set briefMessage to "Morning brief is ready: $BRIEF_FILE

$BRIEF_PREVIEW"
    send briefMessage to participant "+1XXXXXXXXXX" of targetService
end tell
APPLESCRIPT
fi
```

Replace `+1XXXXXXXXXX` with your own phone number.

**Why we removed `exec`:** `exec` replaces the running shell process — meaning nothing after it ever runs. Removing it lets the script continue after Claude finishes, so the delivery step can fire.

### Step 3 — Save and test

Run the launcher manually to verify the full flow works before trusting it to the 6 AM schedule:

```bash
~/.claude/morning-brief-launcher.sh
```

Wait 2–3 minutes. You should:
1. See the brief write to your Obsidian vault
2. Receive a short iMessage with the path to the full brief

---

## Verification checklist

- [ ] Brief still writes to Obsidian (same as before)
- [ ] iMessage arrives on your iPhone within ~3 minutes of the launcher running
- [ ] The iMessage is short enough to read quickly
- [ ] The full brief location is clear
- [ ] No errors in `~/Library/Logs/morning-brief/` (the launchd log)

---

## Gotchas

**"I got an AppleScript error about iMessage accounts"**
The script targets the iMessage account specifically (`service type = iMessage`). If Messages isn't signed into iMessage on this Mac, it will fail. Open Messages → Settings → iMessage → confirm you're signed in.

**"The launcher runs but no iMessage arrives"**
macOS requires your terminal or Claude Code app to have Automation permission to control Messages. Go to: System Settings → Privacy & Security → Automation → find your terminal app → check that Messages is ticked.

**"I want the full brief on my phone"**
You can send the whole file, but that usually becomes unreadable fast. The better pattern is short ping plus link or path to the full write-up.

**"Where should the full brief live?"**
For Sunday, use Obsidian as the reliable baseline. The 8D version can use a Vercel frontend and Supabase backend, which both have free tiers that are enough for a personal morning brief. If you use the brief for a business workflow, review the hosting terms and upgrade when needed.

---

## 4D vs. 8D path

| | 4D | 8D |
|---|---|---|
| **Delivery target** | Your own phone number | Slack channel, Telegram, or Vercel-hosted full brief |
| **Channel** | iMessage short ping | Slack webhook, Claude Code Channel, or custom Slack app |
| **What you edit** | Phone number in the launcher | Webhook URL, channel access, and full-brief destination |

**8D: Slack delivery instead of iMessage**

If you prefer Slack (or want to add it alongside iMessage):

1. Create an incoming webhook in your Slack workspace: workspace settings → Integrations → Incoming Webhooks → Add New Webhook
2. Copy the webhook URL
3. Add this block to your launcher instead of the AppleScript block:

```bash
BRIEF_CONTENT=$(head -40 "$BRIEF_FILE")
curl -s -X POST "$SLACK_BRIEF_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "{\"text\": $(echo "$BRIEF_CONTENT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}"
```

Store `SLACK_BRIEF_WEBHOOK_URL` in 1Password and reference it via `op read` — same pattern as your other API keys.

---

## What this unlocks

You now have:
- A brief that runs automatically (Component 9)
- A short notification that tells you the full brief is ready (Component 10)

What you don't have yet: the ability to reply from your phone and have the agent act on it. That's Component 11.
