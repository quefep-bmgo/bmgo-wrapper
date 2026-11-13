import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from blockmango import BmgAccount
from blockmango.config import Config
from blockmango.constants import APP_VERSION, APP_VERSION_NAME


class ConfigTests(unittest.TestCase):
    def test_defaults_target_3311(self):
        headers = Config().app_headers
        self.assertEqual(headers["appversion"], "5771")
        self.assertEqual(headers["appversionname"], "3.31.1")
        self.assertEqual(APP_VERSION, "5771")
        self.assertEqual(APP_VERSION_NAME, "3.31.1")

    def test_dotenv_and_from_env(self):
        with tempfile.TemporaryDirectory() as temp:
            env_file = Path(temp) / ".env"
            env_file.write_text(
                "BMG_DEVICE_ID=test-device\n"
                "BMG_BMDDH_ID=test-sign\n"
                "BMG_USERNAME=test-user\n"
                "BMG_PASSWORD=test-pass\n",
                encoding="utf-8",
            )
            previous = os.getcwd()
            os.chdir(temp)
            try:
                with patch.dict(os.environ, {}, clear=True):
                    config = Config.from_env()
                    self.assertEqual(config.device_id, "test-device")
                    self.assertEqual(config.bm_ddh_id, "test-sign")
                    account = BmgAccount.from_env()
                    self.assertEqual(account.username, "test-user")
                    self.assertEqual(account.password, "test-pass")
                    self.assertEqual(account.config.device_id, "test-device")
            finally:
                os.chdir(previous)

    def test_client_header_overrides(self):
        with patch.dict(os.environ, {
            "BMG_APP_VERSION": "5771",
            "BMG_APP_VERSION_NAME": "3.31.1",
            "BMG_ANDROID_VERSION": "35",
            "BMG_APP_MD5": "fingerprint-for-test",
        }, clear=True):
            headers = Config.from_env().app_headers
        self.assertEqual(headers["appversion"], "5771")
        self.assertEqual(headers["appversionname"], "3.31.1")
        self.assertEqual(headers["androidversion"], "35")
        self.assertEqual(headers["md5"], "fingerprint-for-test")


if __name__ == "__main__":
    unittest.main()
