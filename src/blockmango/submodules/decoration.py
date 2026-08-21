from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import DecorationItem, Wardrobe


class DecorationAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def get_wardrobe(self, uid: int) -> Wardrobe:
        for path in (
            f"/decoration/api/v1/decorations-v2/users/{uid}/classify/all",
            f"/decoration/api/v1/new/decorations/users/{uid}/classify/all",
        ):
            r = self._account.request("GET", path, language="en_US")
            if r.get("code") == 1:
                return Wardrobe.from_list(r.get("data"))
            if r.get("code") == 3:
                continue
        return Wardrobe()

    def get_current_price(self, skin_id: int, is_suit: bool) -> dict[str, Any]:
        return self._account.request("POST", "/decoration/api/v1/decoration/current/price",
                                     body={"items": [{"id": skin_id, "isSuit": is_suit}]})

    def buy(self, diamond: int, cloth_voucher: int, pay_type: int) -> dict[str, Any]:
        return self._account.request("POST", "/shop/api/v1/new/shop/decorations/buy",
                                     params={"diamond": diamond, "gold": 0, "clothVoucher": cloth_voucher, "payType": pay_type})

    def get_shop_info(self) -> dict[str, Any]:
        r = self._account.request("GET", "/user/api/v1/user/shop/info")
        return r.get("data") or {}

    def equip(self, skin_id: int) -> dict[str, Any]:
        return self._account.request("POST", "/decoration/api/v1/decorations/using/new", params={"ids": skin_id})

    def get_skins(self, uid: int, engine_version: str = "10105") -> list[DecorationItem]:
        params = {"engineVersion": engine_version, "os": "android", "showVip": 1}
        r = self._account.request("GET", f"/decoration/api/v1/new/decorations/users/{uid}/classify/all", params=params)
        if r.get("code") == 1:
            items = [DecorationItem.from_dict(d) for d in (r.get("data") or []) if d]
            return [item for item in items if item is not None]
        return []

    def get_decorations_result(self, uid: int):
        return self._account.get_decorations_result(uid)

    async def async_get_wardrobe(self, uid: int) -> Wardrobe:
        for path in (
            f"/decoration/api/v1/decorations-v2/users/{uid}/classify/all",
            f"/decoration/api/v1/new/decorations/users/{uid}/classify/all",
        ):
            r = await self._account.async_request("GET", path, language="en_US")
            if r.get("code") == 1:
                return Wardrobe.from_list(r.get("data"))
            if r.get("code") == 3:
                continue
        return Wardrobe()

    async def async_get_current_price(self, skin_id: int, is_suit: bool) -> dict[str, Any]:
        return await self._account.async_request("POST", "/decoration/api/v1/decoration/current/price",
                                                 body={"items": [{"id": skin_id, "isSuit": is_suit}]})

    async def async_buy(self, diamond: int, cloth_voucher: int, pay_type: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/shop/api/v1/new/shop/decorations/buy",
                                                 params={"diamond": diamond, "gold": 0, "clothVoucher": cloth_voucher, "payType": pay_type})

    async def async_get_shop_info(self) -> dict[str, Any]:
        r = await self._account.async_request("GET", "/user/api/v1/user/shop/info")
        return r.get("data") or {}

    async def async_equip(self, skin_id: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/decoration/api/v1/decorations/using/new", params={"ids": skin_id})

    async def async_get_skins(self, uid: int, engine_version: str = "10105") -> list[DecorationItem]:
        params = {"engineVersion": engine_version, "os": "android", "showVip": 1}
        r = await self._account.async_request("GET", f"/decoration/api/v1/new/decorations/users/{uid}/classify/all", params=params)
        if r.get("code") == 1:
            items = [DecorationItem.from_dict(d) for d in (r.get("data") or []) if d]
            return [item for item in items if item is not None]
        return []

    async def async_get_decorations_result(self, uid: int):
        return await self._account.async_get_decorations_result(uid)