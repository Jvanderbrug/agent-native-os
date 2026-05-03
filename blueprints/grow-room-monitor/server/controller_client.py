"""AC Infinity cloud API client.

Wraps the reverse-engineered AC Infinity backend used by the homebridge and
Home Assistant community integrations. Handles login, session token caching
on disk (mode 600), and the two read endpoints needed for sensor monitoring.

Source of truth for endpoints:
- github.com/keithah/homebridge-acinfinity (API_REFERENCE.md)
- github.com/dalinicus/homeassistant-acinfinity

Personal use only. AC Infinity has no public API terms of service.
"""

from __future__ import annotations

import json
import os
import stat
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

BASE_URL = "http://www.acinfinityserver.com"
LOGIN_PATH = "/api/user/appUserLogin"
DEVICES_PATH = "/api/user/devInfoListAll"
SENSORS_PATH = "/api/dev/getdevModeSettingList"

DEFAULT_HEADERS = {
    "phoneType": "1",
    "appVersion": "1.9.7",
    "User-Agent": "grow-room-monitor/0.1 (personal use)",
}

# AC Infinity login truncates to first 25 chars of password.
PASSWORD_MAX = 25
# Be polite to the cloud. Twice-daily polling is well below any throttle line.
REQUEST_TIMEOUT = 15.0


def _default_token_path() -> Path:
    return Path(
        os.environ.get(
            "GROW_ROOM_TOKEN_PATH",
            str(Path.home() / ".config" / "grow-room-monitor" / "token.json"),
        )
    )


@dataclass
class SensorReading:
    """One sensor sample for one device port."""

    timestamp: str
    device_id: str
    device_name: str
    port: int
    temperature_f: float | None
    humidity_pct: float | None
    vpd_kpa: float | None

    def as_csv_row(self) -> list[str]:
        return [
            self.timestamp,
            self.device_id,
            self.device_name,
            str(self.port),
            "" if self.temperature_f is None else f"{self.temperature_f:.2f}",
            "" if self.humidity_pct is None else f"{self.humidity_pct:.2f}",
            "" if self.vpd_kpa is None else f"{self.vpd_kpa:.2f}",
        ]


class ACInfinityError(Exception):
    """Any error talking to the AC Infinity cloud."""


class ACInfinityClient:
    def __init__(
        self,
        email: str,
        password: str,
        token_path: Path | None = None,
        base_url: str = BASE_URL,
    ) -> None:
        if not email or not password:
            raise ACInfinityError(
                "CONTROLLER_EMAIL and CONTROLLER_PASSWORD are both required."
            )
        self.email = email
        self.password = password[:PASSWORD_MAX]
        self.token_path = token_path or _default_token_path()
        self.base_url = base_url
        self._token: str | None = None
        self._user_id: str | None = None
        self._client = httpx.Client(timeout=REQUEST_TIMEOUT)

    def __enter__(self) -> "ACInfinityClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self._client.close()

    def authenticate(self, force: bool = False) -> str:
        """Log in or reuse a cached token. Returns the bearer token."""
        if not force:
            cached = self._load_cached_token()
            if cached:
                self._token = cached["appId"]
                self._user_id = cached.get("userId") or cached.get("appId")
                return self._token

        body = {"appEmail": self.email, "appPasswordl": self.password}
        resp = self._client.post(
            self.base_url + LOGIN_PATH,
            data=body,
            headers={**DEFAULT_HEADERS, "Content-Type": "application/x-www-form-urlencoded"},
        )
        payload = self._parse(resp, context="login")
        data = payload.get("data") or {}
        token = data.get("appId")
        if not token:
            raise ACInfinityError(f"login response missing appId: {payload}")
        self._token = token
        self._user_id = token
        self._save_cached_token({"appId": token, "userId": token, "ts": time.time()})
        return token

    def list_devices(self) -> list[dict[str, Any]]:
        """Return the user's controllers and their attached devices."""
        token = self.authenticate()
        resp = self._client.post(
            self.base_url + DEVICES_PATH,
            data={"userId": self._user_id or token},
            headers={**DEFAULT_HEADERS, "token": token},
        )
        payload = self._parse(resp, context="list_devices")
        data = payload.get("data") or []
        if not isinstance(data, list):
            return []
        return data

    def get_sensor_readings(self, device_id: str, ports: list[int] | None = None) -> list[SensorReading]:
        """Read sensor samples for one device. If ports is None, reads ports 1-4."""
        token = self.authenticate()
        ports = ports or [1, 2, 3, 4]
        readings: list[SensorReading] = []
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        for port in ports:
            resp = self._client.post(
                self.base_url + SENSORS_PATH,
                data={"devId": device_id, "port": port},
                headers={**DEFAULT_HEADERS, "token": token},
            )
            payload = self._parse(resp, context=f"sensors port {port}", allow_empty=True)
            data = payload.get("data") or {}
            if not data:
                continue
            # Per homebridge-acinfinity API_REFERENCE: temperature, humidity, vpdnums
            # are stored as integer * 100. Some firmwares omit fields when no probe is attached.
            temp_raw = data.get("temperature")
            hum_raw = data.get("humidity")
            vpd_raw = data.get("vpdnums")
            readings.append(
                SensorReading(
                    timestamp=timestamp,
                    device_id=device_id,
                    device_name=str(data.get("devName") or data.get("devCode") or device_id),
                    port=port,
                    temperature_f=_scale(temp_raw),
                    humidity_pct=_scale(hum_raw),
                    vpd_kpa=_scale(vpd_raw),
                )
            )
        return readings

    # --- internals -----------------------------------------------------

    def _parse(self, resp: httpx.Response, context: str, allow_empty: bool = False) -> dict[str, Any]:
        if resp.status_code != 200:
            raise ACInfinityError(f"{context}: HTTP {resp.status_code} {resp.text[:200]}")
        try:
            payload = resp.json()
        except json.JSONDecodeError as exc:
            raise ACInfinityError(f"{context}: non-JSON body: {resp.text[:200]}") from exc
        code = payload.get("code")
        if code != 200:
            if allow_empty and code in (10001, 100001):
                return {"data": {}}
            raise ACInfinityError(f"{context}: API code={code} msg={payload.get('msg')}")
        return payload

    def _load_cached_token(self) -> dict[str, Any] | None:
        try:
            raw = self.token_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        except OSError:
            return None
        try:
            cached = json.loads(raw)
        except json.JSONDecodeError:
            return None
        # AC Infinity tokens have "no visible expiration" per the API reference,
        # but we refresh after 7 days as a safety net.
        ts = cached.get("ts", 0)
        if time.time() - ts > 7 * 24 * 3600:
            return None
        return cached

    def _save_cached_token(self, payload: dict[str, Any]) -> None:
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        self.token_path.write_text(json.dumps(payload), encoding="utf-8")
        try:
            os.chmod(self.token_path, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass


def _scale(raw: Any) -> float | None:
    """AC Infinity stores temp/humidity/vpd as int * 100."""
    if raw is None or raw == "":
        return None
    try:
        return float(raw) / 100.0
    except (TypeError, ValueError):
        return None
