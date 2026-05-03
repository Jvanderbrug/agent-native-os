---
description: Walk the student through the personalization questionnaire and write their profile into CLAUDE.md
---

You are running the one-time personalization conversation that transforms a generic Claude into a Claude that actually knows this student. This is the unlock for everything else in the repo. Do not skip it. Do not let the student skip it.

## Step 1: Load the questionnaire

Read `configs/get-to-know-you.md` from the repo root. That file is the question bank — three sections (About You, About Your Work, How You Learn and Work). The bank totals roughly 21 questions; you will work through ALL of them, plus follow-ups, to produce a real profile.

## Step 2: Set expectations, then start

Tell the student, in your own words: "I'm going to ask you about 20 questions across three areas. We'll go in batches of 3-5 at a time so it stays conversational, not survey-like. Plan on 10-15 minutes. The output is a personalized CLAUDE.md that every future Claude session in this repo will read automatically — so the better your answers, the smarter your Claude gets."

## Step 3: Force the full conversation (CRITICAL)

If the student tries to short-circuit ("just treat me as a beginner", "skip it", "give me defaults", "I'll fill it in later"), push back once and proceed. Say: "I hear you, but the whole point of this repo is that your Claude is tuned to YOU, not a generic beginner. Sara learned this the hard way — she said 'treat me as a beginner' and ended up with a profile that knew nothing about her actual work. Three minutes per question. Let's do it." Then ask the next question.

Do not accept "I don't know" as a final answer for more than two questions in a row. Reframe, give an example, then ask again.

## Step 4: Walk the bank in batches

Go in this order, batches of 3-5 questions, conversational tone:
- Section 1 (About You): all 7 questions
- Section 2 (About Your Work): all 7 questions
- Section 3 (How You Learn and Work): all 7 questions

After each batch, briefly reflect what you heard back ("So you're spending most mornings on X and the bottleneck is Y — got it") before moving to the next batch. This builds trust and catches misinterpretations early.

## Step 5: Write the profile into CLAUDE.md

When the conversation is done, open the project root `CLAUDE.md` (create if missing). Add or update these sections, populating with the student's actual answers:

```markdown
# About Me
[name, role, domain, location, anything else they shared]

# How I Work
[daily tasks, top tools, biggest bottlenecks, what they wish was automated]

# How I Learn
[structured walkthroughs vs hand-me-the-controls, brief vs deep, feedback style]

# AI Experience
[self-rated 1-10 with context, most impressive thing built, what they wish Claude Code did better]

# Priority Use Cases
[the 3-5 things they most want this Claude to help them with]

# Communication Preferences
[brief vs detailed, direct critique vs suggestions, autonomy level they want]
```

Preserve any existing CLAUDE.md content — only add or update these sections.

## Step 6: Read back for confirmation

Show the student the new CLAUDE.md sections you wrote. Ask: "Anything wrong, missing, or worded oddly? I'll fix it before we lock it in." Edit based on their corrections.

## Step 7: Seed the starter Cairns vault

If the student is doing (or planning to do) the Cairns blueprint, also seed `templates/obsidian-cairns-starter/L0-raw/` (or the student's own Obsidian vault) with one note per interview section. Use simple frontmatter (date, source: personalize-interview, section). These L0 notes are raw input; do not synthesize patterns or metrics that did not come up in the conversation.

If the student is not doing Cairns, skip this step. The repo `CLAUDE.md` is sufficient for personalization on its own.

Both outputs (`CLAUDE.md` and the optional Cairns L0 notes) are derived from the same interview answers. Do not let them drift.
