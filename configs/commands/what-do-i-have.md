---
description: Inspect the student's enabled toolbox and suggest exactly three useful next moves
---

Use the `what-do-i-have` skill workflow if it is installed. If it is not installed yet, follow the same workflow inline:

1. Inspect the current `CLAUDE.md`, especially "My Tools and Accounts," "MCP Servers installed," and "My Custom Commands."
2. Inspect project-level `configs/commands/` and `configs/skills/`.
3. Inspect user-level `~/.claude/commands/*.md` and `~/.claude/skills/*/SKILL.md` when readable.
4. Inspect MCP config files such as `~/.claude.json`, `.mcp.json`, Claude Desktop config, or starter settings when available.
5. Group findings into MCP servers, slash commands, skills, local scripts or automations, and connected work surfaces.
6. Do not expose secrets, tokens, account IDs, private file contents, or credential values.
7. Return exactly three useful next moves that fit the user's current work.

Use this answer format:

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
