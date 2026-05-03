---
name: cairns-ingest
description: Use when the user wants to add any source to a Cairns-style second brain. Preserves raw L3 evidence first, creates an L2 Chain-of-Density Card Catalog entry, and proposes human-approved L1 waypoint updates.
trigger: User asks to ingest, capture, add, process, or promote source material into Cairns.
args:
  - vault_path
  - source
  - source_type
  - promote_l1
---

# Cairns Ingest

You ingest knowledge into the user's local, personal Cairns second brain. This skill is user-scoped. It is not the shared YouTube demo vault and it does not write to production systems.

Default vault root:

```text
${HOME}/Documents/second-brain
```

On Windows, use the user's Documents folder. If the vault path is unclear, ask once.

## Workflow

1. **Confirm vault mode.** If only `cairns/L1/` exists, the user is on the 4D fast path. Do not create L2 or L3 without asking to upgrade the vault shape.
2. **Classify the source.** Identify type: transcript, meeting, paper, article, Slack thread, note, URL, decision context, or other.
3. **Write L3 raw first.** Save the complete source to the right `cairns/L3/` folder. Do not summarize before raw preservation. Do not edit an existing raw source except to add frontmatter or provenance if the user approves.
4. **Create one L2 card.** Write a Card Catalog note in `cairns/L2/cards/YYYY-MM-DD-<source-type>-<slug>.md`, except decisions, which belong under `cairns/L2/decisions/` through `/log-decision`.
5. **Run Chain of Density.** Produce a sparse summary, list missing salient entities and details, rewrite denser at the same length, then write a final 120-180 word dense summary.
6. **Add retrieval hooks.** Include questions this card should answer, tags, entities, related L1 categories, and a backlink to L3.
7. **Propose L1 updates.** If the source changes standing context, propose one short waypoint. Ask before writing L1.
8. **Create lazy personal waypoints only when needed.** First project capture may create `my-projects.md`; first people capture may create `my-people.md`; first learning-goal capture may create `my-learning-goals.md`.
9. **Report paths.** Return the L3 path, L2 card path, and any pending L1 proposal.

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

If approved, append one line under `cairns/L1/personal/<category>.md`:

```text
- YYYY-MM-DD: <waypoint under 220 characters> [L2: <card filename>]
```

If the target personal waypoint does not exist yet, create it with L1 frontmatter, a heading, and the first dated pointer. Keep L1 short and navigational.

## Atomic write pattern

Write L3 and L2 as one operation:

1. Create all new files in a temp stage outside the vault.
2. Validate frontmatter, paths, and backlinks.
3. Copy staged files into the vault only if their target paths do not exist.
4. If any write fails, remove every file copied during this run and report rollback.

## Do not

- Do not create one giant summary for multiple unrelated sources.
- Do not replace L3 raw evidence with a summary.
- Do not promote interesting-but-not-standing-context items to L1.
- Do not lose the path from L2 back to L3.
- Do not provision Supabase or Neo4j. For 8D, document the namespace plan and stop.
