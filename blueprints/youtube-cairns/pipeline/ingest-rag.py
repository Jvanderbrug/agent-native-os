#!/usr/bin/env python3
"""Ingest YouTube Cairns notes into namespaced Supabase vector tables."""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value.strip().strip("\"'"))
def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)
def table(name: str) -> str:
    prefix = env("CAIRNS_PREFIX", "youtube_cairns").strip("_")
    return f"{prefix}_{name}"
def request_json(method: str, url: str, headers: dict, payload: object | None = None) -> object:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"{method} {url} failed: {exc.code} {detail}") from exc
def openai_embedding(text: str) -> list[float]:
    key = env("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required for embeddings")
    payload = {
        "model": env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        "input": text[:12000],
        "dimensions": int(env("OPENAI_EMBEDDING_DIMENSIONS", "768")),
    }
    data = request_json(
        "POST",
        "https://api.openai.com/v1/embeddings",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        payload,
    )
    return data["data"][0]["embedding"]
def supabase_headers(prefer: str = "return=minimal") -> dict:
    key = env("SUPABASE_SERVICE_KEY") or env("SUPABASE_SERVICE_ROLE_KEY")
    if not key:
        raise RuntimeError("SUPABASE_SERVICE_KEY is required")
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": prefer,
    }
def upsert(name: str, rows: list[dict], conflict: str) -> None:
    if not rows:
        return
    base = env("SUPABASE_URL").rstrip("/")
    url = f"{base}/rest/v1/{table(name)}?on_conflict={conflict}"
    request_json("POST", url, supabase_headers("resolution=merge-duplicates,return=minimal"), rows)
def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return text.strip()
def title_from_markdown(path: Path) -> str:
    for line in strip_frontmatter(path.read_text(encoding="utf-8")).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem
def chunks(text: str, size: int = 1200, overlap: int = 150) -> list[dict]:
    words = re.findall(r"\S+", text)
    out = []
    start = 0
    idx = 0
    while start < len(words):
        part = words[start : start + size]
        if not part:
            break
        out.append({"chunk_index": idx, "chunk_text": " ".join(part)})
        idx += 1
        start += max(1, size - overlap)
    return out
def ingest_sources(vault: Path, rows: list[dict], apply: bool) -> tuple[int, int]:
    source_rows = []
    chunk_rows = []
    for row in rows:
        raw_path = vault / row["obsidian_path"]
        body = strip_frontmatter(raw_path.read_text(encoding="utf-8"))
        source_rows.append(
            {
                "source_id": row["source_id"],
                "demo_id": env("DEMO_ID", "youtube-cairns-blueprint"),
                "source_kind": "youtube_transcript",
                "video_id": row["video_id"],
                "title": row["title"],
                "channel_name": row["channel_name"],
                "channel_slug": row["channel_slug"],
                "upload_date": row.get("upload_date", ""),
                "url": row["url"],
                "duration_seconds": row.get("duration_seconds", 0),
                "word_count": row.get("word_count", len(body.split())),
                "obsidian_path": row["obsidian_path"],
                "embedding": openai_embedding(row["title"] + "\n" + body[:2000]) if apply else None,
                "embedding_model": env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
                "metadata": {"card_path": row.get("card_path", ""), "entities": row.get("entities", [])},
            }
        )
        for chunk in chunks(body):
            chunk_rows.append(
                {
                    "demo_id": env("DEMO_ID", "youtube-cairns-blueprint"),
                    "source_id": row["source_id"],
                    "video_id": row["video_id"],
                    "channel_slug": row["channel_slug"],
                    "chunk_index": chunk["chunk_index"],
                    "chunk_text": chunk["chunk_text"],
                    "embedding": openai_embedding(chunk["chunk_text"]) if apply else None,
                    "embedding_model": env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
                    "metadata": {},
                }
            )
    if apply:
        upsert("sources", source_rows, "source_id")
        upsert("chunks", chunk_rows, "source_id,chunk_index")
    return len(source_rows), len(chunk_rows)
def ingest_cairns(vault: Path, apply: bool) -> int:
    paths = sorted((vault / "cairns").glob("L1/*.md")) + sorted((vault / "card-catalog").glob("L2/**/*.md"))
    rows = []
    for path in paths:
        rel = path.relative_to(vault).as_posix()
        body = strip_frontmatter(path.read_text(encoding="utf-8"))
        layer = "L1" if "/L1/" in f"/{rel}" else "L2"
        rows.append(
            {
                "cairn_id": re.sub(r"[^a-zA-Z0-9]+", "-", rel).strip("-").lower(),
                "demo_id": env("DEMO_ID", "youtube-cairns-blueprint"),
                "layer": layer,
                "title": title_from_markdown(path),
                "body": body,
                "obsidian_path": rel,
                "tags": ["youtube-cairns", layer],
                "embedding": openai_embedding(body[:4000]) if apply else None,
                "embedding_model": env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
                "metadata": {},
            }
        )
    if apply:
        upsert("cairns", rows, "cairn_id")
    return len(rows)
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("vault"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--env", type=Path, default=Path("pipeline/.env"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    load_env(args.env)
    manifest = args.manifest or args.vault / "manifests" / "sources.json"
    if not manifest.exists():
        raise SystemExit(f"Missing manifest: {manifest}")
    rows = json.loads(manifest.read_text(encoding="utf-8"))
    source_count, chunk_count = ingest_sources(args.vault, rows, args.apply)
    cairn_count = ingest_cairns(args.vault, args.apply)
    mode = "applied" if args.apply else "dry run"
    print(f"RAG ingest {mode}: {source_count} sources, {chunk_count} chunks, {cairn_count} cairns")
    if not args.apply:
        print("Re-run with --apply after setting pipeline/.env and applying the Supabase migration.")
if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ingest-rag failed: {exc}", file=sys.stderr)
        raise
