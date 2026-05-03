"""CSV append-only logger with daily rotation."""

from __future__ import annotations

import csv
import os
import shutil
from datetime import datetime
from pathlib import Path

from controller_client import SensorReading

CSV_HEADER = [
    "timestamp",
    "device_id",
    "device_name",
    "port",
    "temperature_f",
    "humidity_pct",
    "vpd_kpa",
]

# Rotate when the file passes 5 MB. At twice-daily polling that is years away,
# but it keeps the file from growing unbounded if Vix bumps the schedule later.
ROTATE_BYTES = 5 * 1024 * 1024


def default_log_path() -> Path:
    return Path(
        os.environ.get(
            "GROW_ROOM_LOG_PATH",
            str(Path.home() / "Documents" / "grow-room" / "sensor-log.csv"),
        )
    )


def append_readings(readings: list[SensorReading], log_path: Path | None = None) -> Path:
    path = log_path or default_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    _rotate_if_needed(path)
    write_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if write_header:
            writer.writerow(CSV_HEADER)
        for r in readings:
            writer.writerow(r.as_csv_row())
    return path


def read_all_rows(log_path: Path | None = None) -> list[dict[str, str]]:
    path = log_path or default_log_path()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def _rotate_if_needed(path: Path) -> None:
    if not path.exists():
        return
    if path.stat().st_size < ROTATE_BYTES:
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    rotated = path.with_name(f"{path.stem}.{stamp}{path.suffix}")
    shutil.move(str(path), str(rotated))
