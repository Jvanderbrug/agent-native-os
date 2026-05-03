---
description: Walk the student through the personalization questionnaire and write their profile into CLAUDE.md
---

You are running the one-time personalization conversation that transforms a generic Claude into a Claude that actually knows this student. This is the unlock for everything else in the repo. Do not skip it. Do not let the student skip it.

## Step 1: Load the questionnaire

Read `configs/get-to-know-you.md` from the repo root. That file is the question bank: three sections (About You, About Your Work, How You Learn and Work). The bank totals roughly 21 questions; you will work through ALL of them, plus follow-ups, to produce a real profile.

## Step 2: Set expectations, then start

Tell the student, in your own words: "I'm going to ask you about 20 questions across three areas. We'll go in batches of 3-5 at a time so it stays conversational, not survey-like. Plan on 10-15 minutes. The output is a personalized CLAUDE.md that every future Claude session in this repo will read automatically, so the better your answers, the smarter your Claude gets."

## Step 3: Force the full conversation (CRITICAL)

If the student tries to short-circuit ("just treat me as a beginner", "skip it", "give me defaults", "I'll fill it in later"), push back once and proceed. Say: "I hear you, but the whole point of this repo is that your Claude is tuned to YOU, not a generic beginner. Sara learned this the hard way. She said 'treat me as a beginner' and ended up with a profile that knew nothing about her actual work. Three minutes per question. Let's do it." Then ask the next question.

Do not accept "I don't know" as a final answer for more than two questions in a row. Reframe, give an example, then ask again.

## Step 4: Walk the bank in batches

Go in this order, batches of 3-5 questions, conversational tone:
- Section 1 (About You): all 7 questions
- Section 2 (About Your Work): all 7 questions
- Section 3 (How You Learn and Work): all 7 questions

After each batch, briefly reflect what you heard back ("So you're spending most mornings on X and the bottleneck is Y. Got it.") before moving to the next batch. This builds trust and catches misinterpretations early.

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

Also add or update `My Tools and Accounts`. Include the tools, accounts, commands, and MCP servers the student named. If the student has a tool Claude should use only when explicitly asked, write the tool as `<tool-name> (no-suggest)`.

Add or update `My Custom Commands` with `/what-do-i-have`, described as the on-demand toolbox inventory command that returns exactly three useful next moves.

Then add this Tool Awareness section exactly:

```markdown
## Tool Awareness

You have a growing toolbox: MCP servers, slash commands, skills, scripts, and workflows listed in this file or installed under `~/.claude`. Quietly keep track of what is available as you work. Do not recite the toolbox at startup or on every turn. Instead, when the user names a goal, finishes a build, asks what to do next, or hits a repeatable workflow that an installed tool can help with, offer one timely option in plain language.

Keep it low-friction: one sentence, one suggestion, no sales pitch. Example: "You now have Bland connected - want me to set up a morning brief that calls you?" If the user declines, move on and do not repeat that suggestion unless the context changes.
```

Add this note under `My Tools and Accounts`:

```markdown
**Suggestion opt-out:** Add `(no-suggest)` after any tool name that Claude should still use when you explicitly ask, but should never proactively recommend. Example: `Bland (no-suggest)`.
```

Preserve any existing CLAUDE.md content. Only add or update these sections.

When matching future goals to tools, check `My Tools and Accounts` first. Skip anything marked `(no-suggest)`. Surface at most one timely suggestion, only when it directly fits the user's current goal. If the user declines a suggestion, do not repeat it for the rest of that session unless the context changes. The session decline resets next session. The `(no-suggest)` tag is permanent until removed.

## Step 6: Read back for confirmation

Show the student the new CLAUDE.md sections you wrote. Ask: "Anything wrong, missing, or worded oddly? I'll fix it before we lock it in." Edit based on their corrections.

## Step 7: Check secret-management readiness

Before wrapping, ask the student about how they plan to handle API keys and other secrets. Use this exact prompt:

**Secret Management Preference:**

Which best describes your setup?

- [ ] I have 1Password CLI installed and signed in (`op whoami` works)
- [ ] I will use a `.env` file with `chmod 600` for the workshop and set up 1Password later
- [ ] I want to use Bitwarden, Infisical, or another password manager (we'll point you at docs)

If you picked option 1, you're ready. If option 2, run Guide 05 next. If option 3, ping in `#agent-native-os` for a pointer.

## Step 8: Seed the starter Cairns vault

If the student is doing (or planning to do) the Cairns blueprint, also seed `templates/obsidian-cairns-starter/L0-raw/` (or the student's own Obsidian vault) with one note per interview section. Use simple frontmatter (date, source: personalize-interview, section). These L0 notes are raw input; do not synthesize patterns or metrics that did not come up in the conversation.

If the student is not doing Cairns, skip this step. The repo `CLAUDE.md` is sufficient for personalization on its own.

Both outputs (`CLAUDE.md` and the optional Cairns L0 notes) are derived from the same interview answers. Do not let them drift.
