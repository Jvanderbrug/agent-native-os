---
title: Flow, the Capture Pipeline
status: workshop-ready
audience: workshop-students-2026-05-03
prereqs: 00-what-is-cairns.md, 01-the-three-tiers.md
next: 04-build-your-own-mini-cairns.md
---

# Flow, the Capture Pipeline

If Librarian is how things come out of Cairns, Flow is how things go in. Flow is the named sub-tool inside the Cairns repo (locked in ADR 0002 at `~/GitHub/cairns/decisions/0002-naming.md`). When Tyler says "send it to Flow," he means push it into this pipeline.

Reminder: **Cairns is not built yet.** The Flow pipeline below is the spec from `~/GitHub/cairns/ARCHITECTURE.md` and the dormant production spec at `~/GitHub/AI-Build-Lab-Founders-Lounge/Content-Strategy/AGENT-SPECIFICATIONS/cairns-rag-architecture.md`. Some pieces (YouTube pipeline, Slack archive sync) are already running and will become Flow sources once the rest of Cairns ships.

## The shape

```
CAPTURE -> TRIAGE -> FETCH -> ENRICH -> STORE -> INTELLIGENCE -> OUTPUT -> Tyler -> loops back
```

Every step has a single job. The pipeline is opinionated. Each step is small enough to debug independently.

## Step 1: Capture

**What it does.** Catches everything that crosses your radar across every input channel.

**Tools.** iMessage daemon, Slack listener, X/Twitter monitor, YouTube subscription pipeline, email-monitor.py, voice memo watcher, browser extension, manual `flow ingest <url>` CLI.

**Output.** A raw event with source attribution, a timestamp, and (usually) a URL or file path.

**What could go wrong.** Daemons break (the iMessage daemon has been broken since March 7, 2026 because of a Full Disk Access permission gap). Sources rate-limit you. Captures duplicate (same URL arriving from three places). The triage step handles dedupe so capture stays simple and dumb. Capture should always work even if the rest of the pipeline is down. It just queues.

## Step 2: Triage

**What it does.** Classifies the captured event and prepares it for fetching.

**Tools.** Regex first, agent second. The "regex plus agent everywhere" principle: regex for obvious cases (URL detection, type classification, canonicalization), agent for ambiguous cases (is this a podcast or a meeting? is this a duplicate of something we already have, even though the URL is different?).

**Steps.**

- Detect URL or recognize file type
- Classify type: video, paper, article, repo, post, transcript, image, other
- Canonicalize the URL (strip tracking params, resolve redirects)
- Three-pass dedupe: URL hash, then content hash, then embedding similarity plus agent decision
- Source attribution: track every place this entry arrived from (Hunter sent the TikTok, then Sara shared the same TikTok in Slack, both are logged)

**What could go wrong.** Dedupe over-merges (two genuinely different things get collapsed) or under-merges (the same thing is stored ten times because the URLs differ). The agent pass is what catches both failure modes; regex alone is brittle.

## Step 3: Fetch

**What it does.** Goes and gets the actual content.

**Tools per type.**

- Downie for video (YouTube, Vimeo)
- Firecrawl for web pages
- gh CLI for GitHub repos and gists
- pdf2text for papers
- socialdata for X/Twitter threads
- Direct download for podcasts and audio files
- API calls for Slack archives, Granola transcripts, etc.

**Output.** The raw content saved to L3 (NAS plus git plus the appropriate per-source store).

**What could go wrong.** Firecrawl chokes on heavy single-page apps. YouTube transcripts come back garbage if no captions exist (Whisper fallback handles that). Sites paywall or rate-limit. Each fetcher needs its own retry and fallback policy. Fail loud, not silent.

## Step 4: Enrich

**What it does.** Runs LLM passes to extract structure, meaning, and personal relevance.

**The five passes.**

1. **Summarize.** Chain-of-density summary at the L2 layer. The agent rewrites the summary 3-5 times, each pass denser than the last.
2. **Entities.** Pull people, organizations, places, dates, concepts. These become graph nodes in Neo4j.
3. **Perspectives.** This is the value-add layer. For Tyler, the five perspectives are: builds, business, students, personal, agents. Each captured entry gets analyzed across all five so the agent can later answer "show me everything that touched Cohort 1" or "show me everything relevant to my next client engagement."
4. **Embedding.** Vectorize for pgvector. The summary, the perspectives, and the original content each get their own embedding.
5. **Recursive URL following.** If the captured content links to other URLs, queue them for capture (with a depth limit, otherwise you trip on infinite loops).

**LLM allocation.** Not everything gets Sonnet. Ollama for free batch summarization. Haiku for cheap entity extraction. Sonnet for the perspectives pass (value-adding). Opus reserved for L1 updates and weekly trend detection.

**Cost ceiling.** Hard cap of $500/month on enrichment LLM spend. Soft cap at $300 triggers an alert. Per-entry budget enforced; anything above needs approval.

