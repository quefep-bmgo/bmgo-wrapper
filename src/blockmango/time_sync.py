from __future__ import annotations

import time

import requests

from .config import Config
from .exceptions import NetworkError


class TimeSyncer:
    def __init__(self, config: Config):
        self.config = config
        self._offset: int = 0

    @property
    def offset(self) -> int:
        return self._offset

    def sync(self) -> int:
        for attempt in range(self.config.time_sync_retries):
            try:
                t0 = time.time()
                r = requests.get(
                    self.config.time_api,
                    timeout=self.config.time_sync_timeout,
                    verify=self.config.verify_ssl,
                )
                t1 = time.time()
                r.raise_for_status()
                server_ms = int(r.json()["data"])
                server_sec = server_ms // 1000
                self._offset = int(server_sec - (t0 + t1) / 2)
                return self._offset
            except Exception as e:
                if attempt < self.config.time_sync_retries - 1:
                    time.sleep(0.4 * (attempt + 1))
                else:
                    self._offset = 0
                    raise NetworkError(f"Time sync failed after {self.config.time_sync_retries} attempts: {e}") from e
        return 0

    def force_sync(self) -> int:
        return self.sync()


def sync_time(config: Config) -> int:
    syncer = TimeSyncer(config)
    return syncer.sync()