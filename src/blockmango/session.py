from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .config import Config
from .exceptions import SessionError


class SessionStore:
    def __init__(self, config: Config):
        self.config = config
        self._path = Path(config.session_cache_path).expanduser().resolve()
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def load(self, username: str) -> dict[str, Any]:
        try:
            if not self._path.exists():
                return {}
            with open(self._path, encoding="utf-8") as f:
                data = json.load(f)
            return data.get(username) or {}
        except Exception:
            return {}

    def save(self, username: str, session: dict[str, Any]) -> None:
        if not (session.get("uid") and session.get("token")):
            return
        try:
            data: dict[str, Any] = {}
            if self._path.exists():
                try:
                    with open(self._path, encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            data[username] = session
            tmp = self._path.with_suffix(self._path.suffix + ".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self._path)
        except Exception as e:
            raise SessionError(f"Failed to save session: {e}") from e

    def delete(self, username: str) -> None:
        try:
            if not self._path.exists():
                return
            with open(self._path, encoding="utf-8") as f:
                data = json.load(f)
            if username in data:
                del data[username]
                tmp = self._path.with_suffix(self._path.suffix + ".tmp")
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                os.replace(tmp, self._path)
        except Exception:
            pass


def load_session(config: Config, username: str) -> dict[str, Any]:
    store = SessionStore(config)
    return store.load(username)


def save_session(config: Config, username: str, session: dict[str, Any]) -> None:
    store = SessionStore(config)
    store.save(username, session)