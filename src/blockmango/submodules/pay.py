from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class PayAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def get_pay_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/pay/info")

    def create_payment(self, item_id: str, pay_type: int, amount: int) -> dict[str, Any]:
        return self._account.request("POST", "/pay/api/v1/pay/create",
                                     body={"itemId": item_id, "payType": pay_type, "amount": amount})

    def get_payment_status(self, order_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/pay/status",
                                     params={"orderId": order_id})

    def verify_payment(self, order_id: str, receipt: str) -> dict[str, Any]:
        return self._account.request("POST", "/pay/api/v1/pay/verify",
                                     body={"orderId": order_id, "receipt": receipt})

    def get_order_list(self, page_no: int = 1, page_size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/pay/orders",
                                     params={"pageNo": page_no, "pageSize": page_size})

    def get_payment_receipt(self, order_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/pay/receipt",
                                     params={"orderId": order_id})

    def request_refund(self, order_id: str, reason: str) -> dict[str, Any]:
        return self._account.request("POST", "/pay/api/v1/pay/refund",
                                     body={"orderId": order_id, "reason": reason})

    def get_growth_fund_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/growth/fund/info")

    def get_recharge_recommendations(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/recharge/recommend/gcube-gear")

    def get_subscription_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/sub/info/get")

    def get_user_wealth(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/wealth/user")

    def get_monthly_card_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v2/monthcard/info")

    def receive_monthly_card_reward(self) -> dict[str, Any]:
        return self._account.request("POST", "/pay/api/v2/monthcard/receive")

    def get_vip_gift_products(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/vip/gift/all/product/info")

    def get_gdiamond_exchange_rate(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/pay/gdiamond/cloth-voucher/exchange/rate")

    def exchange_gdiamond(self) -> dict[str, Any]:
        return self._account.request("POST", "/pay/api/v1/pay/gdiamond/cloth-voucher/exchange")

    async def async_get_pay_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/pay/info")

    async def async_create_payment(self, item_id: str, pay_type: int, amount: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/pay/api/v1/pay/create",
                                                  body={"itemId": item_id, "payType": pay_type, "amount": amount})

    async def async_get_payment_status(self, order_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/pay/status",
                                                  params={"orderId": order_id})

    async def async_verify_payment(self, order_id: str, receipt: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/pay/api/v1/pay/verify",
                                                  body={"orderId": order_id, "receipt": receipt})

    async def async_get_order_list(self, page_no: int = 1, page_size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/pay/orders",
                                                  params={"pageNo": page_no, "pageSize": page_size})

    async def async_get_payment_receipt(self, order_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/pay/receipt",
                                                  params={"orderId": order_id})

    async def async_request_refund(self, order_id: str, reason: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/pay/api/v1/pay/refund",
                                                  body={"orderId": order_id, "reason": reason})

    async def async_get_growth_fund_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/growth/fund/info")

    async def async_get_recharge_recommendations(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/recharge/recommend/gcube-gear")

    async def async_get_subscription_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/sub/info/get")

    async def async_get_user_wealth(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/wealth/user")

    async def async_get_monthly_card_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v2/monthcard/info")

    async def async_receive_monthly_card_reward(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/pay/api/v2/monthcard/receive")

    async def async_get_vip_gift_products(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/vip/gift/all/product/info")

    async def async_get_gdiamond_exchange_rate(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/pay/gdiamond/cloth-voucher/exchange/rate")

    async def async_exchange_gdiamond(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/pay/api/v1/pay/gdiamond/cloth-voucher/exchange")
