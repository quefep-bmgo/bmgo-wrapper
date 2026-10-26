import unittest

from blockmango.constants import APP_MD5
from blockmango.crypto import _build_signed_headers

AK = "test-api-key"
SK = "test-secret"
DEVICE = "0123456789abcdef"
DEVICE_SIGN = "test-device-sign"


def build(path, body=""):
    return _build_signed_headers(
        path, [], body, AK, SK, DEVICE, DEVICE_SIGN, 0,
        uid=123, token="raw-token", app_headers={"appversion": "5753"},
        region="LATAM", uid_register_ts="1", device_register_ts="2",
        device_headers={"manufacturer": "Test"},
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


if __name__ == "__main__":
    unittest.main()
