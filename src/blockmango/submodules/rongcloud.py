from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import RongCloudToken


class RongCloudAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def get_token(self) -> RongCloudToken | None:
        r = self._account.request("GET", "/user/api/v1/users/device/token")
        data = r.get("data")
        if isinstance(data, str) and "@" in data:
            return RongCloudToken.from_string(data)
        return None

    def get_raw_token(self) -> str | None:
        r = self._account.request("GET", "/user/api/v1/users/device/token")
        data = r.get("data")
        return data if isinstance(data, str) and "@" in data else None

    async def async_get_token(self) -> RongCloudToken | None:
        r = await self._account.async_request("GET", "/user/api/v1/users/device/token")
        data = r.get("data")
        if isinstance(data, str) and "@" in data:
            return RongCloudToken.from_string(data)
        return None

    async def async_get_raw_token(self) -> str | None:
        r = await self._account.async_request("GET", "/user/api/v1/users/device/token")
        data = r.get("data")
        return data if isinstance(data, str) and "@" in data else None