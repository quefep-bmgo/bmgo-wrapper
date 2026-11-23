from __future__ import annotations

import asyncio
import threading
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor

from .account import BmgAccount
from .config import Config
from .models import AccountFriendMatch
from .transport import GroupMessageResult


class BmgClient:
    __slots__ = ("_accounts", "_by_name", "_config", "_lock", "_pool", "_rr")

    def __init__(self, accounts: list[dict[str, str]], config: Config | None = None):
        self._accounts = accounts
        self._config = config or Config.from_env()
        self._pool: list[BmgAccount] = []
        self._by_name: dict[str, BmgAccount] = {}
        self._lock = threading.Lock()
        self._rr = 0

    def login_all(
        self,
        *,
        load_social: bool = True,
        start_sync: bool = True,
        sync_interval: float = 60.0,
    ) -> dict[str, str]:
        """Log in every configured account and hydrate its friend/group state.

        ``load_social`` performs one full friend and group snapshot after login.
        ``start_sync`` then keeps one daemon polling thread per account so new
        or removed groups/friends become visible through ``account.social``.
        Set either flag to ``False`` when the caller owns scheduling.
        """
        self.close_all()
        results: dict[str, str] = {}
        for acc in self._accounts:
            a = BmgAccount(acc["username"], acc["password"], self._config)
            sess = a.load_session()
            cached = bool(sess and a.restore_session(sess) and a.session_valid())
            if cached:
                ok = True
                results[acc["username"]] = "cached"
                self._prepare_cached_social(a, load_social, start_sync, sync_interval)
            else:
                ok = a.login(
                    load_social=load_social,
                    start_sync=start_sync,
                    sync_interval=sync_interval,
                )
                results[acc["username"]] = "ok" if ok else "FAILED"
            if ok:
                self._pool.append(a)
                self._by_name[acc["username"]] = a
        return results

    async def async_login_all(
        self,
        *,
        load_social: bool = True,
        start_sync: bool = True,
        sync_interval: float = 60.0,
    ) -> dict[str, str]:
        """Async equivalent of :meth:`login_all`."""
        await self.async_close_all()
        results: dict[str, str] = {}
        for acc in self._accounts:
            a = BmgAccount(acc["username"], acc["password"], self._config)
            sess = a.load_session()
            cached = bool(sess and a.restore_session(sess) and await a.async_session_valid())
            if cached:
                ok = True
                results[acc["username"]] = "cached"
                if load_social:
                    try:
                        await a.social.async_refresh()
                    except Exception:
                        pass
                if start_sync:
                    try:
                        await a.social.async_start(sync_interval)
                    except RuntimeError:
                        pass
            else:
                ok = await a.async_login(
                    load_social=load_social,
                    start_sync=start_sync,
                    sync_interval=sync_interval,
                )
                results[acc["username"]] = "ok" if ok else "FAILED"
            if ok:
                self._pool.append(a)
                self._by_name[acc["username"]] = a
        return results

    @staticmethod
    def _prepare_cached_social(
        account: BmgAccount,
        load_social: bool,
        start_sync: bool,
        sync_interval: float,
    ) -> None:
        if load_social:
            try:
                account.social.refresh()
            except Exception:
                # The cached session remains usable; account.social.last_error
                # has the failure and its polling loop will retry.
                pass
        if start_sync:
            try:
                account.social.start(sync_interval)
            except RuntimeError:
                pass

    def start_social_sync(self, interval: float = 60.0) -> None:
        """Start/refresh social polling for all logged-in accounts."""
        for account in self.accounts:
            account.social.start(interval)

    def stop_social_sync(self, timeout: float | None = 5.0) -> None:
        for account in self.accounts:
            account.social.stop(timeout)

    async def async_start_social_sync(self, interval: float = 60.0) -> None:
        for account in self.accounts:
            await account.social.async_start(interval)

    async def async_stop_social_sync(self) -> None:
        for account in self.accounts:
            await account.social.async_stop()

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
    def accounts(self) -> tuple[BmgAccount, ...]:
        """Logged-in accounts, in login order."""
        with self._lock:
            return tuple(self._pool)

    def get_account(self, username: str) -> BmgAccount | None:
        """Return a specific logged-in account by username."""
        with self._lock:
            account = self._by_name.get(username)
            if account is not None:
                return account
            folded = username.casefold()
            return next(
                (candidate for name, candidate in self._by_name.items()
                 if name.casefold() == folded),
                None,
            )

    def find_friends(
        self,
        query: str | int,
        usernames: list[str] | None = None,
        force_refresh: bool = False,
        max_friends: int = 500,
        max_workers: int = 4,
    ) -> list[AccountFriendMatch]:
        """Find matching friends across one or more logged-in accounts.

        Each account keeps its own cached friend snapshot. Calls are parallel
        only across distinct accounts and use a small bounded pool, so a
        multi-account search does not create an unbounded number of HTTP
        requests or threads.
        """
        targets = self._target_accounts(usernames)
        if not targets:
            return []
        if len(targets) == 1:
            account = targets[0]
            matches = account.friends.find_friends(query, max_friends, force_refresh)
            return [AccountFriendMatch(account.username, account.uid, friend) for friend in matches]
        workers = max(1, min(int(max_workers), len(targets)))
        results: list[AccountFriendMatch] = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    account.friends.find_friends,
                    query,
                    max_friends,
                    force_refresh,
                ): account
                for account in targets
            }
            for future, account in futures.items():
                for friend in future.result():
                    results.append(AccountFriendMatch(account.username, account.uid, friend))
        return self._sort_friend_matches(query, results)

    async def async_find_friends(
        self,
        query: str | int,
        usernames: list[str] | None = None,
        force_refresh: bool = False,
        max_friends: int = 500,
    ) -> list[AccountFriendMatch]:
        """Async equivalent of :meth:`find_friends`."""
        targets = self._target_accounts(usernames)
        if not targets:
            return []
        matches = await asyncio.gather(*(
            account.friends.async_find_friends(query, max_friends, force_refresh)
            for account in targets
        ))
        results = [
            AccountFriendMatch(account.username, account.uid, friend)
            for account, account_matches in zip(targets, matches)
            for friend in account_matches
        ]
        return self._sort_friend_matches(query, results)

    def send_group_text(
        self,
        username: str,
        group_id: int,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        """Send through a specific account's configured group transport."""
        account = self.get_account(username)
        if account is None:
            raise ValueError(f"account is not logged in: {username}")
        return account.group.send_text(
            group_id,
            text,
            ext_content=ext_content,
            timeout=timeout,
        )

    async def async_send_group_text(
        self,
        username: str,
        group_id: int,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        account = self.get_account(username)
        if account is None:
            raise ValueError(f"account is not logged in: {username}")
        return await account.group.async_send_text(
            group_id,
            text,
            ext_content=ext_content,
            timeout=timeout,
        )

    def _target_accounts(self, usernames: list[str] | None) -> list[BmgAccount]:
        with self._lock:
            if usernames is None:
                return list(self._pool)
            return [
                account for name, account in self._by_name.items()
                if any(name.casefold() == requested.casefold() for requested in usernames)
            ]

    @staticmethod
    def _sort_friend_matches(
        query: str | int,
        matches: list[AccountFriendMatch],
    ) -> list[AccountFriendMatch]:
        needle = str(query).strip().casefold()

        def key(match: AccountFriendMatch) -> tuple[int, str, str]:
            name = match.friend.nick_name.casefold()
            rank = 0 if name == needle else 1 if name.startswith(needle) else 2
            return rank, name, match.username

        return sorted(matches, key=key)

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
        self._by_name.clear()

    async def async_close_all(self) -> None:
        for acc in self._pool:
            await acc.async_close()
        self._pool.clear()
        self._by_name.clear()

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