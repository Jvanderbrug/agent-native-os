-- YouTube Cairns blueprint schema
--
-- Before running, replace every __CAIRNS_PREFIX__ token with a student-owned
-- lower_snake namespace, for example: alex_youtube_cairns.
--
-- Example table after replacement:
-- public.alex_youtube_cairns_sources

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS public.__CAIRNS_PREFIX___sources (
    source_id           TEXT PRIMARY KEY,
    demo_id             TEXT NOT NULL DEFAULT 'youtube-cairns-blueprint',
    source_kind         TEXT NOT NULL DEFAULT 'youtube_transcript',
    video_id            TEXT NOT NULL,
    title               TEXT NOT NULL DEFAULT '',
    channel_name        TEXT NOT NULL DEFAULT '',
    channel_slug        TEXT NOT NULL DEFAULT '',
    upload_date         TEXT,
    url                 TEXT NOT NULL DEFAULT '',
    duration_seconds    INTEGER DEFAULT 0,
    word_count          INTEGER DEFAULT 0,
    obsidian_path       TEXT NOT NULL DEFAULT '',
    embedding           vector(768),
    embedding_model     TEXT NOT NULL DEFAULT 'text-embedding-3-small',
    metadata            JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (demo_id, video_id)
);

CREATE INDEX IF NOT EXISTS idx___CAIRNS_PREFIX___sources_demo_id
    ON public.__CAIRNS_PREFIX___sources (demo_id);

CREATE INDEX IF NOT EXISTS idx___CAIRNS_PREFIX___sources_channel_slug
    ON public.__CAIRNS_PREFIX___sources (channel_slug);

CREATE INDEX IF NOT EXISTS idx___CAIRNS_PREFIX___sources_embedding
    ON public.__CAIRNS_PREFIX___sources
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 25);

