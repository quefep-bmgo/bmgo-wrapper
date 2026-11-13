import unittest
from unittest.mock import patch

from blockmango.config import Config
from blockmango.device import DevicePool


class DevicePoolTests(unittest.TestCase):
    def test_configured_install_is_used_without_fetching_pool(self):
        config = Config(device_id="app-id", device_sign="app-sign", bm_ddh_id="app-ddh")
        pool = DevicePool(config)
        with patch("blockmango.device.requests.get") as get:
            devices = pool.fetch()
        get.assert_not_called()
        self.assertEqual(devices, [("app-id", "app-sign", "app-ddh")])


if __name__ == "__main__":
    unittest.main()
