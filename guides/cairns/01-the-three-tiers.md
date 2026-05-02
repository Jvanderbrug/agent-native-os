---
title: The Three Tiers (L1, L2, L3)
status: workshop-ready
audience: workshop-students-2026-05-03
prereqs: 00-what-is-cairns.md
next: 02-the-librarian-agent.md
---

# The Three Tiers

Every tier of Cairns increases in volume and decreases in curation. Agents query top down. They start with curated waypoints, descend to summaries for discovery, and only touch raw data when they need direct source material. This is the cache-miss pattern applied to personal knowledge.

Reminder: **Cairns is not built yet.** What follows is the architecture as currently specified. The numbers below (sizes, hit rates, category counts) are design targets pulled from `~/GitHub/cairns/ARCHITECTURE.md` and `~/GitHub/agent-native-os-hq/architecture/CAIRNS-CURRENT-STATE.md`.

## L1 Cairns (always-on waypoints)

**What it is.** Roughly 6,000 tokens of pre-curated, high-signal knowledge chunks across about 16 whole-person categories. Always loaded into the agent's context at session start. The first stop for any query. Designed to resolve 60 to 70 percent of questions before any retrieval happens.

**The 16 categories (proposed, not yet locked).**

| # | Category | Example contents |
|---|---|---|
| 1 | Work, Builds | Active build threads (Cairns, agent-native-os, etc.) |
| 2 | Work, Business | Company ops, finance, legal, infrastructure |
| 3 | Work, Curriculum | Foundations 2.0, Build Lab, future cohort prep |
| 4 | Work, Team | Sara, Wade, Hunter, Michael, future hires |
| 5 | People, Inner Circle | Family, close friends, key network |
| 6 | People, Network | Mentors, collaborators, students, vendors |
| 7 | Family, Spouse | Marriage, anniversaries, plans, decisions |
| 8 | Family, Kids | Schools, activities, milestones, healthcare |
| 9 | Personal, Health | Allergies, meals, fitness, providers |
| 10 | Personal, Finances | Personal accounts, investments |
| 11 | Personal, Tools and Setup | Hardware, software, dotfiles, machine state |
| 12 | Personal, Interests | Music, photography, woodworking, etc. |
| 13 | Personal, Self-Development | Reading, learning goals, journaling themes |
| 14 | Decisions in Flight | Active decisions not yet made (under 24h fresh) |
| 15 | Goals and Commitments | What you said you would do, public and private |
| 16 | Brand and Voice | Voice rules, no em-dashes, etc. (under 90d fresh) |

**Map it to your own life.** You probably do not have 16 categories worth of content yet. Five is fine to start. Pick the categories where you keep losing context: maybe Work-Builds, Health, Family, Active Decisions, Reading List. Each gets one markdown file. Each file is capped (roughly 200 to 400 characters per category if you want to stay disciplined, more if you want to use the full 6K-token L1 budget).

**Per-category staleness thresholds.** Decisions in Flight should be under 24 hours fresh. Brand and Voice can sit for 90 days. Tools and Setup can sit longer. The point is each category has a different rhythm.

**What L1 looks like in practice.** A line in your top-level memory that says "Active workshop: Sunday May 3 11am CDT, 4D + 8D tracks. Open: Component 11 architecture (Sara), Capstone build design." That is a waypoint. The agent does not need to grep your filesystem to know that. It is already in context.

## L2 Card Catalog (deliberately fetched summaries)

**What it is.** A searchable index of every meaningful thing in your knowledge ecosystem. Not the full content. Just enough metadata to find it, assess relevance, and decide whether to fetch L3.

Think of an actual library card catalog. Each card tells you what exists, where it lives, what it is about, and how to get the full thing. The agent uses L2 to navigate without loading everything into context.

**What goes in.** Per-entry chain-of-density summaries (compressed but information-dense paragraphs) of every transcript, every Slack thread worth keeping, every paper, every prompt library entry. Each entry has structured metadata: tags, people mentioned, concepts covered, source path, retrieval priority, and backlinks to L3.

**Where it lives.** Markdown files in git, viewable in Obsidian. Karpathy calls this "the wiki." Same idea.

**Map it to your own life.** Every YouTube video you actually watched, every podcast you listened to, every important Slack thread, every meeting that mattered. Each becomes one L2 card. The card has the 200-word summary, the date, the people, the topic tags, and a link to the raw source.

**The discipline that makes L2 work.** Each L2 file is named so it does not auto-load. The L1 waypoint for a category tells the agent which L2 to fetch when relevant. This is the soul.md pattern (see `~/GitHub/agent-native-os-hq/architecture/MEMORY-TIERING-AND-SOUL-PATTERN.md` section 2). Map, not contents.

## L3 Raw Data (everything that ever crossed your radar)

**What it is.** The complete, unprocessed source material. Every video file. Every PDF. Every Slack export. Every transcript. Every email. Every voice memo. Never edited by an LLM. Always backed up.

**What goes in.** Live session transcripts (Fathom, Whisper). Slack archive (potentially 42K+ messages). Curriculum modules. Voice and brand docs. Student wins. Meeting recordings on the NAS. YouTube transcripts (Tyler's pipeline currently has 56,647). Granola transcripts (1,200+).

**Where it lives.** NAS plus git plus per-source storage. Chunked for retrieval, embedded for semantic search, versioned for traceability.

**Map it to your own life.** Your existing Documents folder. Your Downloads. Your Notes app. Your email. Your screenshots. The point of L3 is you do not throw any of it away. You also do not try to organize it perfectly. You leave it where it lives, you index it, and you let L2 cards point to it.

## How an agent uses all three

```
User asks a question
        |
        v
[1] Check L1 waypoints (already in context)
    Resolved? Return answer.
        |
        v (cache miss)
[2] Search L2 card catalog
    Find 5-10 relevant cards.
    Resolved? Return answer with card content.
        |
        v (need full text)
[3] Fetch L3 chunks for top 3 cards
    Rank chunks by relevance.
    Inject top 3-5 chunks as context.
        |
        v
[4] Generate answer with source attribution
```

The cascading retrieval is the whole point. You do not vector-search every question. You only do expensive retrieval when the cheap layers fail.

Target hit rates from the design spec:

- L1 resolves 60 to 70 percent of queries
- Average retrieval latency under 200ms
- Source attribution accuracy above 95 percent
- Fallback to "I don't know" under 5 percent

## How they map to HOT, WARM, COLD

The HOT/WARM/COLD framework (covered in detail in `~/GitHub/agent-native-os-hq/architecture/MEMORY-TIERING-AND-SOUL-PATTERN.md`) names the same three tiers from the agent's perspective.

| Tier | Cairns layer | What it means |
|---|---|---|
| **HOT** | L1 Cairns | Always in the model's context. No fetch needed. |
| **WARM** | L2 Card Catalog | Known to exist by name. Deliberately fetched on demand. |
| **COLD** | L3 Raw Data | Not known by name. Searched, embedded, or graph-traversed to discover. |

Most agent failures are mis-tiering, not missing data. Putting things in HOT that should be WARM bloats the context. Putting things in WARM that should be HOT means the agent forgets to fetch them. Putting things in COLD that should be WARM forces an expensive search every time for something the agent could just `Read()`.

The 3-tier discipline forces you to decide, for every piece of knowledge, which tier it belongs in. That decision is more valuable than the storage itself.

## What's next

You now understand the data shape. Next: who decides which tier to query and which strategy to use. That job belongs to the Librarian Agent. Read `02-the-librarian-agent.md`.
