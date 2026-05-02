# Component 11: Remote Control

> **This is Block 11: Remote Control.**
>
> **What you'll have:** An iOS Shortcut on your iPhone home screen. Tap it, type a question, get a reply on iMessage within a few minutes. Your agent takes orders from your phone — not just reports to it.
>
> **How this stacks toward the Capstone:** The Capstone (`/build`) is about an agent that builds other agents. Remote Control is the first time you experience the relationship going both ways: you push, it responds. That's what makes it a fleet, not a scheduled script.
>
> **Why now:** You needed the delivery channel first (Component 10). An agent that receives commands but can't send replies is useless. Now both directions work.

---

## What you're building

Three pieces:

1. **A queue folder** on your Mac — a simple directory where commands land
2. **A queue processor** — a script that runs every 60 seconds, picks up any queued commands, runs them through Claude, and sends the result to your phone
3. **An iOS Shortcut** — a one-tap interface on your iPhone home screen that drops a command into the queue via SSH

Why this design instead of polling iMessages directly: iMessage in iCloud doesn't reliably write incoming messages to the local SQLite database. The queue file approach works regardless of your iCloud sync settings.

---

## The install

### Step 1 — Create the queue folder

```bash
mkdir -p ~/.claude/remote-queue
```

### Step 2 — Create the queue processor script

Save this as `~/.claude/remote-queue-processor.sh`:

```bash
#!/bin/zsh
source ~/.zshrc 2>/dev/null

QUEUE_DIR="$HOME/.claude/remote-queue"
MY_PHONE="+1XXXXXXXXXX"   # ← your phone number

for cmd_file in "$QUEUE_DIR"/*.txt(N); do
    [[ -f "$cmd_file" ]] || continue

    CMD=$(cat "$cmd_file")
    [[ -z "$CMD" ]] && { rm -f "$cmd_file"; continue; }

    TEMP_RESPONSE="/tmp/remote-queue-response-$$.txt"
    /opt/homebrew/bin/claude -p --permission-mode bypassPermissions "$CMD" > "$TEMP_RESPONSE" 2>&1

    osascript <<APPLESCRIPT
tell application "Messages"
    set targetService to 1st account whose service type = iMessage
    set responseText to (read POSIX file "$TEMP_RESPONSE" as text)
    send responseText to participant "$MY_PHONE" of targetService
end tell
APPLESCRIPT

    rm -f "$TEMP_RESPONSE"
    rm -f "$cmd_file"
done
```

Make it executable:
```bash
chmod +x ~/.claude/remote-queue-processor.sh
```

### Step 3 — Create the launchd job (every 60 seconds)

Save this to `~/Library/LaunchAgents/com.aibuildlab.remote-queue.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aibuildlab.remote-queue</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/zsh</string>
        <string>/Users/YOUR_USERNAME/.claude/remote-queue-processor.sh</string>
    </array>

    <key>StartInterval</key>
    <integer>60</integer>

    <key>RunAtLoad</key>
    <false/>

    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/Library/Logs/remote-queue/stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/Library/Logs/remote-queue/stderr.log</string>
</dict>
</plist>
```

Replace `YOUR_USERNAME` with your Mac username. Then load it:

```bash
mkdir -p ~/Library/Logs/remote-queue
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.aibuildlab.remote-queue.plist
```

Verify it loaded:
```bash
launchctl list | grep remote-queue
# Should show: -  0  com.aibuildlab.remote-queue
```

### Step 4 — Test the Mac side before touching your phone

Manually drop a command in the queue:

```bash
echo "What are my top 3 priorities today?" > ~/.claude/remote-queue/test.txt
```

Manually fire the processor:

```bash
~/.claude/remote-queue-processor.sh
```

Wait 2–3 minutes. You should get an iMessage with Claude's response. If that works, the Mac side is complete.

---

## Step 5 — The iOS Shortcut

This is what puts the "from your phone" in remote control.

**Prerequisites:**
- Your Mac must be reachable from your phone via SSH
- On your home network: use your Mac's local IP (find it: `ipconfig getifaddr en0`)
- Away from home: install [Tailscale](https://tailscale.com) on both your Mac and iPhone (free). Use your Tailscale IP instead (`tailscale ip`)

**Building the Shortcut:**

1. Open the Shortcuts app on your iPhone
2. Tap **+** to create a new Shortcut
3. Add action: **Text** → type your default command prompt or leave blank
4. Add action: **Ask for Input**
   - Prompt: `What do you want to ask your agent?`
   - Input type: Text
5. Add action: **Run Script Over SSH**
   - Host: your Mac's IP (local or Tailscale)
   - Port: `22`
   - User: your Mac username
   - Auth: Password (enter your Mac login password) OR SSH Key (advanced track)
   - Script:
     ```
     /bin/zsh -l -c "printf '%s' '$input$' > ~/.claude/remote-queue/$(date +%s).txt"
     ```
   - In the Script field, replace `$input$` with the **Shortcut Input** variable from step 4
6. Add action: **Show Notification** → text: `Sent to your agent. Reply coming via iMessage.`
7. Name it **Remote Agent**
8. Long-press the Shortcut → **Add to Home Screen**

**What the Shortcut does in ~2 seconds:**
- Prompts you for a question
- SSHs into your Mac
- Writes the question as a `.txt` file to `~/.claude/remote-queue/`
- Shows a confirmation and exits

Your Mac's queue processor handles the rest. Reply arrives via iMessage within ~3 minutes.

---

## Verification checklist

- [ ] Queue folder exists at `~/.claude/remote-queue/`
- [ ] Processor script is executable (`chmod +x`)
- [ ] launchd job shows in `launchctl list | grep remote-queue`
- [ ] Manual test: drop a file, run processor, get iMessage reply ✓
- [ ] iOS Shortcut SSHs in successfully
- [ ] End-to-end: tap Shortcut → type question → receive iMessage reply

---

## Gotchas

**"SSH connection refused" from Shortcut**
Remote Login must be enabled on your Mac: System Settings → General → Sharing → Remote Login → toggle ON.

**"SSH works on home WiFi but not from phone data"**
You're not on the same network. Install Tailscale on both Mac and iPhone. Use the Tailscale IP instead of local IP.

**"I got a reply but it was empty"**
The processor ran but Claude returned nothing, or the queue file was empty. Check `~/Library/Logs/remote-queue/stderr.log` for errors.

**"I asked a slash command and got an error"**
Slash commands like `/morning-brief` work because they're installed in `~/.claude/commands/`. Any command that works interactively in Claude Code will work here. Natural language questions always work.

**"The reply took more than 5 minutes"**
Normal for complex requests (briefing, calendar lookup). Claude + 3 MCPs can take 3–4 minutes. Shorter questions (no MCP calls) reply in under a minute.

---

## Beginner vs. Advanced track

| | Beginner | Advanced |
|---|---|---|
| **SSH auth** | Mac login password | SSH key pair (no password prompt) |
| **Network access** | Home WiFi only (local IP) | Everywhere (Tailscale IP) |
| **Shortcut** | iOS Shortcuts app (visual builder) | Scriptable app (JavaScript, full API) |
| **Queue format** | Plain text `.txt` files | JSON with metadata (priority, context, return channel) |

---

## What this unlocks

You can now push any question or request to your agent from anywhere. The agent processes it and replies.

What you can't do yet: tell your agent *how much* to do on its own. You still approve everything. Component 12 is where you configure trust — which actions the agent can take without asking first.
