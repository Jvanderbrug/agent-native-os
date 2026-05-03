---
description: Capture a decision into the local second brain with a full record, L3 raw context, an L2 Chain-of-Density card, and an L1 Cairns waypoint update.
---

You are logging a real decision so future sessions remember what was decided, why, and what changes because of it.

## Step 1: Get the decision

If the user gave the decision in the prompt, use it.

If they invoked `/log-decision` with no content, ask:

```text
What's the decision? One sentence with what you decided and why.
```

## Step 2: Get the structure

Ask the user, or use defaults if they say "use defaults":

- Deciders: who made this call? Default to the user.
- Date: today unless they specify another date.
- Reasoning depth: short or full. Default to short.
- Related people: default to none.
- Related projects: ask if unclear.
- Reversibility: less than 1 day, less than 1 week, less than 1 month, or never.
- Review date: default to 90 days from the decision date.
- Tags: default to `decision`.

## Step 3: Resolve vault paths

Default vault root:

```text
${HOME}/Documents/second-brain
```

On Windows, use the user's Documents folder. If the vault path is unclear, ask once.

Create a slug from the one-line decision summary:

```text
YYYY-MM-DD-<3-to-5-word-kebab-slug>
```

## Step 4: Build the files in a temp stage

Use a temp stage outside the vault:

```text
<vault-parent>/.log-decision-stage-<timestamp>/
```

Render all target files into the stage first. Do not write directly into the vault until every staged file validates.

### Full decision record

Target:

```text
<vault-root>/decisions/YYYY-MM-DD-<slug>.md
```

Format:

```markdown
---
date: YYYY-MM-DD
deciders: [name1]
related_people: []
related_projects: []
reversibility: <1d | <1w | <1m | never
review_date: YYYY-MM-DD
status: active
tags: [decision]
---

# <One-line decision summary>

## What we decided
<one paragraph>

## Why
<one paragraph or full detail>

## What we considered and rejected
- <alternative>: <why not>

## What changes because of this
<one paragraph>

## What would make us reverse this
- <condition>

## Provenance
- Decision logged via /log-decision on YYYY-MM-DD HH:MM
- Conversation context: <session ID or one-line note>
```

### L3 raw decision context

Target:

```text
<vault-root>/cairns/L3/decisions/YYYY-MM-DD-<slug>-raw.md
```

Write the raw decision context as captured. Include verbatim user input, relevant conversation excerpt, links, and provenance. Do not run Chain of Density here.

### L2 Chain-of-Density card

Target:

```text
<vault-root>/cairns/L2/decisions/YYYY-MM-DD-<slug>.md
```

Use this frontmatter shape, matching `cairns-ingest`:

```markdown
---
layer: L2
card_type: chain_of_density
source_type: decision
source_path: cairns/L3/decisions/YYYY-MM-DD-<slug>-raw.md
source_url:
created: YYYY-MM-DD
cod_status: final
cairns: [personal/my-decisions]
entities: []
tags: [decision]
---
```

Body:

```markdown
# <One-line decision summary>

## Dense Summary
<120-180 word final Chain-of-Density summary>

## Retrieval Hooks
- <question this decision should answer>

## Key Entities
- <entity>: <why it matters>

## Source Notes
- Raw source: [[cairns/L3/decisions/YYYY-MM-DD-<slug>-raw]]
- Full record: [[decisions/YYYY-MM-DD-<slug>]]
- Evidence level: raw decision context preserved

## L1 Promotion Candidate
<one sentence waypoint>
```

### L1 index row

Target:

```text
<vault-root>/cairns/L1/INDEX.md
```

Append one row to the waypoint table:

```markdown
| YYYY-MM-DD | <one-line decision summary> | [[cairns/L2/decisions/YYYY-MM-DD-<slug>]] | decision, <tags> |
```

### L1 decisions waypoint

Target:

```text
<vault-root>/cairns/L1/personal/my-decisions.md
```

If missing, create it:

```markdown
---
layer: L1
category: personal
slug: my-decisions
updated: YYYY-MM-DD
---

# My Decisions

- YYYY-MM-DD: <one-line decision summary> [L2: [[cairns/L2/decisions/YYYY-MM-DD-<slug>]]]
```

If it exists, append only the dated pointer line and update the `updated` field if present.

## Step 5: Commit the atomic write

The full operation includes:

1. Full record under `decisions/`.
2. L3 raw under `cairns/L3/decisions/`.
3. L2 card under `cairns/L2/decisions/`.
4. L1 row appended to `cairns/L1/INDEX.md`.
5. L1 `my-decisions.md` created or appended.

Commit rule:

- If every staged file validates, copy into the vault.
- If any write fails, remove every file copied during this run and restore the previous `INDEX.md` and `my-decisions.md`.
- If rollback fails, stop and report the exact paths requiring manual review.

This command must never leave a half-written decision.

## Step 6: Read back

Show the user:

- Full decision record path.
- L3 raw path.
- L2 card path.
- L1 index row.
- `my-decisions.md` pointer.

Ask:

```text
Anything wrong, missing, or worded oddly? I'll fix it now.
```

Edit only after confirmation.
