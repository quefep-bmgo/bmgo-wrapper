from __future__ import annotations

import random
import re

import requests

from .config import Config
from .exceptions import NetworkError


class DevicePool:
    def __init__(self, config: Config):
        self.config = config
        self._devices: list[tuple[str, str, str]] = []  # (device_id, device_sign, bm_ddh_id)
        self._fallback = (config.device_id, config.device_sign, config.bm_ddh_id)

    def fetch(self) -> list[tuple[str, str, str]]:
        try:
            r = requests.get(
                self.config.device_pool_url,
                headers={"User-Agent": "vse.taki.wizard"},
                timeout=10, verify=self.config.verify_ssl,
            )
            r.raise_for_status()
            pairs = re.findall(r'"device":\s*"([^"]+)".*?"signature":\s*"([^"]+)"', r.text)
            valid_pairs = [(d, s, s) for d, s in pairs if d not in ("access", "denied")]
            if valid_pairs:
                self._devices = valid_pairs
            return self._devices or [self._fallback]
        except Exception:
            return [self._fallback]

    def get_random(self) -> tuple[str, str, str]:
        pool = self._devices or [self._fallback]
        return random.choice(pool)

    def ensure_loaded(self) -> None:
        if not self._devices:
            self.fetch()


def fetch_devices(config: Config) -> list[tuple[str, str, str]]:
    pool = DevicePool(config)
    return pool.fetch()
