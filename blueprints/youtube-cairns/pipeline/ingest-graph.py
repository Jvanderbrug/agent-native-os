#!/usr/bin/env python3
"""Generate and optionally apply a Neo4j graph for a YouTube Cairns vault."""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key, value.strip().strip("\"'"))
def cypher(value: object) -> str:
    return json.dumps("" if value is None else str(value))
def key(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
def lines_for(rows: list[dict], demo_id: str) -> list[str]:
    lines = [
        "// YouTube Cairns graph export",
        f"// demo_id: {demo_id}",
        "CREATE CONSTRAINT cairns_channel_slug IF NOT EXISTS FOR (n:CairnsChannel) REQUIRE n.slug IS UNIQUE;",
        "CREATE CONSTRAINT cairns_video_id IF NOT EXISTS FOR (n:CairnsVideo) REQUIRE n.video_id IS UNIQUE;",
        "CREATE CONSTRAINT cairns_source_id IF NOT EXISTS FOR (n:CairnsSource) REQUIRE n.source_id IS UNIQUE;",
        "CREATE CONSTRAINT cairns_card_id IF NOT EXISTS FOR (n:CairnsCard) REQUIRE n.card_id IS UNIQUE;",
        "CREATE CONSTRAINT cairns_cairn_id IF NOT EXISTS FOR (n:CairnsCairn) REQUIRE n.cairn_id IS UNIQUE;",
        "CREATE CONSTRAINT cairns_entity_key IF NOT EXISTS FOR (n:CairnsEntity) REQUIRE n.key IS UNIQUE;",
    ]
    cairns = {}
    for row in rows:
        card_id = row.get("card_path") or row["source_id"] + "-card"
        lines.extend(
            [
                f"MERGE (ch:CairnsChannel {{slug: {cypher(row['channel_slug'])}}}) SET ch.name = {cypher(row['channel_name'])}, ch.demo_id = {cypher(demo_id)};",
                f"MERGE (v:CairnsVideo {{video_id: {cypher(row['video_id'])}}}) SET v.title = {cypher(row['title'])}, v.url = {cypher(row['url'])}, v.demo_id = {cypher(demo_id)};",
                f"MERGE (s:CairnsSource {{source_id: {cypher(row['source_id'])}}}) SET s.path = {cypher(row['obsidian_path'])}, s.demo_id = {cypher(demo_id)};",
                f"MERGE (card:CairnsCard {{card_id: {cypher(card_id)}}}) SET card.title = {cypher(row['title'])}, card.path = {cypher(row.get('card_path', ''))}, card.demo_id = {cypher(demo_id)};",
                "MERGE (ch)-[:PUBLISHED]->(v);",
                "MERGE (v)-[:HAS_SOURCE]->(s);",
                "MERGE (s)-[:HAS_CARD]->(card);",
            ]
        )
        for cairn in row.get("cairn_keys", []):
            cairns[cairn] = cairn.replace("-", " ").title()
            lines.append(f"MERGE (c:CairnsCairn {{cairn_id: {cypher(cairn)}}}) SET c.title = {cypher(cairns[cairn])}, c.demo_id = {cypher(demo_id)};")
            lines.append(f"MATCH (card:CairnsCard {{card_id: {cypher(card_id)}}}), (c:CairnsCairn {{cairn_id: {cypher(cairn)}}}) MERGE (card)-[:SUPPORTS_CAIRN]->(c);")
        for entity in row.get("entities", [])[:12]:
            entity_key = key(entity)
            lines.append(f"MERGE (e:CairnsEntity {{key: {cypher(entity_key)}}}) SET e.name = {cypher(entity)}, e.demo_id = {cypher(demo_id)};")
            lines.append(f"MATCH (card:CairnsCard {{card_id: {cypher(card_id)}}}), (e:CairnsEntity {{key: {cypher(entity_key)}}}) MERGE (card)-[:MENTIONS]->(e);")
    return lines
def apply_cypher(path: Path) -> None:
    if not shutil.which("cypher-shell"):
        raise SystemExit("cypher-shell is required for --apply. Install Neo4j tools or run without --apply.")
    cmd = [
        "cypher-shell",
        "-a",
        os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        "-u",
        os.environ.get("NEO4J_USER", "neo4j"),
        "-p",
        os.environ.get("NEO4J_PASSWORD", ""),
        "-f",
        str(path),
    ]
    subprocess.run(cmd, check=True)
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("vault"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--env", type=Path, default=Path("pipeline/.env"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    load_env(args.env)
    manifest = args.manifest or args.vault / "manifests" / "sources.json"
    rows = json.loads(manifest.read_text(encoding="utf-8"))
    output = args.output or args.vault / "manifests" / "graph.cypher"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines_for(rows, os.environ.get("DEMO_ID", "youtube-cairns-blueprint"))) + "\n", encoding="utf-8")
    print(f"Wrote graph Cypher: {output}")
    if args.apply:
        apply_cypher(output)
if __name__ == "__main__":
    main()
