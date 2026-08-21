from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import RankEntry


class RankingAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def get_user_rank(self, uid: int, rank_type: str = "active", rank_kind: str = "overall", is_region: bool = False) -> dict[str, Any]:
        return self._account.request("GET", "/ranking/api/v1/ranking/user/info",
                                     params={"rankType": rank_type, "type": rank_kind, "isRegion": 1 if is_region else 0})

    def get_global_weekly(self, page: int = 1, size: int = 10) -> list[RankEntry]:
        r = self._account.request("GET", "/ranking/api/v1/active/global/weekly/rank", params={"pageNo": page, "pageSize": size})
        data = r.get("data")
        if isinstance(data, dict):
            items = data.get("data") or []
        elif isinstance(data, list):
            items = data
        else:
            items = []
        return [e for e in (RankEntry.from_dict(d) for d in items if d) if e is not None]

    def get_game_ranking(self, game_id: str, period: str = "all", page: int = 1, size: int = 10) -> dict[str, Any]:
        return self._account.get_game_ranking(game_id, period, page, size)

    async def async_get_user_rank(self, uid: int, rank_type: str = "active", rank_kind: str = "overall", is_region: bool = False) -> dict[str, Any]:
        return await self._account.async_request("GET", "/ranking/api/v1/ranking/user/info",
                                                 params={"rankType": rank_type, "type": rank_kind, "isRegion": 1 if is_region else 0})

    async def async_get_global_weekly(self, page: int = 1, size: int = 10) -> list[RankEntry]:
        r = await self._account.async_request("GET", "/ranking/api/v1/active/global/weekly/rank", params={"pageNo": page, "pageSize": size})
        data = r.get("data")
        if isinstance(data, dict):
            items = data.get("data") or []
        elif isinstance(data, list):
            items = data
        else:
            items = []
        return [e for e in (RankEntry.from_dict(d) for d in items if d) if e is not None]

    async def async_get_game_ranking(self, game_id: str, period: str = "all", page: int = 1, size: int = 10) -> dict[str, Any]:
        return await self._account.async_get_game_ranking(game_id, period, page, size)