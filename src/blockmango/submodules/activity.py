from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import SignInStatus, TaskInfo


class ActivityAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def sign_in(self) -> dict[str, Any]:
        return self._account.request("POST", "/activity/api/v1/signIn")

    def get_sign_in_status(self) -> SignInStatus | None:
        r = self._account.request("GET", "/activity/api/v1/signIn")
        if r.get("code") == 1:
            return SignInStatus.from_dict(r.get("data"))
        return None

    def get_tasks(self) -> list[TaskInfo]:
        r = self._account.request("GET", "/activity/api/v1/activity/task")
        data = r.get("data") or []
        tasks = [TaskInfo.from_dict(t) for t in data if t]
        return [t for t in tasks if t is not None]

    def claim_task_reward(self, task_id: int) -> dict[str, Any]:
        return self._account.request(
            "PUT", "/activity/api/v1/activity/task/reward", params={"id": task_id})

    async def async_sign_in(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/activity/api/v1/signIn")

    async def async_get_sign_in_status(self) -> SignInStatus | None:
        r = await self._account.async_request("GET", "/activity/api/v1/signIn")
        if r and isinstance(r, dict) and r.get("code") == 1:
            return SignInStatus.from_dict(r.get("data"))
        return None

    async def async_get_tasks(self) -> list[TaskInfo]:
        r = await self._account.async_request("GET", "/activity/api/v1/activity/task")
        data = r.get("data") or []
        tasks = [TaskInfo.from_dict(t) for t in data if t]
        return [t for t in tasks if t is not None]

    async def async_claim_task_reward(self, task_id: int) -> dict[str, Any]:
        return await self._account.async_request(
            "PUT", "/activity/api/v1/activity/task/reward", params={"id": task_id})