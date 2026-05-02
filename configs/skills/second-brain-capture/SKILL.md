---
name: second-brain-capture
description: Use when the user says "remember this", "save this", "add this to my second brain", drops a scratchpad item, or shares a link/thought that should become durable memory. Writes raw capture first, asks follow-up questions only when needed, and hands source-worthy items to Cairns L2/L1 flow.
---

# Second Brain Capture

You help the user turn loose inputs into durable memory.

This skill should activate when the user:

- Says "remember this", "save this", "capture this", or "add this to my second brain"
- Drops a Slack scratchpad item, URL, article, voice memo transcript, screenshot note, or rough thought
- Mentions that something should be useful later
- Gives a decision-like statement but has not explicitly invoked `/log-decision`

## Storage locations

Use this starter structure:

```text
~/Documents/second-brain/
  inbox/scratchpad/
  decisions/
  cairns/L1/
  cairns/L2/cards/
  cairns/L3/articles/
  cairns/L3/notes/
  cairns/L3/transcripts/
```

Create missing folders before writing.

## Step 1: Classify

Classify the item into one of:

- Decision
- Fact or preference
- Person or relationship context
- Project/build context
- Article or URL
- Open question
- Raw scratchpad

If it is clearly a decision, offer to use `/log-decision`.

If it is not clearly classifiable, ask one follow-up question:

"Should this become a decision, project note, person note, reading item, or just raw scratchpad?"

## Step 2: Write raw capture first

Always preserve the raw input before summarizing.

Write to:

```text
~/Documents/second-brain/inbox/scratchpad/YYYY-MM-DD-HHMM-<slug>.md
```

Include:

```markdown
---
captured_at: ISO_TIMESTAMP
source: user
classification: <classification>
status: unprocessed
---

# <short title>

## Raw
<raw content>

## Initial read
<3-5 bullet interpretation>

## Follow-up needed
<none, or the one question needed>
```

## Step 3: Enrich only when useful

For URLs, fetch or scrape the page if tools are available. Summarize:

- Core claim
- Why it matters to the user's work
- One connection to an existing L1 category if obvious

Do not research every raw thought. Research only links, claims that need validation, or items the user asks you to investigate.

## Step 4: Update L1 only when warranted

If the item is L1-worthy, append one short waypoint to the relevant file under:

```text
~/Documents/second-brain/cairns/L1/
```

Use these default files:

- `work-builds.md`
- `people.md`
- `decisions-in-flight.md`
- `reading-list.md`
- `brand-voice.md`

Keep the L1 line under 220 characters.

## Step 5: Hand off to Cairns ingest when the item is source-worthy

If the capture is a transcript, article, paper, meeting, substantial note, or other source that should be useful later, create or suggest an L2 Card Catalog entry using the `cairns-ingest` skill.

Do not write only raw text and stop when the item is clearly source-worthy. The corrected Cairns flow is:

```text
L3 raw first -> L2 Chain-of-Density card -> optional human-approved L1 waypoint
```

## Step 6: Confirm

Report:

- Raw capture file path
- L2 card path, if created
- L1 file updated, if any
- Follow-up question, if needed

Do not over-explain. The user needs to know where it went and whether anything is blocked.
