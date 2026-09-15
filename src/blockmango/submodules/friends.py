from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import UserProfile


class FriendsAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def list_friends(self, page: int = 1, size: int = 50) -> list[UserProfile]:
        r = self._account.request("GET", "/friend/api/v1/friends/status", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("data") or data.get("list") or []
        return [p for p in (UserProfile.from_dict(i) for i in items if i) if p is not None]

    def get_info(self, friend_id: int) -> UserProfile | None:
        r = self._account.request("GET", f"/friend/api/v1/friends/info/id/{friend_id}")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    def send_request(self, friend_id: int, msg: str = "Hello!") -> dict[str, Any]:
        return self._account.request("POST", "/friend/api/v1/friends",
                                     body={"channel": 1, "friendId": friend_id, "gameId": "", "msg": msg, "type": 1})

    def accept_request(self, friend_id: int) -> dict[str, Any]:
        return self._account.request("PUT", f"/friend/api/v1/friends/{friend_id}/agreement",
                                     params={"source": 1, "gameId": "", "channel": 1})

    def reject_request(self, friend_id: int) -> dict[str, Any]:
        return self._account.request("DELETE", f"/friend/api/v1/friends/{friend_id}/rejection", params={"source": 1})

    def delete_friend(self, friend_id: int) -> dict[str, Any]:
        return self._account.request("DELETE", "/friend/api/v1/friends", params={"friendId": friend_id})

    def get_blocklist(self) -> list[UserProfile]:
        r = self._account.request("GET", "/friend/api/v1/friends/black")
        data = r.get("data") or {}
        items = data.get("list") or data.get("data") or []
        return [p for p in (UserProfile.from_dict(i) for i in items if i) if p is not None]

    def block_user(self, friend_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/friend/api/v1/friends/black", params={"friendId": friend_id})

    def unblock_user(self, friend_id: int) -> dict[str, Any]:
        return self._account.request("DELETE", "/friend/api/v1/friends/black", params={"friendId": friend_id})

    def set_alias(self, friend_id: int, alias: str) -> dict[str, Any]:
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
        return self._account.request("POST", "/friend/api/v1/friends/requests/approve-all")

    def reject_all_requests(self) -> dict[str, Any]:
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
        return self._account.request("DELETE", f"/friend/api/v1/friends/requests/{request_id}")

    def remove_alias(self, friend_id: int) -> dict[str, Any]:
        return self._account.request("DELETE", f"/friend/api/v1/friends/{friend_id}/alias")

    def get_popularity_list(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/popularity/list")

    def get_popularity_props(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/popularity/props")

    def get_tags(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/tag")

    def get_tags_only(self) -> dict[str, Any]:
        return self._account.request("GET", "/friend/api/v1/tag/only")

    async def async_list_friends(self, page: int = 1, size: int = 50) -> list[UserProfile]:
        r = await self._account.async_request("GET", "/friend/api/v1/friends/status", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("data") or data.get("list") or []
        return [p for p in (UserProfile.from_dict(i) for i in items if i) if p is not None]

    async def async_get_info(self, friend_id: int) -> UserProfile | None:
        r = await self._account.async_request("GET", f"/friend/api/v1/friends/info/id/{friend_id}")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    async def async_send_request(self, friend_id: int, msg: str = "Hello!") -> dict[str, Any]:
        return await self._account.async_request("POST", "/friend/api/v1/friends",
                                                 body={"channel": 1, "friendId": friend_id, "gameId": "", "msg": msg, "type": 1})

    async def async_accept_request(self, friend_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", f"/friend/api/v1/friends/{friend_id}/agreement",
                                                 params={"source": 1, "gameId": "", "channel": 1})

    async def async_reject_request(self, friend_id: int) -> dict[str, Any]:
        return await self._account.async_request("DELETE", f"/friend/api/v1/friends/{friend_id}/rejection", params={"source": 1})

    async def async_delete_friend(self, friend_id: int) -> dict[str, Any]:
        return await self._account.async_request("DELETE", "/friend/api/v1/friends", params={"friendId": friend_id})

    async def async_get_blocklist(self) -> list[UserProfile]:
        r = await self._account.async_request("GET", "/friend/api/v1/friends/black")
        data = r.get("data") or {}
        items = data.get("list") or data.get("data") or []
        return [p for p in (UserProfile.from_dict(i) for i in items if i) if p is not None]

    async def async_block_user(self, friend_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/friend/api/v1/friends/black", params={"friendId": friend_id})

    async def async_unblock_user(self, friend_id: int) -> dict[str, Any]:
        return await self._account.async_request("DELETE", "/friend/api/v1/friends/black", params={"friendId": friend_id})

    async def async_set_alias(self, friend_id: int, alias: str) -> dict[str, Any]:
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
        return await self._account.async_approve_all_friend_requests()

    async def async_reject_all_requests(self) -> dict[str, Any]:
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
        return await self._account.async_request("DELETE", f"/friend/api/v1/friends/requests/{request_id}")

    async def async_remove_alias(self, friend_id: int) -> dict[str, Any]:
        return await self._account.async_request("DELETE", f"/friend/api/v1/friends/{friend_id}/alias")

    async def async_get_popularity_list(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/popularity/list")

    async def async_get_popularity_props(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/popularity/props")

    async def async_get_tags(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/tag")

    async def async_get_tags_only(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/friend/api/v1/tag/only")