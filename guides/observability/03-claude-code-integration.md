# 03 — Wire Langfuse Into Claude Code

**Goal:** Every Claude Code session you run sends traces to Langfuse automatically — with user prompts, assistant responses, every tool call, costs, durations, and tags so you can filter later.

You'll do this with two hooks: `Stop` (fires after each assistant response) and `PostToolUse` (fires after every tool execution).

---

## How Claude Code Hooks Work

Claude Code runs shell scripts at specific lifecycle events. They live in `~/.claude/hooks/` and are wired up in `~/.claude/settings.json`. Hooks receive a JSON payload on stdin. For observability we always exit 0 — never block Claude Code if tracing fails.

| Hook | Fires when | We use it for |
|---|---|---|
| `Stop` | Assistant finishes a response | Send the full turn (user + assistant + tool calls) to Langfuse |
| `PostToolUse` | Any tool call completes | Send each tool call as a span in real-time, so long-running agents are visible mid-flight |

**Opt-in pattern:** the hooks check for `TRACE_TO_LANGFUSE=true` and exit silently otherwise. Set it per-shell when you want tracing on. For autonomous agents that should always trace, set it in their launchd plist or systemd unit.

---

## Step 1: Install The Python SDK

```bash
/opt/homebrew/bin/python3.11 -m pip install langfuse
```

Use any Python 3.11+; match the shebang in the hook scripts to the same interpreter.

---

## Step 2: Set Env Vars Globally

Add to `~/.zshrc`:

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="https://us.cloud.langfuse.com"  # or your self-hosted URL
export LANGFUSE_MACHINE="$(hostname -s)"              # optional, used for tagging
export LANGFUSE_AGENT_SOURCE="interactive"            # override in launchd for fleet agents
```

`source ~/.zshrc` and verify with `echo $LANGFUSE_PUBLIC_KEY`. Don't set `TRACE_TO_LANGFUSE=true` globally — keep it per-shell.

---

## Step 3: Drop In The Hook Scripts

Two scripts live in `~/.claude/hooks/`. Both share the same opt-in check, env-var loading, and redaction helpers — so we'll define those once and reuse.

### Shared helpers (top of both files)

```python
#!/opt/homebrew/bin/python3.11
import json, os, re, sys

# 1. Opt-in: exit silently unless tracing is on
if os.environ.get("TRACE_TO_LANGFUSE", "").lower() != "true":
    sys.exit(0)

PUBLIC = os.environ.get("LANGFUSE_PUBLIC_KEY")
SECRET = os.environ.get("LANGFUSE_SECRET_KEY")
HOST = os.environ.get("LANGFUSE_HOST", "https://us.cloud.langfuse.com")
if not (PUBLIC and SECRET):
    sys.exit(0)

# 2. Secret redaction — keep first 4 + last 4 chars for debuggability
SECRET_PATTERNS = [
    re.compile(r'sk-ant-[A-Za-z0-9\-]+'),       # Anthropic
    re.compile(r'sk-proj-[A-Za-z0-9\-_]+'),     # OpenAI
    re.compile(r'xox[bpa]-[A-Za-z0-9\-]+'),     # Slack tokens
    re.compile(r'ghp_[A-Za-z0-9]{36,}'),        # GitHub PATs (classic)
    re.compile(r'github_pat_[A-Za-z0-9_]+'),    # GitHub PATs (fine-grained)
    re.compile(r'[ps]k-lf-[A-Za-z0-9\-]+'),     # Langfuse keys (yes, redact your own)
    re.compile(r'eyJ[A-Za-z0-9\-_]{20,}\.[A-Za-z0-9\-_]{20,}\.[A-Za-z0-9\-_]{20,}'),  # JWT
    re.compile(r'op://[A-Za-z0-9\-/]+'),        # 1Password refs
]

def _mask(m):
    v = m.group(0)
    return v[:4] + "***" + v[-4:] if len(v) > 8 else "[REDACTED]"

def redact(obj):
    if isinstance(obj, str):
        for p in SECRET_PATTERNS:
            obj = p.sub(_mask, obj)
        return obj
    if isinstance(obj, dict): return {k: redact(v) for k, v in obj.items()}
    if isinstance(obj, list): return [redact(x) for x in obj]
    return obj
```

### Stop hook — `~/.claude/hooks/langfuse_trace.py`

Fires at end of every assistant turn. Walks `~/.claude/projects/{project}/{session}.jsonl`, finds new turns since last run (tracked in `~/.claude/state/langfuse_state.json`), and posts each turn via the SDK:

```python
from langfuse import Langfuse
langfuse = Langfuse(public_key=PUBLIC, secret_key=SECRET, host=HOST)

with langfuse.start_as_current_span(
    name=f"Turn {turn_num}",
    input=redact({"role": "user", "content": user_text}),
) as span:
    langfuse.update_current_trace(
        session_id=session_id,
        tags=["claude-code", machine, agent_source, project_name],
    )
    # nested generation for the LLM call, span per tool call...
    span.update(output=redact({"role": "assistant", "content": assistant_text}))

