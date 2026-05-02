---
description: Build from a blueprint. Reads a specific blueprint or goal, asks missing setup questions, then creates the files/scripts/config needed to make it work.
---

You are running a blueprint build session for the user.

This command is not "make a random skill from one sentence." It is the guided builder that turns a well-written blueprint into a working local setup. The Sunday capstone use case is the morning brief system.

## Step 1: Identify the blueprint

If the user named a blueprint path, read it.

If the user gave a goal instead of a file, ask one question:

"Which blueprint should I use, or should I draft a build plan from your goal first?"

Default for the Sunday workshop:

```text
Morning brief system: sources -> compile -> short ping -> full write-up surface
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

