from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class BedwarAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def get_clan_role_for_users(self, user_ids: str) -> dict[str, Any]:
        return self._account.request("GET", "/bedwar/api/v1/friends/clan/by/userIds",
                                     params={"userIds": user_ids})

    def get_ranking(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/bedwar/api/v1/game/rank",
                                     params={"pageNo": page, "pageSize": size})

    def get_game_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/bedwar/api/v1/game/info")

    def get_match(self, match_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/bedwar/api/v1/game/match",
                                     params={"matchId": match_id})

    def get_recent(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/bedwar/api/v1/game/recent",
                                     params={"pageNo": page, "pageSize": size})

    def get_team(self, team_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/bedwar/api/v1/game/team",
                                     params={"teamId": team_id})

    def like(self) -> dict[str, Any]:
        return self._account.request("POST", "/bedwar/api/v1/game/like")

    def get_season(self) -> dict[str, Any]:
        return self._account.request("GET", "/bedwar/api/v1/game/season")

    def get_achievement(self, user_id: int | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return self._account.request("GET", "/bedwar/api/v1/game/achievement",
                                     params=params)

    def get_match_name(self) -> dict[str, Any]:
        return self._account.request("GET", "/bedwar/api/v1/contest/match-name")

    def get_user_game_date_value(self, user_id: int) -> dict[str, Any]:
        return self._account.request("GET", "/bedwar/api/v1/user/game/date/value/get",
                                     params={"userId": user_id})

    async def async_get_clan_role_for_users(self, user_ids: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/bedwar/api/v1/friends/clan/by/userIds",
                                                  params={"userIds": user_ids})

    async def async_get_ranking(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/bedwar/api/v1/game/rank",
                                                  params={"pageNo": page, "pageSize": size})

    async def async_get_game_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/bedwar/api/v1/game/info")

    async def async_get_match(self, match_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/bedwar/api/v1/game/match",
                                                  params={"matchId": match_id})

    async def async_get_recent(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/bedwar/api/v1/game/recent",
                                                  params={"pageNo": page, "pageSize": size})

    async def async_get_team(self, team_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/bedwar/api/v1/game/team",
                                                  params={"teamId": team_id})

    async def async_like(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/bedwar/api/v1/game/like")

    async def async_get_season(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/bedwar/api/v1/game/season")

    async def async_get_achievement(self, user_id: int | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        return await self._account.async_request("GET", "/bedwar/api/v1/game/achievement",
                                                  params=params)

    async def async_get_match_name(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/bedwar/api/v1/contest/match-name")

    async def async_get_user_game_date_value(self, user_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", "/bedwar/api/v1/user/game/date/value/get",
                                                  params={"userId": user_id})
