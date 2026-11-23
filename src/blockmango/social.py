from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from .models import GroupInfo, UserProfile

if TYPE_CHECKING:
    from .account import BmgAccount


SocialListener = Callable[["SocialUpdate"], None]


@dataclass(frozen=True, slots=True)
class SocialSnapshot:
    """Immutable friend and group state for one account."""

    groups: tuple[GroupInfo, ...] = ()
    friends: tuple[UserProfile, ...] = ()
    revision: int = 0
    updated_at: float = 0.0

    @property
    def loaded(self) -> bool:
        return self.updated_at > 0.0

    def group(self, group_id: int) -> GroupInfo | None:
        target = int(group_id)
        return next((group for group in self.groups if group.group_id == target), None)

    def friend(self, user_id: int) -> UserProfile | None:
        target = int(user_id)
        return next((friend for friend in self.friends if friend.user_id == target), None)


@dataclass(frozen=True, slots=True)
class SocialUpdate:
    """One social snapshot plus the real additions and removals."""

    snapshot: SocialSnapshot
    groups_added: tuple[GroupInfo, ...] = ()
    groups_removed: tuple[GroupInfo, ...] = ()
    friends_added: tuple[UserProfile, ...] = ()
    friends_removed: tuple[UserProfile, ...] = ()
    initial: bool = False

    @property
    def changed(self) -> bool:
        return bool(
            self.groups_added
            or self.groups_removed
            or self.friends_added
            or self.friends_removed
        )

    @property
    def group_ids_added(self) -> tuple[int, ...]:
        return tuple(group.group_id for group in self.groups_added)

    @property
    def group_ids_removed(self) -> tuple[int, ...]:
        return tuple(group.group_id for group in self.groups_removed)

    @property
    def friend_ids_added(self) -> tuple[int, ...]:
        return tuple(friend.user_id for friend in self.friends_added)

    @property
    def friend_ids_removed(self) -> tuple[int, ...]:
        return tuple(friend.user_id for friend in self.friends_removed)


class SocialSubscription:
    """Handle returned by :meth:`SocialState.subscribe`."""

    __slots__ = ("_state", "_token")

    def __init__(self, state: "SocialState", token: int):
        self._state = state
        self._token = token

    def unsubscribe(self) -> None:
        self._state._unsubscribe_token(self._token)

    def __enter__(self) -> "SocialSubscription":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.unsubscribe()


