from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class GratitudeAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def list(
        self,
        category_id: int | None = None,
        page: int = 1,
        size: int = 20,
        language: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size}
        if category_id is not None:
            params["categoryId"] = category_id
        return self._account.request(
            "GET", "/user/api/v1/contributor-recognitions", params=params, language=language
        )

    def like(self, target_uid: int) -> dict[str, Any]:
        return self._account.request(
            "POST", "/user/api/v1/contributor-recognitions/likes",
            params={"targetUserId": target_uid},
        )

    def unlike(self, target_uid: int) -> dict[str, Any]:
        return self._account.request(
            "DELETE", "/user/api/v1/contributor-recognitions/likes",
            params={"targetUserId": target_uid},
        )

    async def async_list(
        self,
        category_id: int | None = None,
        page: int = 1,
        size: int = 20,
        language: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size}
        if category_id is not None:
            params["categoryId"] = category_id
        return await self._account.async_request(
            "GET", "/user/api/v1/contributor-recognitions", params=params, language=language
        )

    async def async_like(self, target_uid: int) -> dict[str, Any]:
        return await self._account.async_request(
            "POST", "/user/api/v1/contributor-recognitions/likes",
            params={"targetUserId": target_uid},
        )

    async def async_unlike(self, target_uid: int) -> dict[str, Any]:
        return await self._account.async_request(
            "DELETE", "/user/api/v1/contributor-recognitions/likes",
            params={"targetUserId": target_uid},
        )
