import unittest

from blockmango.constants import APP_MD5
from blockmango.crypto import _build_signed_headers, _encode_access_token
from blockmango.exceptions import CryptoError

AK = "test-api-key"
SK = "test-secret"
DEVICE = "0123456789abcdef"
DEVICE_SIGN = "test-device-sign"


def build(path, body="", token_encoder=None):
    return _build_signed_headers(
        path, [], body, AK, SK, DEVICE, DEVICE_SIGN, 0,
        uid=123, token="raw-token", app_headers={"appversion": "5771"},
        region="LATAM", uid_register_ts="1", device_register_ts="2",
        device_headers={"manufacturer": "Test"},
        token_encoder=token_encoder,
    )


class HeaderTests(unittest.TestCase):
    def test_login_headers(self):
        headers = build("/user/api/v4/account/login", '{"account":"x"}')
        self.assertEqual(headers["bmg-device-id"], DEVICE)
        self.assertEqual(headers["bmg-sign"], DEVICE_SIGN)
        self.assertEqual(headers["userdeviceid"], DEVICE)
        self.assertEqual(headers["md5"], APP_MD5)
        self.assertEqual(headers["region"], "LATAM")
        self.assertEqual(headers["manufacturer"], "Test")
        self.assertEqual(headers["userid"], "123")
        self.assertNotEqual(headers["access-token"], "raw-token")
        self.assertEqual(
            headers["access-token"],
            _encode_access_token("raw-token", headers["x-nonce"], SK),
        )

    def test_token_encoder_override_is_respected(self):
        headers = build("/game/api/v1/games/g1055/rank",
                        token_encoder=lambda *args: "override")
        self.assertEqual(headers["access-token"], "override")

    def test_encoder_failure_is_reported(self):
        def broken(*args):
            raise ValueError("nope")

        with self.assertRaisesRegex(CryptoError, r"encoder failed \(ValueError\)"):
            build("/game/api/v1/games/g1055/rank", token_encoder=broken)

    def test_normal_headers_do_not_include_device_auth(self):
        headers = build("/game/api/v1/games/g1055/rank")
        self.assertNotIn("bmg-device-id", headers)
        self.assertNotIn("bmg-sign", headers)
        self.assertEqual(headers["userdeviceid"], DEVICE)
        self.assertEqual(headers["md5"], APP_MD5)

    def test_third_party_binding_list_includes_device_auth(self):
        headers = build("/user/api/v1/account/tp/list")
        self.assertEqual(headers["bmg-device-id"], DEVICE)
        self.assertEqual(headers["bmg-sign"], DEVICE_SIGN)


if __name__ == "__main__":
    unittest.main()
