import json
import unittest

from blockmango.account import BmgAccount
from blockmango.config import Config
from blockmango.rongcloud_listener import (
    RongCloudListener,
    _decode_downstream,
    _parse_publish,
    _pb_fields,
    _to_group_message,
)
from blockmango.rongcloud_transport import RongCloudTransport


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


def _field(number: int, wire: int, payload: bytes) -> bytes:
    return _varint((number << 3) | wire) + payload


def _string(number: int, value: str) -> bytes:
    encoded = value.encode()
    return _field(number, 2, _varint(len(encoded)) + encoded)


def _int(number: int, value: int) -> bytes:
    return _field(number, 0, _varint(value))


def _utf(value: str) -> bytes:
    encoded = value.encode()
    return len(encoded).to_bytes(2, "big") + encoded


def _downstream(
    *,
    sender: str = "7",
    group_id: str = "42",
    text: str = "hello",
    message_uid: str = "D-TEST",
    sent_at: int = 1795460000000,
) -> bytes:
    content = json.dumps({"content": text}).encode()
    return (
        _string(1, sender)
        + _int(2, 3)
        + _string(3, group_id)
        + _string(4, "RC:TxtMsg")
        + _field(5, 2, _varint(len(content)) + content)
        + _int(6, sent_at)
        + _int(7, 0)
        + _string(9, message_uid)
    )


def _publish(group_id: str, proto: bytes, message_id: int = 1, topic: str = "pgMsgP") -> bytes:
    return (
        bytes([0x33])
        + (1795460000).to_bytes(4, "big")
        + _utf(topic)
        + _utf(group_id)
        + message_id.to_bytes(2, "big")
        + proto
    )


def _query_ack(messages: list[bytes], message_id: int = 1) -> bytes:
    payload = b"".join(
        _field(1, 2, _varint(len(message)) + message) for message in messages
    )
    return bytes([0x63]) + message_id.to_bytes(2, "big") + b"\x00" * 6 + payload


class FakeWebSocket:
    def __init__(self):
        self.sent = []

    def send_binary(self, data):
        self.sent.append(bytes(data))


