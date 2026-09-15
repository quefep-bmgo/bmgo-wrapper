from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class BackpackAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def get_backpack(self, version: str, user_id: str) -> dict[str, Any]:
        return self._account.request("GET", f"/backpack/api/{version}/backpack/{user_id}")

    def get_candy_coupon_list(self) -> dict[str, Any]:
        return self._account.request("GET", "/backpack/api/v1/candy-coupon/list")

    def get_candy_coupon_address_list(self) -> dict[str, Any]:
        return self._account.request("GET", "/backpack/api/v1/candy-coupon/address/list")

    def exchange_candy_coupon(self, coupon_id: str, address_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/backpack/api/v1/candy-coupon/exchange",
                                     body={"couponId": coupon_id, "addressId": address_id})

    def open_box_item(self, version: str, item_id: str, count: int = 1) -> dict[str, Any]:
        return self._account.request("POST", f"/backpack/api/{version}/backpack/box/item",
                                     body={"itemId": item_id, "count": count})

    def use_decoration_item(self, version: str, item_id: str) -> dict[str, Any]:
        return self._account.request("POST", f"/backpack/api/{version}/backpack/decoration/item",
                                     body={"itemId": item_id})

    def batch_fetch_item_details(self, item_ids: list[str]) -> dict[str, Any]:
        return self._account.request("POST", "/backpack/item/batch/fetch/details",
                                     body={"itemIds": item_ids})

    def check_duplicate_items(self, item_ids: list[str]) -> dict[str, Any]:
        return self._account.request("POST", "/backpack/repeat/item/check",
                                     body={"itemIds": item_ids})

    async def async_get_backpack(self, version: str, user_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/backpack/api/{version}/backpack/{user_id}")

    async def async_get_candy_coupon_list(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/backpack/api/v1/candy-coupon/list")

    async def async_get_candy_coupon_address_list(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/backpack/api/v1/candy-coupon/address/list")

    async def async_exchange_candy_coupon(self, coupon_id: str, address_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/backpack/api/v1/candy-coupon/exchange",
                                                  body={"couponId": coupon_id, "addressId": address_id})

    async def async_open_box_item(self, version: str, item_id: str, count: int = 1) -> dict[str, Any]:
        return await self._account.async_request("POST", f"/backpack/api/{version}/backpack/box/item",
                                                  body={"itemId": item_id, "count": count})

    async def async_use_decoration_item(self, version: str, item_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", f"/backpack/api/{version}/backpack/decoration/item",
                                                  body={"itemId": item_id})

    async def async_batch_fetch_item_details(self, item_ids: list[str]) -> dict[str, Any]:
        return await self._account.async_request("POST", "/backpack/item/batch/fetch/details",
                                                  body={"itemIds": item_ids})

    async def async_check_duplicate_items(self, item_ids: list[str]) -> dict[str, Any]:
        return await self._account.async_request("POST", "/backpack/repeat/item/check",
                                                  body={"itemIds": item_ids})
