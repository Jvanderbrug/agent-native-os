#!/usr/bin/env python3
"""Generate L1 Cairns and L2 source cards from L3 transcript notes."""
from __future__ import annotations
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
DEMO_ID = "youtube-cairns-blueprint"
CAIRNS = {
    "agent-architecture": ("Agent Architecture", ["agent", "agents", "architecture", "orchestration", "tool"]),
    "claude-code-agentic-coding": ("Claude Code And Agentic Coding", ["claude", "code", "coding", "developer", "repo"]),
    "context-engineering": ("Context Engineering", ["context", "memory", "prompt", "retrieval", "knowledge"]),
    "local-models-cost-privacy": ("Local Models, Cost, And Privacy", ["local", "privacy", "cost", "ollama", "open source"]),
    "model-platform-landscape": ("Model And Platform Landscape", ["openai", "anthropic", "gemini", "model", "platform"]),
    "morning-brief-capstone": ("Morning Brief Capstone", ["brief", "daily", "digest", "report", "monitor"]),
    "rag-vector-graph-retrieval": ("RAG, Vector Search, And Graph Retrieval", ["rag", "vector", "embedding", "graph", "search"]),
    "safety-permissions-reliability": ("Safety, Permissions, And Reliability", ["safety", "permission", "reliability", "eval", "guardrail"]),
    "second-brain-llm-wiki": ("Second Brain And LLM Wiki", ["second brain", "wiki", "obsidian", "notes", "knowledge base"]),
    "workflow-automation-tools": ("Workflow Automation Tools", ["workflow", "automation", "n8n", "zapier", "mcp"]),
}
def slugify(value: str, limit: int = 80) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return (value or "untitled")[:limit].strip("-")
def yaml_scalar(value: object) -> str:
    return json.dumps("" if value is None else str(value))
def yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(yaml_scalar(value) for value in values) + "]"
def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return text.strip()
def transcript_body(path: Path) -> str:
    text = strip_frontmatter(path.read_text(encoding="utf-8"))
    marker = "## Transcript"
    return text.split(marker, 1)[1].strip() if marker in text else text
def sentence_sample(text: str, limit: int = 4) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text).strip())
    return [part for part in parts if len(part.split()) > 6][:limit]
def top_entities(text: str, limit: int = 10) -> list[str]:
    phrases = re.findall(r"\b[A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+){0,3}\b", text)
    blocked = {"The", "This", "That", "YouTube", "Transcript"}
    counts = Counter(phrase for phrase in phrases if phrase not in blocked)
    return [phrase for phrase, _ in counts.most_common(limit)]
def cairn_keys_for(text: str) -> list[str]:
    lower = text.lower()
    scored = []
    for key, (_, terms) in CAIRNS.items():
        score = sum(lower.count(term) for term in terms)
        if score:
            scored.append((score, key))
    keys = [key for _, key in sorted(scored, reverse=True)[:5]]
    return keys or ["second-brain-llm-wiki"]
def dense_summary(row: dict, body: str, entities: list[str]) -> str:
    sample = sentence_sample(body, 3)
    base = " ".join(sample) if sample else f"{row['title']} is a source from {row['channel_name']}."
    words = base.split()
    summary = " ".join(words[:130])
    if entities:
        summary += " Key entities: " + ", ".join(entities[:6]) + "."
    return summary
