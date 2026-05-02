---
name: cairns-ingest
description: Use when the user wants to add any source to a Cairns-style second brain. Preserves raw L3 evidence first, creates an L2 Chain-of-Density Card Catalog entry, and proposes human-approved L1 waypoint updates.
---

# Cairns Ingest

You ingest knowledge into the user's Cairns-style second brain.

Default vault:

```text
~/Documents/second-brain/cairns/
  L1/
  L2/cards/
  L3/articles/
  L3/notes/
  L3/transcripts/
```

## Workflow

1. **Classify the source.** Identify type: transcript, meeting, paper, article, Slack thread, note, URL, or other.
2. **Write L3 raw first.** Save the complete source to the right `L3/` folder. Do not summarize before raw preservation. Do not edit an existing raw source except to add frontmatter/provenance if the user approves.
3. **Create one L2 card.** Write a Card Catalog note in `L2/cards/YYYY-MM-DD-<source-type>-<slug>.md`.
4. **Run Chain of Density.** Produce a sparse summary, list missing salient entities/details, rewrite denser at the same length, then write a final 120-180 word dense summary.
5. **Add retrieval hooks.** Include questions this card should answer, tags, entities, related L1 categories, and a backlink to L3.
6. **Propose L1 updates.** If the source changes standing context, propose one short waypoint. Ask before writing it.
7. **Report paths.** Return the L3 path, L2 card path, and any pending L1 proposal.

## L2 card template

```markdown
---
layer: L2
card_type: chain_of_density
source_type: <type>
source_path: <L3 path>
source_url:
created: YYYY-MM-DD
cod_status: final
cairns: []
entities: []
tags: []
---

# <Title>

## Dense Summary
<120-180 word final Chain-of-Density summary>

## Retrieval Hooks
- <question this card should answer>

## Key Entities
- <entity>: <why it matters>

## Source Notes
- Raw source: [[<L3 relative path>]]
- Evidence level: raw source preserved

## L1 Promotion Candidate
<one sentence or none>
```

## L1 promotion gate

Never silently update L1. Propose a waypoint only when the source affects active work, decisions, people, preferences, constraints, or durable operating context.

If approved, append one line under `L1/<category>.md`:

```text
- YYYY-MM-DD: <waypoint under 220 characters> [L2: <card filename>]
```

## Do not

- Do not create one giant summary for multiple unrelated sources.
- Do not replace L3 raw evidence with a summary.
- Do not promote interesting-but-not-standing-context items to L1.
- Do not lose the path from L2 back to L3.
