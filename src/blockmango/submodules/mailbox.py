from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class MailboxAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def list_mail(self, page_no: int = 1, page_size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/mailbox/api/v1/mail",
                                     params={"pageNo": page_no, "pageSize": page_size})

    def get_new_mail_count(self) -> dict[str, Any]:
        return self._account.request("GET", "/mailbox/api/v1/mail/new")

    def claim_attachment(self, mail_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/mailbox/api/v1/mail/attachment",
                                     body={"mailId": mail_id})

    def mark_read(self, mail_ids: list[int]) -> dict[str, Any]:
        return self._account.request("PUT", "/mailbox/api/v1/mail",
                                     body={"ids": mail_ids, "status": 1})

    def delete_mails(self, mail_ids: list[int]) -> dict[str, Any]:
        return self._account.request("PUT", "/mailbox/api/v1/mail",
                                     body={"ids": mail_ids, "status": 2})

    async def async_list_mail(self, page_no: int = 1, page_size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/mailbox/api/v1/mail",
                                                  params={"pageNo": page_no, "pageSize": page_size})

    async def async_get_new_mail_count(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/mailbox/api/v1/mail/new")

    async def async_claim_attachment(self, mail_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/mailbox/api/v1/mail/attachment",
                                                  body={"mailId": mail_id})

    async def async_mark_read(self, mail_ids: list[int]) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/mailbox/api/v1/mail",
                                                  body={"ids": mail_ids, "status": 1})

    async def async_delete_mails(self, mail_ids: list[int]) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/mailbox/api/v1/mail",
                                                  body={"ids": mail_ids, "status": 2})
