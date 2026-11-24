from __future__ import annotations

import asyncio
import inspect
import json
import random
import ssl
import struct
import threading
import time
from collections.abc import Callable, Iterable
from typing import Any

from .models import GroupMessage
from .rongcloud_transport import (
    RongCloudTransport,
    RongCloudTransportError,
    _as_bytes,
    _field_int,
    _message_type,
    _parse_puback,
    _publish_frame,
    _utf,
    _validate_group,
)

GroupMessageCallback = Callable[[GroupMessage], None]


class RongCloudListener:
    """Maintain a RongCloud WebSocket and dispatch incoming group messages.

    RongCloud allows one active IM session per token. A listener therefore owns
    the connection for its account and sends through that same socket. Start it
    with :meth:`RongCloudTransport.listen`; do not run a separate listener and
    sender connection for the same account at the same time.
    """

    __slots__ = (
        "_transport", "_callback", "_group_ids", "_include_self", "_backlog",
        "_timeout", "_poll_interval", "_sync_time", "_min_sent_at", "_query_id",
        "_seen", "_stop", "_thread", "_ws", "_ws_lock", "_send_lock",
        "_connected", "_pending", "_pending_lock", "_last_error", "_last_ping",
    )

    def __init__(
        self,
        transport: RongCloudTransport,
        callback: GroupMessageCallback,
        *,
        group_ids: int | str | Iterable[int | str] | None = None,
        include_self: bool = True,
        backlog: bool = False,
        timeout: float = 15.0,
        poll_interval: float = 1.0,
    ):
        if not callable(callback):
            raise TypeError("callback must be callable")
        self._transport = transport
        self._callback = callback
        self._group_ids = _normalize_group_ids(group_ids)
        self._include_self = bool(include_self)
        self._backlog = bool(backlog)
        self._timeout = max(1.0, float(timeout))
        self._poll_interval = max(0.5, float(poll_interval))
        self._sync_time = 0
        self._min_sent_at = 0 if self._backlog else int(time.time() * 1000)
        self._query_id = 1
        self._seen: set[str] = set()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._ws: Any = None
        self._ws_lock = threading.RLock()
        self._send_lock = threading.Lock()
        self._connected = threading.Event()
        self._pending: dict[int, tuple[threading.Event, dict[str, Any]]] = {}
        self._pending_lock = threading.Lock()
        self._last_error: BaseException | None = None
        self._last_ping = 0.0

    @property
    def is_running(self) -> bool:
        return bool(self._thread and self._thread.is_alive())

    @property
    def is_connected(self) -> bool:
        return self._connected.is_set()

    @property
    def last_error(self) -> BaseException | None:
        with self._ws_lock:
            return self._last_error

    def start(self) -> None:
        if self.is_running:
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run,
            name=f"bmg-rong-listener-{getattr(self._transport, '_uid', 'account')}",
            daemon=True,
        )
        self._thread.start()

    def stop(self, timeout: float | None = 5.0) -> None:
        self._stop.set()
        with self._ws_lock:
            ws = self._ws
        if ws is not None:
            try:
                ws.close()
            except Exception:
                pass
        self._fail_pending("listener stopped")
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout)
        self._connected.clear()

    def join(self, timeout: float | None = None) -> None:
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout)

    def send_text(
        self,
        group_id: str,
        text: str,
        *,
        ext_content: dict[str, str] | None = None,
        timeout: float = 10.0,
    ) -> Any:
        from .transport import GroupMessageResult

        target = _validate_group(group_id)
        message = str(text)
        if not message.strip():
            raise ValueError("text must not be empty")
        if len(message.encode("utf-8")) > 10_240:
            raise ValueError("text exceeds Blockman/RongCloud's 10 KiB limit")
        if not self._connected.wait(max(1.0, float(timeout or self._timeout))):
            raise RongCloudTransportError(
                "RongCloud listener is not connected",
                code="NOT_CONNECTED",
                group_id=target,
            )

        message_id = random.randint(1, 65535)
        event = threading.Event()
        outcome: dict[str, Any] = {}
        with self._pending_lock:
            self._pending[message_id] = (event, outcome)
        try:
            with self._send_lock:
                self._write(_publish_frame(target, message, message_id, ext_content))
            if not event.wait(max(1.0, float(timeout or self._timeout))):
                raise RongCloudTransportError(
                    "timed out waiting for RongCloud PubAck",
                    code="TIMEOUT",
                    group_id=target,
                )
            if outcome.get("event") != "success":
                raise RongCloudTransportError(
                    str(outcome.get("message") or "RongCloud send failed"),
                    code=str(outcome.get("code") or "SEND_FAILED"),
                    group_id=target,
                )
            return GroupMessageResult(
                group_id=target,
                message_uid=outcome.get("message_uid"),
                timestamp=outcome.get("timestamp"),
                raw={
                    "transport": "rongcloud",
                    "topic": "pgMsgP",
                    "message_id": message_id,
                    "status": outcome.get("status"),
                },
            )
        finally:
            with self._pending_lock:
                self._pending.pop(message_id, None)

    def _run(self) -> None:
        backoff = 1.0
        while not self._stop.is_set():
            try:
                self._connect_and_read()
                backoff = 1.0
            except Exception as exc:
                with self._ws_lock:
                    self._last_error = exc
            if self._stop.is_set():
                break
            if self._stop.wait(backoff):
                break
            backoff = min(backoff * 2.0, 30.0)

    def _connect_and_read(self) -> None:
        token = self._transport._resolve_token()
        device_id = self._transport._resolve_device_id()
        uid = self._transport._resolve_uid()
        server = self._transport._resolve_server(token)
        url = self._transport._websocket_url(server, token, device_id, uid)
        try:
            import websocket
        except ImportError as exc:
            raise RongCloudTransportError(
                "RongCloudListener requires websocket-client; install bmgo-wrapper"
            ) from exc

        sslopt: dict[str, Any] = {}
        if not self._transport.verify_ssl:
            sslopt = {"cert_reqs": ssl.CERT_NONE, "check_hostname": False}

        ws = websocket.create_connection(
            url,
            timeout=self._timeout,
            sslopt=sslopt or None,
        )
        try:
            ws.settimeout(1.0)
            self._transport._expect_connack(ws)
            with self._ws_lock:
                self._ws = ws
                self._last_error = None
            self._connected.set()
            self._last_ping = time.monotonic()
            self._send_query(ws, uid)
            last_poll = time.monotonic()
            while not self._stop.is_set():
                now = time.monotonic()
                if now - self._last_ping >= 30.0:
                    self._safe_send(ws, b"\xC0")
                    self._last_ping = now
                if now - last_poll >= self._poll_interval:
                    self._send_query(ws, uid)
                    last_poll = now
                try:
                    raw = ws.recv()
                except Exception as exc:
                    if _is_timeout(exc):
                        continue
                    raise
                data = _as_bytes(raw)
                if not data:
                    continue
                if not self._handle_frame(ws, data):
                    break
        finally:
            self._connected.clear()
            with self._ws_lock:
                if self._ws is ws:
                    self._ws = None
            try:
                ws.close()
            except Exception:
                pass

    def _send_query(self, ws: Any, uid: str) -> None:
        query_id = self._query_id
        self._query_id = 1 if query_id >= 65535 else query_id + 1
        payload = (
            _field_int(1, self._sync_time)
            + _field_int(2, 0)
            + _field_int(3, 1)
            + _field_int(4, 1)
        )
        frame = (
            bytes([0x52])
            + _utf("pullMsg")
            + _utf(uid)
            + struct.pack(">H", query_id)
            + payload
        )
        self._safe_send(ws, frame)

    def _handle_frame(self, ws: Any, data: bytes) -> bool:
        kind = _message_type(data)
        if kind == 3:
            self._handle_publish(ws, data)
        elif kind == 4:
            self._handle_puback(data)
        elif kind == 6:
            self._handle_query_ack(ws, data)
        elif kind == 14:
            return False
        return True

    def _handle_publish(self, ws: Any, data: bytes) -> None:
        try:
            date, topic, target, message_id, payload = _parse_publish(data)
        except Exception as exc:
            with self._ws_lock:
                self._last_error = exc
            return
        self._safe_send(ws, bytes([0x40]) + struct.pack(">H", message_id))
        # ``s_ntf`` and other delivery topics are not group messages.
        if topic not in ("pgMsgP",):
            return
        try:
            if payload[:1] == b"\x0a":
                proto = _decode_downstream(payload)
            else:
                proto = _decode_upstream(payload)
        except Exception as exc:
            with self._ws_lock:
                self._last_error = exc
            return
        message = _to_group_message(proto, topic, target, date, self._transport._uid)
        if message is None:
            return
        if self._group_ids is not None and message.group_id not in self._group_ids:
            return
        if not self._include_self and message.is_self:
            return
        try:
            self._callback(message)
        except Exception as exc:
            with self._ws_lock:
                self._last_error = exc

    def _handle_puback(self, data: bytes) -> None:
        message_id, status, timestamp, message_uid = _parse_puback(data)
        if message_id is None:
            return
        with self._pending_lock:
            pending = self._pending.get(message_id)
        if pending is None:
            return
        event, outcome = pending
        if status not in (0, None):
            outcome.update(event="error", code=str(status), message=f"status {status}")
        else:
            outcome.update(
                event="success",
                status=status,
                timestamp=timestamp,
                message_uid=message_uid,
            )
        event.set()

    def _handle_query_ack(self, ws: Any, data: bytes) -> None:
        message_id = int.from_bytes(data[1:3], "big") if len(data) >= 3 else 1
        self._safe_send(ws, bytes([0x70]) + struct.pack(">H", message_id))
        payload = data[9:] if len(data) > 9 else b""
        try:
            fields = _pb_fields(payload)
        except Exception as exc:
            with self._ws_lock:
                self._last_error = exc
            return
        for raw_message in fields.get(1, []):
            if not isinstance(raw_message, (bytes, bytearray)):
                continue
            try:
                proto = _decode_downstream(bytes(raw_message))
            except Exception:
                continue
            message = _to_group_message(
                proto, "pgMsgP", proto.get("group_id") or "", 0, self._transport._uid
            )
            if message is None:
                continue
            if self._group_ids is not None and message.group_id not in self._group_ids:
                continue
            if not self._include_self and message.is_self:
                continue
            try:
                self._callback(message)
            except Exception as exc:
                with self._ws_lock:
                    self._last_error = exc

    def _write(self, data: bytes) -> None:
        with self._ws_lock:
            ws = self._ws
        if ws is None or not self._connected.is_set():
            raise RongCloudTransportError(
                "RongCloud listener is not connected",
                code="NOT_CONNECTED",
            )
        ws.send_binary(data)

    def _safe_send(self, ws: Any, data: bytes) -> None:
        try:
            ws.send_binary(data)
        except Exception:
            pass

    def _fail_pending(self, message: str) -> None:
        with self._pending_lock:
            pending = list(self._pending.values())
        for event, outcome in pending:
            outcome.update(event="error", code="STOPPED", message=message)
            event.set()


