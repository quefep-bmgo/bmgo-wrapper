from __future__ import annotations

import threading

from .account import BmgAccount
from .config import Config


class BmgClient:
    __slots__ = ("_accounts", "_config", "_lock", "_pool", "_rr")

    def __init__(self, accounts: list[dict[str, str]], config: Config | None = None):
        self._accounts = accounts
        self._config = config or Config.from_env()
        self._pool: list[BmgAccount] = []
        self._lock = threading.Lock()
        self._rr = 0

    def login_all(self) -> dict[str, str]:
        results: dict[str, str] = {}
        self._pool = []
        for acc in self._accounts:
            a = BmgAccount(acc["username"], acc["password"], self._config)
            sess = a.load_session()
            if sess and a.restore_session(sess) and a.session_valid():
                ok = True
                results[acc["username"]] = "cached"
            else:
                ok = a.login()
                results[acc["username"]] = "ok" if ok else "FAILED"
            if ok:
                self._pool.append(a)
        return results

    async def async_login_all(self) -> dict[str, str]:
        results: dict[str, str] = {}
        self._pool = []
        for acc in self._accounts:
            a = BmgAccount(acc["username"], acc["password"], self._config)
            sess = a.load_session()
            if sess and a.restore_session(sess) and await a.async_session_valid():
                ok = True
                results[acc["username"]] = "cached"
            else:
                ok = await a.async_login()
                results[acc["username"]] = "ok" if ok else "FAILED"
            if ok:
                self._pool.append(a)
        return results

    def get(self) -> BmgAccount | None:
        with self._lock:
            if not self._pool:
                return None
            acc = self._pool[self._rr % len(self._pool)]
            self._rr += 1
            return acc

    async def async_get(self) -> BmgAccount | None:
        with self._lock:
            if not self._pool:
                return None
            acc = self._pool[self._rr % len(self._pool)]
            self._rr += 1
            return acc

    @property
    def available(self) -> int:
        return len(self._pool)

    @property
    def async_available(self) -> int:
        return len(self._pool)

    def close_all(self) -> None:
        for acc in self._pool:
            acc.close()
        self._pool.clear()

    async def async_close_all(self) -> None:
        for acc in self._pool:
            await acc.async_close()
        self._pool.clear()

    def __enter__(self) -> BmgClient:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_all()

    async def __aenter__(self) -> BmgClient:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.async_close_all()

    def __len__(self) -> int:
        return len(self._pool)

    def __bool__(self) -> bool:
        return bool(self._pool)