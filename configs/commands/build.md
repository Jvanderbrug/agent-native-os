---
description: Blueprint executor — reads a blueprint and runs it. For the morning-brief blueprint, see /build-morning-brief.
---

You are running a generic blueprint build session for the user.

This command is the generic executor: the user names a blueprint or a goal, you turn it into a working local setup. It is **not** specialized for any one capstone. The Sunday capstone (the morning brief system) has its own plain-language entry point at `/build-morning-brief` — if the user is asking for that, hand off to it.

## Step 1: Identify the blueprint

If the user named a blueprint path, read it.

If the user gave a goal instead of a file, ask one question:

"Which blueprint should I use, or should I draft a build plan from your goal first?"

If the goal is "morning brief" or any close paraphrase, suggest:

```text
That is the Sunday capstone. Run /build-morning-brief instead — it is the
plain-language entry point for that build. /build stays the generic executor.
```

## Step 2: Gather only hard blockers

Ask for missing information only when it blocks setup:

- Where should the output live? Obsidian, local markdown, Vercel app, or another surface?
- Which sources are enabled today? Gmail, Calendar, Slack, YouTube transcripts, saved links, files, research topics?
- Which delivery channel should send the short ping? Slack, iMessage, Telegram, email, or none?
- Which accounts require manual auth?
- What is the user's cost ceiling?

Do not ask broad preference questions if a safe default exists.

## Step 3: Plan the build

Return a short plan before edits:

```markdown
## Build Plan
- Files I will create or edit
- Accounts/auth the user must handle
- Commands I will run
- How we will test it
- Rollback plan
```

Wait for approval before making changes unless the user explicitly says to proceed.

## Step 4: Execute in small checkpoints

Build in this order:

1. Create folders and config files.
2. Create the command or script that compiles the output.
3. Create the delivery step.
4. Run the manual test.
5. Only then add scheduling.

Never schedule a task before the manual test passes.

## Step 5: Verify

A build is done only when:

- The output artifact exists.
- The user can inspect it.
- The delivery ping works or is explicitly deferred.
- Secrets are not written in plaintext.
- The user knows the command to run again.

## Step 6: Record the decision

If `/log-decision` is installed, offer to log the final architecture choice:

"Want me to log this build decision to your second brain?"

If yes, call `/log-decision` with the selected architecture, delivery channel, and reason.