def source_card(row: dict, body: str) -> tuple[Path, str, dict]:
    entities = top_entities(body)
    keys = cairn_keys_for(" ".join([row["title"], body[:4000]]))
    summary = dense_summary(row, body, entities)
    raw_path = row["obsidian_path"]
    card_rel = Path("card-catalog") / "L2" / "sources" / row["channel_slug"] / f"{row['video_id']} - {slugify(row['title'])}.md"
    frontmatter = {
        "demo_id": DEMO_ID,
        "layer": "L2",
        "card_type": "chain_of_density",
        "source_id": row["source_id"],
        "video_id": row["video_id"],
        "channel_slug": row["channel_slug"],
        "source_backlink": raw_path,
        "source_url": row["url"],
        "cod_status": "starter_extractive",
    }
    fm = "\n".join(f"{key}: {yaml_scalar(value)}" for key, value in frontmatter.items())
    cairn_links = "\n".join(f"- [[cairns/L1/{key}|{CAIRNS[key][0]}]]" for key in keys)
    entity_lines = "\n".join(f"- {entity}" for entity in entities[:10]) or "- None detected"
    hooks = [
        f"What does {row['channel_name']} say about this topic?",
        f"Which ideas from {row['title']} should become reusable AI workflow context?",
        f"What evidence from {row['title']} supports a L1 waypoint?",
    ]
    hook_lines = "\n".join(f"- {hook}" for hook in hooks)
    text = f"""---
{fm}
cairn_keys: {yaml_list(keys)}
entities: {yaml_list(entities[:10])}
---
# {row["title"]}
## Dense Summary
{summary}
## Chain-of-Density Loop
1. Sparse pass: this source is about `{row["title"]}` from {row["channel_name"]}.
2. Missing entities: {", ".join(entities[:8]) if entities else "none detected"}.
3. Denser rewrite: {summary}
4. Retrieval hooks: see below.
## Retrieval Hooks
{hook_lines}
## Key Entities
{entity_lines}
## Linked Cairns
{cairn_links}
## Source Notes
- Raw source: [[{raw_path}|raw transcript]]
- Source URL: {row["url"]}
- Evidence level: public YouTube captions
## L1 Promotion Candidate
Review only. Promote to L1 if this source changes a durable route-map note.
"""
    enriched = {**row, "card_path": card_rel.as_posix(), "cairn_keys": keys, "entities": entities[:10], "dense_summary": summary}
    return card_rel, text, enriched
def write_l1(vault: Path, rows: list[dict]) -> None:
    by_cairn: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        for key in row.get("cairn_keys", []):
            by_cairn[key].append(row)
    l1_dir = vault / "cairns" / "L1"
    l1_dir.mkdir(parents=True, exist_ok=True)
    index_lines = ["# L1 Cairns Index", "", "Read this first. Pick a waypoint, then search L2 cards before opening L3 transcripts.", ""]
    for key, (title, _) in CAIRNS.items():
        count = len(by_cairn.get(key, []))
        index_lines.append(f"- [[{key}|{title}]] ({count} linked cards)")
    (l1_dir / "_index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    for key, (title, terms) in CAIRNS.items():
        cards = by_cairn.get(key, [])
        links = "\n".join(f"- [[../../card-catalog/L2/sources/{row['channel_slug']}/{row['video_id']} - {slugify(row['title'])}|{row['title']}]]" for row in cards[:12])
        if not links:
            links = "- No source cards linked yet."
        text = f"""---
demo_id: {yaml_scalar(DEMO_ID)}
layer: "L1"
cairn_id: {yaml_scalar(key)}
tags: ["youtube-cairns", "L1"]
---
# {title}
## Use This Cairn For
Questions involving: {", ".join(terms)}.
## Linked L2 Cards
{links}
## L1 Update Rule
Keep this waypoint short. Add durable patterns only after reviewing the linked L2 cards and raw L3 evidence.
"""
        (l1_dir / f"{key}.md").write_text(text, encoding="utf-8")
def write_indexes(vault: Path, rows: list[dict]) -> None:
    l2_dir = vault / "card-catalog" / "L2"
    l2_dir.mkdir(parents=True, exist_ok=True)
    lines = ["# L2 Card Catalog", "", "Search this layer before opening raw transcripts.", ""]
    for row in rows:
        lines.append(f"- [[sources/{row['channel_slug']}/{row['video_id']} - {slugify(row['title'])}|{row['title']}]]")
    (l2_dir / "_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    start = """# YouTube Cairns Vault
Start with `cairns/L1/_index.md`.
Query order:
1. L1 route map.
2. L2 source cards.
3. L3 raw transcripts.
"""
    (vault / "README.md").write_text(start, encoding="utf-8")
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("vault"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    manifest = args.manifest or args.vault / "manifests" / "sources.json"
    rows = json.loads(manifest.read_text(encoding="utf-8"))
    if args.limit:
        rows = rows[: args.limit]
    enriched = []
    for row in rows:
        raw = args.vault / row["obsidian_path"]
        body = transcript_body(raw)
        card_rel, card_text, extra = source_card(row, body)
        target = args.vault / card_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(card_text, encoding="utf-8")
        enriched.append(extra)
        print(f"Wrote L2 {card_rel}")
    write_l1(args.vault, enriched)
    write_indexes(args.vault, enriched)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(enriched, indent=2), encoding="utf-8")
    print(f"Enriched sources: {len(enriched)}")
if __name__ == "__main__":
    main()
