# YouTube Cairns Blueprint

Build a small, source-grounded YouTube second brain from channels you choose.

This blueprint turns public YouTube captions into a three-layer Cairns vault:

- L1: ten durable Cairns that act as the route map.
- L2: one Chain-of-Density card per source.
- L3: raw transcript notes that stay immutable.

It also includes optional Supabase vector ingestion and optional Neo4j graph export, so the same source can move from Obsidian note to semantic search to graph traversal.

## Why this exists

The production reference is a private AI Build Lab demo vault. That vault proves the pattern at larger scale, but it is not the student path. Students should point this blueprint at their own public channels, build their own vault, and inspect the result locally.

The useful pattern is not "download a pile of videos." The useful pattern is:

1. Preserve raw source text.
2. Compress each source into a dense card.
3. Link cards to durable waypoints.
4. Embed the layers for retrieval.
5. Query from L1 to L2 to L3 instead of dumping raw transcripts into context.

## 4D vs 8D split

### 4D: explore the demo read-only

4D students inspect the production reference as a finished artifact. They learn the L1/L2/L3 shape, ask retrieval questions, and see how the agent cites source-backed evidence. They do not clone the private vault or run this pipeline.

### 8D: build your own

8D students use this blueprint to build the same pattern against a channel they care about. They configure a channel URL, pull a small set of public captions with `yt-dlp`, generate L2 cards, run the Supabase migration, ingest embeddings, and query the result.

## What is included

```text
blueprints/youtube-cairns/
+-- README.md
+-- QUICKSTART-8D.md
+-- ARCHITECTURE.md
+-- pipeline/
|   +-- build.py
|   +-- enrich.py
|   +-- ingest-rag.py
|   +-- ingest-graph.py
|   +-- query.py
|   +-- channels.example.yaml
|   +-- .env.example
|   +-- supabase/migrations/0001_youtube_cairns_blueprint.sql
+-- starter-vault/
    +-- cairns/L1/_index.md
    +-- cairns/L1/rag-vector-graph-retrieval.md
    +-- card-catalog/L2/sources/example-channel/example-video.md
    +-- raw/transcripts/example-channel/example-video.md
```

## Student guardrails

- Use public YouTube content or content you have rights to process.
- Keep L3 raw transcripts intact after capture.
- Let generated L2 cards be drafts until a human reviews them.
- Update L1 only when a source changes a durable waypoint.
- Use placeholder env values until you are ready to run locally.

## Typical commands

```bash
cd blueprints/youtube-cairns
cp pipeline/channels.example.yaml pipeline/channels.yaml
cp pipeline/.env.example pipeline/.env

python3 pipeline/build.py --config pipeline/channels.yaml --vault vault --max-videos 3
python3 pipeline/enrich.py --vault vault
python3 pipeline/ingest-rag.py --vault vault --apply
python3 pipeline/query.py "What should I learn from this channel?"
```

For the full 8D flow, use `QUICKSTART-8D.md`.
