from __future__ import annotations

import threading
import time
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import UserProfile


class FriendsAPI:
    """Friends, requests, tags, and popularity.

    Blockman accounts can have up to 500 friends. The helper methods below use
    one cached, deduplicated snapshot of the friend list instead of repeatedly
    walking the API. This keeps multi-account lookups predictable and avoids
    making a request per name or ID.
    """

    __slots__ = (
        "_account", "_cache", "_cache_at", "_cache_complete", "_cache_limit",
        "_cache_lock", "_cache_ttl", "_fetch_lock", "_index_by_id",
        "_index_by_name",
    )

    def __init__(self, account: BmgAccount):
        self._account = account
        self._cache: list[UserProfile] | None = None
        self._cache_at = 0.0
        self._cache_complete = False
        self._cache_limit = 0
        self._cache_ttl = 300.0
        self._cache_lock = threading.RLock()
        self._fetch_lock = threading.RLock()
        self._index_by_id: dict[int, UserProfile] = {}
        self._index_by_name: dict[str, list[UserProfile]] = {}

    def list_friends(self, page: int = 0, size: int = 50) -> list[UserProfile]:
        """List one page of friends. The Blockman API is zero-based."""
        r = self._account.request("GET", "/friend/api/v1/friends", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("data") or data.get("list") or []
        return [p for p in (UserProfile.from_dict(i) for i in items if i) if p is not None]

    def get_info(self, friend_id: int) -> UserProfile | None:
        r = self._account.request("GET", f"/friend/api/v1/friends/info/id/{friend_id}")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    def send_request(self, friend_id: int, msg: str = "Hello!") -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("POST", "/friend/api/v1/friends",
                                     body={"channel": 1, "friendId": friend_id, "gameId": "", "msg": msg, "type": 1})

    def accept_request(self, friend_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("PUT", f"/friend/api/v1/friends/{friend_id}/agreement",
                                     params={"source": 1, "gameId": "", "channel": 1})

    def reject_request(self, friend_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("DELETE", f"/friend/api/v1/friends/{friend_id}/rejection", params={"source": 1})

    def delete_friend(self, friend_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("DELETE", "/friend/api/v1/friends", params={"friendId": friend_id})

    def set_alias(self, friend_id: int, alias: str) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("POST", f"/friend/api/v1/friends/{friend_id}/alias", params={"alias": alias})

    def get_status(self, uids: list[int]) -> list[dict[str, Any]]:
        r = self._account.request("GET", "/friend/api/v2/friends/status", params={"userId": uids})
        return r.get("data") or []

    def add_popularity(self, friend_id: int) -> dict[str, Any]:
        return self._account.request("POST", "/friend/api/v1/popularity", params={"friendId": friend_id})

    def get_popularity(self, friend_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/friend/api/v1/popularity/{friend_id}")

    def get_requests(self, page: int = 1, size: int = 50) -> list[dict[str, Any]]:
        r = self._account.request("GET", "/friend/api/v1/friends/requests", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        return data.get("data") or data.get("list") or []

    def approve_all_requests(self) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("POST", "/friend/api/v1/friends/requests/approve-all")

    def reject_all_requests(self) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("POST", "/friend/api/v1/friends/requests/reject-all")

    def search(self, query: str, page: int = 1, size: int = 20) -> list[UserProfile]:
        r = self._account.request("GET", f"/friend/api/v1/friends/info/{query}",
                                  params={"fuzzyQuery": 1, "pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("list") or data.get("data") or []
        return [p for p in (UserProfile.from_dict(i) for i in items if i) if p is not None]

    def search_friends(self, query: str) -> list[dict[str, Any]]:
        return self._account.search_friends(query)

    def get_family_list(self, uid: int) -> list[dict[str, Any]]:
        return self._account.get_family_list(uid)

    def get_follow_list(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/friends/follow")

    def get_notice_list(self, notice_type: int | None = None) -> dict[str, Any]:
        path = "/friend/api/v1/friends/notice-list"
        if notice_type is not None:
            path += f"/{notice_type}"
        return self._account.request("GET", path)

    def get_recommendations(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/friends/recommendation")

    def get_new_recommendations(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v2/friends/recommendation/new")

    def get_settings(self, uid: int) -> dict[str, Any]:
        return self._account.request("GET", f"/friend/api/v1/friends/settings/{uid}")

    def get_gaming_status(self, friend_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/friend/api/v1/friends/{friend_id}/gaming")

    def get_friends_game_online(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/get/friends/game/online")

    def get_apply_count(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/friends/apply/num")

    def reject_request_by_id(self, request_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("DELETE", f"/friend/api/v1/friends/requests/{request_id}")

    def remove_alias(self, friend_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("DELETE", f"/friend/api/v1/friends/{friend_id}/alias")

    def get_popularity_list(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/popularity/list")

    def get_popularity_props(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/popularity/props")

    def get_tags(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/tag")

    def get_tags_only(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/tag/only")

    def list_all_friends(
        self,
        max_friends: int = 500,
        page_size: int = 50,
        ttl: float = 300.0,
        force_refresh: bool = False,
    ) -> list[UserProfile]:
        """Return a deduplicated friend snapshot, capped at ``max_friends``.

        The snapshot is cached for ``ttl`` seconds. A cached snapshot is reused
        when it is complete or already covers the requested cap. This is the
        low-resource path for accounts with 500 friends and for multi-account
        searches.
        """
        max_friends = max(0, min(int(max_friends), 500))
        if not max_friends:
            return []
        page_size = max(1, min(int(page_size), 500))
        ttl = max(0.0, float(ttl))
        with self._fetch_lock:
            with self._cache_lock:
                if self._friend_cache_valid(max_friends, ttl, force_refresh):
                    return list(self._cache[:max_friends])  # type: ignore[index]
            friends, complete = self._fetch_friend_pages(max_friends, page_size)
            self._store_friend_cache(friends, max_friends, complete, ttl)
            return list(friends[:max_friends])

    def refresh_friends(self, max_friends: int = 500, page_size: int = 50) -> list[UserProfile]:
        """Force a network refresh and replace the friend snapshot."""
        return self.list_all_friends(max_friends, page_size, force_refresh=True)

    def invalidate_cache(self) -> None:
        """Clear the friend snapshot after a friend-list mutation."""
        with self._cache_lock:
            self._cache = None
            self._cache_at = 0.0
            self._cache_complete = False
            self._cache_limit = 0
            self._index_by_id = {}
            self._index_by_name = {}

    def get_friend(self, friend_id: int, max_friends: int = 500) -> UserProfile | None:
        """Look up a friend by numeric ID from the cached snapshot."""
        self.list_all_friends(max_friends)
        with self._cache_lock:
            return self._index_by_id.get(int(friend_id))

    def find_friends(
        self,
        query: str | int,
        max_friends: int = 500,
        force_refresh: bool = False,
    ) -> list[UserProfile]:
        """Find friends by ID, exact nickname, or case-insensitive substring.

        Results are returned in usefulness order: exact nickname, prefix,
        then substring. Numeric queries are treated as user IDs first.
        """
        text = str(query).strip()
        if not text:
            return []
        friends = self.list_all_friends(max_friends, force_refresh=force_refresh)
        if text.isdigit():
            with self._cache_lock:
                exact = self._index_by_id.get(int(text))
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
        return [item[2] for item in scored]

    def find_friend(
        self,
        query: str | int,
        max_friends: int = 500,
        force_refresh: bool = False,
    ) -> UserProfile | None:
        """Return the best single match for :meth:`find_friends`."""
        matches = self.find_friends(query, max_friends, force_refresh)
        return matches[0] if matches else None

    def _friend_cache_valid(self, max_friends: int, ttl: float, force_refresh: bool) -> bool:
        if force_refresh or self._cache is None:
            return False
        if time.monotonic() - self._cache_at > ttl:
            return False
        return self._cache_complete or self._cache_limit >= max_friends

    def _fetch_friend_pages(self, max_friends: int, page_size: int) -> tuple[list[UserProfile], bool]:
        friends: list[UserProfile] = []
        seen: set[int] = set()
        page = 0
        complete = False
        while len(friends) < max_friends and page < 100:
            items = self.list_friends(page=page, size=page_size)
            if not items:
                complete = True
                break
            self._merge_friend_page(friends, seen, items)
            if len(items) < page_size:
                complete = True
                break
            page += 1
        return friends, complete

    @staticmethod
    def _merge_friend_page(
        friends: list[UserProfile],
        seen: set[int],
        items: Iterable[UserProfile],
    ) -> None:
        for friend in items:
            if friend.user_id in seen:
                continue
            seen.add(friend.user_id)
            friends.append(friend)

    def _store_friend_cache(
        self,
        friends: list[UserProfile],
        max_friends: int,
        complete: bool,
        ttl: float,
    ) -> None:
        index_by_id = {friend.user_id: friend for friend in friends}
        index_by_name: dict[str, list[UserProfile]] = {}
        for friend in friends:
            index_by_name.setdefault(friend.nick_name.casefold(), []).append(friend)
        with self._cache_lock:
            self._cache = list(friends)
            self._cache_at = time.monotonic()
            self._cache_complete = complete
            self._cache_limit = max_friends if complete or len(friends) >= max_friends else len(friends)
            self._cache_ttl = ttl
            self._index_by_id = index_by_id
            self._index_by_name = index_by_name

    async def async_list_all_friends(
        self,
        max_friends: int = 500,
        page_size: int = 50,
        ttl: float = 300.0,
        force_refresh: bool = False,
    ) -> list[UserProfile]:
        """Async equivalent of :meth:`list_all_friends`."""
        max_friends = max(0, min(int(max_friends), 500))
        if not max_friends:
            return []
        page_size = max(1, min(int(page_size), 500))
        ttl = max(0.0, float(ttl))
        with self._cache_lock:
            if self._friend_cache_valid(max_friends, ttl, force_refresh):
                return list(self._cache[:max_friends])  # type: ignore[index]
        friends: list[UserProfile] = []
        seen: set[int] = set()
        complete = False
        page = 0
        while len(friends) < max_friends and page < 100:
            items = await self.async_list_friends(page=page, size=page_size)
            if not items:
                complete = True
                break
            self._merge_friend_page(friends, seen, items)
            if len(items) < page_size:
                complete = True
                break
            page += 1
        self._store_friend_cache(friends, max_friends, complete, ttl)
        return list(friends[:max_friends])

    async def async_find_friends(
        self,
        query: str | int,
        max_friends: int = 500,
        force_refresh: bool = False,
    ) -> list[UserProfile]:
        """Async equivalent of :meth:`find_friends`."""
        text = str(query).strip()
        if not text:
            return []
        friends = await self.async_list_all_friends(max_friends, force_refresh=force_refresh)
        if text.isdigit():
            with self._cache_lock:
                exact = self._index_by_id.get(int(text))
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
        return [item[2] for item in scored]

    async def async_find_friend(
        self,
        query: str | int,
        max_friends: int = 500,
        force_refresh: bool = False,
    ) -> UserProfile | None:
        matches = await self.async_find_friends(query, max_friends, force_refresh)
        return matches[0] if matches else None

    async def async_list_friends(self, page: int = 0, size: int = 50) -> list[UserProfile]:
        """List one page of friends. The Blockman API is zero-based."""
        r = await self._account.async_request("GET", "/friend/api/v1/friends", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("data") or data.get("list") or []
        return [p for p in (UserProfile.from_dict(i) for i in items if i) if p is not None]

    async def async_get_info(self, friend_id: int) -> UserProfile | None:
        r = await self._account.async_request("GET", f"/friend/api/v1/friends/info/id/{friend_id}")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    async def async_send_request(self, friend_id: int, msg: str = "Hello!") -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("POST", "/friend/api/v1/friends",
                                                 body={"channel": 1, "friendId": friend_id, "gameId": "", "msg": msg, "type": 1})

    async def async_accept_request(self, friend_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("PUT", f"/friend/api/v1/friends/{friend_id}/agreement",
                                                 params={"source": 1, "gameId": "", "channel": 1})

    async def async_reject_request(self, friend_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("DELETE", f"/friend/api/v1/friends/{friend_id}/rejection", params={"source": 1})

    async def async_delete_friend(self, friend_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("DELETE", "/friend/api/v1/friends", params={"friendId": friend_id})

    async def async_set_alias(self, friend_id: int, alias: str) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("POST", f"/friend/api/v1/friends/{friend_id}/alias", params={"alias": alias})

    async def async_get_status(self, uids: list[int]) -> list[dict[str, Any]]:
        r = await self._account.async_request("GET", "/friend/api/v2/friends/status", params={"userId": uids})
        return r.get("data") or []

    async def async_add_popularity(self, friend_id: int) -> dict[str, Any]:
        return await self._account.async_add_friend_popularity(friend_id)

    async def async_get_popularity(self, friend_id: int) -> dict[str, Any]:
        return await self._account.async_get_friend_popularity(friend_id)

    async def async_get_requests(self, page: int = 1, size: int = 50) -> list[dict[str, Any]]:
        return await self._account.async_get_friend_requests(page, size)

    async def async_approve_all_requests(self) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_approve_all_friend_requests()

    async def async_reject_all_requests(self) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_reject_all_friend_requests()

    async def async_search(self, query: str, page: int = 1, size: int = 20) -> list[UserProfile]:
        r = await self._account.async_request("GET", f"/friend/api/v1/friends/info/{query}",
                                              params={"fuzzyQuery": 1, "pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("list") or data.get("data") or []
        return [p for p in (UserProfile.from_dict(i) for i in items if i) if p is not None]

    async def async_search_friends(self, query: str) -> list[dict[str, Any]]:
        return await self._account.async_search_friends(query)

    async def async_get_family_list(self, uid: int) -> list[dict[str, Any]]:
        return await self._account.async_get_family_list(uid)

    async def async_get_follow_list(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/friends/follow")

    async def async_get_notice_list(self, notice_type: int | None = None) -> dict[str, Any]:
        path = "/friend/api/v1/friends/notice-list"
        if notice_type is not None:
            path += f"/{notice_type}"
        return await self._account.async_request("GET", path)

    async def async_get_recommendations(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/friends/recommendation")

    async def async_get_new_recommendations(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v2/friends/recommendation/new")

    async def async_get_settings(self, uid: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/friend/api/v1/friends/settings/{uid}")

    async def async_get_gaming_status(self, friend_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/friend/api/v1/friends/{friend_id}/gaming")

    async def async_get_friends_game_online(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/get/friends/game/online")

    async def async_get_apply_count(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/friends/apply/num")

    async def async_reject_request_by_id(self, request_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("DELETE", f"/friend/api/v1/friends/requests/{request_id}")

    async def async_remove_alias(self, friend_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("DELETE", f"/friend/api/v1/friends/{friend_id}/alias")

    async def async_get_popularity_list(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/popularity/list")

    async def async_get_popularity_props(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/popularity/props")

    async def async_get_tags(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/tag")

    async def async_get_tags_only(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/tag/only")
