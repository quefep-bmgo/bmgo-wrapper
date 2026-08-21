from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import GroupInfo


class GroupAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def create(self, member_ids: list[int], cost: int = 0) -> dict[str, Any]:
        return self._account.request("POST", "/msg/api/v2/msg/group/chat",
                                     body={"cost": cost, "currency": 1, "memberIds": member_ids, "userId": self._account.uid})

    def get_info(self, group_id: int) -> GroupInfo | None:
        r = self._account.request("GET", "/msg/api/v1/msg/group/chat/info", params={"groupId": group_id})
        if r.get("code") == 1:
            return GroupInfo.from_dict(r.get("data"))
        return None

    def list_groups(self, page: int = 1, size: int = 50) -> list[GroupInfo]:
        r = self._account.request("GET", "/msg/api/v1/msg/group/chat/list", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("data") or data.get("list") or []
        return [g for g in (GroupInfo.from_dict(i) for i in items if i) if g is not None]

    def rename(self, group_id: int, name: str) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                     body={"groupId": group_id, "groupName": name, "inviterId": self._account.uid})

    def edit(self, group_id: int, name: str, notice: str, invite_status: int, notice_pics: list[str] | None = None) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                     body={"groupId": group_id, "groupName": name, "groupNotice": notice,
                                           "inviteStatus": invite_status, "inviterId": self._account.uid, "noticePic": notice_pics or []})

    def invite(self, group_id: int, member_ids: list[int]) -> dict[str, Any]:
        return self._account.request("POST", "/msg/api/v1/msg/group/chat/invite", params={"groupId": group_id, "memberIds": member_ids})

    def kick(self, group_id: int, member_ids: list[int], group_name: str | None = None) -> dict[str, Any]:
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
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/agreement",
                                     body={"groupId": group_id, "operateId": operate_id, "type": join_type, "userId": self._account.uid})

    def quit(self, group_id: int, group_name: str) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/quit", params={"groupId": group_id, "groupName": group_name})

    def apply(self, group_id: int, msg: str) -> dict[str, Any]:
        return self._account.request("POST", "/msg/api/v1/msg/group/chat/apply", params={"groupId": group_id, "msg": msg})

    def transfer_ownership(self, group_id: int, new_owner_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/transfer",
                                     body={"groupId": group_id, "inviterId": self._account.uid, "userId": new_owner_id})

    def allow_invite(self, group_id: int, group_name: str, invite_status: int) -> dict[str, Any]:
        return self._account.request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                     body={"groupId": group_id, "groupName": group_name, "inviteStatus": invite_status, "inviterId": self._account.uid})

    async def async_create(self, member_ids: list[int], cost: int = 0) -> dict[str, Any]:
        return await self._account.async_request("POST", "/msg/api/v2/msg/group/chat",
                                                 body={"cost": cost, "currency": 1, "memberIds": member_ids, "userId": self._account.uid})

    async def async_get_info(self, group_id: int) -> GroupInfo | None:
        r = await self._account.async_request("GET", "/msg/api/v1/msg/group/chat/info", params={"groupId": group_id})
        if r.get("code") == 1:
            return GroupInfo.from_dict(r.get("data"))
        return None

    async def async_list_groups(self, page: int = 1, size: int = 50) -> list[GroupInfo]:
        r = await self._account.async_request("GET", "/msg/api/v1/msg/group/chat/list", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("data") or data.get("list") or []
        return [g for g in (GroupInfo.from_dict(i) for i in items if i) if g is not None]

    async def async_rename(self, group_id: int, name: str) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                                 body={"groupId": group_id, "groupName": name, "inviterId": self._account.uid})

    async def async_edit(self, group_id: int, name: str, notice: str, invite_status: int, notice_pics: list[str] | None = None) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                                 body={"groupId": group_id, "groupName": name, "groupNotice": notice,
                                                       "inviteStatus": invite_status, "inviterId": self._account.uid, "noticePic": notice_pics or []})

    async def async_invite(self, group_id: int, member_ids: list[int]) -> dict[str, Any]:
        return await self._account.async_request("POST", "/msg/api/v1/msg/group/chat/invite", params={"groupId": group_id, "memberIds": member_ids})

    async def async_kick(self, group_id: int, member_ids: list[int], group_name: str | None = None) -> dict[str, Any]:
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
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/agreement",
                                                 body={"groupId": group_id, "operateId": operate_id, "type": join_type, "userId": self._account.uid})

    async def async_quit(self, group_id: int, group_name: str) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/quit", params={"groupId": group_id, "groupName": group_name})

    async def async_apply(self, group_id: int, msg: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/msg/api/v1/msg/group/chat/apply", params={"groupId": group_id, "msg": msg})

    async def async_transfer_ownership(self, group_id: int, new_owner_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/transfer",
                                                 body={"groupId": group_id, "inviterId": self._account.uid, "userId": new_owner_id})

    async def async_allow_invite(self, group_id: int, group_name: str, invite_status: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/msg/api/v1/msg/group/chat/modify",
                                                 body={"groupId": group_id, "groupName": group_name, "inviteStatus": invite_status, "inviterId": self._account.uid})