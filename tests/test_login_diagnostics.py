import unittest
from unittest.mock import patch

from blockmango import BmgAccount
from blockmango.config import Config


class FakeResponse:
    def json(self):
        return {"code": 100008, "message": "access denied"}


class FakeSession:
    def post(self, *args, **kwargs):
        return FakeResponse()


class LoginDiagnosticsTests(unittest.TestCase):
    def test_login_exposes_the_server_code_without_credentials(self):
        account = BmgAccount(
            "test-user", "test-password",
            Config(device_id="app-id", device_sign="app-sign", bm_ddh_id="app-sign"),
        )
        with (
            patch.object(BmgAccount, "_sync_time"),
            patch.object(BmgAccount, "_get_session", return_value=FakeSession()),
            patch.object(account._device_pool, "ensure_loaded"),
            patch("blockmango.account.time.sleep"),
        ):
            self.assertFalse(account.login(tries=1))
        self.assertEqual(account.last_login_code, 100008)
        self.assertFalse(account.is_logged_in)
        account.close()


if __name__ == "__main__":
    unittest.main()
