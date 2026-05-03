# Grow Room Monitor

A small agent-native blueprint that pulls live sensor data from an AC Infinity grow-room controller, logs it to a local CSV, and renders a self-contained HTML dashboard. Twice-daily polling by default. Runs entirely on the user's machine. No external infrastructure.

## What it builds

- A Python MCP server (`server/`) that wraps the reverse-engineered AC Infinity cloud API. Exposes named tools: `authenticate`, `list_devices`, `get_sensor_data`, `log_reading`, `render`, `summarize`.
- A `grow-room-monitor` Claude Code skill (`skills/grow-room-monitor/SKILL.md`) that orchestrates the tools.
- A scheduled-task config (`schedule/grow-room-monitor.cron.json`) for twice-daily polling at 8 AM and 8 PM local.
- A simple HTML dashboard rendered on each run, covering temperature, humidity, and VPD with a 200-point sparkline.
- Sample data so the dashboard works on the first run before any real readings have been pulled.

## Why

AC Infinity controllers are popular for indoor grow rooms but the vendor publishes no official API. The Homebridge and Home Assistant communities have fully reverse-engineered the cloud endpoints. This blueprint wraps those endpoints in an agent-native shape so Claude Code can do the polling, the logging, and the analysis on a schedule.

## Who it is for

Indoor growers who run an AC Infinity controller and want a personal time-series log plus a dashboard, without standing up Home Assistant or paying for a SaaS.

This blueprint was built as a Cohort 1 workshop gift for Vix Joyce on 2026-05-03. The handoff note is in `HANDOFF-TO-VIX.md`.

## Architecture at a glance

```
AC Infinity cloud
        ^
        | HTTP + JSON, token header
        |
+---------------------+        +---------------------+
| controller_client.py |  -->   | sensors.py          |
| (auth, device, read) |        | (auth + list + read)|
+---------------------+        +----------+----------+
                                          |
                                          v
+---------------------+        +---------------------+
| logger.py           | <----- | main.py / FastMCP   |
| (CSV append, rotate)|        | (tools + --once)    |
+----------+----------+        +----------+----------+
           |                              |
           v                              v
   sensor-log.csv             dashboard.py + index.html
```

Polling is twice daily so we are well below any rate-limit risk. Token is cached at `~/.config/grow-room-monitor/token.json` mode 600 so the user does not log in on every run.

## Source-of-truth references

- `github.com/keithah/homebridge-acinfinity` (API_REFERENCE.md) for endpoint shapes and auth flow.
- `github.com/dalinicus/homeassistant-acinfinity` for the production-grade Python implementation pattern.

Personal use only. AC Infinity has no public API terms of service. Do not use this to monitor anyone else's grow room.

## Setup

See `QUICKSTART.md`.

## Files

```
grow-room-monitor/
  README.md                 - this file
  QUICKSTART.md             - 5-step setup
  HANDOFF-TO-VIX.md         - personal hand-off note for Cohort 1 student Vix
  .gitignore
  server/
    main.py                 - FastMCP entrypoint and CLI
    controller_client.py    - AC Infinity HTTP client + token cache
    sensors.py              - high-level read flow
    logger.py               - CSV append + rotation
    dashboard.py            - HTML render
    requirements.txt
    .env.example
  skills/grow-room-monitor/
    SKILL.md                - Claude Code skill orchestrating the MCP tools
  schedule/
    grow-room-monitor.cron.json
    README.md
  dashboards/               - rendered HTML output (gitignored except sample screenshot)
    sample-screenshot.png   - what the dashboard looks like on first run
  sample-data/
    sensor-log.csv          - 14 rows of synthetic data so the dashboard works pre-pull
```
