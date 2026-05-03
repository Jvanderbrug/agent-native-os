# Quickstart 8D

Goal: build your own YouTube Cairns vault from one public YouTube channel in about one Sunday session.

## Prerequisites

- Python 3.10 or newer.
- `yt-dlp` installed.
- A Supabase project with the `vector` extension available.
- An OpenAI API key for embeddings. If your team has an Anthropic-based enrichment variant, you can use it for L2 drafting, but this starter uses OpenAI embeddings.
- Optional: Neo4j Desktop, Aura, or a local Neo4j server.

## Step 1: install local tools

```bash
brew install yt-dlp
python3 -m venv .venv
source .venv/bin/activate
```

The scripts call the `yt-dlp` command directly and use Python standard-library HTTP calls for OpenAI, Supabase, and optional Neo4j-free ingestion.

## Step 2: configure env and channel

```bash
cd blueprints/youtube-cairns
cp pipeline/.env.example pipeline/.env
cp pipeline/channels.example.yaml pipeline/channels.yaml
```

Edit `pipeline/.env`:

```text
SUPABASE_URL=YOUR_SUPABASE_URL_HERE
SUPABASE_SERVICE_KEY=YOUR_SUPABASE_SERVICE_KEY_HERE
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=YOUR_NEO4J_PASSWORD_HERE
CAIRNS_PREFIX=yourname_youtube_cairns
```

Edit `pipeline/channels.yaml`:

```yaml
channels:
  - slug: favorite-channel
    name: Favorite Channel
    url: https://www.youtube.com/@YourFavoriteChannel
    status: active
    max_videos: 3
```

Use a stable slug. That slug becomes part of L2 and L3 paths.

## Step 3: create your Supabase tables

Open `pipeline/supabase/migrations/0001_youtube_cairns_blueprint.sql`.

Replace `__CAIRNS_PREFIX__` with the same value you put in `CAIRNS_PREFIX`, for example:

```text
yourname_youtube_cairns
```

Run the edited SQL in the Supabase SQL editor. It creates namespaced tables:

- `yourname_youtube_cairns_sources`
- `yourname_youtube_cairns_chunks`
- `yourname_youtube_cairns_cairns`
- `yourname_youtube_cairns_graph_nodes`
- `yourname_youtube_cairns_graph_edges`

It also creates `match_*` retrieval functions for sources, chunks, and Cairns notes.

## Step 4: build the vault and L2 cards

```bash
python3 pipeline/build.py --config pipeline/channels.yaml --vault vault --max-videos 3
python3 pipeline/enrich.py --vault vault
```

Open `vault/` in Obsidian. Start at:

```text
vault/cairns/L1/_index.md
```

Then follow one L1 Cairn to an L2 card and finally to the L3 transcript.

## Step 5: ingest and query

```bash
set -a
source pipeline/.env
set +a

python3 pipeline/ingest-rag.py --vault vault --apply
python3 pipeline/query.py "What are the strongest reusable ideas in this channel?"
```

Optional Neo4j graph export:

```bash
python3 pipeline/ingest-graph.py --vault vault --output vault/graph.cypher
python3 pipeline/ingest-graph.py --vault vault --output vault/graph.cypher --apply
```

If the query returns L1 waypoints, L2 cards, and L3 transcript evidence, your blueprint is working.
