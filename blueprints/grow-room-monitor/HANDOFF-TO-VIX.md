# Hand-off to Vix

Hey Vix,

Tyler here. I built this for you over the weekend as a Sunday workshop gift, before we even kicked off Cohort 1. Quick context on why this one in particular: I came up through Grower's Solution before AI Build Lab existed, so when you posted the AC Infinity question in the cohort channel I recognized the setup immediately. This is exactly the kind of build that turns Claude Code from "chat tool" into "thing that quietly takes care of your room while you sleep."

## What you are getting

A small, self-contained agent that:

1. Logs into your AC Infinity account using the same email and password you use for the mobile app.
2. Pulls live temperature, humidity, and VPD from every device on your account, twice a day.
3. Appends each reading to a CSV on your machine.
4. Re-renders a clean local HTML dashboard so you can eyeball trends.
5. Lets you ask Claude things like "summarize my last week of grow room readings" and the same skill answers from the CSV.

The whole thing runs locally. No SaaS, no cloud function, no monthly bill. Token is cached on disk so it does not re-login every run.

## What is in the folder

- `README.md` is the technical overview if you want it.
- `QUICKSTART.md` is the 5-step setup. Start there.
- `server/` is the Python MCP server. The five files inside are small and easy to read.
- `skills/grow-room-monitor/SKILL.md` is the Claude Code skill that orchestrates the MCP tools.
- `schedule/` has the twice-daily cron config and notes on two ways to run it.
- `sample-data/` has 14 rows of fake readings so the dashboard works on day one before any real pulls.
- `dashboards/sample-screenshot.png` is what the dashboard looks like the first time you open it.

## Three things to do tonight if you want to be ready Sunday

1. **Capture your AC Infinity credentials.** Just have your email and app password handy. Note the cloud only honors the first 25 characters of the password.
2. **Install Python 3.10 or newer.** If you already have it, skip this. `python3 --version` will tell you.
3. **Copy `server/.env.example` to `server/.env`** and paste your credentials. The `.env` is gitignored so it stays on your machine.

That is it. The actual install of the dependencies and the first manual pull are step 2 and step 4 of `QUICKSTART.md` and they take about three minutes together.

## Sample data so you see the shape on day one

Before you run a real pull, you can do this:

```bash
cd blueprints/grow-room-monitor/server
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
GROW_ROOM_USE_SAMPLE_DATA=1 python main.py --once
```

That replays the bundled sample CSV and renders the dashboard. Open `dashboards/index.html` in your browser. The screenshot in `dashboards/sample-screenshot.png` is what you should see.

## Where the live data goes

Once you are running for real, your CSV lives at `~/Documents/grow-room/sensor-log.csv`. Open it in Numbers, drag it into Cursor, feed it to Claude, whatever you like. Two readings per day means about 700 rows per year. Tiny.

## Where this fits with the bigger picture you mentioned

You said you eventually want this feeding a personal landing page that combines the sensor stream with an AI camera feed and an analyzing agent. This blueprint is the sensor leg of that. The CSV is the join point. When the camera leg comes together, both can land in the same place and the agent reads from both. We can wire that part during a Lab session once you have a few weeks of real data flowing.

## When you get stuck

You have backup. All of these humans (and Gigawatt) live in the workshop Slack and any of them can help you unjam if a step is weird:

- Tyler (me)
- Sara
- Wade
- Hunter
- MAIIA (she did the original Perplexity research that made this possible)
- Gigawatt (the agent)

Drop a screenshot of the error in the cohort channel and someone will jump.

## One small ask

This is personal use only. AC Infinity has no public API terms of service, so the convention in the community is "monitor your own room, do not resell." I just want you to have your dashboard, not turn it into a product.

Have fun with it. See you Sunday.

Tyler
