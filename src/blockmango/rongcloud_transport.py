from __future__ import annotations

import asyncio
import json
import os
import random
import ssl
import struct
import time
from collections.abc import Callable, Iterable, Mapping
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

import requests

from .transport import GroupMessageResult

if TYPE_CHECKING:
    from .account import BmgAccount


DEFAULT_RONG_APP_KEY = "y745wfm8yg89v"
DEFAULT_SDK_VERSION = "2.5.3"
NAVI_CALLBACK = "getServerEndpoint"


class RongCloudTransportError(RuntimeError):
    """RongCloud transport could not authenticate or publish a message."""

    def __init__(self, message: str, *, code: str | None = None, group_id: str | None = None):
        super().__init__(message)
        self.code = code
        self.group_id = group_id


class RongCloudTransport:
    """Pure-Python RongCloud group sender.

    This transport obtains the RongCloud token and device identity from a
    logged-in :class:`~blockmango.BmgAccount`, resolves the RongCloud WebSocket
    endpoint through the token's navi host, and publishes a group text message
    with the RongCloud RMTP wire format.

    No Android device, emulator, Frida, or local Blockman app is required.
    """

    __slots__ = (
        "_account", "app_key", "device_id", "token", "timeout", "verify_ssl",
        "sdk_version", "_uid", "_listener",
    )

    def __init__(
        self,
        account: "BmgAccount",
        *,
        app_key: str | None = None,
        token: str | None = None,
        device_id: str | None = None,
        timeout: float = 15.0,
        verify_ssl: bool = True,
        sdk_version: str = DEFAULT_SDK_VERSION,
    ):
        self._account = account
        self.app_key = app_key or os.getenv("BMG_RONG_APP_KEY") or DEFAULT_RONG_APP_KEY
        self.device_id = device_id
        self.token = token
        self.timeout = max(1.0, float(timeout))
        self.verify_ssl = bool(verify_ssl)
        self.sdk_version = sdk_version
        self._uid = str(getattr(account, "uid", "") or "")
        self._listener: Any = None

    def send_text(
        self,
        group_id: str,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        target = _validate_group(group_id)
        message = str(text)
        if not message.strip():
            raise ValueError("text must not be empty")
        if len(message.encode("utf-8")) > 10_240:
            raise ValueError("text exceeds Blockman/RongCloud's 10 KiB limit")

        listener = self._listener
        if listener is not None and listener.is_running:
            return listener.send_text(
                target,
                message,
                ext_content=ext_content,
                timeout=timeout,
            )

        token = self._resolve_token()
        device_id = self._resolve_device_id()
        uid = self._resolve_uid()
        server = self._resolve_server(token)
        url = self._websocket_url(server, token, device_id, uid)

        try:
            import websocket
        except ImportError as exc:
            raise RongCloudTransportError(
                "RongCloudTransport requires websocket-client; "
                "install bmgo-wrapper"
            ) from exc

        sslopt: dict[str, Any] = {}
        if not self.verify_ssl:
            sslopt = {"cert_reqs": ssl.CERT_NONE, "check_hostname": False}

        ws = None
        try:
            ws = websocket.create_connection(
                url,
                timeout=self.timeout,
                sslopt=sslopt or None,
            )
            ws.settimeout(max(1.0, float(timeout or self.timeout)))
            self._expect_connack(ws)
            message_id = random.randint(1, 65535)
            ws.send_binary(_publish_frame(target, message, message_id, ext_content))
            return self._wait_for_puback(ws, target, message_id, timeout)
        except RongCloudTransportError:
            raise
        except Exception as exc:
            raise RongCloudTransportError(
                f"RongCloud WebSocket send failed: {exc}",
                group_id=target,
            ) from exc
        finally:
            if ws is not None:
                try:
                    ws.close()
                except Exception:
                    pass

    async def async_send_text(
        self,
        group_id: str,
        text: str,
        *,
        ext_content: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> GroupMessageResult:
        return await asyncio.to_thread(
            self.send_text,
            group_id,
            text,
            ext_content=ext_content,
            timeout=timeout,
        )

    def listen(
        self,
        callback: Callable[..., Any],
        *,
        group_ids: int | str | Iterable[int | str] | None = None,
        include_self: bool = True,
        backlog: bool = False,
        poll_interval: float = 1.0,
    ) -> Any:
        """Start receiving incoming group messages for this account.

        A listener owns the account's RongCloud session. ``send_text`` on this
        transport uses that same connection while it is running.
        """
        from .rongcloud_listener import GroupMessageSubscription, RongCloudListener

        listener = self._listener
        if listener is not None and listener.is_running:
            raise RuntimeError("a RongCloud listener is already running for this account")
        listener = RongCloudListener(
            self,
            callback,
            group_ids=group_ids,
            include_self=include_self,
            backlog=backlog,
            timeout=self.timeout,
            poll_interval=poll_interval,
        )
        self._listener = listener
        listener.start()
        return GroupMessageSubscription(listener)

    def stop_listening(self, timeout: float | None = 5.0) -> None:
        listener = self._listener
        self._listener = None
        if listener is not None:
            listener.stop(timeout)

    def _resolve_token(self) -> str:
        if self.token:
            return self.token.strip()
        token = self._account.rongcloud.get_raw_token()
        if not token:
            raise RongCloudTransportError(
                "could not obtain a RongCloud token from the account; "
                "log in first or pass token=..."
            )
        self.token = token
        return token

    def _resolve_device_id(self) -> str:
        if self.device_id:
            return str(self.device_id)
        account_device = getattr(self._account, "device_id", None)
        config = getattr(self._account, "config", None)
        device = account_device or getattr(config, "device_id", None)
        if not device:
            raise RongCloudTransportError(
                "RongCloud requires the app installation's device ID; "
                "log in with BMG_DEVICE_ID/BMG_BMDDH_ID or pass device_id=..."
            )
        self.device_id = str(device)
        return self.device_id

    def _resolve_uid(self) -> str:
        if not self._uid:
            self._uid = str(getattr(self._account, "uid", "") or "")
        if not self._uid:
            raise RongCloudTransportError("account has no user ID; log in first")
        return self._uid

    def _resolve_server(self, token: str) -> str:
        navi_host = _navi_host(token)
        url = (
            f"https://{navi_host}/navi.js?appId={quote(self.app_key, safe='')}"
            f"&token={quote(token, safe='')}&callBack={NAVI_CALLBACK}"
            f"&v={quote(self.sdk_version, safe='')}&r={int(time.time() * 1000)}"
        )
        try:
            response = requests.get(url, timeout=self.timeout, verify=self.verify_ssl)
            response.raise_for_status()
            payload = _parse_navi(response.text)
        except Exception as exc:
            raise RongCloudTransportError(
                f"RongCloud navi request failed: {exc}"
            ) from exc
        if payload.get("code") not in (200, "200"):
            raise RongCloudTransportError(
                f"RongCloud navi rejected the token: {payload.get('code')}"
            )
        server = payload.get("server")
        if not server:
            raise RongCloudTransportError("RongCloud navi returned no server")
        return str(server)

    def _websocket_url(self, server: str, token: str, device_id: str, uid: str) -> str:
        host = server.strip()
        if host.startswith("ws://") or host.startswith("wss://"):
            base = host.rstrip("/")
        else:
            base = f"wss://{host}"
        params = {
            "appId": self.app_key,
            "token": token,
            "sdkVer": self.sdk_version,
            "apiVer": str(random.randint(0, 999999)),
            "deviceId": device_id,
            "clientId": uid,
            "platform": "android",
        }
        query = "&".join(f"{key}={quote(str(value), safe='')}" for key, value in params.items())
        return f"{base}/websocket?{query}"

    def _expect_connack(self, ws: Any) -> None:
        try:
            raw = ws.recv()
        except Exception as exc:
            raise RongCloudTransportError(f"RongCloud connect failed: {exc}") from exc
        data = _as_bytes(raw)
        if not data:
            raise RongCloudTransportError("RongCloud closed the connection before ConnAck")
        if _message_type(data) != 2:
            raise RongCloudTransportError(
                f"expected RongCloud ConnAck, got type {_message_type(data)}"
            )
        if len(data) < 3:
            raise RongCloudTransportError("malformed RongCloud ConnAck")
        status = data[2]
        if status != 0:
            raise RongCloudTransportError(
                f"RongCloud rejected the session (status {status})",
                code=str(status),
            )

    def _wait_for_puback(
        self,
        ws: Any,
        group_id: str,
        message_id: int,
        timeout: float,
    ) -> GroupMessageResult:
        deadline = time.monotonic() + max(1.0, float(timeout or self.timeout))
        while time.monotonic() < deadline:
            try:
                raw = ws.recv()
            except Exception as exc:
                raise RongCloudTransportError(
                    f"RongCloud closed the connection before PubAck: {exc}",
                    group_id=group_id,
                    code="CONNECTION_CLOSED",
                ) from exc
            data = _as_bytes(raw)
            if not data:
                continue
            kind = _message_type(data)
            if kind == 4:
                ack_id, status, timestamp, message_uid = _parse_puback(data)
                if ack_id != message_id:
                    continue
                if status not in (0, None):
                    raise RongCloudTransportError(
                        f"RongCloud rejected the group message (status {status})",
                        code=str(status),
                        group_id=group_id,
                    )
                return GroupMessageResult(
                    group_id=group_id,
                    message_uid=message_uid,
                    timestamp=timestamp,
                    raw={
                        "transport": "rongcloud",
                        "topic": "pgMsgP",
                        "message_id": message_id,
                        "status": status,
                    },
                )
            if kind == 14:
                raise RongCloudTransportError(
                    "RongCloud disconnected the session",
                    code="DISCONNECTED",
                    group_id=group_id,
                )
            # Ignore unrelated server traffic (for example PingResp).
        raise RongCloudTransportError(
            "timed out waiting for RongCloud PubAck",
            code="TIMEOUT",
            group_id=group_id,
        )


def _validate_group(group_id: str | int) -> str:
    target = str(group_id).strip()
    if not target.isdigit() or int(target) <= 0:
        raise ValueError("group_id must be a positive numeric group ID")
    return target


def _navi_host(token: str) -> str:
    if "@" in token:
        hosts = token.split("@", 1)[1]
        host = hosts.split(";", 1)[0].strip()
        if host:
            return host
    return "nav.cn.ronghub.com"


def _parse_navi(text: str) -> dict[str, Any]:
    body = text.strip()
    marker = NAVI_CALLBACK + "("
    start = body.find(marker)
    end = body.rfind(")")
    if start >= 0 and end > start:
        body = body[start + len(marker):end]
    data = json.loads(body)
    if not isinstance(data, dict):
        raise ValueError("navi response is not an object")
    return data


def _message_type(data: bytes) -> int:
    return (data[0] >> 4) & 15


def _as_bytes(raw: Any) -> bytes:
    if isinstance(raw, bytes):
        return raw
    if isinstance(raw, bytearray):
        return bytes(raw)
    if isinstance(raw, str):
        return raw.encode("latin-1", "ignore")
    return bytes(raw)


def _utf(value: str) -> bytes:
    encoded = value.encode("utf-8")
    if len(encoded) > 65535:
        raise ValueError("RongCloud UTF field is too long")
    return struct.pack(">H", len(encoded)) + encoded


def _varint(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def _field(number: int, wire_type: int, payload: bytes) -> bytes:
    return _varint((number << 3) | wire_type) + payload


def _field_string(number: int, value: str) -> bytes:
    encoded = value.encode("utf-8")
    return _field(number, 2, _varint(len(encoded)) + encoded)


def _field_int(number: int, value: int) -> bytes:
    return _field(number, 0, _varint(value))


def _publish_frame(
    group_id: str,
    text: str,
    message_id: int,
    ext_content: Mapping[str, str] | None = None,
) -> bytes:
    content: dict[str, str] = {"content": text}
    if ext_content:
        content["extra"] = json.dumps(dict(ext_content), separators=(",", ":"), ensure_ascii=False)
    encoded_content = json.dumps(
        content,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    upstream = (
        _field_int(1, 3)                       # TextMessage message tag / sessionId
        + _field_string(2, "RC:TxtMsg")        # objectName
        + _field(3, 2, _varint(len(encoded_content)) + encoded_content)
    )
    return (
        bytes([0x32])                         # PUBLISH, QoS 1
        + _utf("pgMsgP")                      # group topic
        + _utf(str(group_id))
        + struct.pack(">H", message_id)
        + upstream
    )


def _parse_puback(data: bytes) -> tuple[int | None, int | None, int | None, str | None]:
    payload = data[1:]
    if len(payload) < 2:
        return None, None, None, None
    message_id = int.from_bytes(payload[:2], "big")
    if len(payload) < 10:
        return message_id, None, None, None
    date = int.from_bytes(payload[2:6], "big")
    status = int.from_bytes(payload[6:8], "big")
    millisecond = int.from_bytes(payload[8:10], "big")
    message_uid = None
    if len(payload) >= 12:
        length = int.from_bytes(payload[10:12], "big")
        if len(payload) >= 12 + length:
            message_uid = payload[12:12 + length].decode("utf-8", "replace")
    return message_id, status, date * 1000 + millisecond, message_uid
