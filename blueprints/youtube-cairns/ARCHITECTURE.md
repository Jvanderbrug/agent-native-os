# Architecture

This blueprint follows the Cairns three-layer contract from the production reference, adapted for a student-owned YouTube corpus.

## The contract

```text
L1 route map -> L2 source cards -> L3 raw evidence
```

Agents should answer in that order. L1 orients the query, L2 selects the source, and L3 provides exact evidence.

## L1: ten Cairns

L1 is the small, durable waypoint layer. It is not a summary of every video. It is the map an agent reads first so it can decide where to look.

This blueprint generates ten default Cairns:

1. Agent Architecture
2. Claude Code And Agentic Coding
3. Context Engineering
4. Local Models, Cost, And Privacy
5. Model And Platform Landscape
6. Morning Brief Capstone
7. RAG, Vector Search, And Graph Retrieval
8. Safety, Permissions, And Reliability
9. Second Brain And LLM Wiki
10. Workflow Automation Tools

L1 should stay small. A new source can propose an L1 update, but it should not silently rewrite the waypoint layer unless a human has delegated that authority.

## L2: Chain-of-Density per source

L2 is the Card Catalog. Every source gets one card.

The card captures:

- A dense summary.
- Retrieval hooks.
- Key entities.
- Linked Cairns.
- Source path and source URL.
- A promotion note for whether L1 should change.

The Chain-of-Density loop used here is practical, not academic theatre:

1. Write a sparse source summary.
2. Identify missing salient entities.
3. Rewrite at similar length with more specific signal.
4. Add retrieval questions.
5. Keep the backlink to L3 visible.

The production reference uses richer enrichment. This blueprint keeps the starter deterministic so students can inspect and modify it.

## L3: raw transcript

L3 is the source of truth. It is the raw transcript note with metadata, URL, video ID, channel slug, and transcript body.

Do not rewrite L3 to make it prettier. If the transcript is bad, record the correction in L2 or create a reviewed derivative. The raw layer exists so an agent can cite evidence and a human can audit the answer.

## Retrieval path

When a user asks a question:

1. Search L1 Cairns to pick waypoints.
2. Search L2 cards for source-level relevance.
3. Open L3 transcripts only for exact evidence.
4. Cite the L2 card and L3 source metadata.

This keeps context windows small while preserving traceability.

## Storage path

Obsidian is the local source surface:

```text
vault/cairns/L1/
vault/card-catalog/L2/
vault/raw/transcripts/
```

Supabase is the semantic retrieval layer:

```text
<prefix>_sources
<prefix>_chunks
<prefix>_cairns
```

Neo4j is optional. The graph export creates channels, videos, source cards, entities, and Cairns relationships from the same manifest.

## What this does not do

- It does not grant access to the private production vault.
- It does not process private channels.
- It does not promise perfect captions.
- It does not replace human judgment on L1 promotion.
- It does not require Neo4j for the Sunday build.
