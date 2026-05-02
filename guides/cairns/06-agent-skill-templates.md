---
title: Agent Skill Templates for Cairns
status: workshop-ready
audience: workshop-students-2026-05-03
prereqs: 04-build-your-own-mini-cairns.md, 05-card-catalog-chain-of-density.md
next: none
---

# Agent Skill Templates for Cairns

This repo includes three installable skills for a student-scale Cairns system:

- `cairns-ingest` - captures any knowledge item into L3, writes an L2 Chain-of-Density card, and proposes L1 waypoint updates.
- `cairns-query` - answers questions using the retrieval order L1 -> L2 -> L3.
- `cairns-lint` - audits the vault for weak cards, missing links, stale L1 entries, and raw sources with no L2 card.

These are templates. They are designed to work with local markdown first. If you later add pgvector, Neo4j, or an external database, keep the same contract and add those as retrieval accelerators.

## Install

From the repo root:

```bash
mkdir -p ~/.claude/skills
cp -R configs/skills/cairns-ingest ~/.claude/skills/cairns-ingest
cp -R configs/skills/cairns-query ~/.claude/skills/cairns-query
cp -R configs/skills/cairns-lint ~/.claude/skills/cairns-lint
```

Restart Claude Code after copying.

## Expected vault shape

```text
~/Documents/second-brain/
  cairns/
    L1/
      work-builds.md
      people.md
      decisions-in-flight.md
      reading-list.md
      brand-voice.md
    L2/
      cards/
    L3/
      articles/
      notes/
      transcripts/
```

The starter vault in `templates/obsidian-cairns-starter/` already follows this shape.

## How to use them

### Ingest a source

```text
Use the cairns-ingest skill. Save this YouTube transcript to my second brain, create the L2 Card Catalog entry, and tell me if any L1 waypoint should be updated.

<paste transcript or path>
```

### Ask a question

```text
Use the cairns-query skill. What have I captured about agentic RAG patterns, and which raw sources should I read next?
```

### Audit your vault

```text
Use the cairns-lint skill. Check my second brain for raw L3 files that do not have L2 cards, weak Chain-of-Density summaries, broken backlinks, and stale L1 route-map entries.
```

## Safety defaults

The skills follow three rules:

- L3 raw evidence is append-only. Do not rewrite raw sources.
- L2 cards can be generated and revised by the agent, but must keep provenance.
- L1 route-map updates require user approval because they affect always-on memory.

## When you outgrow local markdown

Keep the same layers and add infrastructure behind them:

- Embed L2 and L3 in pgvector for semantic search.
- Add Neo4j for entity and relationship traversal.
- Add a Librarian Agent when more than one agent needs the same knowledge base.
- Add scheduled linting or a nightly consolidation pass.

The tool stack can change. The contract stays: L1 route map, L2 Card Catalog, L3 raw evidence.
