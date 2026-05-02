---
description: Capture a decision into your second brain with structured frontmatter and an L1 Cairns waypoint update (when Cairns is wired)
---

You are logging a real decision so that future-you (and your agent fleet) remembers what was decided, why, and by whom. This is the bridge skill between "agents do work" and "agents remember what was decided."

## Step 1: Get the decision

If the user gave you the decision in the prompt (e.g., "log decision: we're going with Mattermost over Slack for agent comms because it's self-hosted and unlimited"), use that.

If they invoked `/log-decision` with no content, ask: "What's the decision? One sentence. What you decided + why."

## Step 2: Get the structure

Ask the user (or default if they say "use defaults"):
- **Deciders**: who made this call? (default: just the user)
- **Date**: today, unless they specify (default: today)
- **Reasoning depth**: short (one paragraph) or full (multiple paragraphs)? (default: short)
- **Related people**: anyone else this affects? (default: none)
- **Related projects**: which project / repo / cohort? (default: ask)
- **Reversibility**: can this be undone in <1 day, <1 week, <1 month, never? (default: ask)
- **Review date**: when should this be reconsidered? (default: 90 days)

## Step 3: Write the file

Write to `~/Documents/second-brain/decisions/<YYYY-MM-DD>-<short-slug>.md`. Slug is 3-5 words from the decision summary, kebab-case.

Format:

```markdown
---
date: YYYY-MM-DD
deciders: [name1, name2]
related_people: [optional list]
related_projects: [optional list]
reversibility: <1d | <1w | <1m | never
review_date: YYYY-MM-DD
status: active
---

# <One-line decision summary>

## What we decided
<one paragraph>

## Why
<one paragraph or full as requested>

## What we considered and rejected
<bullet list of alternatives + one-line why-not for each>

## What changes because of this
<one paragraph: what concrete thing happens differently going forward>

## What would make us reverse this
<one bullet list>

## Provenance
- Decision logged via /log-decision on YYYY-MM-DD HH:MM
- Conversation context: <session ID or one-line note>
```

## Step 4: Update L1 Cairns waypoint (if wired)

If the user has a `~/Documents/second-brain/cairns/L1/decisions-in-flight.md` file, append a new line:

```
- YYYY-MM-DD: <one-line summary> [<short-slug>]
```

If the file does not exist, create it with a header. Cap the file at 50 lines (oldest entries trim out — they're still in the L3 raw).

If the user has Cairns L1 wired into their `~/.claude/CLAUDE.md` via include or symlink, the next Claude session will see this decision automatically.

## Step 5: Optional Slack post

Ask the user: "Want me to post this to Slack so the team knows? (yes/no, channel name if yes)"

If yes, post the one-line summary + a link to the full file via `slack-cli chat post <channel> "<message>"`.

## Step 6: Read back

Show the user the file you wrote, the L1 line you added, and confirm. If they want changes, edit and re-confirm.

---

This skill demonstrates the Cairns memory tiering pattern in miniature:
- The full decision file is L3 raw (immutable, every detail preserved)
- The L1 waypoint line is the always-on summary
- The provenance line is the backlink

When the full Cairns is built, this same skill writes to the production system. For now, it writes to the local filesystem and any agent that reads the second-brain folder gets the context.
