from __future__ import annotations

import json
import os
from collections.abc import Mapping
from dataclasses import dataclass

from .constants import (
    API_BASE, DEFAULT_APP_HEADERS, DEFAULT_SESSION_CACHE,
    DEFAULT_USER_AGENT, DEVICE_POOL_URL, KEY_PAIRS, RSA_KEY, TIME_API,
)


def _parse_key_pairs(env_val: str) -> tuple[tuple[str, str], ...]:
    try:
        parsed = json.loads(env_val)
        return tuple(tuple(pair) for pair in parsed)
    except Exception:
        return KEY_PAIRS


@dataclass(slots=True, frozen=True)
class Config:
    api_base: str = API_BASE
    time_api: str = TIME_API
    device_pool_url: str = DEVICE_POOL_URL
    key_pairs: tuple[tuple[str, str], ...] = KEY_PAIRS
    rsa_key: bytes = RSA_KEY
    app_headers: Mapping[str, str] = DEFAULT_APP_HEADERS
    request_timeout: float = 15.0
    login_timeout: float = 15.0
    time_sync_timeout: float = 10.0
    time_sync_retries: int = 3
    login_max_tries: int = 6
    session_cache_path: str = DEFAULT_SESSION_CACHE
    verify_ssl: bool = False
    user_agent: str = DEFAULT_USER_AGENT

    @classmethod
    def from_env(cls) -> Config:
        return cls(
            api_base=os.getenv("BMG_API_BASE", API_BASE),
            time_api=os.getenv("BMG_TIME_API", TIME_API),
            device_pool_url=os.getenv("BMG_DEVICE_POOL_URL", DEVICE_POOL_URL),
            key_pairs=_parse_key_pairs(os.getenv("BMG_KEY_PAIRS_JSON", "")),
            rsa_key=os.getenv("BMG_RSA_KEY", "").encode() or RSA_KEY,
            request_timeout=float(os.getenv("BMG_REQUEST_TIMEOUT", "15.0")),
            login_timeout=float(os.getenv("BMG_LOGIN_TIMEOUT", "15.0")),
            time_sync_timeout=float(os.getenv("BMG_TIME_SYNC_TIMEOUT", "10.0")),
            time_sync_retries=int(os.getenv("BMG_TIME_SYNC_RETRIES", "3")),
            login_max_tries=int(os.getenv("BMG_LOGIN_MAX_TRIES", "6")),
            session_cache_path=os.getenv("BMG_SESSION_CACHE", DEFAULT_SESSION_CACHE),
            verify_ssl=os.getenv("BMG_VERIFY_SSL", "false").lower() == "true",
            user_agent=os.getenv("BMG_USER_AGENT", DEFAULT_USER_AGENT),
        )

    def with_session_cache(self, path: str) -> Config:
        return Config(
            api_base=self.api_base, time_api=self.time_api,
            device_pool_url=self.device_pool_url, key_pairs=self.key_pairs,
            rsa_key=self.rsa_key, app_headers=self.app_headers,
            request_timeout=self.request_timeout, login_timeout=self.login_timeout,
            time_sync_timeout=self.time_sync_timeout,
            time_sync_retries=self.time_sync_retries,
            login_max_tries=self.login_max_tries,
            session_cache_path=path, verify_ssl=self.verify_ssl,
            user_agent=self.user_agent,
        )