**What could go wrong.** The perspectives pass can hallucinate. The recursive follower can run away (cap depth at 2). Embeddings can drift if the model version changes (re-embed when you upgrade).

## Step 5: Store

**What it does.** Writes to the right tier and the right backing store.

**The destinations.**

| Layer | Where it lives |
|---|---|
| L3 raw | NAS + git + per-source store |
| L2 card | Obsidian markdown vault, viewable as graph |
| L1 waypoint | Curated waypoint files; daemon proposes, human approves |
| Vectors | pgvector (Supabase) |
| Graph | Neo4j (Hostinger) |
| People | Twenty CRM (planned, not deployed yet) |

**The provenance rule.** Every L2 entry has a backlink to its L3 source. Always. Never lose provenance. Karpathy's wall-quote applies: "this lets you skip writing but it doesn't let you skip reading and thinking."

**The HITL gate.** L1 writes go through a human approval queue. The daemon can propose new waypoints; Tyler approves with one keystroke. This is the protection against agent-induced memory drift.

**What could go wrong.** A Slack post that arrives twice ends up as two L3 entries because the dedupe in step 2 missed it. The graph DB can grow stale relationships if entities get renamed. The HITL queue can pile up if Tyler ignores it for a week.

## Step 6: Intelligence

**What it does.** Runs scheduled passes that turn stored content into insight.

**Examples.**

- Trend detection: "you have read 8 things about agentic graph RAG this month, here is the synthesis"
- Cross-reference: "this paper you saved last week directly answers the question you asked your CRM agent yesterday"
- Recommender: "Sara just shared a post that connects to your Wednesday voice memo"
- Brief generation: the morning brief that summarizes "what crossed your firehose yesterday"

**Tools.** A nightly `/dream` consolidation pass (see `~/GitHub/agent-native-os-hq/architecture/MEMORY-TIERING-AND-SOUL-PATTERN.md` section 4B for the full spec). Weekly trend detection on Opus. The Recommender daemon for proactive surfacing.

**What could go wrong.** Cross-references can hallucinate connections that aren't real. Briefs can become noise if they fire too often. The right cadence is a tuning problem, not a build problem.

## Step 7: Output

**What it does.** Surfaces the right thing to the right channel at the right time.

**Channels.**

- Morning Slack brief in the personal ops channel
- Inline drops to relevant team channels (Sara sees curriculum-relevant items)
- `flow ask "what was the name of the woodworking guy from October"` CLI
- Agent tool: any agent in the fleet can call Librarian, which is reading from Cairns
- Curriculum mining: AI Build Lab modules pull examples from Tyler's enriched archive

**Loop closure.** Tyler reads the output, acts on something (sends a message, builds a thing, makes a decision), and that action is itself captured at step 1. The system compounds.

## A worked example: a YouTube video

Tyler watches a 45-minute YouTube video at lunch. Here is where it ends up in 90 seconds.

```
12:00:00 - Watched on phone, "watch later" link captured by browser ext
12:00:01 - Capture: event {url, source: browser-ext, timestamp}
12:00:02 - Triage: regex matches youtube.com/watch, classify=video, canonicalize URL
12:00:03 - Triage agent: dedupe check (not seen), three-pass dedupe clears
12:00:05 - Fetch: Downie pulls video to ~/Movies/MacWhisper Queue/
12:00:10 - Fetch: yt-dlp pulls captions if available (otherwise Whisper transcribes)
12:00:30 - Enrich pass 1 (Ollama): chain-of-density summary written to L2
12:00:45 - Enrich pass 2 (Haiku): entities extracted, graph nodes proposed
12:01:00 - Enrich pass 3 (Sonnet): 5-perspective analysis (builds, business, students, personal, agents)
12:01:15 - Enrich pass 4: embeddings generated for summary + perspectives + raw transcript
12:01:20 - Store: L3 raw transcript -> NAS+git, L2 card -> Obsidian vault,
           vectors -> pgvector, entities -> Neo4j, person mentions -> Twenty CRM queue
12:01:25 - Intelligence: cross-ref check finds 2 related items from past 30 days
12:01:30 - Output: nothing fires immediately. Will appear in tomorrow morning's brief.
```

Tomorrow at 5am, the morning brief includes a one-line entry: "Yesterday: video on agentic RAG patterns from [author]. Connects to your Wednesday voice memo and last month's Karpathy gist research. L2 card at obsidian://card/youtube-2026-05-02-a1b2c3d4."

## The principle behind all of it

**Regex plus agent everywhere.** Regex is fast and free for the obvious 80 percent. The agent handles the ambiguous 20 percent. Tag team. Never use the agent where regex would do; never trust regex alone where ambiguity matters.

## What's next

You understand the architecture. Now build a tiny version yourself. Read `04-build-your-own-mini-cairns.md`.