class GroupMessageSubscription:
    """Handle returned by ``account.group.listen``."""

    __slots__ = ("_listener",)

    def __init__(self, listener: RongCloudListener):
        self._listener = listener

    @property
    def is_running(self) -> bool:
        return self._listener.is_running

    @property
    def is_connected(self) -> bool:
        return self._listener.is_connected

    def stop(self, timeout: float | None = 5.0) -> None:
        self._listener.stop(timeout)

    def join(self, timeout: float | None = None) -> None:
        self._listener.join(timeout)

    def __enter__(self) -> "GroupMessageSubscription":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()


def async_listen(
    group_api: Any,
    callback: Callable[[GroupMessage], Any],
    *,
    group_ids: int | str | Iterable[int | str] | None = None,
    include_self: bool = True,
    backlog: bool = False,
    poll_interval: float = 1.0,
) -> GroupMessageSubscription:
    """Start a listener and route messages to an async callback.

    The listener runs in its own daemon thread. Coroutine callbacks are
    scheduled on the current event loop; regular callbacks are invoked inline.
    """
    loop = asyncio.get_running_loop()
    is_coroutine = inspect.iscoroutinefunction(callback)

    def dispatch(message: GroupMessage) -> None:
        if is_coroutine:
            asyncio.run_coroutine_threadsafe(callback(message), loop)
        else:
            callback(message)

    return group_api.listen(
        dispatch,
        group_ids=group_ids,
        include_self=include_self,
        backlog=backlog,
        poll_interval=poll_interval,
    )


