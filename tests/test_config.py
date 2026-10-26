import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from blockmango import BmgAccount
from blockmango.config import Config


class ConfigTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