class SocialState:
    """Friends and groups for an account, with diffing and polling.

    The account login path hydrates this state once and starts a daemon polling
    thread by default. Polling is deliberately cheap and bounded:

    * one thread per account, 60 seconds between checks
    * one cached friend snapshot capped at 500 entries
    * one cached group snapshot capped at 1000 entries
    * callbacks fire only when an entry is actually added or removed

    A caller that manages its own scheduler can use ``refresh()`` and ignore
    ``start()``; a caller using asyncio can use ``async_refresh()`` and
    ``async_start()`` instead.
    """

    def __init__(
        self,
        account: "BmgAccount",
        *,
        max_friends: int = 500,
        max_groups: int = 1000,
        page_size: int = 50,
        emit_initial: bool = False,
    ):
        self._account = account
        self.max_friends = max(0, min(int(max_friends), 500))
        self.max_groups = max(0, min(int(max_groups), 1000))
        self.page_size = max(1, min(int(page_size), 500))
        self.emit_initial = bool(emit_initial)

        self._snapshot = SocialSnapshot()
        self._group_by_id: dict[int, GroupInfo] = {}
        self._friend_by_id: dict[int, UserProfile] = {}
        self._last_update: SocialUpdate | None = None
        self._last_error: BaseException | None = None
        self._lock = threading.RLock()
        self._condition = threading.Condition(self._lock)
        self._refresh_lock = threading.Lock()
        self._listeners: dict[int, SocialListener] = {}
        self._next_listener = 0
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._async_task: asyncio.Task[Any] | None = None
        self._async_stop_event: asyncio.Event | None = None

    @property
    def snapshot(self) -> SocialSnapshot:
        with self._lock:
            return self._snapshot

    @property
    def groups(self) -> tuple[GroupInfo, ...]:
        return self.snapshot.groups

    @property
    def friends(self) -> tuple[UserProfile, ...]:
        return self.snapshot.friends

    @property
    def loaded(self) -> bool:
        return self.snapshot.loaded

    @property
    def revision(self) -> int:
        return self.snapshot.revision

    @property
    def last_update(self) -> SocialUpdate | None:
        with self._lock:
            return self._last_update

    @property
    def last_error(self) -> BaseException | None:
        with self._lock:
            return self._last_error

    @property
    def is_running(self) -> bool:
        with self._lock:
            thread_alive = bool(self._thread and self._thread.is_alive())
            task_alive = bool(self._async_task and not self._async_task.done())
            return thread_alive or task_alive

    def get_group(self, group_id: int) -> GroupInfo | None:
        if not self.loaded:
            self.refresh()
        with self._lock:
            return self._group_by_id.get(int(group_id))

    def get_friend(self, user_id: int) -> UserProfile | None:
        if not self.loaded:
            self.refresh()
        with self._lock:
            return self._friend_by_id.get(int(user_id))

    def find_groups(self, query: str, limit: int = 20) -> list[GroupInfo]:
        """Search the current group snapshot by case-insensitive name."""
        needle = str(query).strip().casefold()
        if not needle:
            return []
        if not self.loaded:
            self.refresh()
        groups = self.groups
        exact = [group for group in groups if group.group_name.casefold() == needle]
        partial = [
            group
            for group in groups
            if group.group_name.casefold() != needle
            and needle in group.group_name.casefold()
        ]
        return (exact + partial)[: max(0, int(limit))]

    def find_friends(self, query: str | int, limit: int = 20) -> list[UserProfile]:
        """Search the current friend snapshot by ID or nickname."""
        text = str(query).strip()
        if not text:
            return []
        if not self.loaded:
            self.refresh()
        friends = self.friends
        if text.isdigit():
            with self._lock:
                exact = self._friend_by_id.get(int(text))
            if exact is not None:
                return [exact]
        needle = text.casefold()
        scored: list[tuple[int, str, UserProfile]] = []
        for friend in friends:
            name = friend.nick_name.casefold()
            if name == needle:
                scored.append((0, name, friend))
            elif name.startswith(needle):
                scored.append((1, name, friend))
            elif needle in name:
                scored.append((2, name, friend))
        scored.sort(key=lambda item: (item[0], item[1]))
        return [item[2] for item in scored[: max(0, int(limit))]]

    def refresh(
        self,
        *,
        max_friends: int | None = None,
        max_groups: int | None = None,
        page_size: int | None = None,
        notify: bool = True,
    ) -> SocialUpdate:
        """Fetch fresh friends and groups, diff them, and emit one update."""
        friend_cap = self.max_friends if max_friends is None else max(0, min(int(max_friends), 500))
        group_cap = self.max_groups if max_groups is None else max(0, min(int(max_groups), 1000))
        size = self.page_size if page_size is None else max(1, min(int(page_size), 500))
        with self._refresh_lock:
            try:
                friends = self._account.friends.list_all_friends(
                    friend_cap,
                    size,
                    force_refresh=True,
                )
                groups = self._account.group.list_all_groups(
                    group_cap,
                    size,
                    force_refresh=True,
                )
            except Exception as exc:
                with self._lock:
                    self._last_error = exc
                raise
            return self._apply(tuple(groups), tuple(friends), notify=notify)

    async def async_refresh(
        self,
        *,
        max_friends: int | None = None,
        max_groups: int | None = None,
        page_size: int | None = None,
        notify: bool = True,
    ) -> SocialUpdate:
        """Async equivalent of :meth:`refresh`."""
        friend_cap = self.max_friends if max_friends is None else max(0, min(int(max_friends), 500))
        group_cap = self.max_groups if max_groups is None else max(0, min(int(max_groups), 1000))
        size = self.page_size if page_size is None else max(1, min(int(page_size), 500))
        with self._refresh_lock:
            try:
                friends, groups = await asyncio.gather(
                    self._account.friends.async_list_all_friends(
                        friend_cap,
                        size,
                        force_refresh=True,
                    ),
                    self._account.group.async_list_all_groups(
                        group_cap,
                        size,
                        force_refresh=True,
                    ),
                )
            except Exception as exc:
                with self._lock:
                    self._last_error = exc
                raise
            return self._apply(tuple(groups), tuple(friends), notify=notify)

    def ensure_loaded(self) -> SocialSnapshot:
        """Return the current snapshot, hydrating it on first use."""
        with self._lock:
            if self._snapshot.loaded:
                return self._snapshot
        return self.refresh().snapshot

    async def async_ensure_loaded(self) -> SocialSnapshot:
        with self._lock:
            if self._snapshot.loaded:
                return self._snapshot
        return (await self.async_refresh()).snapshot

    def subscribe(self, listener: SocialListener) -> SocialSubscription:
        """Register ``listener(update)`` and return an unsubscribe handle."""
        if not callable(listener):
            raise TypeError("listener must be callable")
        with self._lock:
            token = self._next_listener
            self._next_listener += 1
            self._listeners[token] = listener
        return SocialSubscription(self, token)

    # Ergonomic alias.
    on_change = subscribe

    def unsubscribe(self, listener: SocialListener) -> None:
        """Remove a listener previously passed to :meth:`subscribe`."""
        with self._lock:
            token = next(
                (key for key, value in self._listeners.items() if value is listener),
                None,
            )
        if token is not None:
            self._unsubscribe_token(token)

    def _unsubscribe_token(self, token: int) -> None:
        with self._lock:
            self._listeners.pop(token, None)

    def wait_for_update(self, timeout: float | None = None) -> SocialUpdate | None:
        """Block until the next real change or initial hydration.

        Returns ``None`` on timeout. This is useful in scripts and tests that
        prefer a blocking call over callbacks.
        """
        with self._condition:
            start_revision = self._snapshot.revision
            start_updated = self._snapshot.updated_at
            self._condition.wait_for(
                lambda: (
                    self._snapshot.revision,
                    self._snapshot.updated_at,
                )
                != (start_revision, start_updated),
                timeout,
            )
            if (
                self._snapshot.revision,
                self._snapshot.updated_at,
            ) == (start_revision, start_updated):
                return None
            return self._last_update

    def start(self, interval: float = 60.0, *, initial: bool = True) -> None:
        """Start the daemon polling thread. Calling twice is a no-op."""
        interval = max(0.05, float(interval))
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            if self._async_task and not self._async_task.done():
                raise RuntimeError("async social sync is already running")
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._run,
                args=(interval, initial),
                daemon=True,
                name=f"bmg-social-{getattr(self._account, 'uid', 'account')}",
            )
            thread = self._thread
        thread.start()

    def stop(self, timeout: float | None = 5.0) -> None:
        """Stop the polling thread and wait briefly for it to exit."""
        self._stop_event.set()
        with self._lock:
            thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout)
        with self._lock:
            if thread is not None and self._thread is thread and not thread.is_alive():
                self._thread = None

    async def async_start(self, interval: float = 60.0, *, initial: bool = True) -> None:
        """Start async polling in the current event loop."""
        interval = max(0.05, float(interval))
        with self._lock:
            if self._async_task and not self._async_task.done():
                return
            if self._thread and self._thread.is_alive():
                raise RuntimeError("sync social sync is already running")
            self._async_stop_event = asyncio.Event()
            self._async_task = asyncio.create_task(self._async_run(interval, initial))

    async def async_stop(self) -> None:
        """Stop the async polling task."""
        with self._lock:
            event = self._async_stop_event
            task = self._async_task
        if event is not None:
            event.set()
        if task is not None and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            except Exception:
                pass
        with self._lock:
            if self._async_task is task:
                self._async_task = None
            self._async_stop_event = None

    def clear(self) -> None:
        """Forget the snapshot, for example after logging out."""
        with self._lock:
            self._snapshot = SocialSnapshot()
            self._group_by_id.clear()
            self._friend_by_id.clear()
            self._last_update = None
            self._last_error = None
            self._condition.notify_all()

    def _run(self, interval: float, initial: bool) -> None:
        try:
            if initial and not self.loaded:
                try:
                    self.refresh()
                except Exception:
                    pass
            while not self._stop_event.wait(interval):
                try:
                    self.refresh()
                except Exception:
                    # Keep polling; last_error is exposed to the caller.
                    pass
        finally:
            with self._lock:
                if self._thread is threading.current_thread():
                    self._thread = None

    async def _async_run(self, interval: float, initial: bool) -> None:
        try:
            if initial and not self.loaded:
                try:
                    await self.async_refresh()
                except Exception:
                    pass
            while True:
                event = self._async_stop_event
                if event is None:
                    return
                try:
                    await asyncio.wait_for(event.wait(), interval)
                    return
                except asyncio.TimeoutError:
                    pass
                try:
                    await self.async_refresh()
                except Exception:
                    pass
        except asyncio.CancelledError:
            raise
        finally:
            with self._lock:
                if self._async_task is asyncio.current_task():
                    self._async_task = None

    def _apply(
        self,
        groups: tuple[GroupInfo, ...],
        friends: tuple[UserProfile, ...],
        *,
        notify: bool,
    ) -> SocialUpdate:
        now = time.monotonic()
        with self._lock:
            old = self._snapshot
            old_groups = self._group_by_id
            old_friends = self._friend_by_id
            new_groups = {group.group_id: group for group in groups}
            new_friends = {friend.user_id: friend for friend in friends}
            groups_added = tuple(
                group for group_id, group in new_groups.items() if group_id not in old_groups
            )
            groups_removed = tuple(
                group for group_id, group in old_groups.items() if group_id not in new_groups
            )
            friends_added = tuple(
                friend for user_id, friend in new_friends.items() if user_id not in old_friends
            )
            friends_removed = tuple(
                friend for user_id, friend in old_friends.items() if user_id not in new_friends
            )
            changed = bool(groups_added or groups_removed or friends_added or friends_removed)
            initial = not old.loaded
            revision = old.revision + (1 if changed else 0)
            snapshot = SocialSnapshot(
                groups=groups,
                friends=friends,
                revision=revision,
                updated_at=now,
            )
            update = SocialUpdate(
                snapshot=snapshot,
                groups_added=groups_added,
                groups_removed=groups_removed,
                friends_added=friends_added,
                friends_removed=friends_removed,
                initial=initial,
            )
            self._snapshot = snapshot
            self._group_by_id = new_groups
            self._friend_by_id = new_friends
            self._last_update = update
            self._last_error = None
            should_notify = notify and changed and (not initial or self.emit_initial)
            listeners = tuple(self._listeners.values()) if should_notify else ()
            if changed or initial:
                self._condition.notify_all()
        for listener in listeners:
            try:
                listener(update)
            except Exception:
                # A broken observer must not stop polling or other observers.
                pass
        return update

    def __repr__(self) -> str:
        snapshot = self.snapshot
        return (
            f"SocialState(groups={len(snapshot.groups)}, "
            f"friends={len(snapshot.friends)}, revision={snapshot.revision}, "
            f"running={self.is_running})"
        )
