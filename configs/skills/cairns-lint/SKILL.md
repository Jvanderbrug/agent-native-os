---
name: cairns-lint
description: Use to audit a Cairns-style second brain for weak L1 route-map notes, missing L2 Chain-of-Density cards, broken L2-to-L3 backlinks, stale waypoints, duplicate cards, and raw sources that have not been cataloged.
trigger: User asks to audit, validate, lint, or check a personal Cairns vault.
args:
  - vault_path
  - mode
---

# Cairns Lint

You audit the user's local, personal Cairns second brain.

Default vault root:

```text
${HOME}/Documents/second-brain
```

On Windows, use the user's Documents folder. If the vault path is unclear, ask once.

## Checks

Run these checks in order.

### 1. Folder shape

Detect mode first:

- 4D fast path: `CLAUDE.md`, `AGENTS.md`, `cairns/L1/INDEX.md`, and `cairns/L1/personal/`.
- 8D full path: 4D plus L2, L3, inbox, decisions, daily-briefs, meeting-prep, and daily-reviews.

For 4D, confirm:

```text
CLAUDE.md
AGENTS.md
cairns/L1/INDEX.md
cairns/L1/personal/my-self.md
cairns/L1/personal/my-tools.md
cairns/L1/personal/my-style.md
```

For 8D, also confirm:

```text
cairns/L2/cards/
cairns/L2/decisions/
cairns/L3/articles/
cairns/L3/notes/
cairns/L3/transcripts/
cairns/L3/decisions/
inbox/scratchpad/
decisions/
daily-briefs/
meeting-prep/
daily-reviews/
```

Report missing folders and suggest the exact `mkdir -p` command.

### 2. L3 sources without L2 cards

Skip this check in 4D mode. For 8D mode, check every file under `cairns/L3/`. Confirm at least one L2 card references it in `source_path`, `Raw source`, or a wiki link.

Report unmatched L3 files as:

```text
Needs L2 card: <L3 path>
```

### 3. Weak L2 cards

Flag L2 cards that have:

- No `source_path`
- No backlink to L3
- No `Dense Summary`
- Dense summary under 80 words or over 220 words
- Generic filler phrases with no source-specific entities
- No retrieval hooks
- No entities or tags

### 4. L1 route-map quality

Flag L1 notes that:

- Are longer than useful for always-on context
- Contain raw summaries instead of waypoints
- Do not point to any L2 cards or folders
- Include stale decisions without dates
- Mix unrelated categories

L1 should say where to go, not carry the whole archive.

Day-one L1 should only include `INDEX.md`, `my-self.md`, `my-tools.md`, and `my-style.md`. Do not flag missing `my-projects.md`, `my-people.md`, `my-decisions.md`, or `my-learning-goals.md` until the corresponding first capture exists.

### 5. Broken links and duplicates

Check for:

- L2 cards pointing to missing L3 files
- Duplicate L2 cards for the same L3 source
- Different L3 files with identical titles or URLs
- L1 links to missing cards

### 6. Privacy and namespace isolation

Confirm the vault-root `.gitignore` excludes:

```text
CLAUDE.md
cairns/
decisions/
inbox/
daily-briefs/
meeting-prep/
daily-reviews/
```

If 8D config exists, confirm:

- Supabase tables use `personal_cairns_<user_slug>_*`.
- Neo4j labels use `Personal<UserSlugCamel>*`.
- No references target `ai_demo_*`, `AIDemo*`, production Cairns labels, or another user's namespace.

## Output

Return a concise report:

```markdown
## Cairns Lint Report

### Summary
- L3 sources: N
- L2 cards: N
- Missing L2 cards: N
- Weak L2 cards: N
- L1 issues: N
- Privacy issues: N
- Namespace issues: N

### Fix First
1. <highest impact fix>
2. <next fix>
3. <next fix>

### Detailed Findings
- [P1] <issue> - <path>
- [P2] <issue> - <path>
```

Prioritize missing L2 cards and broken provenance first. Do not rewrite files unless the user asks you to fix them.
