# Quickstart

Five steps. About 10 minutes start to finish.

## 1. Get your AC Infinity credentials

Use the same email and password you log in to the AC Infinity mobile app with. The cloud API only returns data your app account already sees, so the controller must be paired in the app first. If you can see live readings in the app, you are good.

Note: the cloud only honors the first 25 characters of your password. Long passphrases get silently truncated.

## 2. Install Python and the dependencies

This blueprint runs on Python 3.10 or newer.

```bash
cd blueprints/grow-room-monitor/server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If the `pip install` fails on `fastmcp`, upgrade pip first: `pip install --upgrade pip`.

## 3. Configure your .env

Copy the template and fill in your credentials.

```bash
cp .env.example .env
```

Open `.env` in your editor and set `CONTROLLER_EMAIL` and `CONTROLLER_PASSWORD`. Save the file. The `.env` is gitignored, so it never gets committed.

Optional flags:

- `GROW_ROOM_LOG_PATH` overrides where the CSV lives. Default is `~/Documents/grow-room/sensor-log.csv`.
- `GROW_ROOM_DASHBOARD_PATH` overrides where the HTML lands. Default is `../dashboards/index.html` next to this folder.
- `GROW_ROOM_USE_SAMPLE_DATA=1` makes every run replay the bundled sample CSV instead of hitting the real API. Useful for testing the dashboard without burning a real pull.

## 4. Run a manual test

From `server/` with the venv active:

```bash
python main.py --once
```

You should see a printed dict with `readings_count`, `log_path`, and `dashboard_path`. Open the dashboard path in your browser. You should see a temperature, humidity, and VPD card plus a sparkline.

If you get an auth error, double-check the email and password in `.env`. If you get zero readings, open the AC Infinity mobile app and confirm the controller is online.

## 5. Schedule it

Pick one of the two paths in `schedule/README.md`:

- **Inside Claude Code:** ask Claude to schedule the `grow-room-monitor` skill at 8 AM and 8 PM in your timezone.
- **System cron:** add the line from `schedule/README.md` to your crontab.

That is it. Open the dashboard whenever you want a snapshot. Ask Claude things like "summarize my last week of grow room data" and the skill will pull from the CSV.

## Common follow-ups

- Look at the CSV anytime: `~/Documents/grow-room/sensor-log.csv`.
- Force a fresh login if the cached token misbehaves: `python main.py --once` after deleting `~/.config/grow-room-monitor/token.json`.
- Re-render the dashboard without polling: `python main.py --render`.
- Quick stats: `python main.py --summary`.
