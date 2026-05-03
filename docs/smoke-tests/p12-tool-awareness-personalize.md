# P12 Tool Awareness Personalize Smoke Test

This fixture verifies that `/personalize` seeds Tool Awareness for a fresh student profile.

## Fresh User Fixture

- Name: Jordan Lee
- Role: Operations consultant
- Top tools: Gmail, Google Calendar, Slack, Obsidian, Bland
- MCPs installed: Gmail, Google Calendar, Slack
- Tool opt-out: Bland `(no-suggest)`
- Priority use cases: client updates, calendar triage, meeting notes

## Expected CLAUDE.md Output

The generated `CLAUDE.md` must include:

```markdown
## Tool Awareness

You have a growing toolbox: MCP servers, slash commands, skills, scripts, and workflows listed in this file or installed under `~/.claude`. Quietly keep track of what is available as you work. Do not recite the toolbox at startup or on every turn. Instead, when the user names a goal, finishes a build, asks what to do next, or hits a repeatable workflow that an installed tool can help with, offer one timely option in plain language.

Keep it low-friction: one sentence, one suggestion, no sales pitch. Example: "You now have Bland connected - want me to set up a morning brief that calls you?" If the user declines, move on and do not repeat that suggestion unless the context changes.
```

The generated `My Tools and Accounts` section must also include:

```markdown
- Gmail
- Google Calendar
- Slack
- Obsidian
- Bland (no-suggest)
```

## Pass Criteria

- Tool Awareness section appears once.
- The Tool Awareness text matches the design insertion exactly.
- `(no-suggest)` syntax appears in `My Tools and Accounts`.
- The docs explain that session decline resets next session.
- The docs explain that `(no-suggest)` is permanent until removed.
- `/what-do-i-have` has a slash command entrypoint and a matching skill workflow.
