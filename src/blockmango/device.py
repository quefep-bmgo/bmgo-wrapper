from __future__ import annotations

import random
import re

import requests

from .config import Config
from .exceptions import NetworkError


class DevicePool:
    def __init__(self, config: Config):
        self.config = config
        self._devices: list[tuple[str, str]] = []
        self._fallback = ("ddf7f7006c5947a6", "sRxNhXlmxJcVOKVue0VD7WGnBTBGa7G+Z6GrYGw3C+Q=")

    def fetch(self) -> list[tuple[str, str]]:
        try:
            r = requests.get(
                self.config.device_pool_url,
                headers={"User-Agent": "vse.taki.wizard"},
                timeout=10, verify=self.config.verify_ssl,
            )
            r.raise_for_status()
            pairs = re.findall(r'"device":\s*"([^"]+)".*?"signature":\s*"([^"]+)"', r.text)
            if pairs:
                self._devices = pairs
            return self._devices or [self._fallback]
        except Exception as e:
            raise NetworkError(f"Failed to fetch device pool: {e}") from e

    def get_random(self) -> tuple[str, str]:
        pool = self._devices or [self._fallback]
        return random.choice(pool)

    def ensure_loaded(self) -> None:
        if not self._devices:
            self.fetch()


def fetch_devices(config: Config) -> list[tuple[str, str]]:
    pool = DevicePool(config)
    return pool.fetch()