# Get To Know You -- Personalization Conversation

You are about to have a personalization session with the user. Your job is to learn who they are, what they do, and how they want Claude to work for them. Walk through the questionnaire as if they are a new student. The point is to test whether the questionnaire -> CLAUDE.md personalization pipeline actually works and creates a meaningfully different experience.

## How This Works

Walk through the questions naturally. The user will probably give detailed answers. After the conversation, compile their answers into a profile at `profiles/{user-slug}-profile.md`, where `{user-slug}` is the kebab-case form of the user's stated first and last name during the conversation (e.g., "Jane Doe" -> `jane-doe`).

## Section 1: About You (pick 3-5)

1. What does a typical workday look like for you right now?
2. How would you rate your AI/tech expertise on a scale of 1-10?
3. What's the most impressive thing you've built with AI tools?
4. If you could automate ONE thing starting tomorrow, what would it be?
5. What's your personality type? (Enneagram, DISC, Myers-Briggs)
6. What excites you most about where AI is headed?
7. What part of Claude Code do you wish worked differently?

## Section 2: About Your Work (pick 3-5)

1. What are your top 3 daily tasks in your work?
2. Which tools do you use most?
3. What takes you the most time that you wish was automated?
4. How do you handle meeting notes and follow-ups?
5. What's the biggest operational bottleneck in your work right now?
6. If you could train 1,000 people on one AI skill, what would it be?
7. What would it look like if Claude Code was handling 80% of your repetitive work?

## Section 3: How You Learn and Work (pick 3-5)

1. When you're evaluating a new tool, what's the first thing you do?
2. Do you prefer structured walkthroughs or "give me the controls and I'll figure it out"?
3. Brief responses or detailed deep dives?
4. What makes a great tutorial vs a bad one?
5. How do you prefer to give feedback? (Direct critique, suggestions, examples)
6. What's the fastest you've ever learned a new technology? What made it click?
7. When teaching others, what's your biggest frustration?

## After the Conversation

Compile results into `profiles/{user-slug}-profile.md` with the standard structure:

```markdown
# {User Name} -- Profile

## Personal Context
[Summary]

## Business Context
[Summary]

## Working Style
[Summary]

## AI Experience Level
[Rating with context]

## Priority Use Cases
[Top 3-5]

## Workshop Design Feedback
[Meta observations about the questionnaire itself -- what worked, what felt off, what they'd change]
```

Also update the CLAUDE.md with any new preferences.
