from __future__ import annotations

import threading
import time
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import GroupInfo, GroupMember
from ..rongcloud_listener import GroupMessageSubscription, async_listen as start_async_listener
from ..transport import (
    GroupMessageResult,
    GroupMessageTransport,
    GroupMessagingUnavailable,
)


class GroupAPI:
    """Chat-group discovery, membership, and transport-backed messaging.

    Blockman's HTTP API exposes group metadata and management only. Actual
    group messages are published by RongCloud. :class:`~blockmango.BmgAccount`
    installs a pure-Python RongCloud transport automatically; a standalone
    ``GroupAPI`` must call :meth:`set_transport` first.
    """

    __slots__ = (
        "_account", "_cache", "_cache_at", "_cache_complete", "_cache_limit",
        "_cache_lock", "_cache_ttl", "_fetch_lock", "_transport",
    )

    def __init__(self, account: BmgAccount):
        self._account = account
        self._cache: list[GroupInfo] | None = None
        self._cache_at = 0.0
        self._cache_complete = False
        self._cache_limit = 0
        self._cache_lock = threading.RLock()
        self._cache_ttl = 300.0
        self._fetch_lock = threading.RLock()
        self._transport: GroupMessageTransport | None = None

    def set_transport(self, transport: GroupMessageTransport | None) -> None:
        """Install the backend used by :meth:`send_text`.

        The transport is intentionally injected. It can be a RongCloud SDK
        adapter, a local sidecar, or an application-specific bridge. Passing
        ``None`` disables sending and restores the documented error.
        """
        self._transport = transport

    @property
    def transport(self) -> GroupMessageTransport | None:
        return self._transport

    def list_all_groups(
        self,
        max_groups: int = 1000,
        page_size: int = 50,
        ttl: float = 300.0,
        force_refresh: bool = False,
    ) -> list[GroupInfo]:
        """Return a deduplicated group snapshot, capped at ``max_groups``.

        Group metadata is cached because it changes far less often than chat
        traffic. The cap prevents accidental unbounded pagination on accounts
        with a large number of groups.
        """
        max_groups = max(0, min(int(max_groups), 1000))
        if not max_groups:
            return []
        page_size = max(1, min(int(page_size), 500))
        ttl = max(0.0, float(ttl))
        with self._fetch_lock:
            with self._cache_lock:
                if self._group_cache_valid(max_groups, ttl, force_refresh):
                    return list(self._cache[:max_groups])  # type: ignore[index]
            groups, complete = self._fetch_group_pages(max_groups, page_size)
            self._store_group_cache(groups, max_groups, complete, ttl)
            return list(groups[:max_groups])

    def refresh_groups(self, max_groups: int = 1000, page_size: int = 50) -> list[GroupInfo]:
        return self.list_all_groups(max_groups, page_size, force_refresh=True)

    def invalidate_cache(self) -> None:
        with self._cache_lock:
            self._cache = None
            self._cache_at = 0.0
            self._cache_complete = False
            self._cache_limit = 0

    def find_group(
        self,
        group_id: int | None = None,
        name: str | None = None,
        max_groups: int = 1000,
        force_refresh: bool = False,
    ) -> GroupInfo | None:
        """Find a group by ID or case-insensitive name substring."""
        if group_id is None and not name:
            raise ValueError("provide group_id or name")
        groups = self.list_all_groups(max_groups, force_refresh=force_refresh)
        if group_id is not None:
            gid = int(group_id)
            return next((group for group in groups if group.group_id == gid), None)
        needle = str(name).strip().casefold()
        if not needle:
            return None
        exact = next((g for g in groups if g.group_name.casefold() == needle), None)
        if exact is not None:
            return exact
        return next((g for g in groups if needle in g.group_name.casefold()), None)

    def search_groups(
        self,
        query: str,
        limit: int = 20,
        max_groups: int = 1000,
        force_refresh: bool = False,
    ) -> list[GroupInfo]:
        """Search group names locally after one cached snapshot fetch."""
        needle = str(query).strip().casefold()
        if not needle or limit <= 0:
            return []
        groups = self.list_all_groups(max_groups, force_refresh=force_refresh)
        exact = [g for g in groups if g.group_name.casefold() == needle]
        partial = [g for g in groups if g.group_name.casefold() != needle and needle in g.group_name.casefold()]
        return (exact + partial)[:limit]

    def get_members(self, group_id: int) -> list[GroupMember]:
        """Return the member list embedded in the group-info response."""
        info = self.get_info(group_id)
        return list(info.members) if info is not None else []

    def send_text(
        self,
        group_id: int,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        """Send a text message to a group through the installed transport.

        This method deliberately does not fabricate an HTTP endpoint: group
        chats are RongCloud conversations and require a transport.
        """
        target = str(int(group_id))
        if not target or group_id <= 0:
            raise ValueError("group_id must be a positive integer")
        message = str(text)
        if not message.strip():
            raise ValueError("text must not be empty")
        if len(message.encode("utf-8")) > 10_240:
            raise ValueError("text exceeds Blockman/RongCloud's 10 KiB limit")
        if self._transport is None:
            raise GroupMessagingUnavailable(
                "group messaging requires a transport; call account.group.set_transport(...) "
                "with a RongCloud client adapter"
            )
        return self._transport.send_text(
            target,
            message,
            ext_content=ext_content,
            timeout=timeout,
        )

    async def async_send_text(
        self,
        group_id: int,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        target = str(int(group_id))
        if not target or group_id <= 0:
            raise ValueError("group_id must be a positive integer")
        message = str(text)
        if not message.strip():
            raise ValueError("text must not be empty")
        if len(message.encode("utf-8")) > 10_240:
            raise ValueError("text exceeds Blockman/RongCloud's 10 KiB limit")
        if self._transport is None:
            raise GroupMessagingUnavailable(
                "group messaging requires a transport; call account.group.set_transport(...) "
                "with a RongCloud client adapter"
            )
        return await self._transport.async_send_text(
            target,
            message,
            ext_content=ext_content,
            timeout=timeout,
        )

    def listen(
        self,
        callback,
        *,
        group_ids=None,
        include_self: bool = True,
        backlog: bool = False,
    ) -> GroupMessageSubscription:
        """Start receiving incoming group messages.

        ``callback`` receives a :class:`~blockmango.GroupMessage` for each
        matching message. The listener owns the RongCloud session, so
        ``send_text`` uses the same connection while it is active.
        """
        transport = self._transport
        if transport is None or not hasattr(transport, "listen"):
            raise GroupMessagingUnavailable(
                "the installed transport does not support incoming messages"
            )
        return transport.listen(
            callback,
            group_ids=group_ids,
            include_self=include_self,
            backlog=backlog,
        )

    async def async_listen(
        self,
        callback,
        *,
        group_ids=None,
        include_self: bool = True,
        backlog: bool = False,
    ) -> GroupMessageSubscription:
        """Start a listener whose callback may be async."""
        return start_async_listener(
            self,
            callback,
            group_ids=group_ids,
            include_self=include_self,
            backlog=backlog,
        )

    def stop_listening(self, timeout: float | None = 5.0) -> None:
        transport = self._transport
        if transport is not None and hasattr(transport, "stop_listening"):
            transport.stop_listening(timeout)

    def close(self) -> None:
        """Stop any active message listener."""
        self.stop_listening()

    def _group_cache_valid(self, max_groups: int, ttl: float, force_refresh: bool) -> bool:
        if force_refresh or self._cache is None:
            return False
        if time.monotonic() - self._cache_at > ttl:
            return False
        return self._cache_complete or self._cache_limit >= max_groups

    def _fetch_group_pages(self, max_groups: int, page_size: int) -> tuple[list[GroupInfo], bool]:
        groups: list[GroupInfo] = []
        seen: set[int] = set()
        page = 0
        complete = False
        while len(groups) < max_groups and page < 100:
            items = self.list_groups(page=page, size=page_size)
            if not items:
                complete = True
                break
            for group in items:
                if group.group_id not in seen:
                    seen.add(group.group_id)
                    groups.append(group)
            if len(items) < page_size:
                complete = True
                break
            page += 1
        return groups, complete

    def _store_group_cache(
        self,
        groups: list[GroupInfo],
        max_groups: int,
        complete: bool,
        ttl: float,
    ) -> None:
        with self._cache_lock:
            self._cache = list(groups)
            self._cache_at = time.monotonic()
            self._cache_complete = complete
            self._cache_limit = max_groups if complete or len(groups) >= max_groups else len(groups)
            self._cache_ttl = ttl

    async def async_list_all_groups(
        self,
        max_groups: int = 1000,
        page_size: int = 50,
        ttl: float = 300.0,
        force_refresh: bool = False,
    ) -> list[GroupInfo]:
        max_groups = max(0, min(int(max_groups), 1000))
        if not max_groups:
            return []
        page_size = max(1, min(int(page_size), 500))
        ttl = max(0.0, float(ttl))
        with self._cache_lock:
            if self._group_cache_valid(max_groups, ttl, force_refresh):
                return list(self._cache[:max_groups])  # type: ignore[index]
        groups: list[GroupInfo] = []
        seen: set[int] = set()
        page = 0
        complete = False
        while len(groups) < max_groups and page < 100:
            items = await self.async_list_groups(page=page, size=page_size)
            if not items:
                complete = True
                break
            for group in items:
                if group.group_id not in seen:
                    seen.add(group.group_id)
                    groups.append(group)
            if len(items) < page_size:
                complete = True
                break
            page += 1
        self._store_group_cache(groups, max_groups, complete, ttl)
        return list(groups[:max_groups])

    async def async_find_group(
        self,
        group_id: int | None = None,
        name: str | None = None,
        max_groups: int = 1000,
        force_refresh: bool = False,
    ) -> GroupInfo | None:
        if group_id is None and not name:
            raise ValueError("provide group_id or name")
        groups = await self.async_list_all_groups(max_groups, force_refresh=force_refresh)
        if group_id is not None:
            gid = int(group_id)
            return next((group for group in groups if group.group_id == gid), None)
        needle = str(name).strip().casefold()
        if not needle:
            return None
        exact = next((g for g in groups if g.group_name.casefold() == needle), None)
        if exact is not None:
            return exact
        return next((g for g in groups if needle in g.group_name.casefold()), None)

    async def async_search_groups(
        self,
        query: str,
        limit: int = 20,
        max_groups: int = 1000,
        force_refresh: bool = False,
    ) -> list[GroupInfo]:
        needle = str(query).strip().casefold()
        if not needle or limit <= 0:
            return []
        groups = await self.async_list_all_groups(max_groups, force_refresh=force_refresh)
        exact = [g for g in groups if g.group_name.casefold() == needle]
        partial = [g for g in groups if g.group_name.casefold() != needle and needle in g.group_name.casefold()]
        return (exact + partial)[:limit]

    def create(self, member_ids: list[int], cost: int = 0) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("POST", "/msg/api/v2/msg/group/chat",
                                     body={"cost": cost, "currency": 1, "memberIds": member_ids, "userId": self._account.uid})

    def get_info(self, group_id: int) -> GroupInfo | None:
        r = self._account.request("GET", "/msg/api/v1/msg/group/chat/info", params={"groupId": group_id})
        if r.get("code") == 1:
            return GroupInfo.from_dict(r.get("data"))
        return None

    def list_groups(self, page: int = 0, size: int = 50) -> list[GroupInfo]:
        """List one page of groups. The Blockman API is zero-based."""
        r = self._account.request("GET", "/msg/api/v1/msg/group/chat/list", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("data") or data.get("list") or []
        return [g for g in (GroupInfo.from_dict(i) for i in items if i) if g is not None]

    def rename(self, group_id: int, name: str) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                     body={"groupId": group_id, "groupName": name, "inviterId": self._account.uid})

    def edit(self, group_id: int, name: str, notice: str, invite_status: int, notice_pics: list[str] | None = None) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                     body={"groupId": group_id, "groupName": name, "groupNotice": notice,
                                           "inviteStatus": invite_status, "inviterId": self._account.uid, "noticePic": notice_pics or []})

    def invite(self, group_id: int, member_ids: list[int]) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("POST", "/msg/api/v1/msg/group/chat/invite", params={"groupId": group_id, "memberIds": member_ids})

    def kick(self, group_id: int, member_ids: list[int], group_name: str | None = None) -> dict[str, Any]:
        self.invalidate_cache()
        if not group_name:
            info = self.get_info(group_id)
            group_name = info.group_name if info else ""
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/kickOut",
                                     body={"groupId": group_id, "groupName": group_name, "inviterId": self._account.uid, "memberIds": member_ids})

    def set_admin(self, group_id: int, member_id: int, operation_type: int) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/member",
                                     body={"groupId": group_id, "inviterId": self._account.uid, "memberIds": [member_id], "operationType": operation_type})

    def mute(self, group_id: int, member_id: int, minutes: int) -> dict[str, Any]:
        return self._account.request("POST", "/msg/api/v1/msg/group/chat/forbidden/member",
                                     body={"groupId": group_id, "memberId": member_id, "minutes": minutes})

    def approve_join(self, group_id: int, operate_id: int, join_type: int) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/agreement",
                                     body={"groupId": group_id, "operateId": operate_id, "type": join_type, "userId": self._account.uid})

    def quit(self, group_id: int, group_name: str) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/quit", params={"groupId": group_id, "groupName": group_name})

    def apply(self, group_id: int, msg: str) -> dict[str, Any]:
        return self._account.request("POST", "/msg/api/v1/msg/group/chat/apply", params={"groupId": group_id, "msg": msg})

    def transfer_ownership(self, group_id: int, new_owner_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/transfer",
                                     body={"groupId": group_id, "inviterId": self._account.uid, "userId": new_owner_id})

    def allow_invite(self, group_id: int, group_name: str, invite_status: int) -> dict[str, Any]:
        self.invalidate_cache()
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                     body={"groupId": group_id, "groupName": group_name, "inviteStatus": invite_status, "inviterId": self._account.uid})

    def get_creation_price(self) -> dict[str, Any]:
        return self._account.request("GET", "/msg/api/v1/group/chat/price")

    def get_invite_count(self, group_id: int, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/msg/api/v1/msg/group/chat/invite/count",
                                     params={"groupId": group_id}, language=language)

    def get_join_requests(self) -> dict[str, Any]:
        return self._account.request("GET", "/msg/api/v1/msg/group/chat/request/list")

    def get_vip_group_info(self, group_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/msg/api/v1/vip-group/info", params={"groupId": group_id})

    def approve_all_join_requests(self) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/agreement-all")

    def reject_all_join_requests(self) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/reject-all")

    def recall_message(self, message_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/msg/api/v1/msg/group/chat/recall/message",
                                     params={"messageId": message_id})

    def mute_all_members(self) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/forbidden",
                                     params={"forbiddenStatus": 1})

    def unmute_all_members(self) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/forbidden",
                                     params={"forbiddenStatus": 0})

    def remove_member_ban(self, member_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/remove/forbidden/member",
                                     params={"memberId": member_id})

    def add_member_by_email(self, email: str) -> dict[str, Any]:
        return self._account.request("POST", "/msg/api/v1/msg/group/chat/mail/add",
                                     params={"email": email})

    async def async_create(self, member_ids: list[int], cost: int = 0) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("POST", "/msg/api/v2/msg/group/chat",
                                                 body={"cost": cost, "currency": 1, "memberIds": member_ids, "userId": self._account.uid})

    async def async_get_info(self, group_id: int) -> GroupInfo | None:
        r = await self._account.async_request("GET", "/msg/api/v1/msg/group/chat/info", params={"groupId": group_id})
        if r.get("code") == 1:
            return GroupInfo.from_dict(r.get("data"))
        return None

    async def async_list_groups(self, page: int = 0, size: int = 50) -> list[GroupInfo]:
        """List one page of groups. The Blockman API is zero-based."""
        r = await self._account.async_request("GET", "/msg/api/v1/msg/group/chat/list", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("data") or data.get("list") or []
        return [g for g in (GroupInfo.from_dict(i) for i in items if i) if g is not None]

    async def async_rename(self, group_id: int, name: str) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                                 body={"groupId": group_id, "groupName": name, "inviterId": self._account.uid})

    async def async_edit(self, group_id: int, name: str, notice: str, invite_status: int, notice_pics: list[str] | None = None) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                                 body={"groupId": group_id, "groupName": name, "groupNotice": notice,
                                                       "inviteStatus": invite_status, "inviterId": self._account.uid, "noticePic": notice_pics or []})

    async def async_invite(self, group_id: int, member_ids: list[int]) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("POST", "/msg/api/v1/msg/group/chat/invite", params={"groupId": group_id, "memberIds": member_ids})

    async def async_kick(self, group_id: int, member_ids: list[int], group_name: str | None = None) -> dict[str, Any]:
        self.invalidate_cache()
        if not group_name:
            info = await self.async_get_info(group_id)
            group_name = info.group_name if info else ""
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/kickOut",
                                                 body={"groupId": group_id, "groupName": group_name, "inviterId": self._account.uid, "memberIds": member_ids})

    async def async_set_admin(self, group_id: int, member_id: int, operation_type: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/member",
                                                 body={"groupId": group_id, "inviterId": self._account.uid, "memberIds": [member_id], "operationType": operation_type})

    async def async_mute(self, group_id: int, member_id: int, minutes: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/msg/api/v1/msg/group/chat/forbidden/member",
                                                 body={"groupId": group_id, "memberId": member_id, "minutes": minutes})

    async def async_approve_join(self, group_id: int, operate_id: int, join_type: int) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/agreement",
                                                 body={"groupId": group_id, "operateId": operate_id, "type": join_type, "userId": self._account.uid})

    async def async_quit(self, group_id: int, group_name: str) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/quit", params={"groupId": group_id, "groupName": group_name})

    async def async_apply(self, group_id: int, msg: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/msg/api/v1/msg/group/chat/apply", params={"groupId": group_id, "msg": msg})

    async def async_transfer_ownership(self, group_id: int, new_owner_id: int) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/transfer",
                                                 body={"groupId": group_id, "inviterId": self._account.uid, "userId": new_owner_id})

    async def async_allow_invite(self, group_id: int, group_name: str, invite_status: int) -> dict[str, Any]:
        self.invalidate_cache()
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                                 body={"groupId": group_id, "groupName": group_name, "inviteStatus": invite_status, "inviterId": self._account.uid})

    async def async_get_creation_price(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/msg/api/v1/group/chat/price")

    async def async_get_invite_count(self, group_id: int, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/msg/api/v1/msg/group/chat/invite/count",
                                                  params={"groupId": group_id}, language=language)

    async def async_get_join_requests(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/msg/api/v1/msg/group/chat/request/list")

    async def async_get_vip_group_info(self, group_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/msg/api/v1/vip-group/info", params={"groupId": group_id})

    async def async_approve_all_join_requests(self) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/agreement-all")

    async def async_reject_all_join_requests(self) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/reject-all")

    async def async_recall_message(self, message_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/msg/api/v1/msg/group/chat/recall/message",
                                                 params={"messageId": message_id})

    async def async_mute_all_members(self) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/forbidden",
                                                 params={"forbiddenStatus": 1})

    async def async_unmute_all_members(self) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/forbidden",
                                                 params={"forbiddenStatus": 0})

    async def async_remove_member_ban(self, member_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/remove/forbidden/member",
                                                 params={"memberId": member_id})

    async def async_add_member_by_email(self, email: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/msg/api/v1/msg/group/chat/mail/add",
                                                 params={"email": email})
