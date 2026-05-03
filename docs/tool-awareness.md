# Tool Awareness

Tool Awareness is a quiet reminder pattern for Claude Code. It helps Claude notice the tools, commands, skills, scripts, and workflows you already installed, then mention one useful option when it directly fits your current goal.

This is not a startup checklist. Claude should not recite your whole toolbox at the beginning of every session. The reminder should appear only when it helps you take the next useful step.

## How It Works

Claude reads the tools you list in `CLAUDE.md`, especially:

- `My Tools and Accounts`
- `MCP Servers installed`
- `My Custom Commands`
- Project skills under `configs/skills/`
- Slash commands under `configs/commands/`

When you name a goal, finish a build, ask what to do next, or repeat a manual workflow, Claude can offer one timely suggestion in plain language.

Example:

```text
You now have Bland connected - want me to set up a morning brief that calls you?
```

## The `(no-suggest)` Tag

You can permanently silence proactive suggestions for a tool by adding `(no-suggest)` after the tool name in `CLAUDE.md`.

```markdown
## My Tools and Accounts
- Bland (no-suggest)
- Gmail
- Calendar
```

`Bland (no-suggest)` means Claude can still use Bland when you explicitly ask for it, but Claude should never proactively bring it up.

## Session Decline vs. `(no-suggest)`

- Session decline: You said "no thanks" to a suggestion in the current session. Claude should move on and not repeat that suggestion unless the context changes. This resets in a new session.
- `(no-suggest)` tag: Permanent until you remove the tag. Claude should not proactively surface that tool in any session.

If Claude is uncertain whether a tool is welcome, it should stay quiet.

## When Claude Should Suggest a Tool

Claude may surface one reminder when:

- Your goal maps directly to an installed tool, such as email, calendar, notes, Slack, calling, or logging decisions.
- You finish installing or testing a tool and there is an obvious next setup step.
- You ask what to do next or how to use the setup in real life.
- A repeated manual workflow appears twice in the same session and a configured command or skill could reduce it.
- You complete a build and the next step is activation, scheduling, capture, delivery, or documentation.

## When Claude Should Stay Quiet

Claude should not surface a reminder when:

- You are debugging.
- You asked for a narrow answer, edit, review, or command output.
- The suggestion would require a new account, paid service, or external communication without prior consent.
- You already declined the same suggestion this session.
- The match is vague, speculative, or based only on a keyword.

## Cadence

- Claude gets at most one implicit tool-awareness suggestion per session.
- If you decline an implicit suggestion, Claude should not offer another one that session.
- A new session resets the one-suggestion budget.
- Explicit requests are different. If you invoke `/what-do-i-have`, Claude can give exactly three useful next moves because you asked for the inventory.

## `/what-do-i-have`

Use `/what-do-i-have` when you want Claude to inspect your current toolbox and suggest three useful next moves. The command should group installed MCPs, slash commands, skills, scripts, and connected work surfaces without exposing secrets, tokens, account IDs, or private credential values.

This repo ships both:

- `configs/commands/what-do-i-have.md`, the slash command entrypoint
- `configs/skills/what-do-i-have/SKILL.md`, the reusable skill workflow
