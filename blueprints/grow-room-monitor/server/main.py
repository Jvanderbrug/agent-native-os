"""FastMCP server entry point for the grow-room-monitor blueprint.

Tools exposed to Claude:
  - authenticate
  - list_devices
  - get_sensor_data
  - log_reading
  - render_dashboard
  - summarize_recent

Run directly:
    python main.py             # serves over stdio for local Claude Code
    python main.py --once      # do one full pull + log + dashboard render and exit

Environment is read from a sibling .env file if present.
"""

from __future__ import annotations

import argparse
import os
import statistics
import sys
from pathlib import Path

# Allow `python main.py` from the server/ directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from controller_client import ACInfinityClient, SensorReading  # noqa: E402
from dashboard import default_dashboard_path, render_dashboard  # noqa: E402
from logger import append_readings, default_log_path, read_all_rows  # noqa: E402
from sensors import fetch_all_readings, using_sample_data  # noqa: E402

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass


def _client() -> ACInfinityClient:
    return ACInfinityClient(
        email=os.environ.get("CONTROLLER_EMAIL", ""),
        password=os.environ.get("CONTROLLER_PASSWORD", ""),
    )


def _readings_from_sample() -> list[SensorReading]:
    """Replay the bundled sample CSV as if it had just been pulled."""
    sample_csv = Path(__file__).resolve().parent.parent / "sample-data" / "sensor-log.csv"
    if not sample_csv.exists():
        return []
    rows = read_all_rows(sample_csv)
    return [
        SensorReading(
            timestamp=r["timestamp"],
            device_id=r["device_id"],
            device_name=r["device_name"],
            port=int(r["port"]),
            temperature_f=float(r["temperature_f"]) if r["temperature_f"] else None,
            humidity_pct=float(r["humidity_pct"]) if r["humidity_pct"] else None,
            vpd_kpa=float(r["vpd_kpa"]) if r["vpd_kpa"] else None,
        )
        for r in rows
    ]


def do_pull_and_log() -> dict:
    """Run the twice-daily flow: auth, pull all sensors, append CSV, render dashboard."""
    if using_sample_data():
        readings = _readings_from_sample()
    else:
        with _client() as client:
            readings = fetch_all_readings(client)
    log_path = append_readings(readings)
    dash_path = render_dashboard(log_path=log_path)
    return {
        "readings_count": len(readings),
        "log_path": str(log_path),
        "dashboard_path": str(dash_path),
    }


def summarize_recent(window: int = 24) -> dict:
    """Summary stats over the most recent N readings (default 24, ~12 days at 2x/day)."""
    rows = read_all_rows(default_log_path())[-window:]
    if not rows:
        return {"window": window, "count": 0}
    temps = [float(r["temperature_f"]) for r in rows if r.get("temperature_f")]
    hums = [float(r["humidity_pct"]) for r in rows if r.get("humidity_pct")]
    vpds = [float(r["vpd_kpa"]) for r in rows if r.get("vpd_kpa")]

    def stats(xs: list[float]) -> dict | None:
        if not xs:
            return None
        return {
            "min": round(min(xs), 2),
            "max": round(max(xs), 2),
            "avg": round(statistics.fmean(xs), 2),
            "n": len(xs),
        }

    return {
        "window": window,
        "count": len(rows),
        "temperature_f": stats(temps),
        "humidity_pct": stats(hums),
        "vpd_kpa": stats(vpds),
        "latest": rows[-1],
    }


def build_mcp():
    """Build and return a FastMCP server with the grow-room tools registered."""
    from fastmcp import FastMCP

    mcp = FastMCP("grow-room-monitor")

    @mcp.tool()
    def authenticate() -> dict:
        """Log in to AC Infinity. Caches the session token on disk for reuse."""
        with _client() as client:
            token = client.authenticate(force=True)
        return {"ok": True, "token_preview": token[:6] + "..."}

    @mcp.tool()
    def list_devices() -> dict:
        """Return the list of AC Infinity controllers on this account."""
        with _client() as client:
            devices = client.list_devices()
        return {"devices": devices, "count": len(devices)}

    @mcp.tool()
    def get_sensor_data(device_id: str = "") -> dict:
        """Read live sensor data. If device_id is empty, reads every device."""
        with _client() as client:
            if device_id:
                readings = client.get_sensor_readings(device_id)
            else:
                readings = fetch_all_readings(client)
        return {"readings": [r.__dict__ for r in readings], "count": len(readings)}

    @mcp.tool()
    def log_reading() -> dict:
        """Pull live readings, append to CSV, and re-render the dashboard. The twice-daily flow."""
        return do_pull_and_log()

    @mcp.tool()
    def render() -> dict:
        """Re-render the HTML dashboard from the existing CSV without pulling new data."""
        path = render_dashboard()
        return {"dashboard_path": str(path)}

    @mcp.tool()
    def summarize(window: int = 24) -> dict:
        """Quick stats over the most recent N rows of the CSV."""
        return summarize_recent(window=window)

    return mcp


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run one pull + log + render and exit.")
    parser.add_argument("--render", action="store_true", help="Render dashboard from existing CSV and exit.")
    parser.add_argument("--summary", action="store_true", help="Print summary stats and exit.")
    args = parser.parse_args()

    if args.once:
        result = do_pull_and_log()
        print(result)
        return 0
    if args.render:
        path = render_dashboard()
        print({"dashboard_path": str(path)})
        return 0
    if args.summary:
        print(summarize_recent())
        return 0

    mcp = build_mcp()
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
