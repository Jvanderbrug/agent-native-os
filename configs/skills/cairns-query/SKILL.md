---
name: cairns-query
description: Use when answering questions from a Cairns-style second brain. Reads L1 route-map waypoints first, searches L2 Chain-of-Density Card Catalog cards second, and opens L3 raw evidence only when needed.
---

# Cairns Query

You answer questions using the user's Cairns-style second brain.

Default vault:

```text
~/Documents/second-brain/cairns/
```

## Retrieval order

Always use this cascade:

```text
L1 route map -> L2 Card Catalog -> L3 raw evidence
```

## Step 1: Read L1

Read the relevant files in `L1/`. If the vault is small, read all L1 files.

Use L1 to identify:

- Active projects, people, decisions, and constraints
- Which L2 cards or folders are likely relevant
- What not to answer from stale or out-of-scope memory

If L1 answers the question completely, answer with the L1 file path as provenance.

## Step 2: Search L2

If L1 does not answer fully, search `L2/cards/` by:

- Keywords from the user question
- L1 category names
- People, project, tool, or topic names
- Retrieval hooks and tags in card frontmatter/body

Read the top 3-8 cards. Prefer dense summaries with clear source links. If the cards answer the question, cite the L2 card paths.

## Step 3: Fetch L3 only when needed

Open L3 raw sources only when:

- The answer needs exact evidence, timestamps, quotes, or details
- L2 points to a source but does not preserve enough detail
- The user explicitly asks for the raw source
- You need to verify a claim before relying on it

When using L3, cite both the L2 card and the raw L3 path.

## Optional retrieval accelerators

If the user has them configured, use them after L1 and before broad manual search:

- Full-text search with `rg`
- pgvector or Supabase semantic search over L2/L3
- Neo4j graph traversal for people, tools, topics, and relationships

These accelerate retrieval. They do not replace the tier order.

## Answer format

Keep answers concise:

```markdown
## Answer
<direct answer>

## Sources Used
- L1: <path>
- L2: <path>
- L3: <path, only if opened>

## Confidence
High | Medium | Low, with one reason
```

If the system does not have enough evidence, say that directly and suggest what to ingest next.

## Do not

- Do not skip L1.
- Do not search raw L3 first.
- Do not invent citations.
- Do not treat vector similarity as proof.
- Do not load more raw sources than needed.
