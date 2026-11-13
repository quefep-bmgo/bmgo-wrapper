import io
import os
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.get_device_values import find_bm_ddh_id_bytes, find_device_value_in_waydroid, write_env_values


def encode_varint(value: int) -> bytes:
    out = bytearray()
    while value >= 0x80:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def make_mmkv_string(key: bytes, value: bytes) -> bytes:
    wrapped = encode_varint(len(value)) + value
    return key + encode_varint(len(wrapped)) + wrapped


def make_tar(name: str, content: bytes) -> bytes:
    result = io.BytesIO()
    with tarfile.open(fileobj=result, mode="w:") as archive:
        member = tarfile.TarInfo(name)
        member.size = len(content)
        archive.addfile(member, io.BytesIO(content))
    return result.getvalue()


class DeviceValueTests(unittest.TestCase):
    def test_extracts_device_sign_from_mmkv_bytes(self):
        data = b"prefix" + make_mmkv_string(b"bm_ddh_id", b"device-sign-example")
        self.assertEqual(find_bm_ddh_id_bytes(data), "device-sign-example")

    def test_reads_waydroid_tar_without_writing_mmkv_to_disk(self):
        payload = b"prefix" + make_mmkv_string(b"bm_ddh_id", b"device-sign-example")
        archive = make_tar("mutilProcessData", payload)
        with patch("tools.get_device_values.waydroid_root_command", return_value=archive):
            mmkv_dir, ddh = find_device_value_in_waydroid("app.example")
        self.assertEqual(mmkv_dir, "/data/user/0/app.example/files/mmkv")
        self.assertEqual(ddh, "device-sign-example")

    def test_output_env_preserves_other_settings_and_is_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            path.write_text("BMG_USERNAME=test-user\nBMG_DEVICE_ID=old\n", encoding="utf-8")
            write_env_values(path, "android-id", "device-sign")
            text = path.read_text(encoding="utf-8")
            self.assertIn("BMG_USERNAME=test-user", text)
            self.assertIn("BMG_DEVICE_ID=android-id", text)
            self.assertIn("BMG_BMDDH_ID=device-sign", text)
            self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
