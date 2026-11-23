from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


class GroupMessagingUnavailable(RuntimeError):
    """Raised when a group send is attempted without a configured transport.

    Blockman GO's HTTP API manages group membership but does not publish chat
    messages. Group messages are carried by RongCloud, so callers must install
    a transport that can talk to RongCloud (or another compatible backend).
    """


@dataclass(frozen=True, slots=True)
class GroupMessageResult:
    """Normalized result returned by a group message transport."""

    group_id: str
    message_id: str | None = None
    message_uid: str | None = None
    timestamp: int | None = None
    raw: Mapping[str, Any] = field(default_factory=dict)


@runtime_checkable
class GroupMessageTransport(Protocol):
    """Minimal contract for sending one text message to one group.

    Implementations are responsible for authentication, connection lifetime,
    retries, and translating the provider response into a
    :class:`GroupMessageResult`. The wrapper deliberately does not assume a
    particular RongCloud transport (native SDK, sidecar, or bridge).
    """

    def send_text(
        self,
        group_id: str,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        ...

    async def async_send_text(
        self,
        group_id: str,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        ...


class FunctionGroupTransport:
    """Adapter for a plain Python send callable.

    This is the smallest integration point for applications that already have
    a RongCloud client. The callable receives keyword arguments:

    ``group_id``, ``text``, ``ext_content``, ``timeout``
    """

    __slots__ = ("_send", "_async_send")

    def __init__(
        self,
        send: Callable[..., GroupMessageResult | Mapping[str, Any]],
        async_send: Callable[..., Awaitable[GroupMessageResult | Mapping[str, Any]]] | None = None,
    ):
        self._send = send
        self._async_send = async_send

    def send_text(
        self,
        group_id: str,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        result = self._send(
            group_id=group_id,
            text=text,
            ext_content=ext_content,
            timeout=timeout,
        )
        return _coerce_result(group_id, result)

    async def async_send_text(
        self,
        group_id: str,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        if self._async_send is not None:
            result = await self._async_send(
                group_id=group_id,
                text=text,
                ext_content=ext_content,
                timeout=timeout,
            )
        else:
            result = await asyncio.to_thread(
                self._send,
                group_id=group_id,
                text=text,
                ext_content=ext_content,
                timeout=timeout,
            )
        return _coerce_result(group_id, result)


def _coerce_result(
    group_id: str,
    result: GroupMessageResult | Mapping[str, Any],
) -> GroupMessageResult:
    if isinstance(result, GroupMessageResult):
        return result
    if not isinstance(result, Mapping):
        raise TypeError("group transport must return GroupMessageResult or a mapping")
    return GroupMessageResult(
        group_id=group_id,
        message_id=_optional_str(result.get("message_id") or result.get("messageId")),
        message_uid=_optional_str(result.get("message_uid") or result.get("messageUId")),
        timestamp=_optional_int(result.get("timestamp") or result.get("sentTime")),
        raw=dict(result),
    )


def _optional_str(value: Any) -> str | None:
    return None if value in (None, "") else str(value)


def _optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)
