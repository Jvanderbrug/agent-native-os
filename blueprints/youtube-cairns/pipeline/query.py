#!/usr/bin/env python3
"""Query the Supabase retrieval layer for a YouTube Cairns vault."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key, value.strip().strip("\"'"))
def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)
def prefix() -> str:
    return env("CAIRNS_PREFIX", "youtube_cairns").strip("_")
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
def headers() -> dict:
    key = env("SUPABASE_SERVICE_KEY") or env("SUPABASE_SERVICE_ROLE_KEY")
    if not key:
        raise RuntimeError("SUPABASE_SERVICE_KEY is required")
    return {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"}
def openai_embedding(text: str) -> list[float]:
    key = env("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload = {
        "model": env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        "input": text,
        "dimensions": int(env("OPENAI_EMBEDDING_DIMENSIONS", "768")),
    }
    data = request_json("POST", "https://api.openai.com/v1/embeddings", {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, payload)
    return data["data"][0]["embedding"]
def vector(values: list[float]) -> str:
    return "[" + ",".join(str(value) for value in values) + "]"
def rpc(name: str, payload: dict) -> list[dict]:
    base = env("SUPABASE_URL").rstrip("/")
    result = request_json("POST", f"{base}/rest/v1/rpc/{name}", headers(), payload)
    return result if isinstance(result, list) else []
def print_rows(title: str, rows: list[dict], fields: list[str]) -> None:
    print(f"\n## {title}")
    if not rows:
        print("No matches.")
        return
    for idx, row in enumerate(rows, 1):
        bits = []
        for field in fields:
            value = row.get(field)
            if value:
                bits.append(f"{field}: {value}")
        score = row.get("similarity")
        suffix = f" score={score:.3f}" if isinstance(score, (float, int)) else ""
        print(f"{idx}. " + " | ".join(bits) + suffix)
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--env", type=Path, default=Path("pipeline/.env"))
    parser.add_argument("--sources", type=int, default=6)
    parser.add_argument("--chunks", type=int, default=4)
    parser.add_argument("--cairns", type=int, default=5)
    parser.add_argument("--threshold", type=float, default=0.2)
    args = parser.parse_args()
    load_env(args.env)
    embedding = vector(openai_embedding(args.query))
    base_payload = {
        "query_embedding": embedding,
        "match_threshold": args.threshold,
        "target_demo_id": env("DEMO_ID", "youtube-cairns-blueprint"),
    }
    cairns = rpc(f"match_{prefix()}_cairns", {**base_payload, "match_count": args.cairns})
    sources = rpc(f"match_{prefix()}_sources", {**base_payload, "match_count": args.sources})
    chunks = rpc(f"match_{prefix()}_chunks", {**base_payload, "match_count": args.chunks})
    print(f"# Query\n{args.query}")
    print_rows("L1 And L2 Cairns", cairns, ["title", "layer", "obsidian_path"])
    print_rows("Source Matches", sources, ["title", "channel_name", "url", "obsidian_path"])
    print_rows("Transcript Evidence", chunks, ["title", "channel_name", "chunk_text"])
if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"query failed: {exc}", file=sys.stderr)
        raise
