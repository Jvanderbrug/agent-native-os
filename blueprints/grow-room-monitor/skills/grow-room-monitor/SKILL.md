---
name: grow-room-monitor
description: Pull AC Infinity sensor data, log to CSV, and render a local dashboard. Use when the user says pull grow room data, log sensor readings, dashboard update, what is my VPD, or check the tent.
---

# Grow Room Monitor

This skill orchestrates the `grow-room-monitor` MCP server tools (built in this blueprint) to keep a local time-series log of temperature, humidity, and VPD from an AC Infinity controller, and to render a simple HTML dashboard from that log.

## When to run

- On the twice-daily schedule defined in `schedule/grow-room-monitor.cron.json` (8 AM and 8 PM local).
- On demand when the user asks for the latest reading or a fresh dashboard.

## Tool flow

1. Call `authenticate` if no session has been used today. The MCP server caches the token on disk; you usually do not need to call this manually.
2. Call `log_reading` for the canonical end-to-end pull. It will:
   - List devices on the AC Infinity account.
   - Read every port on every device.
   - Append rows to the CSV log.
   - Re-render the HTML dashboard.
3. If the user wants just a refreshed dashboard from existing data, call `render`.
4. If the user wants insight, call `summarize` with a sensible window (24 rows is about 12 days at twice-daily polling) and read back the highs, lows, and averages.

## Talking to the user

- Always report the dashboard file path so they can open it.
- If `log_reading` returns 0 readings, ask the user to confirm the controller is online in the AC Infinity mobile app. The cloud only returns data the app would see.
- VPD outside 0.8 to 1.5 kPa during flower is worth flagging. Outside 0.4 to 0.8 in early veg is worth flagging.
- Never paste the token, password, or full API response into chat. Show summaries.

## Failure modes

- API code 10001 or 100001 means the cached token is stale. Call `authenticate` once to refresh, then retry.
- HTTP errors usually mean the AC Infinity cloud is having a hiccup. Wait a few minutes and try again.
- If the user has no devices yet (empty `list_devices`), tell them the AC Infinity app must be paired with the controller first.

## Personal use only

The AC Infinity API is community-reverse-engineered, not publicly documented by the vendor. This skill is for the user's own grow room. Do not use it to monitor anyone else's setup.
