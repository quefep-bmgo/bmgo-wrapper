import base64
import hashlib
import unittest
from unittest.mock import patch

from blockmango.crypto import (
    _canonical_body,
    _encode_access_token,
    _is_raw_sign_path,
    _sign,
)

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


class CanonicalBodyTests(unittest.TestCase):
    def test_keys_are_sorted(self):
        self.assertEqual(_canonical_body('{"b":1,"a":2}'), '{"a":2,"b":1}')

    def test_whitespace_is_removed(self):
        self.assertEqual(
            _canonical_body('{ "a": 1, "b": [1, 2] }'),
            '{"a":1,"b":[1,2]}',
        )

    def test_non_json_is_left_alone(self):
        self.assertEqual(_canonical_body("not json"), "not json")


class AccessTokenTests(unittest.TestCase):
    def test_shape_matches_client(self):
        token = "t" * 211
        nonce = "n" * 36
        value = _encode_access_token(token, nonce, SK)
        self.assertEqual(len(value), 344)
        self.assertEqual(len(base64.b64decode(value)), 256)

    def test_same_inputs_give_same_header(self):
        first = _encode_access_token("token", "nonce", SK)
        second = _encode_access_token("token", "nonce", SK)
        self.assertEqual(first, second)

    def test_nonce_changes_output(self):
        self.assertNotEqual(
            _encode_access_token("token", "nonce-a", SK),
            _encode_access_token("token", "nonce-b", SK),
        )

    def test_empty_token_gives_empty_header(self):
        self.assertEqual(_encode_access_token("", "nonce", SK), "")


if __name__ == "__main__":
    unittest.main()
