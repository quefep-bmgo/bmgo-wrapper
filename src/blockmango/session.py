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
            os.chmod(self._path, 0o600)
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
            self._write_private(data)
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
                self._write_private(data)
        except Exception:
            pass

    def _write_private(self, data: dict[str, Any]) -> None:
        tmp = self._path.with_suffix(self._path.suffix + ".tmp")
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            try:
                os.close(fd)
            except OSError:
                pass
            raise
        os.chmod(tmp, 0o600)
        os.replace(tmp, self._path)
        os.chmod(self._path, 0o600)


def load_session(config: Config, username: str) -> dict[str, Any]:
    store = SessionStore(config)
    return store.load(username)


def save_session(config: Config, username: str, session: dict[str, Any]) -> None:
    store = SessionStore(config)
    store.save(username, session)
