import asyncio
import unittest

from blockmango.account import BmgAccount
from blockmango.config import Config
from blockmango.rongcloud_transport import (
    RongCloudTransport,
    _navi_host,
    _parse_navi,
    _parse_puback,
    _publish_frame,
)
from blockmango.transport import GroupMessageResult


class RongCloudProtocolTests(unittest.TestCase):
    def test_navi_host_comes_from_token(self):
        self.assertEqual(_navi_host("abc@475c.sg.rongnav.com;cfg.example"), "475c.sg.rongnav.com")
        self.assertEqual(_navi_host("abc"), "nav.cn.ronghub.com")

    def test_navi_jsonp_with_semicolon(self):
        parsed = _parse_navi('getServerEndpoint({"code":200,"server":"ws.example:443"});')
        self.assertEqual(parsed["server"], "ws.example:443")

    def test_publish_frame(self):
        frame = _publish_frame("42", "hello", 7)
        self.assertEqual(frame[0], 0x32)
        self.assertEqual(frame[1:3], b"\x00\x06")
        self.assertEqual(frame[3:9], b"pgMsgP")
        self.assertEqual(frame[9:11], b"\x00\x02")
        self.assertEqual(frame[11:13], b"42")
        self.assertEqual(frame[13:15], b"\x00\x07")
        self.assertIn(b"RC:TxtMsg", frame)
        self.assertIn(b'{"content":"hello"}', frame)

    def test_puback_parse(self):
        raw = bytes.fromhex(
            "4100016b049ddd0000030e0013443231382d353450502d4b4a38442d49345249"
        )
        message_id, status, timestamp, uid = _parse_puback(raw)
        self.assertEqual(message_id, 1)
        self.assertEqual(status, 0)
        self.assertEqual(timestamp, 1795464669782)
        self.assertEqual(uid, "D218-54PP-KJ8D-I4RI")

    def test_validation_happens_before_network(self):
        account = BmgAccount("user", "pass", Config())
        transport = RongCloudTransport(account)
        with self.assertRaises(ValueError):
            transport.send_text("not-a-group", "hello")
        with self.assertRaises(ValueError):
            transport.send_text("42", "   ")
        account.close()

    def test_default_transport_is_installed(self):
        account = BmgAccount("user", "pass", Config())
        self.assertIsInstance(account.group.transport, RongCloudTransport)
        account.close()

    def test_resolves_token_and_device_from_account(self):
        class FakeRongCloud:
            def get_raw_token(self):
                return "token@nav.example;cfg.example"

        account = BmgAccount("user", "pass", Config(device_id="device-1"))
        account._uid = 99
        account.rongcloud = FakeRongCloud()
        transport = RongCloudTransport(account)
        self.assertEqual(transport._resolve_token(), "token@nav.example;cfg.example")
        self.assertEqual(transport._resolve_device_id(), "device-1")
        self.assertEqual(transport._resolve_uid(), "99")
        account.close()

    def test_websocket_url_contains_device_identity(self):
        account = BmgAccount("user", "pass", Config())
        transport = RongCloudTransport(account)
        url = transport._websocket_url("ws.example:443", "token@nav", "device-1", "99")
        self.assertTrue(url.startswith("wss://ws.example:443/websocket?"))
        self.assertIn("deviceId=device-1", url)
        self.assertIn("clientId=99", url)
        self.assertIn("platform=android", url)
        account.close()


class FakeRongCloudTransport(RongCloudTransport):
    def __init__(self):
        self.calls = []

    def send_text(self, group_id, text, *, ext_content=None, timeout=10.0):
        self.calls.append((group_id, text, ext_content, timeout))
        return GroupMessageResult(group_id=str(group_id), message_uid="uid")


class AsyncRongCloudTransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_async_delegates(self):
        transport = FakeRongCloudTransport()
        result = await transport.async_send_text(42, "hello", timeout=3)
        self.assertEqual(result.message_uid, "uid")
        self.assertEqual(transport.calls, [(42, "hello", None, 3)])


if __name__ == "__main__":
    unittest.main()
