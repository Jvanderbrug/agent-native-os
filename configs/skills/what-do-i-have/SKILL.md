---
name: what-do-i-have
description: Use when the user asks what tools, MCPs, commands, skills, or automations they have available, or asks what they should try next after setup or a build.
---

# What Do I Have

You help the user understand their enabled agent toolbox and choose the next useful action.

## Step 1: Inspect available sources

Check, in order:

- The current `CLAUDE.md`, especially "My Tools and Accounts," "MCP Servers installed," and "My Custom Commands"
- `~/.claude/commands/*.md`
- `~/.claude/skills/*/SKILL.md`
- Project-level `configs/commands/` and `configs/skills/`
- MCP config files such as `~/.claude.json`, `.mcp.json`, Claude Desktop config, or starter settings when available

If a source is missing or unreadable, say that briefly and continue.

## Step 2: Normalize the inventory

Group findings into:

- MCP servers
- Slash commands
- Skills
- Local scripts or automations
- Connected work surfaces, such as email, calendar, notes, files, Slack, or voice/calling

Do not expose secrets, tokens, account IDs, private file contents, or credential values.

## Step 3: Connect tools to current context

Use the user's recent request, active project, and stated workshop goals to choose exactly three suggestions. Prefer tools that are already installed and tested. Avoid suggesting setup for tools that are not connected yet unless the user asked for setup ideas.

Each suggestion should include:

- Tool name
- What it can do next
- Why it fits the user's current work
- The command or next approval needed

## Step 4: Answer format

Use this format:

```markdown
## Installed Toolbox
- MCPs: ...
- Commands: ...
- Skills: ...
- Automations/scripts: ...

## 3 Useful Next Moves
1. <tool>: <specific action>. Want me to set it up/run it?
2. <tool>: <specific action>. Want me to set it up/run it?
3. <tool>: <specific action>. Want me to set it up/run it?

## Gaps
<missing or unverified tools, if relevant>
```

Keep the answer practical. Do not turn it into a lecture or a full audit unless asked.
