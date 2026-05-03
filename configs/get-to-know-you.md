# Get To Know You -- Personalization Conversation

You are about to have a personalization session with the user. Your job is to learn who they are, what they do, and how they want Claude to work for them. Walk through the questionnaire as if they are a new student. The point is to test whether the questionnaire -> CLAUDE.md personalization pipeline actually works and creates a meaningfully different experience.

## How This Works

For the workshop, ask all 21 questions unless Tyler explicitly says to shorten the interview. Walk through the questions naturally in batches of 3-5 so it stays conversational. After the conversation, the answers feed two outputs in this order:

1. **Repo `CLAUDE.md` and any `sub.md` files** for Claude Code's personalized memory, using the seven-section structure in `guides/03-your-first-claude-md.md`. This is the primary output and is required for every student.
2. **Starter Cairns vault seed** at `templates/obsidian-cairns-starter/` (or the student's own Obsidian vault if they have one), so the personal second-brain system has L0 raw notes from the interview to build on. This is required when the student is also doing the Cairns blueprint and optional otherwise.

Do not create a separate `profiles/{user-slug}-profile.md` unless the student explicitly asks for an archive copy. Both required outputs above are derived from the same set of answers; do not let them drift.

## Section 1: About You (ask all 7)

1. What does a typical workday look like for you right now?
2. How would you rate your AI/tech expertise on a scale of 1-10?
3. What's the most impressive thing you've built with AI tools?
4. If you could automate ONE thing starting tomorrow, what would it be?
5. What's your personality type? (Enneagram, DISC, Myers-Briggs)
6. What excites you most about where AI is headed?
7. What part of Claude Code do you wish worked differently?

## Section 2: About Your Work (ask all 7)

1. What are your top 3 daily tasks in your work?
2. Which tools do you use most?
3. What takes you the most time that you wish was automated?
4. How do you handle meeting notes and follow-ups?
5. What's the biggest operational bottleneck in your work right now?
6. If you could train 1,000 people on one AI skill, what would it be?
7. What would it look like if Claude Code was handling 80% of your repetitive work?

## Section 3: How You Learn and Work (ask all 7)

1. When you're evaluating a new tool, what's the first thing you do?
2. Do you prefer structured walkthroughs or "give me the controls and I'll figure it out"?
3. Brief responses or detailed deep dives?
4. What makes a great tutorial vs a bad one?
5. How do you prefer to give feedback? (Direct critique, suggestions, examples)
6. What's the fastest you've ever learned a new technology? What made it click?
7. When teaching others, what's your biggest frustration?

## After the Conversation

Write the answers into the repo's `CLAUDE.md` using the seven-section structure in `guides/03-your-first-claude-md.md`. Preserve any existing `CLAUDE.md` content; only add or update the personalization sections.

If the student is also doing the Cairns blueprint, seed their starter vault with L0 raw notes from the interview. Drop one note per section into `templates/obsidian-cairns-starter/L0-raw/` (or the student's own Obsidian vault) using simple frontmatter (date, source: personalize-interview, section). Do not invent metrics or production claims that did not come up in the conversation.

Do not create `profiles/{user-slug}-profile.md` unless the student explicitly asks for an archive copy. The CLAUDE.md and Cairns L0 notes are the canonical outputs.
