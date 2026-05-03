"""Render a single self-contained HTML dashboard from the CSV log."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from logger import default_log_path, read_all_rows

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Grow Room Monitor</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    :root { color-scheme: light dark; }
    body { font: 14px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
           margin: 0; padding: 24px; max-width: 960px; margin-left: auto; margin-right: auto; }
    h1 { font-weight: 600; margin: 0 0 4px; }
    .sub { color: #666; margin-bottom: 24px; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
             gap: 12px; margin-bottom: 24px; }
    .card { border: 1px solid #ddd; border-radius: 10px; padding: 14px 16px; }
    .card .label { color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }
    .card .value { font-size: 28px; font-weight: 600; margin-top: 4px; }
    .card .unit { font-size: 14px; color: #888; margin-left: 4px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th, td { padding: 6px 8px; text-align: left; border-bottom: 1px solid #eee; }
    th { color: #666; font-weight: 500; }
    canvas { width: 100%; height: 220px; margin-bottom: 16px; }
    .empty { color: #888; font-style: italic; padding: 24px; text-align: center;
             border: 1px dashed #ccc; border-radius: 10px; }
    @media (prefers-color-scheme: dark) {
      body { background: #111; color: #ddd; }
      .card, table { border-color: #333; }
      th, td { border-bottom-color: #2a2a2a; }
    }
  </style>
</head>
<body>
  <h1>Grow Room Monitor</h1>
  <div class="sub">Generated {{ generated_at }}. {{ row_count }} readings logged.</div>

  {% if not rows %}
  <div class="empty">No readings yet. Run a manual pull or wait for the scheduled job.</div>
  {% else %}
  <div class="cards">
    <div class="card"><div class="label">Latest temperature</div>
      <div class="value">{{ latest.temp }}<span class="unit">F</span></div></div>
    <div class="card"><div class="label">Latest humidity</div>
      <div class="value">{{ latest.hum }}<span class="unit">%</span></div></div>
    <div class="card"><div class="label">Latest VPD</div>
      <div class="value">{{ latest.vpd }}<span class="unit">kPa</span></div></div>
    <div class="card"><div class="label">Last reading</div>
      <div class="value" style="font-size:18px;">{{ latest.ts }}</div></div>
  </div>

  <canvas id="chart"></canvas>

  <h2>Recent readings</h2>
  <table>
    <thead><tr>
      <th>Time</th><th>Device</th><th>Port</th><th>Temp F</th><th>Humidity %</th><th>VPD kPa</th>
    </tr></thead>
    <tbody>
      {% for r in recent %}
      <tr>
        <td>{{ r.timestamp }}</td><td>{{ r.device_name }}</td><td>{{ r.port }}</td>
        <td>{{ r.temperature_f }}</td><td>{{ r.humidity_pct }}</td><td>{{ r.vpd_kpa }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <script>
    const series = {{ series_json }};
    const canvas = document.getElementById('chart');
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    function resize() {
      canvas.width = canvas.clientWidth * dpr;
      canvas.height = canvas.clientHeight * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      draw();
    }
    function draw() {
      const w = canvas.clientWidth, h = canvas.clientHeight;
      ctx.clearRect(0, 0, w, h);
      if (!series.points.length) return;
      const xs = series.points.map((_, i) => i);
      const lines = [
        { key: 'temp', color: '#e07a5f', label: 'Temp F' },
        { key: 'hum', color: '#3d5a80', label: 'Humidity %' },
        { key: 'vpd', color: '#81b29a', label: 'VPD kPa x10' },
      ];
      lines.forEach(line => {
        const ys = series.points.map(p => p[line.key]);
        const valid = ys.filter(v => v !== null);
        if (!valid.length) return;
        const yMin = Math.min(...valid), yMax = Math.max(...valid);
        const yRange = (yMax - yMin) || 1;
        ctx.strokeStyle = line.color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        let started = false;
        ys.forEach((v, i) => {
          if (v === null) return;
          const x = (i / Math.max(1, xs.length - 1)) * (w - 40) + 30;
          const y = h - 20 - ((v - yMin) / yRange) * (h - 40);
          if (!started) { ctx.moveTo(x, y); started = true; } else { ctx.lineTo(x, y); }
        });
        ctx.stroke();
      });
    }
    window.addEventListener('resize', resize);
    resize();
  </script>
  {% endif %}
</body>
</html>
"""


def default_dashboard_path() -> Path:
    return Path(
        os.environ.get(
            "GROW_ROOM_DASHBOARD_PATH",
            str(Path(__file__).resolve().parent.parent / "dashboards" / "index.html"),
        )
    )


def render_dashboard(log_path: Path | None = None, output_path: Path | None = None) -> Path:
    rows = read_all_rows(log_path)
    out = output_path or default_dashboard_path()
    out.parent.mkdir(parents=True, exist_ok=True)

    latest = {"temp": "n/a", "hum": "n/a", "vpd": "n/a", "ts": "n/a"}
    if rows:
        last = rows[-1]
        latest = {
            "temp": last.get("temperature_f") or "n/a",
            "hum": last.get("humidity_pct") or "n/a",
            "vpd": last.get("vpd_kpa") or "n/a",
            "ts": last.get("timestamp") or "n/a",
        }
    recent = list(reversed(rows[-20:]))
    points = [
        {
            "ts": r.get("timestamp"),
            "temp": _num(r.get("temperature_f")),
            "hum": _num(r.get("humidity_pct")),
            # VPD is small (0.5-2.0 typically). Multiply 10x so it shares the axis cleanly.
            "vpd": (lambda v: v * 10 if v is not None else None)(_num(r.get("vpd_kpa"))),
        }
        for r in rows[-200:]
    ]
    html = _render(TEMPLATE, {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "row_count": len(rows),
        "rows": rows,
        "latest": latest,
        "recent": recent,
        "series_json": json.dumps({"points": points}),
    })
    out.write_text(html, encoding="utf-8")
    return out


def _num(s: str | None) -> float | None:
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _render(template: str, ctx: dict) -> str:
    # Minimal Jinja2-style render. We keep the import local so the file can be
    # read without jinja2 installed if Vix is just inspecting it.
    from jinja2 import Template

    return Template(template).render(**ctx)
