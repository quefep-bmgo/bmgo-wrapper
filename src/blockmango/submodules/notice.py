"""Server notice and announcement endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class NoticeAPI:
    """Server notice configuration."""

    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def get_server_notice_config(self) -> dict[str, Any]:
        return self._account.request("GET", "/notice/api/v1/server-notice/config")

    async def async_get_server_notice_config(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/notice/api/v1/server-notice/config")
