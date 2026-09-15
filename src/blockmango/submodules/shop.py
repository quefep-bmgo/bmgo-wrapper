from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class ShopAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def list_shop_items(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/new/shop/list",
                                     params={"pageNo": page, "pageSize": size})

    def get_shop_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/new/shop/info")

    def buy_decoration(self, diamond: int, gold: int, cloth_voucher: int, pay_type: int) -> dict[str, Any]:
        return self._account.request("POST", "/shop/api/v1/new/shop/decorations/buy",
                                     params={"diamond": diamond, "gold": gold, "clothVoucher": cloth_voucher, "payType": pay_type})

    def list_shop_decorations(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/shop/decorations/list",
                                     params={"pageNo": page, "pageSize": size})

    def get_shop_banners(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/shop/banners")

    def get_recommended_items(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/shop/recommend")

    def purchase(self, item_id: int, quantity: int = 1, pay_type: int = 0) -> dict[str, Any]:
        return self._account.request("POST", "/shop/api/v1/shop/purchase",
                                     body={"itemId": item_id, "quantity": quantity, "payType": pay_type})

    def get_currency_balance(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/shop/currency/balance")

    def get_vip_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/shop/vip/info")

    def purchase_vip(self, vip_type: int, pay_type: int = 0) -> dict[str, Any]:
        return self._account.request("POST", "/shop/api/v1/shop/vip/purchase",
                                     body={"vipType": vip_type, "payType": pay_type})

    def get_decorations_by_classify(self, classify_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/shop/api/v1/new/shop/decorations/classify/{classify_id}")

    def get_decoration_by_type(self, type_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/shop/api/v1/new/shop/decorations/{type_id}")

    def get_suit_list_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/new/shop/suit/list/info")

    def get_suit_info(self, suit_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/shop/api/v1/new/shop/suit/info/{suit_id}")

    def get_suit_decorations(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/new/shop/suit/decorations")

    def get_recommend_decorations(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/new/shop/recommend-decorations")

    def get_recommend_decorations_alt(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/new/shop/recommend/decorations")

    def get_v2_decorations_by_classify(self, classify_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/shop/api/v1/shop-v2/decorations/classify/{classify_id}")

    def get_v2_decoration_details(self, decoration_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/shop/api/v1/shop-v2/decorations/details/{decoration_id}")

    def get_v2_suit_decorations(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/shop-v2/suit/decorations")

    def get_v2_suit_decorations_by_ids(self, suit_ids: str) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v1/shop-v2/suit/decorations/by/suitIds",
                                     params={"suitIds": suit_ids})

    def get_game_props_shop(self) -> dict[str, Any]:
        return self._account.request("GET", "/shop/api/v2/shop/game/props/new")

    async def async_list_shop_items(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/new/shop/list",
                                                 params={"pageNo": page, "pageSize": size})

    async def async_get_shop_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/new/shop/info")

    async def async_buy_decoration(self, diamond: int, gold: int, cloth_voucher: int, pay_type: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/shop/api/v1/new/shop/decorations/buy",
                                                 params={"diamond": diamond, "gold": gold, "clothVoucher": cloth_voucher, "payType": pay_type})

    async def async_list_shop_decorations(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/shop/decorations/list",
                                                 params={"pageNo": page, "pageSize": size})

    async def async_get_shop_banners(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/shop/banners")

    async def async_get_recommended_items(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/shop/recommend")

    async def async_purchase(self, item_id: int, quantity: int = 1, pay_type: int = 0) -> dict[str, Any]:
        return await self._account.async_request("POST", "/shop/api/v1/shop/purchase",
                                                 body={"itemId": item_id, "quantity": quantity, "payType": pay_type})

    async def async_get_currency_balance(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/shop/currency/balance")

    async def async_get_vip_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/shop/vip/info")

    async def async_purchase_vip(self, vip_type: int, pay_type: int = 0) -> dict[str, Any]:
        return await self._account.async_request("POST", "/shop/api/v1/shop/vip/purchase",
                                                 body={"vipType": vip_type, "payType": pay_type})

    async def async_get_decorations_by_classify(self, classify_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/shop/api/v1/new/shop/decorations/classify/{classify_id}")

    async def async_get_decoration_by_type(self, type_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/shop/api/v1/new/shop/decorations/{type_id}")

    async def async_get_suit_list_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/new/shop/suit/list/info")

    async def async_get_suit_info(self, suit_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/shop/api/v1/new/shop/suit/info/{suit_id}")

    async def async_get_suit_decorations(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/new/shop/suit/decorations")

    async def async_get_recommend_decorations(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/new/shop/recommend-decorations")

    async def async_get_recommend_decorations_alt(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/new/shop/recommend/decorations")

    async def async_get_v2_decorations_by_classify(self, classify_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/shop/api/v1/shop-v2/decorations/classify/{classify_id}")

    async def async_get_v2_decoration_details(self, decoration_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/shop/api/v1/shop-v2/decorations/details/{decoration_id}")

    async def async_get_v2_suit_decorations(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/shop-v2/suit/decorations")

    async def async_get_v2_suit_decorations_by_ids(self, suit_ids: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v1/shop-v2/suit/decorations/by/suitIds",
                                                 params={"suitIds": suit_ids})

    async def async_get_game_props_shop(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/shop/api/v2/shop/game/props/new")
