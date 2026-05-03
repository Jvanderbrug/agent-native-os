"""High level sensor read flow that ties auth + device list + sensor calls together."""

from __future__ import annotations

import os

from controller_client import ACInfinityClient, SensorReading


def fetch_all_readings(client: ACInfinityClient) -> list[SensorReading]:
    """Authenticate, list devices, read every port on every device.

    Returns one SensorReading per (device, port) pair that reports any data.
    """
    client.authenticate()
    devices = client.list_devices()
    out: list[SensorReading] = []
    for dev in devices:
        device_id = str(dev.get("devId") or dev.get("devCode") or "")
        if not device_id:
            continue
        out.extend(client.get_sensor_readings(device_id))
    return out


def using_sample_data() -> bool:
    return os.environ.get("GROW_ROOM_USE_SAMPLE_DATA") == "1"