def _normalize_group_ids(
    group_ids: int | str | Iterable[int | str] | None,
) -> set[str] | None:
    if group_ids is None:
        return None
    if isinstance(group_ids, (str, int)):
        return {_validate_group(group_ids)}
    return {_validate_group(group_id) for group_id in group_ids}


def _parse_publish(data: bytes) -> tuple[int, str, str, int, bytes]:
    pos = 1
    date = int.from_bytes(data[pos:pos + 4], "big")
    pos += 4
    topic, pos = _read_utf(data, pos)
    target, pos = _read_utf(data, pos)
    message_id = int.from_bytes(data[pos:pos + 2], "big")
    pos += 2
    return date, topic, target, message_id, data[pos:]


def _read_utf(data: bytes, pos: int) -> tuple[str, int]:
    length = int.from_bytes(data[pos:pos + 2], "big")
    pos += 2
    value = data[pos:pos + length].decode("utf-8", "replace")
    return value, pos + length


def _pb_fields(data: bytes) -> dict[int, list[Any]]:
    fields: dict[int, list[Any]] = {}
    pos = 0
    while pos < len(data):
        key, pos = _read_varint(data, pos)
        number = key >> 3
        wire = key & 7
        if wire == 0:
            value, pos = _read_varint(data, pos)
        elif wire == 2:
            length, pos = _read_varint(data, pos)
            value = data[pos:pos + length]
            pos += length
        elif wire == 1:
            value = data[pos:pos + 8]
            pos += 8
        elif wire == 5:
            value = data[pos:pos + 4]
            pos += 4
        else:
            raise ValueError(f"unsupported protobuf wire type {wire}")
        fields.setdefault(number, []).append(value)
    return fields


