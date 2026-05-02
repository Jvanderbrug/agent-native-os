---
title: Build Your Own Mini Cairns
status: workshop-ready
audience: workshop-students-2026-05-03
prereqs: 00-what-is-cairns.md, 01-the-three-tiers.md, 02-the-librarian-agent.md, 03-flow-the-capture-pipeline.md
next: none (this is the last doc in the series)
---

# Build Your Own Mini Cairns

This is your first prototype. It is not the production Cairns. It will not have a Librarian Agent. It will not distinguish L2 from L3. It will not enrich with five perspectives. It will not have Neo4j or Twenty CRM.

What it will have: an L1, a `/capture` skill, and an `/ask-cairns` skill. That is enough to learn the pattern. Once you live with it for two weeks, you will know what to add next from your own pain.

Be honest about what this is: **a student-scale demo, not the production Cairns.** Tyler's spec has 21 sections of stakeholder intake gating the real build. Yours has none. That is fine. You are not building the system; you are learning the shape.

## What you're building

```
~/Documents/second-brain/
├── L1/
│   ├── work-builds.md
│   ├── people.md
│   ├── decisions-in-flight.md
│   ├── reading-list.md
│   └── brand-voice.md
└── L3/
    ├── transcripts/
    ├── notes/
    └── articles/

~/.claude/skills/
├── capture/
│   └── SKILL.md
└── ask-cairns/
    └── SKILL.md
```

Five L1 categories. Two skills. One folder for raw captures. That is the entire system.

You can swap Claude Code skills for slash commands if you are using a different harness. The pattern is the same.

## Step 1: Define your 5 L1 categories

Pick five places in your life where you keep losing context. Not 16. Five. Examples that work for most people:

| File | What goes in |
|---|---|
| `work-builds.md` | Active projects you're shipping. Status, blockers, decisions. |
| `people.md` | Names, roles, last interaction, what you owe them. |
| `decisions-in-flight.md` | Open decisions. The options. The deadline. (Stale after 24 hours.) |
| `reading-list.md` | What you're reading. The thesis. The takeaway you want to remember. |
| `brand-voice.md` | How you write. Words you use. Words you don't. Style rules. |

Create the folder and the files:

```bash
mkdir -p ~/Documents/second-brain/L1
mkdir -p ~/Documents/second-brain/L3/{transcripts,notes,articles}
touch ~/Documents/second-brain/L1/{work-builds,people,decisions-in-flight,reading-list,brand-voice}.md
```

Write a one-line waypoint in each file to start. The format that works: a header, then one or two short bullets per item. Keep each file under 400 characters until you have a reason to grow it. The point of the cap is to force selectivity. Without the cap, every file will eventually contain everything.

Example `work-builds.md`:

```markdown
# Work, Builds

- Cairns docs (in progress, due Sunday workshop, blocked on nothing)
- Personal site rewrite (paused, picking back up week of May 13)
- Client X CRM build (kicking off May 6, RCICE in scope doc)
```

That is your L1 for that category. Three lines. Always-on context. Every agent that reads your top-level memory now knows your active builds without you having to say so.

## Step 2: Write the /capture skill

This skill takes a snippet (a URL, a thought, a quote, a transcript) and writes it to the right place. The minimum viable version writes to `L3/notes/` with a date-stamped filename and optionally appends a one-line waypoint to the relevant L1 file.

Create `~/.claude/skills/capture/SKILL.md`:

```markdown
---
name: capture
description: Capture a thought, URL, or snippet to your second brain. Writes to L3 raw, optionally appends a one-line waypoint to L1.
---

# /capture

You capture content into the user's second brain at `~/Documents/second-brain/`.

## What you do

1. Determine the content type:
   - URL: fetch the page (use WebFetch), summarize in 3-5 sentences, save the
     summary plus URL to `L3/articles/YYYY-MM-DD-<slug>.md`.
   - Transcript: save raw text to `L3/transcripts/YYYY-MM-DD-<slug>.md`.
   - Plain note: save to `L3/notes/YYYY-MM-DD-<slug>.md`.

2. Decide if it is L1-worthy. Ask yourself:
   - Is this an active build update? -> append to `L1/work-builds.md`.
   - Is this a person, role, or commitment? -> append to `L1/people.md`.
   - Is this a decision in flight? -> append to `L1/decisions-in-flight.md`.
   - Is this a thing you're reading? -> append to `L1/reading-list.md`.
   - None of the above? Just live in L3.

3. When appending to L1, keep the line under 200 characters. If the L1 file
   is over 400 characters, propose what to drop before adding new content.
   Never silently exceed the cap.

4. Always write the L3 file first. The L1 update is optional and only happens
   if the user explicitly says "and pin it" or the content is clearly L1-worthy
   by the rules above.

## What you do NOT do

- Do not edit existing L3 files. They are append-only.
- Do not create new L1 categories. Only the 5 that exist.
- Do not enrich with 5-perspective analysis. That is production Cairns. This
  is the mini version.
```

The skill is intentionally simple. No vector embedding. No graph. No Librarian. Just disciplined file writes.

## Step 3: Write the /ask-cairns skill

This skill answers questions by reading L1 first, then grepping L3, then (if you have pgvector set up) doing a vector lookup.

