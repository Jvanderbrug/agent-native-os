# Component 11: Remote Control

> **This is Block 11: Remote Control.**
>
> **What you'll have:** A way to keep working with a Claude Code session from your phone, another computer, Slack, Telegram, Discord, or iMessage depending on which path you choose.
>
> **How this stacks toward the capstone:** Your morning brief should not be trapped on your laptop. The short version should ping you where you already look. The full version should be one click away. Remote Control is how you steer the system after it starts working for you.
>
> **Why now:** Components 8 through 10 gave you a brief, a schedule, and delivery. This component makes the relationship two-way.

---

## The three paths

Use the native path first. Add the others only when you have a reason.

| Path | What it does | Best for |
|---|---|---|
| Remote Control | Continue a local Claude Code session from Claude mobile or `claude.ai/code` | Everyone |
| Channels | Send messages into a running local Claude Code session from iMessage, Telegram, Discord, or fakechat | 8D students and Lab members |
| Dedicated agent identity | Run the agent through its own iCloud/phone identity so messages come from the agent, not from you talking to yourself | 8D fleet builders and production personal agents |
| Custom Slack app | Build your own Gigawatt-style Slack mention listener and agent control plane | 8D fleet builders |

The old iOS Shortcut plus queue-folder pattern is now a fallback, not the main path. It still teaches queues and workers, but Anthropic's native Remote Control and Channels are the right first stop.

---

## Path 1: Native Remote Control

Remote Control lets you keep a Claude Code session running on your machine while you drive it from another device.

Start a Remote Control session in your project:

```bash
claude --remote-control
```

Or turn on Remote Control inside an existing Claude Code session:

```text
/remote-control
```

Claude shows a URL and QR code. Open it from:

- Claude mobile on iOS or Android
- `https://claude.ai/code` on another computer

The work still runs on your machine. Your files, MCP servers, project config, and local tools stay available.

### Server mode

If you want one long-running doorway into your machine:

```bash
claude remote-control --name "Agent OS Home Base"
```

Useful flags:

```bash
claude remote-control --spawn worktree --capacity 8
```

That lets remote sessions spawn into separate git worktrees so they do not stomp on each other.

### Verification

From your phone, send:

```text
What project directory are you running in? List the top-level files.
```

The answer should reflect the local project on your computer.

### Limitations

- The local Claude process must keep running.
- Your machine must stay awake and online.
- Some local-only picker commands still need the terminal.
- Push notifications require a recent Claude Code version. If push matters, update before demoing it.

---

## Path 2: Claude Code Channels

Channels push messages from another app into an already-running local Claude Code session. Unlike Remote Control, you are not opening the Claude mobile/web interface. You are texting or messaging the session from another channel.

Prerequisites:

```bash
bun --version
claude --version
```

Claude Code Channels require Claude Code `2.1.80` or later. Team and Enterprise organizations may need an admin to enable Channels.

### iMessage

macOS only. No bot token. Uses your local Messages database and sends replies through Messages.

Install:

```text
/plugin install imessage@claude-plugins-official
```

Restart Claude Code:

```bash
claude --channels plugin:imessage@claude-plugins-official
```

Then text yourself from Messages. Self-chat is allowed by default.

Important caveat: native iMessage Channels are convenient, but the self-chat version can feel odd. In Tyler's first setup, replies landed in the same thread as his own self-messages, so the agent did not feel like a separate entity. That is fine for a workshop demo and quick tests, but it is not the cleanest production pattern.

The first run may ask for:

- Full Disk Access for the terminal app that launched Claude
- Automation permission to let the terminal control Messages

Allow another sender:

```text
/imessage:access allow +15551234567
```

### Dedicated agent identity

The cleaner 8D pattern is to give the agent its own communication identity.

AI Build Lab runs Gigawatt this way:

- Gigawatt has its own iCloud/iMessage identity and phone number/email surface.
- The sending machine is the M1 Max, not Tyler's main workstation.
- Tyler receives messages from Gigawatt as a separate contact.
- Replies feel like talking to an agent, not texting yourself.

Use this pattern when you want a personal or team agent to feel real, durable, and distinct:

1. Create or use a dedicated Apple ID for the agent.
2. Sign that Apple ID into Messages on the Mac that will host outbound iMessage.
3. Give the agent a clear contact name and avatar in your phone.
4. Route outbound messages through that machine only.
5. Add a signature or visible identity marker so humans know the message is automated.

This is more setup than native Channels, so do not make it the 4D path. Teach native Remote Control and native Channels first. Then show the dedicated identity pattern as the fleet-builder upgrade.

### Telegram

Best cross-platform phone path.

Install:

```text
/plugin install telegram@claude-plugins-official
```

Create a Telegram bot with `@BotFather`, then configure the token:

```text
/telegram:configure <bot-token>
```

Restart:

```bash
claude --channels plugin:telegram@claude-plugins-official
```

DM your bot. It replies with a pairing code. Pair inside Claude Code:

```text
/telegram:access pair <code>
/telegram:access policy allowlist
```

### Discord

Good for students who already live in Discord. Requires a Discord application, bot token, server invite, and Message Content Intent.

```text
/plugin install discord@claude-plugins-official
/discord:configure <bot-token>
```

Restart:

```bash
claude --channels plugin:discord@claude-plugins-official
```

Then DM the bot, pair the code, and switch to allowlist.

### fakechat

Local demo channel. Good for teaching the concept without external auth.

```text
/plugin install fakechat@claude-plugins-official
```

Restart:

```bash
claude --channels plugin:fakechat@claude-plugins-official
```

Open:

```text
http://localhost:8787
```

Type a message. It arrives in your Claude Code session.

---

## Path 3: Custom Slack App

The AI Build Lab fleet pattern is a custom Slack app plus mention listener:

1. Slack app receives mentions or scratchpad messages.
2. Listener verifies sender and channel.
3. Listener writes an event or task.
4. Heartbeat or a persistent Claude Code session picks it up.
5. Claude replies in Slack or links to a full artifact.

This is how you graduate from "I can reach Claude" to "I have an agent operations control plane."

Use this when you want:

- Team visibility
- Custom routing rules
- Scratchpad channels
- Long-running agent behavior
- Audit logs

Do not make this the first path on workshop day. It is an 8D/Lab extension.

---

## Scratchpad pattern

Create one private Slack channel for raw captures, for example:

```text
#my-agent-scratchpad
```

Drop links, thoughts, voice memo transcripts, decisions, and screenshots there. Your agent can periodically read the channel, classify each item, ask follow-up questions, then write to your second brain.

Recommended routing:

| Message type | Destination |
|---|---|
| "Decision: ..." | `/log-decision` |
| "Remember this ..." | second-brain capture skill |
| URL or article | L3 article capture, optional L1 waypoint |
| Open question | decisions-in-flight or work-builds |
| Random thought | scratchpad inbox until reviewed |

The scratchpad is not the memory. It is the inbox. Cairns is the memory.

---

## 4D vs. 8D path

| | 4D | 8D |
|---|---|---|
| Required | Try native Remote Control | Try Remote Control plus one Channel |
| Best channel | Claude mobile or browser | Telegram, fakechat, native iMessage for demos, or dedicated-agent iMessage for production |
| Slack | Understand the pattern | Build or inspect the Slack app/listener pattern |
| Deliverable | Can continue a local session from another device | Can send a message from a channel into a running session |

---

## What this unlocks

You can now reach the agent while it is working.

The next layer is not "more channels." The next layer is routing: when a message arrives, should Claude answer, ask a follow-up, log a decision, add something to the second brain, schedule work, or escalate to you?
