"""Extract Blockman GO device values from a rooted Android device.

Usage:
    python tools/get_device_values.py [--serial SERIAL]

The script uses adb, restarts adbd as root, reads
``Settings.Secure.ANDROID_ID``, pulls the app's MMKV directory into a temporary
folder, and prints:

    BMG_DEVICE_ID=...
    BMG_BMDDH_ID=...

It deliberately does not print access tokens or account credentials.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACKAGE = "com.sandboxol.blockymods"
MMKV_DIR = f"/data/data/{PACKAGE}/files/mmkv"
ADB_CANDIDATES = (
    os.environ.get("ADB", ""),
    shutil.which("adb") or "",
    r"C:\Program Files\Netease\MuMuPlayer\nx_main\adb.exe",
    r"C:\Program Files\Netease\MuMuPlayer-12.0\shell\adb.exe",
    r"C:\Program Files\Netease\MuMu Player 12\shell\adb.exe",
)


def find_adb() -> str:
    for candidate in ADB_CANDIDATES:
        if candidate and Path(candidate).is_file():
            return candidate
    raise SystemExit("adb was not found. Set ADB to the full adb.exe path.")


def run(adb: str, args: list[str], serial: str | None = None) -> str:
    command = [adb]
    if serial:
        command += ["-s", serial]
    command += args
    proc = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return (proc.stdout or "").strip()


def choose_serial(adb: str, requested: str | None) -> str:
    serial = requested or os.environ.get("BMG_ADB_SERIAL") or os.environ.get("ANDROID_SERIAL")
    if serial:
        return serial
    output = run(adb, ["devices"])
    devices = []
    for line in output.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    if len(devices) == 1:
        return devices[0]
    if not devices:
        raise SystemExit("No adb device found. Start the emulator and enable USB debugging.")
    raise SystemExit(
        "Multiple adb devices are connected. Re-run with --serial or set BMG_ADB_SERIAL:\n  "
        + "\n  ".join(devices)
    )


def read_varint(data: bytes, position: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while position < len(data):
        byte = data[position]
        position += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, position
        shift += 7
    raise ValueError("truncated MMKV varint")


def find_bm_ddh_id(path: Path) -> str | None:
    key = b"bm_ddh_id"
    data = path.read_bytes()
    start = 0
    while True:
        offset = data.find(key, start)
        if offset < 0:
            return None
        start = offset + 1
        try:
            value_size, value_start = read_varint(data, offset + len(key))
            text_size, text_start = read_varint(data, value_start)
            if text_size <= 0 or text_start + text_size > value_start + value_size:
                continue
            value = data[text_start:text_start + text_size]
            if value and all(32 <= byte < 127 for byte in value):
                return value.decode("ascii")
        except ValueError:
            continue


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serial", help="adb serial (otherwise auto-detect)")
    args = parser.parse_args()

    adb = find_adb()
    serial = choose_serial(adb, args.serial)
    print(f"# adb: {adb}", file=sys.stderr)
    print(f"# device: {serial}", file=sys.stderr)

    root_output = run(adb, ["root"], serial)
    if root_output:
        print(f"# adb root: {root_output}", file=sys.stderr)
    run(adb, ["wait-for-device"], serial)

    android_id = run(adb, ["shell", "settings", "get", "secure", "android_id"], serial)
    if not android_id or android_id == "null":
        raise SystemExit("Could not read Settings.Secure.ANDROID_ID; is the device rooted?")

    with tempfile.TemporaryDirectory(prefix="bmgo-device-") as temp:
        destination = Path(temp) / "mmkv"
        pull = subprocess.run(
            [adb, "-s", serial, "pull", MMKV_DIR, str(destination)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if not destination.exists():
            raise SystemExit(
                f"Could not pull {MMKV_DIR}.\n"
                "Make sure the app has been opened at least once and adb is running as root.\n"
                f"{pull.stderr or pull.stdout}"
            )

        ddh = None
        for path in sorted(destination.rglob("*")):
            if not path.is_file() or path.name.endswith(".crc"):
                continue
            ddh = find_bm_ddh_id(path)
            if ddh:
                print(f"# bm_ddh_id found in {path.name}", file=sys.stderr)
                break

    if not ddh:
        raise SystemExit(
            "bm_ddh_id was not found. Inspect every file under "
            f"{MMKV_DIR} (not just mutilProcessData) and try again."
        )

    print(f"BMG_DEVICE_ID={android_id}")
    print(f"BMG_BMDDH_ID={ddh}")


if __name__ == "__main__":
    main()