def _read_varint(data: bytes, pos: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while pos < len(data):
        byte = data[pos]
        pos += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, pos
        shift += 7
    raise ValueError("truncated protobuf varint")


def _first(fields: dict[int, list[Any]], number: int, default: Any = None) -> Any:
    values = fields.get(number)
    return values[0] if values else default


def _decode_downstream(data: bytes) -> dict[str, Any]:
    fields = _pb_fields(data)
    content = _first(fields, 5, b"")
    return {
        "from_user_id": _decode_text(_first(fields, 1, b"")),
        "type": _first(fields, 2, 0),
        "group_id": _decode_text(_first(fields, 3, b"")),
        "classname": _decode_text(_first(fields, 4, b"")),
        "content": bytes(content) if isinstance(content, (bytes, bytearray)) else b"",
        "data_time": _first(fields, 6, 0),
        "status": _first(fields, 7, 0),
        "extra": _first(fields, 8, 0),
        "msg_id": _decode_text(_first(fields, 9, b"")),
        "direction": _first(fields, 10, 0),
    }


def _decode_upstream(data: bytes) -> dict[str, Any]:
    fields = _pb_fields(data)
    content = _first(fields, 3, b"")
    return {
        "session_id": _first(fields, 1, 0),
        "classname": _decode_text(_first(fields, 2, b"")),
        "content": bytes(content) if isinstance(content, (bytes, bytearray)) else b"",
        "push_text": _decode_text(_first(fields, 4, b"")),
        "app_data": _decode_text(_first(fields, 5, b"")),
    }


def _decode_text(value: Any) -> str:
    if isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8", "replace")
    return str(value or "")


def _to_group_message(
    proto: dict[str, Any],
    topic: str,
    target: str,
    date: int,
    uid: str,
) -> GroupMessage | None:
    classname = str(proto.get("classname") or "")
    group_id = str(proto.get("group_id") or target or "")
    if not group_id:
        return None
    raw_content = proto.get("content") or b""
    content: dict[str, Any] | None = None
    if raw_content:
        try:
            parsed = json.loads(bytes(raw_content).decode("utf-8"))
            if isinstance(parsed, dict):
                content = parsed
        except Exception:
            content = None
    sender_id = str(proto.get("from_user_id") or uid or "")
    text = content.get("content") if classname == "RC:TxtMsg" and content else None
    sent_at = proto.get("data_time") or (date * 1000 if date else None)
    return GroupMessage(
        group_id=group_id,
        sender_id=sender_id,
        object_name=classname,
        text=str(text) if text is not None else None,
        content=content,
        message_uid=proto.get("msg_id") or None,
        sent_at=int(sent_at) if sent_at else None,
        is_self=bool(sender_id and sender_id == str(uid)),
        raw={
            "topic": topic,
            "target_id": target,
            "date": date,
            "proto": proto,
        },
    )


def _is_timeout(exc: BaseException) -> bool:
    return type(exc).__name__ in ("WebSocketTimeoutException", "TimeoutError")
