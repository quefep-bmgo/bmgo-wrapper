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

    def get_campaign_list(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/worldCup")

    def place_campaign_bet(self, body: dict[str, Any]) -> dict[str, Any]:
        return self._account.request("POST", "/activity/api/v1/activity/worldCup", body=body)

    def get_campaign_history(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/worldCup/history")

    def get_campaign_notice(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/worldCup/notice")

    def get_campaign_integral(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/worldCup/integral")

    def get_my_integral_rank(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/user/integral/rank")

    def get_integral_leaderboard(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/integral/rank")

    def get_integral_rewards(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/user/integral/reward")

    def claim_integral_reward(self) -> dict[str, Any]:
        return self._account.request("PUT", "/activity/api/v1/activity/user/integral/reward")

    def get_rank_reward_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/user/rank/reward")

    def get_activity_actions(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/action")

    def receive_action_reward(self) -> dict[str, Any]:
        return self._account.request("POST", "/activity/api/v1/receive/reward")

    def get_activity_titles(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v2/activity/title")

    def get_treasure_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/treasure/bowl/info")

    def buy_treasure(self) -> dict[str, Any]:
        return self._account.request("POST", "/activity/api/v1/treasure/bowl/buy")

    def get_seven_day_sign_data(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/seven/day/sign/data/get")

    def claim_seven_day_sign_reward(self) -> dict[str, Any]:
        return self._account.request("POST", "/activity/api/v1/seven/day/sign/reward/receive")

    async def async_get_campaign_list(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/worldCup")

    async def async_place_campaign_bet(self, body: dict[str, Any]) -> dict[str, Any]:
        return await self._account.async_request("POST", "/activity/api/v1/activity/worldCup", body=body)

    async def async_get_campaign_history(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/worldCup/history")

    async def async_get_campaign_notice(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/worldCup/notice")

    async def async_get_campaign_integral(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/worldCup/integral")

    async def async_get_my_integral_rank(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/user/integral/rank")

    async def async_get_integral_leaderboard(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/integral/rank")

    async def async_get_integral_rewards(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/user/integral/reward")

    async def async_claim_integral_reward(self) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/activity/api/v1/activity/user/integral/reward")

    async def async_get_rank_reward_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/user/rank/reward")

    async def async_get_activity_actions(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/action")

    async def async_receive_action_reward(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/activity/api/v1/receive/reward")

    async def async_get_activity_titles(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v2/activity/title")

    async def async_get_treasure_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/treasure/bowl/info")

    async def async_buy_treasure(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/activity/api/v1/treasure/bowl/buy")

    async def async_get_seven_day_sign_data(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/seven/day/sign/data/get")

    async def async_claim_seven_day_sign_reward(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/activity/api/v1/seven/day/sign/reward/receive")