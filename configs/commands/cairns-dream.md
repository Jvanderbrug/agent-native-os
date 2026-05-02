---
description: Run a memory consolidation pass — distill recent activity into L2 cards and update L1 waypoints
---

You are running the consolidation pass that promotes raw activity into structured memory. The metaphor is sleep memory consolidation: during the day you accumulate; during /dream you distill, organize, and pin what matters.

## Step 1: Get the scope

If the user invoked `/cairns-dream` with no args, ask:
- Scope? (default = this-session) — options: `this-session`, `today`, `this-week`, `<category-slug>`, `all`

Defaults:
- `this-session`: review only what happened this conversation
- `today`: review the last 24h of L3 activity (file changes, commits, terminal history if available)
- `this-week`: last 7 days
- `<category-slug>`: only review entries related to this L1 category
- `all`: full consolidation pass (slow — overnight job)

If they invoked `/cairns-dream --scope=<x>` directly, use that.

## Step 2: Read the relevant L3 raw

Depending on scope, gather:

- **this-session**: this conversation's history (you have it in context)
- **today / this-week**: read git logs (`git log --since`), modified files in `~/Documents/`, modified files in `~/GitHub/`, recent Granola transcripts if available, recent Slack messages from `~/.claude/cache/slack/` if synced, etc.
- **<category-slug>**: only L3 raw tagged with this category (or matching category-relevant keywords)
- **all**: everything

Cap at ~50K tokens of input — if scope is too big, sample.

## Step 3: Distill into L2 card candidates

For each cluster of related raw activity, generate a chain-of-density summary suitable for an L2 Card Catalog entry:

- 3-5 sentences max per card
- Includes specific facts, not vague summaries
- Includes backlinks to L3 sources (file paths, commit hashes, message timestamps)
- Tagged with the relevant L1 category

Example L2 card:

```markdown
# Workshop /personalize merge resolved

The /personalize slash command was unmerged on agent-native-os main as of
2026-05-01 03:34 UTC, blocking Cohort 1 students from running their personalization
step before Sunday's workshop. Orchestrator merged PR #1 overnight 2026-05-02
07:19 UTC after verifying mergeStateStatus=CLEAN.

Source: PR #1 squash commit, decision logged to
~/Documents/second-brain/decisions/2026-05-02-merge-personalize-pr.md.

Category: Work-Builds, Decisions-In-Flight (resolved).
```

## Step 4: Propose L1 waypoint updates

If any cluster of L3 raw was referenced 3+ times, propose an L1 waypoint:

"I noticed you mentioned [topic] 5 times this week. I propose adding to L1 [category]: '<one-line entry>'. Approve? (yes/no/edit)"

Char-cap each proposed L1 entry at 220.

## Step 5: Write L2 cards (with HITL approval)

For each L2 card candidate, ask the user:
- "Approve this L2 card? (yes / no / edit)"

On approve: write to `~/Documents/second-brain/cairns/L2/<category>/<topic-slug>.md`.

On edit: take the user's revisions, then write.

On no: discard the candidate.

## Step 6: Apply approved L1 updates

For each approved L1 waypoint update, call `/cairns-memory <category> "<entry>"` (or the equivalent file write).

## Step 7: Output a dream report

Show the user:
- N L2 cards written
- N L1 waypoints updated
- N candidates discarded
- Top 3 themes that emerged across the period
- Anything surprising (e.g., "you mentioned Mattermost 7 times this week but it's not in any L1 category — should it be?")

## Step 8: Schedule next /dream (optional)

Ask: "Want to schedule /dream nightly via launchd? (yes / no / I already have it)"

If yes, generate a launchd plist that runs `/dream --scope=today` at 03:00 daily.

## What this skill does NOT do (yet)

- Does not call a real Librarian Agent — that's the Cairns v1 build
- Does not run cross-category trend detection — that's a separate Recommender skill
- Does not auto-promote L2 cards to L1 without approval — HITL is mandatory

When Cairns production system is built, this skill triggers the Librarian Agent's consolidation pass. For now it writes locally with HITL approval at every step.

---

Pattern reference: `MEMORY-TIERING-AND-SOUL-PATTERN.md` § 4B in `agent-native-os-hq/architecture/`.
The "dream" metaphor: AI Jason's `/dream` slash command, adapted for Cairns.
