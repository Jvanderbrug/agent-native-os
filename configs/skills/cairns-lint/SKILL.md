---
name: cairns-lint
description: Use to audit a Cairns-style second brain for weak L1 route-map notes, missing L2 Chain-of-Density cards, broken L2-to-L3 backlinks, stale waypoints, duplicate cards, and raw sources that have not been cataloged.
---

# Cairns Lint

You audit the user's Cairns-style second brain.

Default vault:

```text
~/Documents/second-brain/cairns/
```

## Checks

Run these checks in order.

### 1. Folder shape

Confirm:

```text
L1/
L2/cards/
L3/articles/
L3/notes/
L3/transcripts/
```

Report missing folders and suggest the exact `mkdir -p` command.

### 2. L3 sources without L2 cards

For every file under `L3/`, check whether any L2 card references it in `source_path`, `Raw source`, or a wiki link.

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

### 5. Broken links and duplicates

Check for:

- L2 cards pointing to missing L3 files
- Duplicate L2 cards for the same L3 source
- Different L3 files with identical titles or URLs
- L1 links to missing cards

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

### Fix First
1. <highest impact fix>
2. <next fix>
3. <next fix>

### Detailed Findings
- [P1] <issue> - <path>
- [P2] <issue> - <path>
```

Prioritize missing L2 cards and broken provenance first. Do not rewrite files unless the user asks you to fix them.
