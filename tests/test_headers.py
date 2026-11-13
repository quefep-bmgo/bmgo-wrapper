import unittest

from blockmango.constants import APP_MD5, APP_VERSION
from blockmango.crypto import _build_signed_headers
from blockmango.exceptions import CryptoError

AK = "test-api-key"
SK = "test-secret"
DEVICE = "0123456789abcdef"
DEVICE_SIGN = "test-device-sign"


def build(path, body="", app_headers=None, token_encoder=None):
    return _build_signed_headers(
        path, [], body, AK, SK, DEVICE, DEVICE_SIGN, 0,
        uid=123, token="raw-token",
        app_headers={"appversion": APP_VERSION, **(app_headers or {})},
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
        self.assertEqual(headers["access-token"], "raw-token")

    def test_normal_headers_do_not_include_device_auth(self):
        headers = build("/game/api/v1/games/g1055/rank")
        self.assertNotIn("bmg-device-id", headers)
        self.assertNotIn("bmg-sign", headers)
        self.assertEqual(headers["userdeviceid"], DEVICE)
        self.assertEqual(headers["md5"], APP_MD5)

    def test_live_client_md5_override_is_respected(self):
        headers = build("/game/api/v1/games/g1055/rank", app_headers={"md5": "live-fingerprint"})
        self.assertEqual(headers["md5"], "live-fingerprint")

    def test_token_encoder_error_is_reported_instead_of_falling_back(self):
        def broken_encoder(*args):
            raise ValueError("private callback detail")

        with self.assertRaisesRegex(CryptoError, r"Access-Token encoder failed \(ValueError\)"):
            build("/game/api/v1/games/g1055/rank", token_encoder=broken_encoder)

if __name__ == "__main__":
    unittest.main()