Create `~/.claude/skills/ask-cairns/SKILL.md`:

```markdown
---
name: ask-cairns
description: Answer a question using the user's second brain. Reads L1 first, then greps L3, then optionally does a vector lookup.
---

# /ask-cairns

You answer questions using the user's second brain at `~/Documents/second-brain/`.

## Retrieval order (cascading, never skip a step)

1. **L1 first.** Read all 5 files in `L1/` - They are short. The whole tier
   fits in your context. If the answer is here, return it. Cite the L1 file.

2. **L3 grep if L1 missed.** Use `grep -ri "<keywords>" ~/Documents/second-brain/L3/`.
   Take the top 3-5 hits. Read them. If the answer is here, return it. Cite
   the file paths.

3. **Vector lookup if grep missed AND pgvector is wired.** (Most students
   will not have this on day one. That is fine. Skip this step.) If the
   user has a pgvector index over their L3 transcripts, query it for the
   top-5 nearest neighbors and read those files.

4. **If all three miss, say so.** Do not invent an answer. Tell the user
   the second brain does not have this. Suggest a `/capture` to add it.

## What you do NOT do

- Do not skip step 1 to go straight to grep. L1 is free; grep costs time.
- Do not return more than 3 sources unless the user asks for more.
- Do not summarize across sources without showing where each piece came from.
  Provenance always preserved.
```

That is your retrieval pipeline. It mirrors the production Cairns cascade (L1 -> L2 -> L3) at student scale (L1 -> grep -> vector). The shape is the same; the tools are simpler.

## Step 4: Daily ritual

The system only works if you actually use it. Two habits, both small:

**End of day, three minutes.** Open your L1 files. Look at `decisions-in-flight.md` first. Update or close anything that resolved. Look at `work-builds.md` - Update status. That is the entire ritual. If you do this for two weeks, your L1 will start being right more often than wrong.

**Whenever something useful crosses your screen.** Run `/capture` and paste the URL or paragraph. Do not over-think where it goes. The skill decides. If you find yourself running `/capture` more than 10 times a day, you are ready to graduate to a real Flow pipeline. If you are running it less than 5 times a week, your categories are wrong and you should re-pick.

**Once a week, ten minutes.** Read your `reading-list.md` and `decisions-in-flight.md` - Anything stale? Drop it. The cap forces selectivity. The selectivity is the value.

## What you didn't build (and that's fine)

You did not build:

- A Librarian Agent. You have one agent (the one running `/ask-cairns`) and one user. No mediation needed.
- L2 chain-of-density summaries. Your L3 files are short enough to grep. When your L3 grows past a few hundred files, you will start wishing for L2. That is the right time to add it.
- Five-perspective enrichment. You are not running a fleet of agents that need different cuts of your data. When you are, this is what you add.
- Neo4j or Twenty CRM. Graph relationships matter when you are reasoning about networks of people and events at scale. You can map a personal network in `people.md` for free.
- Auto-ingest daemons. You are running `/capture` manually. That is appropriate when you are capturing 10-20 things a day. When you cross 50 a day, daemons start to pay for themselves.
- A morning brief. You can build one with a launchd job and a daily prompt to your agent. Tyler's version reads from L1 every morning and surfaces "what changed yesterday." Yours can be one paragraph.

The pattern is: build the next piece when your current setup hurts. Not before.

## Where to go from here

When you have lived with mini-Cairns for two weeks, you will know which piece to add next. Some likely directions:

- **Add pgvector.** When grep stops finding things because your L3 is too big or your queries are too fuzzy.
- **Split L2 from L3.** When reading L3 files in full takes too long. The L2 summary lets the agent decide whether to load the full L3.
- **Add a second category.** When you find yourself force-fitting things into existing buckets. Add Health. Add Family. Add a hobby. Five was a starting point, not a ceiling.
- **Add an enrichment pass.** When you want answers that span perspectives ("show me everything that affects my next client engagement").
- **Spec a Librarian.** When you have a second agent that needs to read from your second brain. Then a third. Then it is time.

If you want the deeper pattern, re-read `02-the-librarian-agent.md` and `03-flow-the-capture-pipeline.md` - They describe the production Cairns. Your mini version is the same shape with fewer pieces.

The big idea is not the system. The big idea is the tier discipline. HOT for what you always need. WARM for what you sometimes need by name. COLD for everything else. Once you internalize that, every knowledge tool you ever build will be cleaner.

## Reference

- `00-what-is-cairns.md` - the 90-second version
- `01-the-three-tiers.md` - L1, L2, L3 walkthrough
- `02-the-librarian-agent.md` - agentic-RAG mediation pattern
- `03-flow-the-capture-pipeline.md` - how content gets in
- `~/GitHub/agent-native-os-hq/architecture/CAIRNS-CURRENT-STATE.md` - what production Cairns looks like (when it ships)
- `~/GitHub/agent-native-os-hq/architecture/MEMORY-TIERING-AND-SOUL-PATTERN.md` - the HOT/WARM/COLD framework in detail
- `~/GitHub/cairns/STAKEHOLDER_INTAKE.md` - the 80 questions Tyler still has to answer before the production build can start
