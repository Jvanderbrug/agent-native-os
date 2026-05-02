---
title: Card Catalog and Chain of Density
status: workshop-ready
audience: workshop-students-2026-05-03
prereqs: 00-what-is-cairns.md, 01-the-three-tiers.md
next: 06-agent-skill-templates.md
---

# Card Catalog and Chain of Density

The Card Catalog is L2. It is the layer most people accidentally skip.

If L1 is a route map and L3 is the raw evidence, L2 is the catalog that lets an agent move between them without loading your whole archive. Every meaningful source gets one card. That card is short enough to browse and retrieve, dense enough to be useful, and linked back to the raw source.

## The rule

One source, one L2 card.

Examples:

- One YouTube transcript -> one card
- One meeting transcript -> one card
- One paper -> one card
- One Slack thread worth preserving -> one card
- One article or saved URL -> one card

Do not make one giant "AI videos summary" note. That is too broad to retrieve well. Do not leave a folder of raw transcripts with no cards. That forces the agent to search the raw layer every time.

## Where it lives

Use this folder:

```text
~/Documents/second-brain/cairns/L2/cards/
```

A good filename:

```text
YYYY-MM-DD-source-type-short-title.md
```

Examples:

```text
2026-05-02-youtube-agentic-rag-patterns.md
2026-05-02-meeting-client-onboarding.md
2026-05-02-paper-chain-of-density.md
```

## The card format

```markdown
---
layer: L2
card_type: chain_of_density
source_type: youtube | meeting | paper | article | slack | note | other
source_path: ~/Documents/second-brain/cairns/L3/transcripts/example.md
source_url:
created: YYYY-MM-DD
cod_status: draft | final
cairns:
  - work-builds
  - reading-list
entities:
  - Person or concept
tags:
  - agentic-rag
  - second-brain
---

# <Source title>

## Dense Summary
<Final 120-180 word Chain-of-Density summary. Specific, entity-rich, no filler.>

## Retrieval Hooks
- What question would make this card relevant?
- What term, person, tool, project, or decision should retrieve this?
- What L1 Cairn should point here?

## Key Entities
- Entity: why it matters in this source
- Tool or concept: why it matters in this source

## Source Notes
- Raw source: [[relative/path/to/L3/source]]
- Source URL: <URL if available>
- Evidence level: raw transcript | notes | human-written | generated

## L1 Promotion Candidate
<One sentence only if this source should update L1. Otherwise: none.>
```

## Chain-of-Density loop

The Chain-of-Density paper showed that summaries get better when you repeatedly add missing salient entities while keeping length fixed. For Cairns, use this practical version:

1. **Pass 0: Sparse summary.** Write a basic 80-120 word summary.
2. **Pass 1: Missing entities.** List 5-10 important names, tools, concepts, claims, dates, or constraints missing from the summary.
3. **Pass 2: Denser rewrite.** Rewrite at the same length while including the missing signal.
4. **Pass 3: Missing retrieval hooks.** List questions this source should answer that the summary does not yet support.
5. **Pass 4: Final dense card.** Rewrite one final time. Same length, more useful. No generic phrases like "the video discusses" unless they carry meaning.

The goal is not a longer summary. The goal is a better card.

## What makes a good L2 card

A good card lets the agent decide three things quickly:

- Is this source relevant?
- Which exact L3 raw file should I open if I need evidence?
- Should any L1 route-map note point here?

Strong L2 cards contain:

- Specific entities, not vague topic labels
- Concrete claims, decisions, constraints, examples, or workflows
- Backlinks to raw L3 evidence
- Retrieval questions phrased the way a user might ask
- Tags that match your actual work
- A clear "do not promote" or "promote to L1" recommendation

Weak L2 cards look like:

```text
This video talks about AI tools and productivity. It covers workflows,
automation, and different ways to use agents.
```

That card is almost useless. It names no source-specific signal.

Better:

```text
Cole Medin demonstrates a Claude Code second-brain workflow that stores
YouTube transcripts as raw evidence, creates Obsidian-readable summaries,
and routes retrieval through a local agent before escalating to vector search.
The useful pattern is not "summarize videos"; it is source-backed ingestion:
raw transcript preserved, dense card generated, then agent uses the card to
decide whether to load the transcript.
```

## Promotion rules

L2 can propose L1 updates, but it does not silently write them.

Promote to L1 only when the source changes standing context:

- A new active project, deadline, or blocker
- A decision that affects future work
- A person relationship that matters repeatedly
- A durable preference, voice rule, constraint, or operating principle
- A source that becomes a route-map anchor for a larger cluster

Do not promote to L1 just because the source is interesting.

## Query order

When answering from Cairns:

```text
L1 route map -> L2 Card Catalog -> L3 raw evidence
```

Start with L1 because it is small and already in context. Search L2 next because it is dense and cheap to read. Fetch L3 last because it is large and should be used for evidence, exact details, and citations.

## References

- Chain of Density paper: https://arxiv.org/abs/2309.04269
- Karpathy LLM knowledge-base gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## What's next

Install the skills that make this repeatable: `06-agent-skill-templates.md`.
