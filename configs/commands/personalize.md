---
description: Walk the student through the personalization questionnaire, write their CLAUDE.md profile, and optionally seed a local personal Cairns vault.
---

You are running the one-time personalization conversation that turns a generic Claude into a Claude that knows this student. Do not skip it. Do not let the student skip it.

## Step 1: Load the questionnaire

Read `configs/get-to-know-you.md` from the repo root. That file is the question bank with three sections:

- About You
- About Your Work
- How You Learn and Work

The bank totals roughly 21 questions. Work through all of them, plus follow-ups, to produce a real profile.

## Step 2: Set expectations, then start

Tell the student, in your own words:

```text
I'm going to ask you about 20 questions across three areas. We'll go in batches of 3-5 at a time so it stays conversational, not survey-like. Plan on 10-15 minutes. The output is a personalized CLAUDE.md that every future Claude session in this repo will read automatically, so the better your answers, the smarter your Claude gets.
```

Ask once for the personal vault path while expectations are clear:

```text
Where should your local second-brain vault live? Press Enter for the default Documents/second-brain folder.
```

Default to the user's Documents folder, not a hard-coded machine path.

## Step 3: Force the full conversation

If the student tries to short-circuit with "just treat me as a beginner", "skip it", "give me defaults", or "I'll fill it in later", push back once and proceed:

```text
I hear you, but the whole point of this repo is that your Claude is tuned to you, not a generic beginner. A thin profile creates a thin assistant. Three minutes per question. Let's do it.
```

Then ask the next question.

Do not accept "I don't know" as a final answer for more than two questions in a row. Reframe, give an example, then ask again.

## Step 4: Walk the bank in batches

Go in this order, in batches of 3-5 questions:

1. Section 1, About You: all 7 questions.
2. Section 2, About Your Work: all 7 questions.
3. Section 3, How You Learn and Work: all 7 questions.

After each batch, briefly reflect what you heard back ("So you're spending most mornings on X and the bottleneck is Y. Got it.") before moving to the next batch. This builds trust and catches misinterpretations early.

## Step 5: Write the profile into `CLAUDE.md`

When the conversation is done, open the project root `CLAUDE.md` and create it if missing. Add or update these sections with the student's actual answers:

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

Show the student the new `CLAUDE.md` sections you wrote. Ask:

```text
Anything wrong, missing, or worded oddly? I'll fix it before we lock it in.
```

Edit based on their corrections.

## Step 7: Check secret-management readiness

Before wrapping, ask the student about how they plan to handle API keys and other secrets. Use this exact prompt:

**Secret Management Preference:**

Which best describes your setup?

- [ ] I have 1Password CLI installed and signed in (`op whoami` works)
- [ ] I will use a `.env` file with `chmod 600` for the workshop and set up 1Password later
- [ ] I want to use Bitwarden, Infisical, or another password manager (we'll point you at docs)

If you picked option 1, you're ready. If option 2, run Guide 05 next. If option 3, ping in `#agent-native-os` for a pointer.

## Step 8: Seed the personal Cairns vault

Ask exactly:

```text
scaffold your personal Cairns vault now? [Y/n]
```

Add this privacy note before they answer:

```text
It's a local folder. Nothing leaves your machine unless you later choose to connect remote services.
```

If the student answers no, stop after confirming that `CLAUDE.md` is the source of truth for now.

If the student answers yes or presses Enter, invoke the `cairns-init` skill with:

- `vault_path`: the path collected in Step 2, or the default Documents second-brain folder.
- `mode`: `4D`.
- `profile_source`: the completed `CLAUDE.md` sections and questionnaire answers.
- `reseed`: `false` unless the student explicitly passed `--reseed`.

## Step 9: 4D fast path requirements

The 4D init path must complete in under 60 seconds on a normal laptop. It must not stand up Supabase, Neo4j, Docker, remote sync, or a graph database.

The 4D critical path is:

1. `<vault-root>/CLAUDE.md`
2. `<vault-root>/cairns/L1/INDEX.md`
3. `<vault-root>/cairns/L1/personal/my-self.md`
4. `<vault-root>/cairns/L1/personal/my-tools.md`
5. `<vault-root>/cairns/L1/personal/my-style.md`
6. Vault privacy guardrail
7. Minimal folder shape needed for future captures

Do not create `my-projects.md`, `my-people.md`, `my-decisions.md`, or `my-learning-goals.md` during init. Those are created on first relevant capture.

## Step 10: Idempotency and reseed

`/personalize` is idempotent.

Without `--reseed`:

- Preserve existing `CLAUDE.md`.
- Preserve existing `cairns/L1/INDEX.md`.
- Preserve each existing `cairns/L1/personal/*.md` file.
- Create only missing files and folders.
- Report created, preserved, and skipped counts.

With `--reseed`:

- Ask for confirmation before replacing each existing file.
- Never delete the whole vault.
- Never overwrite user content silently.

## Step 11: Demo the cascade

After `cairns-init` completes, tell the student:

```text
Your local Cairns starter is ready. Next, run /log-decision with one harmless real decision so you can see the L1, L2, and L3 cascade.
```
