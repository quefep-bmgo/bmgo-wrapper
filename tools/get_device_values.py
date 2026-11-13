"""Extract Blockman GO device values from a rooted Android device.

Usage:
    python tools/get_device_values.py [--serial SERIAL] [--package PACKAGE]
    python tools/get_device_values.py --waydroid [--serial SERIAL]

By default the script uses a rooted ADB device. Waydroid does not support
``adb root``, so pass ``--waydroid`` to read MMKV through ``sudo waydroid
shell`` instead. Blockman GO 3.31.1 uses the app's ``android.id`` value from
MMKV (or ``Settings.System.android_id`` when present), not the shell-scoped
``Settings.Secure.ANDROID_ID``. The tool reads it with ``bm_ddh_id`` and prints:

    BMG_DEVICE_ID=...
    BMG_BMDDH_ID=...

It deliberately does not print access tokens or account credentials.
"""

from __future__ import annotations

import argparse
import io
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

PACKAGE = os.environ.get("BMG_PACKAGE_NAME", "com.sandboxol.blockymods.channel.official")
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


def find_mmkv_string_bytes(data: bytes, key: str) -> str | None:
    key_bytes = key.encode("ascii")
    start = 0
    while True:
        offset = data.find(key_bytes, start)
        if offset < 0:
            return None
        start = offset + 1
        try:
            value_size, value_start = read_varint(data, offset + len(key_bytes))
            text_size, text_start = read_varint(data, value_start)
            if text_size <= 0 or text_start + text_size > value_start + value_size:
                continue
            value = data[text_start:text_start + text_size]
            if value and all(32 <= byte < 127 for byte in value):
                return value.decode("ascii")
        except ValueError:
            continue


def find_bm_ddh_id_bytes(data: bytes) -> str | None:
    return find_mmkv_string_bytes(data, "bm_ddh_id")


def find_bm_ddh_id(path: Path) -> str | None:
    return find_bm_ddh_id_bytes(path.read_bytes())


def waydroid_root_command(args: list[str]) -> bytes:
    """Run one root command inside Waydroid without writing its output to disk."""
    prefix = shlex.split(os.environ.get("BMG_WAYDROID_ROOT_PREFIX", "sudo waydroid"))
    proc = subprocess.run(
        prefix + ["shell", "--", *args],
        capture_output=True,
        timeout=60,
    )
    if proc.returncode:
        detail = (proc.stderr or proc.stdout).decode("utf-8", "replace").strip()
        raise SystemExit(f"Waydroid root command failed: {detail or 'unknown error'}")
    return proc.stdout


def find_device_value_in_waydroid(package: str) -> tuple[str, str | None, str]:
    """Read the app-scoped android.id and bm_ddh_id from Waydroid MMKV."""
    mmkv_dir = f"/data/user/0/{package}/files/mmkv"
    # One root-shell call avoids repeated sudo prompts and keeps the MMKV
    # archive in memory; only the two required device values leave this function.
    archive_bytes = waydroid_root_command([
        "sh", "-c", f"tar -C {shlex.quote(mmkv_dir)} -cf - .",
    ])
    android_id = None
    ddh = None
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
            for member in archive:
                if not member.isfile() or member.name.endswith(".crc"):
                    continue
                stream = archive.extractfile(member)
                if stream is None:
                    continue
                content = stream.read()
                android_id = android_id or find_mmkv_string_bytes(content, "android.id")
                ddh = ddh or find_bm_ddh_id_bytes(content)
                if android_id and ddh:
                    break
    except tarfile.TarError as error:
        raise SystemExit(f"Could not read Waydroid MMKV data: {error}") from error
    if not ddh:
        raise SystemExit(f"bm_ddh_id was not found under {mmkv_dir}")
    return mmkv_dir, android_id, ddh


def write_env_values(path: Path, android_id: str, ddh: str) -> None:
    """Update only the two device entries, preserving other local .env values."""
    keys = {"BMG_DEVICE_ID", "BMG_BMDDH_ID"}
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    lines = [line for line in lines if line.partition("=")[0] not in keys]
    lines.extend((f"BMG_DEVICE_ID={android_id}", f"BMG_BMDDH_ID={ddh}"))
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temp.chmod(0o600)
    temp.replace(path)
    path.chmod(0o600)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serial", help="adb serial (otherwise auto-detect)")
    parser.add_argument("--package", default=PACKAGE, help="installed Blockman GO package name")
    parser.add_argument("--waydroid", action="store_true",
                        help="read MMKV with the Waydroid root shell (ADB root is unsupported there)")
    parser.add_argument("--output-env", type=Path,
                        help="save device values into an ignored local env file instead of printing them")
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9._]+", args.package):
        raise SystemExit("Invalid Android package name")

    adb = find_adb()
    serial = choose_serial(adb, args.serial)
    print(f"# adb: {adb}", file=sys.stderr)
    print(f"# device: {serial}", file=sys.stderr)

    if args.waydroid:
        mmkv_dir, android_id, ddh = find_device_value_in_waydroid(args.package)
        if not android_id:
            android_id = run(adb, ["shell", "settings", "get", "system", "android_id"], serial)
    else:
        root_output = run(adb, ["root"], serial)
        if root_output:
            print(f"# adb root: {root_output}", file=sys.stderr)
        run(adb, ["wait-for-device"], serial)
        android_id = run(adb, ["shell", "settings", "get", "system", "android_id"], serial)
        mmkv_dir = f"/data/user/0/{args.package}/files/mmkv"
        with tempfile.TemporaryDirectory(prefix="bmgo-device-") as temp:
            destination = Path(temp) / "mmkv"
            pull = subprocess.run(
                [adb, "-s", serial, "pull", mmkv_dir, str(destination)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if not destination.exists():
                raise SystemExit(
                    f"Could not pull {mmkv_dir}.\n"
                    "Make sure the app has been opened and ADB root is available.\n"
                    f"{pull.stderr or pull.stdout}"
                )

            app_android_id = None
            ddh = None
            for path in sorted(destination.rglob("*")):
                if not path.is_file() or path.name.endswith(".crc"):
                    continue
                content = path.read_bytes()
                app_android_id = app_android_id or find_mmkv_string_bytes(content, "android.id")
                ddh = ddh or find_bm_ddh_id_bytes(content)
                if app_android_id and ddh:
                    print(f"# bm_ddh_id found in {path.name}", file=sys.stderr)
                    break
            android_id = app_android_id or android_id

    if not android_id or android_id == "null":
        raise SystemExit(
            "Blockman GO's android.id was not found. Open the app once and rerun the extractor."
        )

    if not ddh:
        raise SystemExit(
            "bm_ddh_id was not found. Open Blockman GO once and check the app package name."
        )

    if args.output_env:
        write_env_values(args.output_env, android_id, ddh)
        print(f"Saved device values to {args.output_env} (permissions 0600)", file=sys.stderr)
        return

    print(f"BMG_DEVICE_ID={android_id}")
    print(f"BMG_BMDDH_ID={ddh}")


if __name__ == "__main__":
    main()