class ListenerTests(unittest.TestCase):
    def _listener(self, callback, **kwargs):
        account = BmgAccount("user", "pass", Config())
        account._uid = 7
        transport = RongCloudTransport(account)
        listener = RongCloudListener(transport, callback, **kwargs)
        return account, listener

    def test_publish_parses_and_acknowledges(self):
        seen = []
        account, listener = self._listener(seen.append)
        ws = FakeWebSocket()
        listener._handle_publish(ws, _publish("42", _downstream()))
        self.assertEqual(len(seen), 1)
        message = seen[0]
        self.assertEqual(message.group_id, "42")
        self.assertEqual(message.sender_id, "7")
        self.assertEqual(message.object_name, "RC:TxtMsg")
        self.assertEqual(message.text, "hello")
        self.assertEqual(message.message_uid, "D-TEST")
        self.assertEqual(ws.sent, [b"\x40\x00\x01"])
        account.close()

    def test_group_filter_and_self_filter(self):
        seen = []
        account, listener = self._listener(
            seen.append,
            group_ids=["99"],
            include_self=False,
        )
        ws = FakeWebSocket()
        listener._handle_publish(ws, _publish("42", _downstream()))
        self.assertEqual(seen, [])
        account.close()

    def test_notification_topic_is_ignored(self):
        seen = []
        account, listener = self._listener(seen.append)
        ws = FakeWebSocket()
        listener._handle_publish(
            ws,
            _publish("45890736", _downstream(sender="45890736"), topic="s_ntf"),
        )
        self.assertEqual(seen, [])
        self.assertEqual(ws.sent, [b"\x40\x00\x01"])
        account.close()

    def test_query_ids_increment(self):
        account, listener = self._listener(lambda message: None)
        ws = FakeWebSocket()
        listener._send_query(ws, "7")
        listener._send_query(ws, "7")
        first_id = ws.sent[0][13:15]
        second_id = ws.sent[1][13:15]
        self.assertNotEqual(first_id, second_id)
        account.close()

    def test_query_ack_dispatches_messages(self):
        seen = []
        account, listener = self._listener(seen.append)
        ws = FakeWebSocket()
        listener._handle_query_ack(ws, _query_ack([_downstream(), _downstream(text="second")]))
        self.assertEqual([message.text for message in seen], ["hello", "second"])
        self.assertTrue(ws.sent)
        self.assertEqual(ws.sent[0][0], 0x70)
        account.close()

    def test_callback_errors_are_isolated(self):
        def broken(message):
            raise RuntimeError("callback failed")

        account, listener = self._listener(broken)
        ws = FakeWebSocket()
        listener._handle_publish(ws, _publish("42", _downstream()))
        self.assertIsInstance(listener.last_error, RuntimeError)
        account.close()

    def test_send_without_connection_is_a_clear_error(self):
        account, listener = self._listener(lambda message: None)
        with self.assertRaises(Exception) as context:
            listener.send_text("42", "hello", timeout=1)
        self.assertIn("not connected", str(context.exception).lower())
        account.close()

    def test_malformed_publish_does_not_crash_listener(self):
        account, listener = self._listener(lambda message: None)
        ws = FakeWebSocket()
        listener._handle_publish(ws, _publish("42", b"\x0a"))
        self.assertIsNotNone(listener.last_error)
        account.close()

    def test_image_message_exposes_image_url(self):
        content = json.dumps({"imageUri": "https://cdn.example/image.jpg"}).encode()
        message = _to_group_message(
            {
                "from_user_id": "7",
                "group_id": "42",
                "classname": "RC:ImgMsg",
                "content": content,
                "data_time": 1795460000000,
                "msg_id": "D-IMAGE",
            },
            "pgMsgP",
            "42",
            1795460000,
            "7547551998",
        )
        self.assertIsNotNone(message)
        self.assertEqual(message.object_name, "RC:ImgMsg")
        self.assertIsNone(message.text)
        self.assertEqual(message.image_url, "https://cdn.example/image.jpg")
        self.assertEqual(message.message_uid, "D-IMAGE")

    def test_publish_protobuf_shape(self):
        parsed = _parse_publish(_publish("42", _downstream()))
        date, topic, target, message_id, payload = parsed
        self.assertEqual(date, 1795460000)
        self.assertEqual(topic, "pgMsgP")
        self.assertEqual(target, "42")
        self.assertEqual(message_id, 1)
        proto = _decode_downstream(payload)
        self.assertEqual(proto["from_user_id"], "7")
        self.assertEqual(proto["group_id"], "42")
        self.assertEqual(proto["msg_id"], "D-TEST")

    def test_query_ack_payload_parsing(self):
        payload = _field(1, 2, _varint(len(_downstream())) + _downstream())
        fields = _pb_fields(payload)
        self.assertIn(1, fields)
        self.assertEqual(_decode_downstream(fields[1][0])["group_id"], "42")


class FakeTransport:
    def __init__(self):
        self.listen_args = None

    def listen(self, callback, **kwargs):
        self.listen_args = (callback, kwargs)
        return "subscription"


class ListenDelegationTests(unittest.TestCase):
    def test_group_api_delegates_listen(self):
        from blockmango.submodules.group import GroupAPI

        class Account:
            uid = 1

        api = GroupAPI(Account())
        transport = FakeTransport()
        api.set_transport(transport)
        callback = lambda message: None
        result = api.listen(callback, group_ids=[42], include_self=False)
        self.assertEqual(result, "subscription")
        self.assertEqual(transport.listen_args[0], callback)
        self.assertEqual(transport.listen_args[1]["group_ids"], [42])
        self.assertFalse(transport.listen_args[1]["include_self"])


if __name__ == "__main__":
    unittest.main()
