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

    def sign_in(self, language: str = "en") -> dict[str, Any]:
        return self._account.request("POST", "/activity/api/v1/signIn", language=language)

    def get_sign_in_status(self, language: str = "en") -> SignInStatus | None:
        r = self._account.request("GET", "/activity/api/v1/signIn", language=language)
        if r.get("code") == 1:
            return SignInStatus.from_dict(r.get("data"))
        return None

    def get_tasks(self, language: str = "en") -> list[TaskInfo]:
        r = self._account.request("GET", "/activity/api/v1/activity/task", language=language)
        data = r.get("data") or []
        tasks = [TaskInfo.from_dict(t) for t in data if t]
        return [t for t in tasks if t is not None]

    def claim_task_reward(self, task_id: int, language: str = "en") -> dict[str, Any]:
        return self._account.request(
            "PUT", "/activity/api/v1/activity/task/reward", params={"id": task_id}, language=language)

    async def async_sign_in(self, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("POST", "/activity/api/v1/signIn", language=language)

    async def async_get_sign_in_status(self, language: str = "en") -> SignInStatus | None:
        r = await self._account.async_request("GET", "/activity/api/v1/signIn", language=language)
        if r and isinstance(r, dict) and r.get("code") == 1:
            return SignInStatus.from_dict(r.get("data"))
        return None

    async def async_get_tasks(self, language: str = "en") -> list[TaskInfo]:
        r = await self._account.async_request("GET", "/activity/api/v1/activity/task", language=language)
        data = r.get("data") or []
        tasks = [TaskInfo.from_dict(t) for t in data if t]
        return [t for t in tasks if t is not None]

    async def async_claim_task_reward(self, task_id: int, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request(
            "PUT", "/activity/api/v1/activity/task/reward", params={"id": task_id}, language=language)

    def get_campaign_list(self, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/worldCup", language=language)

    def place_campaign_bet(self, body: dict[str, Any], language: str = "en") -> dict[str, Any]:
        return self._account.request("POST", "/activity/api/v1/activity/worldCup", body=body, language=language)

    def get_campaign_history(self, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/worldCup/history", language=language)

    def get_campaign_notice(self, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/worldCup/notice", language=language)

    def get_campaign_integral(self, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/worldCup/integral", language=language)

    def get_my_integral_rank(self, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/user/integral/rank", language=language)

    def get_integral_leaderboard(self, page_no: int = 1, page_size: int = 20, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/integral/rank",
                                     params={"pageNo": page_no, "pageSize": page_size}, language=language)

    def get_integral_rewards(self, type_: str = "", language: str = "en") -> dict[str, Any]:
        params = {}
        if type_:
            params["type"] = type_
        return self._account.request("GET", "/activity/api/v1/activity/user/integral/reward",
                                     params=params or None, language=language)

    def claim_integral_reward(self, type_: str = "", decoration_id: int = 0, language: str = "en") -> dict[str, Any]:
        params: dict[str, Any] = {}
        if type_:
            params["type"] = type_
        if decoration_id:
            params["decorationId"] = decoration_id
        return self._account.request("PUT", "/activity/api/v1/activity/user/integral/reward",
                                     params=params or None, language=language)

    def get_rank_reward_info(self, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/activity/user/rank/reward", language=language)

    def get_activity_actions(self, title_type: str = "", language: str = "en") -> dict[str, Any]:
        params = {}
        if title_type:
            params["titleType"] = title_type
        return self._account.request("GET", "/activity/api/v1/activity/action",
                                     params=params or None, language=language)

    def receive_action_reward(self, title_type: str = "", action_id: int = 0, language: str = "en") -> dict[str, Any]:
        params: dict[str, Any] = {}
        if title_type:
            params["titleType"] = title_type
        if action_id:
            params["actionId"] = action_id
        return self._account.request("POST", "/activity/api/v1/receive/reward",
                                     params=params or None, language=language)

    def get_activity_titles(self, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v2/activity/title", language=language)

    def get_treasure_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/treasure/bowl/info")

    def buy_treasure(self) -> dict[str, Any]:
        return self._account.request("POST", "/activity/api/v1/treasure/bowl/buy")

    def get_seven_day_sign_data(self, activity_id: str, language: str = "en") -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/seven/day/sign/data/get",
                                     language=language, _extra_headers={"activityId": activity_id})

    def claim_seven_day_sign_reward(self, card_id: int = 0, activity_id: str = "", language: str = "en") -> dict[str, Any]:
        extra = {}
        if card_id:
            extra["cardId"] = str(card_id)
        if activity_id:
            extra["activityId"] = activity_id
        return self._account.request("POST", "/activity/api/v1/seven/day/sign/reward/receive",
                                     language=language, _extra_headers=extra or None)

    async def async_get_campaign_list(self, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/worldCup", language=language)

    async def async_place_campaign_bet(self, body: dict[str, Any], language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("POST", "/activity/api/v1/activity/worldCup", body=body, language=language)

    async def async_get_campaign_history(self, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/worldCup/history", language=language)

    async def async_get_campaign_notice(self, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/worldCup/notice", language=language)

    async def async_get_campaign_integral(self, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/worldCup/integral", language=language)

    async def async_get_my_integral_rank(self, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/user/integral/rank", language=language)

    async def async_get_integral_leaderboard(self, page_no: int = 1, page_size: int = 20, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/integral/rank",
                                                  params={"pageNo": page_no, "pageSize": page_size}, language=language)

    async def async_get_integral_rewards(self, type_: str = "", language: str = "en") -> dict[str, Any]:
        params = {}
        if type_:
            params["type"] = type_
        return await self._account.async_request("GET", "/activity/api/v1/activity/user/integral/reward",
                                                  params=params or None, language=language)

    async def async_claim_integral_reward(self, type_: str = "", decoration_id: int = 0, language: str = "en") -> dict[str, Any]:
        params: dict[str, Any] = {}
        if type_:
            params["type"] = type_
        if decoration_id:
            params["decorationId"] = decoration_id
        return await self._account.async_request("PUT", "/activity/api/v1/activity/user/integral/reward",
                                                  params=params or None, language=language)

    async def async_get_rank_reward_info(self, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/activity/user/rank/reward", language=language)

    async def async_get_activity_actions(self, title_type: str = "", language: str = "en") -> dict[str, Any]:
        params = {}
        if title_type:
            params["titleType"] = title_type
        return await self._account.async_request("GET", "/activity/api/v1/activity/action",
                                                  params=params or None, language=language)

    async def async_receive_action_reward(self, title_type: str = "", action_id: int = 0, language: str = "en") -> dict[str, Any]:
        params: dict[str, Any] = {}
        if title_type:
            params["titleType"] = title_type
        if action_id:
            params["actionId"] = action_id
        return await self._account.async_request("POST", "/activity/api/v1/receive/reward",
                                                  params=params or None, language=language)

    async def async_get_activity_titles(self, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v2/activity/title", language=language)

    async def async_get_treasure_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/treasure/bowl/info")

    async def async_buy_treasure(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/activity/api/v1/treasure/bowl/buy")

    async def async_get_seven_day_sign_data(self, activity_id: str, language: str = "en") -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/seven/day/sign/data/get",
                                                  language=language, _extra_headers={"activityId": activity_id})

    async def async_claim_seven_day_sign_reward(self, card_id: int = 0, activity_id: str = "", language: str = "en") -> dict[str, Any]:
        extra = {}
        if card_id:
            extra["cardId"] = str(card_id)
        if activity_id:
            extra["activityId"] = activity_id
        return await self._account.async_request("POST", "/activity/api/v1/seven/day/sign/reward/receive",
                                                  language=language, _extra_headers=extra or None)