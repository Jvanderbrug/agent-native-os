---
title: Build Your Own Mini Cairns
status: workshop-ready
audience: workshop-students-2026-05-03
prereqs: 00-what-is-cairns.md, 01-the-three-tiers.md, 02-the-librarian-agent.md, 03-flow-the-capture-pipeline.md
next: 05-card-catalog-chain-of-density.md
---

# Build Your Own Mini Cairns

This is your first prototype. It is not the production Cairns. It will not have a full Librarian service, Neo4j, Twenty CRM, or automatic multi-agent routing.

What it will have: L1 waypoints, L2 Card Catalog cards, L3 raw evidence, and skills for ingestion, query, and linting. That is enough to learn the real pattern without shipping the full production stack.

Be honest about what this is: **a student-scale demo, not the production Cairns.** Tyler's spec has 21 sections of stakeholder intake gating the real build. Yours has none. That is fine. You are not building the system; you are learning the shape.

## What you're building

```
~/Documents/second-brain/
├── cairns/
│   ├── L1/
│   │   ├── work-builds.md
│   │   ├── people.md
│   │   ├── decisions-in-flight.md
│   │   ├── reading-list.md
│   │   └── brand-voice.md
│   ├── L2/
│   │   └── cards/
│   └── L3/
│       ├── transcripts/
│       ├── notes/
│       └── articles/

~/.claude/skills/
├── cairns-ingest/
│   └── SKILL.md
├── cairns-query/
│   └── SKILL.md
└── cairns-lint/
    └── SKILL.md
```

Five L1 categories. One L2 folder of dense cards. One L3 folder for raw captures. Three skills. That is the entire system.

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
mkdir -p ~/Documents/second-brain/cairns/L1
mkdir -p ~/Documents/second-brain/cairns/L2/cards
mkdir -p ~/Documents/second-brain/cairns/L3/{transcripts,notes,articles}
touch ~/Documents/second-brain/cairns/L1/{work-builds,people,decisions-in-flight,reading-list,brand-voice}.md
```

Write a one-line waypoint in each file to start. The format that works: a header, then one or two short bullets per item. Keep each file under 400 characters until you have a reason to grow it. The point of the cap is to force selectivity. Without the cap, every file will eventually contain everything.

Example `work-builds.md`:

```markdown
# Work, Builds

- Cairns docs (in progress, due Sunday workshop, blocked on nothing)
- Personal site rewrite (paused, picking back up week of May 13)
- Client X CRM build (kicking off May 6, RCICE in scope doc)
```

That is your L1 for that category. Three lines. Always-on route-map context. Every agent that reads your top-level memory now knows where to begin without you restating it.

## Step 2: Add L2 Card Catalog

Create one L2 card for every meaningful L3 source. The card is not a normal summary. It is a Chain-of-Density card:

- Start sparse: write the core point.
- Identify missing salient entities, claims, constraints, dates, names, and terms.
- Rewrite at the same length with more signal and less filler.
- Repeat 3-5 times.
- Link back to the raw L3 source.

Read `05-card-catalog-chain-of-density.md` for the full card format.

## Step 3: Install the skills

This repo ships installable skill templates:

```bash
mkdir -p ~/.claude/skills
cp -R configs/skills/cairns-ingest ~/.claude/skills/cairns-ingest
cp -R configs/skills/cairns-query ~/.claude/skills/cairns-query
cp -R configs/skills/cairns-lint ~/.claude/skills/cairns-lint
```

Restart Claude Code after copying them.

The skills do three jobs:

- `cairns-ingest`: write L3 raw first, generate the L2 Chain-of-Density card, and propose L1 waypoint updates.
- `cairns-query`: answer by reading L1 -> searching L2 -> fetching L3 only when needed.
- `cairns-lint`: audit the vault for weak L1 waypoints, missing L2 cards, broken backlinks, and stale route maps.

## Step 4: Daily ritual

The system only works if you actually use it. Two habits, both small:

**End of day, three minutes.** Open your L1 files. Look at `decisions-in-flight.md` first. Update or close anything that resolved. Look at `work-builds.md` - Update status. That is the entire ritual. If you do this for two weeks, your L1 will start being right more often than wrong.

**Whenever something useful crosses your screen.** Use the `cairns-ingest` skill and paste the URL, paragraph, transcript, or file path. Do not over-think where it goes. The skill writes L3 raw, creates the L2 card, and proposes any L1 update. If you find yourself ingesting more than 10 things a day, you are ready to graduate to a real Flow pipeline. If you are ingesting less than 5 things a week, your categories are probably wrong and you should re-pick.

**Once a week, ten minutes.** Read your `reading-list.md` and `decisions-in-flight.md` - Anything stale? Drop it. The cap forces selectivity. The selectivity is the value.

## What you didn't build (and that's fine)

You did not build:

- A full Librarian service. The `cairns-query` skill gives you the retrieval order, but it is not a persistent cross-agent service.
- Five-perspective enrichment. You are not running a fleet of agents that need different cuts of your data. When you are, this is what you add.
- Neo4j or Twenty CRM. Graph relationships matter when you are reasoning about networks of people and events at scale. You can map a personal network in `people.md` for free.
- Auto-ingest daemons. You are running `cairns-ingest` manually. That is appropriate when you are capturing 10-20 things a day. When you cross 50 a day, daemons start to pay for themselves.
- A morning brief. You can build one with a launchd job and a daily prompt to your agent. Tyler's version reads from L1 every morning and surfaces "what changed yesterday." Yours can be one paragraph.

The pattern is: build the next piece when your current setup hurts. Not before.

## Where to go from here

When you have lived with mini-Cairns for two weeks, you will know which piece to add next. Some likely directions:

- **Add pgvector for L2 and L3.** When keyword search stops finding things because your corpus is too big or your queries are too fuzzy.
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
- `05-card-catalog-chain-of-density.md` - L2 card format and Chain-of-Density loop
- `06-agent-skill-templates.md` - installable skill templates
- `~/GitHub/agent-native-os-hq/architecture/CAIRNS-CURRENT-STATE.md` - what production Cairns looks like
- `~/GitHub/agent-native-os-hq/architecture/MEMORY-TIERING-AND-SOUL-PATTERN.md` - the HOT/WARM/COLD framework in detail
- `~/GitHub/cairns/STAKEHOLDER_INTAKE.md` - questions that gate the production build
