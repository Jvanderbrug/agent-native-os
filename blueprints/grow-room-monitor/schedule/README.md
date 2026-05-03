# Scheduling

Two ways to run the twice-daily pull. Pick one.

## Option A: Claude Code scheduled tasks (preferred)

Inside a Claude Code session, ask Claude:

> Schedule the grow-room-monitor skill to run at 8 AM and 8 PM Eastern every day.

Claude will create a scheduled task using the cron expression in `grow-room-monitor.cron.json`. The task invokes the skill, which calls the MCP server's `log_reading` tool.

## Option B: System cron

If you prefer to run outside Claude Code, add this to `crontab -e`:

```
0 8,20 * * * cd /path/to/grow-room-monitor/server && /usr/bin/env python main.py --once >> ../dashboards/cron.log 2>&1
```

Adjust the path. The `--once` flag does one pull, logs the readings, re-renders the dashboard, and exits.

## What each run does

1. Authenticate to AC Infinity (uses cached token if fresh).
2. List devices on the account.
3. Read every port on every device.
4. Append rows to `~/Documents/grow-room/sensor-log.csv`.
5. Re-render `dashboards/index.html`.

A run takes about 2 to 5 seconds. No external infrastructure required.
