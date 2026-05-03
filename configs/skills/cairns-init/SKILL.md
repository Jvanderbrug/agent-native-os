---
name: cairns-init
description: Use when the user wants to seed a local personal Cairns vault from personalization answers. Creates the vault scaffold, day-one L1 waypoints, privacy guardrails, and optional 4D or 8D layer shape without overwriting existing content.
trigger: User asks to scaffold, initialize, seed, or reseed a personal Cairns vault.
args:
  - vault_path
  - mode
  - profile_source
  - reseed
---

# Cairns Init

You create a local, user-scoped Cairns vault. The vault is a personal second brain, not the shared AI YouTube demo and not a production graph.

Default vault path:

```text
${HOME}/Documents/second-brain
```

On Windows, use the user's Documents folder. If that path is not obvious, ask once and accept an absolute path.

## Inputs

- `vault_path`: optional. Default to the user's Documents second-brain folder.
- `mode`: `4D` or `8D`. Default to `4D`.
- `profile_source`: the completed personalization answers or the new `CLAUDE.md` profile.
- `reseed`: optional boolean. Default `false`.

## Non-negotiable rules

- 4D mode is the default and must stay markdown-only.
- 4D mode creates `CLAUDE.md` plus `cairns/L1/` only, with privacy files and the minimal inbox shape.
- 8D mode adds L2 and L3 folders for cards, decisions, articles, notes, and transcripts.
- Never overwrite user content unless `reseed` is true and the user confirms the exact files first.
- Stage writes outside the vault, validate the stage, then commit into the vault. If validation fails, delete the stage and leave the vault unchanged.
- Never create tables, graph labels, API keys, or remote services in this skill.

## Scaffold

Use this shape for the full vault:

```text
<vault-root>/
  CLAUDE.md
  AGENTS.md
  inbox/
    scratchpad/
  decisions/
  cairns/
    L1/
      INDEX.md
      personal/
        my-self.md
        my-tools.md
        my-style.md
    L2/
      cards/
      decisions/
    L3/
      articles/
      notes/
      transcripts/
      decisions/
  daily-briefs/
  meeting-prep/
  daily-reviews/
```

Lazy files are not created during init:

- `cairns/L1/personal/my-projects.md`
- `cairns/L1/personal/my-people.md`
- `cairns/L1/personal/my-decisions.md`
- `cairns/L1/personal/my-learning-goals.md`

Create those only on first relevant capture or first `/log-decision`.

## Atomic write pattern

1. Resolve `vault_path` to an absolute path.
2. Create a sibling stage folder named `.cairns-init-stage-<timestamp>`.
3. Render every file that is missing from the target vault into the stage folder.
4. Validate the stage has the required paths for the chosen mode.
5. For each staged file, copy it into the vault only if the target path does not exist.
6. If any copy fails, remove every file copied during this run and report the rollback.
7. Remove the stage folder.
8. Report `created`, `preserved`, and `skipped`.

If `reseed` is true, ask for confirmation before replacing each existing file. Do not bulk delete the vault.

## Day-one L1 files

Seed only short route-map waypoints. Keep each file under about 30 lines.

### `cairns/L1/INDEX.md`

```markdown
---
layer: L1
category: index
updated: YYYY-MM-DD
---

# Cairns Index

| date | summary | L2 card link | tags |
|------|---------|--------------|------|
| YYYY-MM-DD | Personalization completed and day-one L1 waypoints seeded | none yet | personalization, profile |
```

### `cairns/L1/personal/my-self.md`

```markdown
---
layer: L1
category: personal
slug: my-self
updated: YYYY-MM-DD
---

# My Self

## Identity
- Name:
- Role:
- Company:
- Industry:

## Working hours
- Default:
- Hard stops:

## Voice anchor
- See [[my-style]] for tone rules.
```

### `cairns/L1/personal/my-tools.md`

```markdown
---
layer: L1
category: personal
slug: my-tools
updated: YYYY-MM-DD
---

# My Tools

## Core stack
- Email:
- Calendar:
- Communication:
- Project management:
- File storage:

## MCP install state
- Gmail:
- Google Calendar:
- Notion:
- Slack:

## Credential rule
- Store secrets in a password manager or approved secret store. Do not paste keys into this vault.
```

### `cairns/L1/personal/my-style.md`

```markdown
---
layer: L1
category: personal
slug: my-style
updated: YYYY-MM-DD
---

# My Style

## Response style
- Preferred length:
- Tone:
- Feedback style:

## Autonomy
- Current setting:
- Check before:

## Avoid
-
```

## Vault `AGENTS.md`

Write this at the vault root:

```markdown
# Personal Cairns Vault Agent Contract

This vault is a local, user-scoped Cairns second brain.

## Layers

- `cairns/L1/` is the waypoint layer. Read it first. Keep it small.
- `cairns/L2/` is the Chain-of-Density card layer. Read source cards before raw notes.
- `cairns/L3/` is raw evidence. Preserve it and do not rewrite it.

## Query Order

1. Read `cairns/L1/INDEX.md`.
2. Open relevant L1 personal waypoints.
3. Open linked L2 cards or search `cairns/L2/`.
4. Open raw L3 files only for exact evidence.
5. Cite the L1, L2, and L3 paths used.

## Ingest Order

1. Save immutable source text under `cairns/L3/`.
2. Create one L2 card using the Chain-of-Density contract.
3. Link the card to one or more L1 waypoints.
4. Propose L1 updates only when the new source changes durable context.

## Human Approval Gate

Agents may write L2 and L3 during ingest. Agents must ask before updating L1 unless the user explicitly delegates that authority.
```

## Privacy guardrail

Write a vault-root `.gitignore` with:

```gitignore
CLAUDE.md
cairns/
decisions/
inbox/
daily-briefs/
meeting-prep/
daily-reviews/
```

Tell the user this keeps the personal vault local by default. Do not push the vault to GitHub unless the user explicitly asks.

## 8D namespace note

For 8D users, only write the namespace plan. Do not provision.

- Derive `user_slug` by hashing a stable user identifier with sha256 and taking the first 8 hex characters.
- Supabase tables must use `personal_cairns_<user_slug>_*`.
- Neo4j labels must use `Personal<UserSlugCamel>*`.
- Refuse any setup that collides with `ai_demo_*`, `AIDemo*`, or another personal namespace.

## Final response

Return:

```markdown
## Cairns Init Complete
- Mode: 4D | 8D
- Vault: <path>
- Created: <count>
- Preserved: <count>
- Skipped: <count>
- Next: run /log-decision with one harmless real decision
```
