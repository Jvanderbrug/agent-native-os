# Obsidian Cairns Starter Vault

This is the smallest useful second-brain structure for the workshop.

It is not production Cairns. It is a local Obsidian-friendly vault structure that lets Claude Code:

- Save raw scratchpad captures
- Log decisions
- Keep short L1 waypoints always available
- Build toward a morning brief

## Install

From the repo root:

```bash
mkdir -p ~/Documents/second-brain
cp -R templates/obsidian-cairns-starter/* ~/Documents/second-brain/
```

Then install the commands and skill:

```bash
mkdir -p ~/.claude/commands ~/.claude/skills
cp configs/commands/log-decision.md ~/.claude/commands/log-decision.md
cp -R configs/skills/second-brain-capture ~/.claude/skills/second-brain-capture
```

Restart Claude Code after installing.

## Recommended Claude prompt

```text
Set up my second brain using the Obsidian Cairns starter structure in this repo. Install /log-decision globally, install the second-brain-capture skill globally, then test by logging one harmless decision.
```

## Folder map

```text
inbox/scratchpad/       Raw things you dropped in before processing
decisions/              Full decision records from /log-decision
cairns/L1/              Short always-on waypoints
cairns/L3/articles/     Article and URL captures
cairns/L3/notes/        Notes and scratchpad captures
cairns/L3/transcripts/  Meeting, voice, and video transcripts
daily-briefs/           Morning brief outputs
meeting-prep/           /prep-for-meeting outputs
daily-reviews/          /end-of-day outputs
```

