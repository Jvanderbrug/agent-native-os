---
checkpoint: 7
number: 7
name: morning-cron
layer: L4
est_duration_min: 30
time_block: "2:00-3:30"
master_outline_section: Appendix A - Per-Checkpoint Prompt Index
---

# Checkpoint 07 - morning-cron

## What This Does
Schedules the daily run. (4D plan only, 8D wire live.)

## Master Outline Cross Reference
`SUNDAY-MASTER-OUTLINE-2026-05-02.md`, Appendix A, Per-Checkpoint Prompt Index.

## Appendix A Source Row

```markdown
| 2:00-3:30 | L4 | `crontab -e` then `0 7 * * * claude -p "/morning"` | Schedules the daily run. (4D plan only, 8D wire live.) |
```

## Kick-Off Prompt

```text
crontab -e
0 7 * * * claude -p "/morning"
```
