import hashlib
import unittest
from unittest.mock import patch

from blockmango.crypto import _is_raw_sign_path, _sign

AK = "test-api-key"
SK = "test-secret"
DEVICE = "0123456789abcdef"


def md5(value):
    return hashlib.md5(value.encode()).hexdigest()


class SigningTests(unittest.TestCase):
    def test_raw_config_path(self):
        with patch("blockmango.crypto.time.time", return_value=1700000000), patch(
            "blockmango.crypto.uuid.uuid4", return_value="nonce"
        ):
            nonce, ts, sign = _sign("/config/files/example", [], "", AK, SK, DEVICE, 0)
        base = AK + "/config/files/example" + nonce + ts + "" + "" + SK
        self.assertEqual(sign, md5(base))
        self.assertTrue(_is_raw_sign_path("/config/files/example"))

    def test_device_wrapped_path(self):
        with patch("blockmango.crypto.time.time", return_value=1700000000), patch(
            "blockmango.crypto.uuid.uuid4", return_value="nonce"
        ):
            nonce, ts, sign = _sign("/game/api/v1/games/g1055/rank", [], "", AK, SK, DEVICE, 0)
        base = AK + "/game/api/v1/games/g1055/rank" + nonce + ts + "" + "" + SK
        self.assertEqual(sign, md5(md5(base) + DEVICE))
        self.assertFalse(_is_raw_sign_path("/game/api/v1/games/g1055/rank"))

    def test_account_login_is_raw_signed(self):
        self.assertTrue(_is_raw_sign_path("/user/api/v4/account/login"))


if __name__ == "__main__":
    unittest.main()
