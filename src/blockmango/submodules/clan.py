from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import ClanInfo, ClanMember, ClanRole


class ClanAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def get_own_clan(self) -> ClanInfo | None:
        r = self._account.request("GET", "/clan/api/v1/clan/tribe/base")
        if r.get("code") == 1:
            return ClanInfo.from_dict(r.get("data"))
        return None

    def get_info(self, clan_id: int) -> ClanInfo | None:
        r = self._account.request("GET", "/clan/api/v2/clan/tribe", params={"clanId": clan_id})
        if r.get("code") == 1:
            return ClanInfo.from_dict(r.get("data"))
        return None

    def get_members(self) -> list[ClanMember]:
        r = self._account.request("GET", "/clan/api/v1/clan/tribe/member")
        data = r.get("data") or []
        members = [ClanMember.from_dict(m) for m in data if m]
        return [m for m in members if m is not None]

    def join(self, clan_id: int, msg: str = "") -> dict[str, Any]:
        return self._account.request("POST", "/clan/api/v1/clan/tribe/member", body={"clanId": clan_id, "msg": msg})

    def leave(self, clan_id: int) -> dict[str, Any]:
        return self._account.request("DELETE", "/clan/api/v1/clan/tribe/member", params={"clanId": clan_id})

    def search(self, clan_name: str, page: int = 0, size: int = 20) -> list[ClanInfo]:
        r = self._account.request("GET", "/clan/api/v1/clan/tribe/blurry/info",
                                  params={"clanName": clan_name, "pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("list") or data.get("data") or []
        return [c for c in (ClanInfo.from_dict(i) for i in items if i) if c is not None]

    def invite(self, friend_ids: list[int], msg: str = "") -> dict[str, Any]:
        return self._account.request("POST", "/clan/api/v1/clan/tribe/member/invite", body={"friendIds": friend_ids, "msg": msg})

    def approve_member(self, other_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tribe/member/agreement", params={"otherId": other_id})

    def reject_member(self, other_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tribe/member/rejection", params={"otherId": other_id})

    def mute_member(self, member_id: int, minutes: int) -> dict[str, Any]:
        return self._account.request("POST", "/clan/api/v1/clan/tribe/mute/member", params={"memberId": member_id, "minute": minutes})

    def unmute_member(self, member_id: int) -> dict[str, Any]:
        return self._account.request("DELETE", "/clan/api/v1/clan/tribe/mute/member", params={"memberId": member_id})

    def mute_all(self) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tribe/mute", params={"muteStatus": 1})

    def unmute_all(self) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tribe/mute", params={"muteStatus": 0})

    def remove_members(self, member_ids: list[int]) -> dict[str, Any]:
        return self._account.request("DELETE", "/clan/api/v1/clan/tribe/member/remove/batch", body={"memberIds": member_ids})

    def edit(self, clan_id: int, currency: int = 0, details: str = "", head_pic: str = "", name: str = "", tags: list[str] | None = None) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tribe",
                                     body={"clanId": clan_id, "currency": currency, "details": details, "headPic": head_pic, "name": name, "tags": tags or []})

    def edit_elders(self, type_: int, elder_ids: list[int]) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tribe/members", params={"type": type_, "otherIds": elder_ids})

    def set_verification(self, enabled: bool) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/free/verification", params={"freeVerify": 1 if enabled else 0})

    def buy_decoration(self, decoration_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/decorations/purchase", params={"decorationId": decoration_id})

    def accept_task(self, task_id: int, is_team_task: bool) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tasks/accept", params={"id": task_id, "type": 0 if is_team_task else 1})

    def claim_task(self, task_id: int, is_team_task: bool) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tasks", params={"id": task_id, "type": 0 if is_team_task else 1})

    def get_personal_tasks(self, task_type: int = 1) -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v3/clan/personal/tasks", params={"type": task_type})

    def post_bulletin(self, content: str) -> dict[str, Any]:
        return self._account.request("POST", "/clan/api/v1/clan/tribe/bulletin", body={"content": content})

    def transfer_chief(self, new_chief_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tribe/member", params={"otherId": new_chief_id, "type": 3})

    def create(self, clan_id: int = 0, currency: int = 2, details: str = "", head_pic: str = "", name: str = "", tags: list[str] | None = None) -> dict[str, Any]:
        return self._account.request("POST", "/clan/api/v3/clan/tribe",
                                     body={"clanId": clan_id, "currency": currency, "details": details, "headPic": head_pic, "name": name, "tags": tags or []})

    def dissolve(self, clan_id: int) -> dict[str, Any]:
        return self._account.request("DELETE", "/clan/api/v1/clan/tribe", params={"clanId": clan_id})

    def get_donation_info(self) -> dict[str, Any]:
        r = self._account.request("GET", "/clan/api/v1/clan/tribe/donation")
        return r.get("data") if r.get("code") == 1 else r

    def get_donation_history_page(self, page: int = 0, size: int = 50) -> dict[str, Any]:
        return self._account.request(
            "GET", "/clan/api/v2/clan/tribe/donation/history",
            params={"pageNo": page, "pageSize": size},
        )

    def get_donation_history_all(self, size: int = 50, delay: float = 0.3) -> list[dict[str, Any]]:
        import time as _time
        out: list[dict[str, Any]] = []
        page = 0
        while True:
            r = self.get_donation_history_page(page, size)
            if r.get("code") != 1:
                raise RuntimeError(f"donation history page {page} failed: {r}")
            pd = r.get("data") or {}
            items = pd.get("data") or pd.get("list") or []
            out.extend(items)
            if pd.get("lastPage", True):
                break
            page += 1
            if delay:
                _time.sleep(delay)
        return out

    def get_user_clan_role(self, uid: int) -> ClanRole | None:
        r = self._account.request("GET", "/bedwar/api/v1/friends/clan/by/userIds", params={"userIds": str(uid)})
        if r.get("code") != 1:
            return None
        data = r.get("data")
        if not isinstance(data, list) or not data:
            return None
        role = (data[0] or {}).get("clanRole") or {}
        if role.get("clanId") in (None, "", 0, "0"):
            return None
        return ClanRole.from_dict(role)

    def apply_to_clan(self, clan_id: int, msg: str = "") -> dict[str, Any]:
        return self._account.apply_to_clan(clan_id, msg)

    def leave_clan(self) -> dict[str, Any]:
        return self._account.leave_clan()

    def get_clan_info(self, clan_id: int) -> dict[str, Any] | None:
        return self._account.get_clan_info(clan_id)

    def get_clan_members(self) -> list[dict[str, Any]]:
        return self._account.get_clan_members()

    async def async_get_own_clan(self) -> ClanInfo | None:
        r = await self._account.async_request("GET", "/clan/api/v1/clan/tribe/base")
        if r.get("code") == 1:
            return ClanInfo.from_dict(r.get("data"))
        return None

    async def async_get_info(self, clan_id: int) -> ClanInfo | None:
        r = await self._account.async_request("GET", "/clan/api/v2/clan/tribe", params={"clanId": clan_id})
        if r.get("code") == 1:
            return ClanInfo.from_dict(r.get("data"))
        return None

    async def async_get_members(self) -> list[ClanMember]:
        r = await self._account.async_request("GET", "/clan/api/v1/clan/tribe/member")
        data = r.get("data") or []
        members = [ClanMember.from_dict(m) for m in data if m]
        return [m for m in members if m is not None]

    async def async_join(self, clan_id: int, msg: str = "") -> dict[str, Any]:
        return await self._account.async_request("POST", "/clan/api/v1/clan/tribe/member", body={"clanId": clan_id, "msg": msg})

    async def async_leave(self, clan_id: int) -> dict[str, Any]:
        return await self._account.async_request("DELETE", "/clan/api/v1/clan/tribe/member", params={"clanId": clan_id})

    async def async_search(self, clan_name: str, page: int = 0, size: int = 20) -> list[ClanInfo]:
        r = await self._account.async_request("GET", "/clan/api/v1/clan/tribe/blurry/info",
                                              params={"clanName": clan_name, "pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        items = data.get("list") or data.get("data") or []
        return [c for c in (ClanInfo.from_dict(i) for i in items if i) if c is not None]

    async def async_invite(self, friend_ids: list[int], msg: str = "") -> dict[str, Any]:
        return await self._account.async_request("POST", "/clan/api/v1/clan/tribe/member/invite", body={"friendIds": friend_ids, "msg": msg})

    async def async_approve_member(self, other_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tribe/member/agreement", params={"otherId": other_id})

    async def async_reject_member(self, other_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tribe/member/rejection", params={"otherId": other_id})

    async def async_mute_member(self, member_id: int, minutes: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/clan/api/v1/clan/tribe/mute/member", params={"memberId": member_id, "minute": minutes})

    async def async_unmute_member(self, member_id: int) -> dict[str, Any]:
        return await self._account.async_request("DELETE", "/clan/api/v1/clan/tribe/mute/member", params={"memberId": member_id})

    async def async_mute_all(self) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tribe/mute", params={"muteStatus": 1})

    async def async_unmute_all(self) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tribe/mute", params={"muteStatus": 0})

    async def async_remove_members(self, member_ids: list[int]) -> dict[str, Any]:
        return await self._account.async_request("DELETE", "/clan/api/v1/clan/tribe/member/remove/batch", body={"memberIds": member_ids})

    async def async_edit(self, clan_id: int, currency: int = 0, details: str = "", head_pic: str = "", name: str = "", tags: list[str] | None = None) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tribe",
                                                 body={"clanId": clan_id, "currency": currency, "details": details, "headPic": head_pic, "name": name, "tags": tags or []})

    async def async_edit_elders(self, type_: int, elder_ids: list[int]) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tribe/members", params={"type": type_, "otherIds": elder_ids})

    async def async_set_verification(self, enabled: bool) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/free/verification", params={"freeVerify": 1 if enabled else 0})

    async def async_buy_decoration(self, decoration_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/decorations/purchase", params={"decorationId": decoration_id})

    async def async_accept_task(self, task_id: int, is_team_task: bool) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tasks/accept", params={"id": task_id, "type": 0 if is_team_task else 1})

    async def async_claim_task(self, task_id: int, is_team_task: bool) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tasks", params={"id": task_id, "type": 0 if is_team_task else 1})

    async def async_get_personal_tasks(self, task_type: int = 1) -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v3/clan/personal/tasks", params={"type": task_type})

    async def async_post_bulletin(self, content: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/clan/api/v1/clan/tribe/bulletin", body={"content": content})

    async def async_transfer_chief(self, new_chief_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tribe/member", params={"otherId": new_chief_id, "type": 3})

    async def async_create(self, clan_id: int = 0, currency: int = 2, details: str = "", head_pic: str = "", name: str = "", tags: list[str] | None = None) -> dict[str, Any]:
        return await self._account.async_request("POST", "/clan/api/v3/clan/tribe",
                                                 body={"clanId": clan_id, "currency": currency, "details": details, "headPic": head_pic, "name": name, "tags": tags or []})

    async def async_dissolve(self, clan_id: int) -> dict[str, Any]:
        return await self._account.async_request("DELETE", "/clan/api/v1/clan/tribe", params={"clanId": clan_id})

    async def async_get_donation_info(self) -> dict[str, Any]:
        r = await self._account.async_request("GET", "/clan/api/v1/clan/tribe/donation")
        return r.get("data") if r.get("code") == 1 else r

    async def async_get_donation_history_page(self, page: int = 0, size: int = 50) -> dict[str, Any]:
        return await self._account.async_request(
            "GET", "/clan/api/v2/clan/tribe/donation/history",
            params={"pageNo": page, "pageSize": size},
        )

    async def async_get_donation_history_all(self, size: int = 50, delay: float = 0.3) -> list[dict[str, Any]]:
        import asyncio as _asyncio
        out: list[dict[str, Any]] = []
        page = 0
        while True:
            r = await self.async_get_donation_history_page(page, size)
            if r.get("code") != 1:
                raise RuntimeError(f"donation history page {page} failed: {r}")
            pd = r.get("data") or {}
            items = pd.get("data") or pd.get("list") or []
            out.extend(items)
            if pd.get("lastPage", True):
                break
            page += 1
            if delay:
                await _asyncio.sleep(delay)
        return out

    async def async_get_user_clan_role(self, uid: int) -> ClanRole | None:
        r = await self._account.async_request("GET", "/bedwar/api/v1/friends/clan/by/userIds", params={"userIds": str(uid)})
        if r.get("code") != 1:
            return None
        data = r.get("data")
        if not isinstance(data, list) or not data:
            return None
        role = (data[0] or {}).get("clanRole") or {}
        if role.get("clanId") in (None, "", 0, "0"):
            return None
        return ClanRole.from_dict(role)

    async def async_apply_to_clan(self, clan_id: int, msg: str = "") -> dict[str, Any]:
        return await self._account.async_request("POST", "/clan/api/v1/clan/tribe/member", body={"clanId": clan_id, "msg": msg or "Bot join request"})

    async def async_leave_clan(self) -> dict[str, Any]:
        return await self._account.async_request("DELETE", "/clan/api/v1/clan/tribe/member")

    async def async_get_clan_info(self, clan_id: int) -> dict[str, Any] | None:
        r = await self._account.async_request("GET", "/clan/api/v2/clan/tribe", params={"clanId": clan_id})
        return r.get("data") if r.get("code") == 1 else None

    def get_clan_rank(self, rank_type: str = "weekly", page: int = 0, size: int = 20, rank_key: str = "clanBattle") -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v1/clan/rank", params={
            "type": rank_type, "pageNo": page, "pageSize": size, "rankKey": rank_key,
        }, language="en_US")

    def get_clan_rank_new(self) -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v1/clan/rank/new", language="en_US")

    def get_user_clan_rank(self, rank_type: str = "weekly", rank_key: str = "clanBattle") -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v1/clan/user/rank", params={
            "type": rank_type, "rankKey": rank_key,
        }, language="en_US")

    def get_user_clan_rank_new(self, rank_type: str = "weekly") -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v1/clan/user/rank/new", params={
            "type": rank_type,
        }, language="en_US")

    def get_clan_currency(self) -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v1/clan/tribe/currency", language="en_US")

    def donate(self, currency: int = 0, quantity: int = 0) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v3/clan/tribe/donation", params={
            "currency": currency, "quantity": quantity,
        }, language="en_US")

    def get_bulletin(self) -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v1/clan/tribe/bulletin", language="en_US")

    def get_recommendations(self) -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v1/clan/tribe/recommendation", language="en_US")

    def get_clan_id(self) -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v1/clan/tribe/id", language="en_US")

    def accept_invitation(self, invitation_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tribe/member/agreement/invitation", params={
            "id": invitation_id,
        }, language="en_US")

    def reject_invitation(self, invitation_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/clan/api/v1/clan/tribe/member/rejection/invitation", params={
            "id": invitation_id,
        }, language="en_US")

    def get_member_messages(self) -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v2/clan/tribe/member/message", language="en_US")

    def get_red_point(self) -> dict[str, Any]:
        return self._account.request("GET", "/clan/api/v1/red-point")

    def get_decorations_by_type(self, type_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/clan/api/v1/clan/decorations/{type_id}", language="en_US")

    def report_clan(self) -> dict[str, Any]:
        return self._account.request("POST", "/clan/api/v1/clan/tribe/report", language="en_US")

    async def async_get_clan_rank(self, rank_type: str = "weekly", page: int = 0, size: int = 20, rank_key: str = "clanBattle") -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v1/clan/rank", params={
            "type": rank_type, "pageNo": page, "pageSize": size, "rankKey": rank_key,
        }, language="en_US")

    async def async_get_clan_rank_new(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v1/clan/rank/new", language="en_US")

    async def async_get_user_clan_rank(self, rank_type: str = "weekly", rank_key: str = "clanBattle") -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v1/clan/user/rank", params={
            "type": rank_type, "rankKey": rank_key,
        }, language="en_US")

    async def async_get_user_clan_rank_new(self, rank_type: str = "weekly") -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v1/clan/user/rank/new", params={
            "type": rank_type,
        }, language="en_US")

    async def async_get_clan_currency(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v1/clan/tribe/currency", language="en_US")

    async def async_donate(self, currency: int = 0, quantity: int = 0) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v3/clan/tribe/donation", params={
            "currency": currency, "quantity": quantity,
        }, language="en_US")

    async def async_get_bulletin(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v1/clan/tribe/bulletin", language="en_US")

    async def async_get_recommendations(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v1/clan/tribe/recommendation", language="en_US")

    async def async_get_clan_id(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v1/clan/tribe/id", language="en_US")

    async def async_accept_invitation(self, invitation_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tribe/member/agreement/invitation", params={
            "id": invitation_id,
        }, language="en_US")

    async def async_reject_invitation(self, invitation_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/clan/api/v1/clan/tribe/member/rejection/invitation", params={
            "id": invitation_id,
        }, language="en_US")

    async def async_get_member_messages(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v2/clan/tribe/member/message", language="en_US")

    async def async_get_red_point(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/clan/api/v1/red-point")

    async def async_get_decorations_by_type(self, type_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/clan/api/v1/clan/decorations/{type_id}", language="en_US")

    async def async_report_clan(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/clan/api/v1/clan/tribe/report", language="en_US")

    async def async_get_clan_members(self) -> list[dict[str, Any]]:
        r = await self._account.async_request("GET", "/clan/api/v1/clan/tribe/member")
        return r.get("data") or []