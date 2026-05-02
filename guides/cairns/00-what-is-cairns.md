---
title: What Is Cairns
status: workshop-ready
audience: workshop-students-2026-05-03
prereqs: none
next: 01-the-three-tiers.md
---

# What Is Cairns

Cairns are stacked stone markers used for wayfinding in wilderness terrain. They mark the path when there is no trail. Tyler Fisk has been designing a knowledge system by that name since September 2024. This guide is your first contact with the pattern.

Important up front: **Cairns is not a single app you install.** It is an architecture for making your agents use memory well. The full production system has more automation than this repo ships, but the student-scale version is concrete: an Obsidian vault, three memory layers, and a few agent skills that know how to write and query those layers. By the end of this series you will know enough to build the pattern for yourself (see `04-build-your-own-mini-cairns.md`, `05-card-catalog-chain-of-density.md`, and `06-agent-skill-templates.md`).

## Why Tyler built it

In September 2024, Tyler reverse-engineered ChatGPT's "memory" feature and discovered something surprising. It was not a giant vector database. It was a small structured notepad, capped at roughly 6,000 tokens. That insight reframed the entire personal-knowledge-system problem.

Three real problems were stacked on his desk:

1. AI agents had no efficient way to load deeply personal context without blowing the context window.
2. Pure vector search was lossy on temporal and relational data. Ask "who is the CEO" and you get a hit from 2022 instead of 2026.
3. No single architecture served quick personalization, semantic search, and full-fidelity citation at the same time.

Cairns is the answer to all three. A small always-on layer of curated waypoints. A middle layer of summarized cards that point to source material. A bottom layer of every raw thing that ever crossed the radar. And one agent that decides which layer to query for any given question.

For the deeper origin story and the 18-month design history, see `~/GitHub/agent-native-os-hq/architecture/CAIRNS-CURRENT-STATE.md`.

## The 3 tiers in plain English

**L1 Cairns (always on).** A small set of high-signal route-map notes. They are not summaries of everything. They are selective waypoints that tell the agent what matters, what exists, and where to look next.

**L2 Card Catalog (deliberately fetched).** One Chain-of-Density card per meaningful L3 source. Each card compresses the source into a dense, source-linked summary that is good for retrieval, browsing, and deciding whether to fetch the raw evidence.

**L3 Raw Data (immutable evidence).** Every video transcript, paper, meeting note, Slack export, email, voice memo, or article. Never edited by the agent. L2 points back to it. L3 is only loaded when the answer needs the full source.

For a concrete walk-through with examples mapped to your own life, read `01-the-three-tiers.md` next.

## What it is NOT

Cairns is not a vector store. Vectors are one of several retrieval strategies it can choose from. The architecture is bigger than any one storage tool.

Cairns is not a chatbot. There is no UI. Other agents call it. You query it through your existing agents.

Cairns is not Notion or Obsidian. Those are visual tools for humans browsing knowledge. Cairns is plumbing for agents reasoning over knowledge. The two can coexist. L2 can live in an Obsidian vault and Cairns will not care.

Cairns is not a finished product. It is a design pattern with one running production component (the Hey Gigawatt v2 Neo4j on Hostinger, currently at 88,314 nodes and 117,574 relationships). Everything else is spec, research, and the dedicated repo at `~/GitHub/cairns/`.

## A note on Karpathy's gist

In April 2026, Andrej Karpathy published a viral gist called "LLM Knowledge Bases" describing essentially the same shape Tyler designed in September 2024. They rhyme. They are not derivative either way. Convergent evolution. Both arrived at the same answer because there are only so many right answers to the personal-knowledge-system design problem. Tyler's design predates by 18 months and goes further on multi-agent orchestration, cost discipline, and access control. See `CAIRNS-CURRENT-STATE.md` section 6 for the full comparison.

## Where to read more

- `01-the-three-tiers.md` - concrete walkthrough of L1, L2, L3
- `02-the-librarian-agent.md` - the agentic-RAG mediator pattern
- `03-flow-the-capture-pipeline.md` - how content gets into Cairns
- `04-build-your-own-mini-cairns.md` - your first prototype
- `05-card-catalog-chain-of-density.md` - the corrected L2 Card Catalog pattern
- `06-agent-skill-templates.md` - installable agent skills for ingestion, query, and linting
- `~/GitHub/agent-native-os-hq/architecture/CAIRNS-CURRENT-STATE.md` - the canonical "what Cairns is now" doc
- `~/GitHub/agent-native-os-hq/architecture/MEMORY-TIERING-AND-SOUL-PATTERN.md` - how Cairns marries the HOT/WARM/COLD memory framework
- `~/GitHub/cairns/ARCHITECTURE.md` - the v0 architecture in the dedicated repo

You are about to learn a pattern that will outlast any specific tool. Vector databases will come and go. The 3-tier shape will not.