langfuse.flush()
sys.exit(0)  # always exit 0 — never block Claude Code
```

A production-grade version also handles: an offline queue (`~/.claude/state/pending_traces.jsonl`) that drains when Langfuse is reachable again, truncation of tool outputs over 50k chars, and 0600 file permissions on state files.

### PostToolUse hook — `~/.claude/hooks/langfuse_tool_hook.py`

Fires after every tool call. Posts that one call as a span via raw HTTP (no SDK import — keeps execution under 100ms):

```python
import time, urllib.request
from base64 import b64encode

try: data = json.load(sys.stdin)
except Exception: sys.exit(0)

session_id   = data.get("session_id", "unknown")
tool_name    = data.get("tool_name", "unknown")
tool_use_id  = data.get("tool_use_id", f"tool-{int(time.time())}")
machine      = os.environ.get("LANGFUSE_MACHINE", os.uname().nodename)
agent_source = os.environ.get("LANGFUSE_AGENT_SOURCE", "interactive")
now          = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

payload = {"batch": [
    {"type": "trace-create", "id": session_id, "timestamp": now,
     "body": {"id": session_id, "name": "claude-code-session", "sessionId": session_id,
              "tags": ["claude-code", machine, agent_source, "realtime"]}},
    {"type": "span-create", "id": tool_use_id, "timestamp": now,
     "body": {"traceId": session_id, "id": tool_use_id, "name": f"Tool: {tool_name}",
              "startTime": now, "endTime": now,
              "input": redact(data.get("tool_input", {})),
              "output": redact(data.get("tool_response", {}))}},
]}

auth = b64encode(f"{PUBLIC}:{SECRET}".encode()).decode()
req = urllib.request.Request(f"{HOST}/api/public/ingestion",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
    method="POST")
try: urllib.request.urlopen(req, timeout=5)
except Exception: pass  # never block
sys.exit(0)
```

Make both executable:

```bash
chmod +x ~/.claude/hooks/langfuse_trace.py ~/.claude/hooks/langfuse_tool_hook.py
```

---

## Step 4: Register The Hooks In settings.json

Edit `~/.claude/settings.json` and add:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{"type": "command", "command": "/Users/yourname/.claude/hooks/langfuse_trace.py"}]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{"type": "command", "command": "/Users/yourname/.claude/hooks/langfuse_tool_hook.py"}]
    }]
  }
}
```

Use absolute paths. Hooks run from a working directory you don't control, so relative paths break.

---

## Step 5: Test It

```bash
export TRACE_TO_LANGFUSE=true
cd ~/some-project && claude
```

Have a short conversation — ask Claude to read a file, run a command, write something. Exit. In the Langfuse dashboard you should see a new session, each turn as its own trace, each tool call as a nested span with input + output, and tags including your hostname and `interactive`.

If nothing shows up: `tail ~/.claude/state/langfuse_hook.log` and `tail ~/.claude/state/langfuse_tool_hook.log`. The hooks log every run including errors.

---

## Secret Redaction — How It Works

The `redact()` helper recursively walks every string in the payload (through dicts and lists) and masks known secret patterns: Anthropic, OpenAI, Slack, GitHub, Langfuse, JWTs, 1Password refs. Each match becomes `xxxx***yyyy` — first 4 + last 4 chars kept on purpose so you can debug "did I leak the right kind of token?" without exposing the value.

This is defense in depth, not a guarantee. Treat redacted traces as safe to keep in your own dashboard, not safe to publish openly.

---

## Tagging Strategy

Tags are the main filtering tool. The recommended set:

- `claude-code` — always present, identifies the source platform
- **Machine hostname** — so you can filter "what did each machine do today?"
- **Agent source** — `interactive` (human at keyboard), `mention-listener`, `responder`, `cron-job`. Separates "I did this" from "the fleet did this."
- **Project name** — derived from the repo path. Filter "everything for client X."

Override env vars in launchd plists or systemd units for autonomous agents so their traces tag correctly:

```xml
<!-- launchd plist snippet -->
<key>EnvironmentVariables</key>
<dict>
    <key>TRACE_TO_LANGFUSE</key><string>true</string>
    <key>LANGFUSE_AGENT_SOURCE</key><string>mention-listener</string>
    <key>LANGFUSE_MACHINE</key><string>m1-max</string>
</dict>
```

---

## Real-World Example

The AI Build Lab production fleet runs this exact pattern across multiple machines, with two separate Langfuse projects on the same self-hosted instance: one for the agent fleet (interactive sessions + mention-listeners + responders, tagged by machine), one dedicated to financial pipelines (kept separate so general agent noise doesn't drown out the audit trail). Different projects, different dashboards, different alerting rules.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| No traces appearing | `TRACE_TO_LANGFUSE` not exported in this shell | `echo $TRACE_TO_LANGFUSE` should print `true` |
| Traces appear but missing tool calls | PostToolUse hook not registered | Re-check `settings.json`, restart Claude Code |
| `langfuse_hook.log` shows `Langfuse unavailable` | Network blocking, or wrong host | Curl your `$LANGFUSE_HOST` from the same shell |
| Login worked but traces 401 | Stale or wrong API keys | Rotate keys in Langfuse, update env vars |
| Hook crashed Claude Code | A hook returned non-zero somehow | Hooks should always `sys.exit(0)`. Check the log. |

---

## Next

You're now sending traces. Continue to `04-using-the-dashboard.md`.
