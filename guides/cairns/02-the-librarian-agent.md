---
title: The Librarian Agent
status: workshop-ready
audience: workshop-students-2026-05-03
prereqs: 00-what-is-cairns.md, 01-the-three-tiers.md
next: 03-flow-the-capture-pipeline.md
---

# The Librarian Agent

This is the piece that turns Cairns from "a 3-tier knowledge store" into "agentic RAG." Without the Librarian, Cairns is just a clever filing system. With the Librarian, every other agent in your fleet gets a single mediated entry point to the entire knowledge fabric.

Reminder: **the full Librarian service is not what you are installing today.** The student version uses the `cairns-query` skill to practice the same retrieval order. The production version turns that pattern into a mediated service other agents can call.

## The problem with every agent doing its own retrieval

When you run multiple agents (Gigawatt, a mention listener, a heartbeat, a curriculum agent, a personal assistant), the naive pattern is for each one to query the data layer directly:

```
gigawatt          -> pgvector.query("...")
archie            -> pgvector.query("...")
mention-listener  -> pgvector.query("...")
heartbeat         -> pgvector.query("...")
```

Four separate problems show up immediately:

1. **Strategy duplication.** Every agent has to decide independently: vector search, graph traversal, full-text search, MCP call, or some combination. Most agents will pick one and stick with it forever, missing better answers.
2. **Cost explosion.** Every agent runs its own embeddings, its own re-ranks, its own re-tries. No shared cache.
3. **Inconsistent quality.** One agent's prompt for "search for X" is not the same as another's. Quality drifts. Hard to debug.
4. **Security boundary leak.** Every agent that touches the data layer needs credentials, scoped permissions, audit logging. That surface area only grows.

The agentic-RAG pattern solves all four with one move. Add a single agent whose entire job is retrieval. Every other agent calls it.

## What Librarian decides

```
gigawatt          ─┐
archie            ─┤
mention-listener  ─┼──► Librarian Agent ──► L1 / L2 / L3 / pgvector / Neo4j / MCP / FTS5
heartbeat         ─┘    (chooses strategy)
```

For every incoming query, Librarian decides:

**Which tier to hit.** L1 first (free, instant). L2 next (Chain-of-Density cards that explain what sources exist). L3 last, only when the answer needs raw evidence, exact quotes, timestamps, or details not preserved in the card.

**Which retrieval strategy to use.** Vector search for "find me concepts similar to X." Graph traversal for "who reports to whom" or "what events led to Y." Full-text search for "find the exact phrase Z." MCP call for "what is the current state of system A." Often a combination.

**How many passes to run.** Single-pass for direct lookups. Multi-pass with self-correction for ambiguous queries. Re-rank if the first pass returned weak results. Fall back to a different strategy if a confidence threshold fails.

**What to return.** Just the answer? Answer plus citations? Raw chunks for the calling agent to summarize itself? The contract is per-agent.

From the Hey Gigawatt v2 vision doc:

> "Specialized agent for ALL knowledge retrieval. Other agents query Librarian (not direct DB access). Decides retrieval strategy (graph vs vector vs MCP vs combo). Multi-pass agentic RAG with self-correction. Quality control and security boundary."

## Per-agent retrieval profiles

Different agents need different cuts of the knowledge fabric. Librarian honors that.

| Agent | L1 priority | L2 priority | L3 priority | Profile |
|---|---|---|---|---|
| **Gigawatt (main)** | FAQ pairs, culture anchors, course overview | Community messages, Slack posts, student wins | Specific quotes, announcements | Broad and shallow. Knows a little about everything. |
| **The Professor** | Concept anchors, decision trees, pedagogical frameworks | Module content, curriculum structure, learning sequences | Full lesson content, worked examples | Deep on curriculum, structured by learning path. |
| **MitchPlease** | Business frameworks, pricing guides, scoping templates | Case studies, client engagement patterns | Meeting transcripts, business strategy docs | Business-focused, case-study-heavy. |
| **Gigawatt Unhinged** | Culture anchors, community lore, running jokes | Everything (broad access for unexpected connections) | Pop culture references, advanced demos | Broad and unpredictable. Value comes from surprising connections. |

The point is not that you build four agents. The point is that one agent (Librarian) can serve all four with the right profile, and you can add a fifth without re-implementing retrieval.

## How to spec your own Librarian for your fleet

When you have more than one agent and they all need to read from your knowledge store, write a Librarian spec. The minimum viable spec answers six questions:

1. **What stores does it have access to?** L1 file paths, L2 directory, pgvector connection, graph DB connection, MCP servers, full-text indexes.
2. **What strategies can it choose between?** List them explicitly. Vector, graph, FTS, MCP, hybrid. Spell out when each is right.
3. **What is the retrieval contract per calling agent?** What does Gigawatt expect back? What does Professor? Document it.
4. **What is the cost ceiling per query?** Cap LLM tokens, cap re-ranks, cap fallback chains. Without a ceiling, costs run away.
5. **What gets logged?** Every retrieval should leave a trail: which strategy fired, how many passes, how many tokens, what was returned. This is your debugging surface when answers go wrong.
6. **What is the security boundary?** Sara's agent should not see Tyler's family category. Wade's agent should not see finances. Librarian enforces this with role-aware filtering. Hard rules, not vibes.

In the current Cairns spec, Librarian is a Claude Code subagent invoked via the Task tool. That keeps it simple. A future version may be a long-running process with its own API endpoint to support cross-machine queries.

## Why this is "agentic RAG" not just RAG

Standard RAG is passive. You embed a query, you cosine-similarity against a vector index, you return the top K chunks. The retrieval strategy is hardcoded. The system has no opinions about whether the strategy was right.

Agentic RAG is active. Seven primitives that distinguish it from passive RAG:

1. **Cascading retrieval with cache misses.** L1 first. L2 only if L1 misses or points to relevant cards. L3 only if L2 lacks specifics or the answer needs raw evidence.
2. **Strategy selection by Librarian.** Decides vector vs graph vs MCP vs combo based on query shape, not query embedding.
3. **Triage and dedupe agents on capture.** "Regex plus agent everywhere." Fast regex for obvious cases, agent for ambiguous. Three-pass dedupe (URL hash, content hash, embedding similarity plus agent decision).
4. **5-perspective enrichment pass.** Every captured entry gets analyzed across five lenses (for Tyler: builds, business, students, personal, agents) so retrieval can match by intent, not just text.
5. **Per-agent retrieval profiles.** Same store, different cuts.
6. **Recommender daemon.** Proactive surfacing, not just reactive query. The morning brief includes "what crossed your firehose yesterday."
7. **Outputs file back into the system.** Answers worth keeping become derived L2 notes. The system compounds.

Plus an 8th operational principle: **LLM allocation matched to value.** Ollama for free batch tasks. Haiku for cheap classification. Sonnet for the value-adding 5-perspective enrichment. Opus for L1 updates and weekly trend detection. The Librarian picks the model per task, the same way it picks the strategy.

## The honest part

Librarian is the piece that has been talked about the longest and built the least. The closest thing in production today is the Hey Gigawatt v2 Neo4j on Hostinger (88,314 nodes / 117,574 relationships as of May 2, 2026), and that runs without a formal Librarian agent in front of it.

The lesson for you is not "build Librarian first." The lesson is: when you have one agent and one store, talk to it directly. When you have three or more agents and two or more stores, that is when you spec a Librarian. Until then, the abstraction costs more than it saves.

## What's next

You know how knowledge moves out of Cairns. Next: how it gets in. Read `03-flow-the-capture-pipeline.md`.