CREATE TABLE IF NOT EXISTS public.__CAIRNS_PREFIX___chunks (
    id                BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    demo_id           TEXT NOT NULL DEFAULT 'youtube-cairns-blueprint',
    source_id         TEXT NOT NULL REFERENCES public.__CAIRNS_PREFIX___sources(source_id) ON DELETE CASCADE,
    video_id          TEXT NOT NULL,
    channel_slug      TEXT NOT NULL DEFAULT '',
    chunk_index       INTEGER NOT NULL,
    chunk_text        TEXT NOT NULL,
    embedding         vector(768),
    embedding_model   TEXT NOT NULL DEFAULT 'text-embedding-3-small',
    metadata          JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (source_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx___CAIRNS_PREFIX___chunks_demo_id
    ON public.__CAIRNS_PREFIX___chunks (demo_id);

CREATE INDEX IF NOT EXISTS idx___CAIRNS_PREFIX___chunks_source_id
    ON public.__CAIRNS_PREFIX___chunks (source_id);

CREATE INDEX IF NOT EXISTS idx___CAIRNS_PREFIX___chunks_embedding
    ON public.__CAIRNS_PREFIX___chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 75);

CREATE TABLE IF NOT EXISTS public.__CAIRNS_PREFIX___cairns (
    cairn_id          TEXT PRIMARY KEY,
    demo_id           TEXT NOT NULL DEFAULT 'youtube-cairns-blueprint',
    layer             TEXT NOT NULL CHECK (layer IN ('L1', 'L2')),
    title             TEXT NOT NULL DEFAULT '',
    body              TEXT NOT NULL DEFAULT '',
    obsidian_path     TEXT NOT NULL DEFAULT '',
    tags              TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    embedding         vector(768),
    embedding_model   TEXT NOT NULL DEFAULT 'text-embedding-3-small',
    metadata          JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx___CAIRNS_PREFIX___cairns_demo_id
    ON public.__CAIRNS_PREFIX___cairns (demo_id);

CREATE INDEX IF NOT EXISTS idx___CAIRNS_PREFIX___cairns_layer
    ON public.__CAIRNS_PREFIX___cairns (layer);

CREATE INDEX IF NOT EXISTS idx___CAIRNS_PREFIX___cairns_embedding
    ON public.__CAIRNS_PREFIX___cairns
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 10);

CREATE TABLE IF NOT EXISTS public.__CAIRNS_PREFIX___graph_nodes (
    node_id     TEXT PRIMARY KEY,
    demo_id     TEXT NOT NULL DEFAULT 'youtube-cairns-blueprint',
    node_type   TEXT NOT NULL,
    name        TEXT NOT NULL,
    properties  JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.__CAIRNS_PREFIX___graph_edges (
    edge_id     TEXT PRIMARY KEY,
    demo_id     TEXT NOT NULL DEFAULT 'youtube-cairns-blueprint',
    from_node   TEXT NOT NULL REFERENCES public.__CAIRNS_PREFIX___graph_nodes(node_id) ON DELETE CASCADE,
    to_node     TEXT NOT NULL REFERENCES public.__CAIRNS_PREFIX___graph_nodes(node_id) ON DELETE CASCADE,
    edge_type   TEXT NOT NULL,
    weight      INTEGER NOT NULL DEFAULT 1,
    properties  JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.__CAIRNS_PREFIX___sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.__CAIRNS_PREFIX___chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.__CAIRNS_PREFIX___cairns ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.__CAIRNS_PREFIX___graph_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.__CAIRNS_PREFIX___graph_edges ENABLE ROW LEVEL SECURITY;

CREATE POLICY service_role_all___CAIRNS_PREFIX___sources
    ON public.__CAIRNS_PREFIX___sources FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY service_role_all___CAIRNS_PREFIX___chunks
    ON public.__CAIRNS_PREFIX___chunks FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY service_role_all___CAIRNS_PREFIX___cairns
    ON public.__CAIRNS_PREFIX___cairns FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY service_role_all___CAIRNS_PREFIX___graph_nodes
    ON public.__CAIRNS_PREFIX___graph_nodes FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY service_role_all___CAIRNS_PREFIX___graph_edges
    ON public.__CAIRNS_PREFIX___graph_edges FOR ALL
    USING (auth.role() = 'service_role');

CREATE OR REPLACE FUNCTION match___CAIRNS_PREFIX___sources(
    query_embedding vector(768),
    match_count INT DEFAULT 10,
    match_threshold FLOAT DEFAULT 0.2,
    target_demo_id TEXT DEFAULT 'youtube-cairns-blueprint'
)
RETURNS TABLE (
    source_id TEXT,
    video_id TEXT,
    title TEXT,
    channel_name TEXT,
    channel_slug TEXT,
    url TEXT,
    obsidian_path TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.source_id,
        s.video_id,
        s.title,
        s.channel_name,
        s.channel_slug,
        s.url,
        s.obsidian_path,
        1 - (s.embedding <=> query_embedding) AS similarity
    FROM public.__CAIRNS_PREFIX___sources s
    WHERE s.demo_id = target_demo_id
      AND s.embedding IS NOT NULL
      AND 1 - (s.embedding <=> query_embedding) > match_threshold
    ORDER BY s.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

CREATE OR REPLACE FUNCTION match___CAIRNS_PREFIX___chunks(
    query_embedding vector(768),
    match_count INT DEFAULT 10,
    match_threshold FLOAT DEFAULT 0.2,
    target_demo_id TEXT DEFAULT 'youtube-cairns-blueprint'
)
RETURNS TABLE (
    source_id TEXT,
    video_id TEXT,
    chunk_index INT,
    chunk_text TEXT,
    title TEXT,
    channel_name TEXT,
    channel_slug TEXT,
    url TEXT,
    obsidian_path TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.source_id,
        c.video_id,
        c.chunk_index,
        c.chunk_text,
        s.title,
        s.channel_name,
        s.channel_slug,
        s.url,
        s.obsidian_path,
        1 - (c.embedding <=> query_embedding) AS similarity
    FROM public.__CAIRNS_PREFIX___chunks c
    JOIN public.__CAIRNS_PREFIX___sources s ON s.source_id = c.source_id
    WHERE c.demo_id = target_demo_id
      AND c.embedding IS NOT NULL
      AND 1 - (c.embedding <=> query_embedding) > match_threshold
    ORDER BY c.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

CREATE OR REPLACE FUNCTION match___CAIRNS_PREFIX___cairns(
    query_embedding vector(768),
    match_count INT DEFAULT 10,
    match_threshold FLOAT DEFAULT 0.2,
    target_demo_id TEXT DEFAULT 'youtube-cairns-blueprint'
)
RETURNS TABLE (
    cairn_id TEXT,
    layer TEXT,
    title TEXT,
    body TEXT,
    obsidian_path TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.cairn_id,
        c.layer,
        c.title,
        c.body,
        c.obsidian_path,
        1 - (c.embedding <=> query_embedding) AS similarity
    FROM public.__CAIRNS_PREFIX___cairns c
    WHERE c.demo_id = target_demo_id
      AND c.embedding IS NOT NULL
      AND 1 - (c.embedding <=> query_embedding) > match_threshold
    ORDER BY c.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
