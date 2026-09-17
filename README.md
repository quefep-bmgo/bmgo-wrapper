# bmgo-wrapper

Python client for the reverse-engineered Blockman GO (BlockyMods) HTTP API and its x-sign request format.

The code currently targets the Android client headers used by Blockman GO v3.28.2 (version code 5742). This is not an official SDK. Server behavior, keys, headers, and endpoints can change without notice.

## Requirements

- Python 3.10 or newer
- A Blockman GO app installation or rooted Android emulator from which device values can be read
- A Blockman GO account and password
- `BMG_DEVICE_ID` and `BMG_BMDDH_ID` from that app installation

Install the package in editable mode:

```bash
python -m pip install -e .
```

## Device Values

The wrapper cannot log in with only a username and password. The API also expects device headers.

`BMG_DEVICE_ID` is the emulator's `Settings.Secure.ANDROID_ID`:

```bash
adb shell settings get secure android_id
```

`BMG_BMDDH_ID` is the exact `bm_ddh_id` value saved by Blockman GO in its MMKV data. It is a separate value from `ANDROID_ID`; it is not a hash or encoding that this package can recreate. Do not substitute a value copied from another emulator or an unrelated app installation.

For a rooted MuMu instance, pull the app's MMKV file. The file names and layout can vary by app version; this is the location used by current Blockman GO installs:

```bash
adb root
adb pull /data/data/com.sandboxol.blockymods/files/mmkv/mutilProcessData ./mutilProcessData
```

Some versions keep the value in another MMKV file. Inspect the files under `/data/data/com.sandboxol.blockymods/files/mmkv/` rather than assuming that `bmg_cache` contains it. A simple `strings | grep` lookup is not reliable for every MMKV build.

If `bm_ddh_id` is present in a pulled file, this small parser prints only that value:

```python
from pathlib import Path

data = Path("mutilProcessData").read_bytes()
key = b"bm_ddh_id"
offset = data.find(key)
if offset < 0:
    raise SystemExit("bm_ddh_id was not found; inspect the other MMKV files")

def read_varint(position):
    value = 0
    shift = 0
    while position < len(data):
        byte = data[position]
        position += 1
        value |= (byte & 0x7f) << shift
        if not byte & 0x80:
            return value, position
        shift += 7
    raise ValueError("truncated MMKV value")

value_size, value_start = read_varint(offset + len(key))
text_size, text_start = read_varint(value_start)
if text_start + text_size > value_start + value_size:
    raise ValueError("invalid MMKV string value")
print(data[text_start:text_start + text_size].decode())
```

The value must be paired with the device state from the same emulator/app installation. `BMG_DEVICE_SIGN` is optional and is only needed when using a separate device-pool signature. For a direct rooted-emulator setup, leave it empty unless you have a matching value.

The default device-pool URL is not a credential source. It may return no usable devices, so set both required values explicitly.

## Configuration

Copy the example file and fill in the two required values:

```bash
cp .env.example .env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

Example:

```dotenv
BMG_DEVICE_ID=your_android_id
BMG_BMDDH_ID=your_bm_ddh_id
# BMG_DEVICE_SIGN=your_matching_device_pool_signature
```

Never commit `.env`, account passwords, access tokens, pulled MMKV files, or `.sessions.json`.

Useful optional settings include:

| Variable | Default | Purpose |
| --- | --- | --- |
| `BMG_API_BASE` | `https://gw.sandboxol.com` | API base URL |
| `BMG_TIME_API` | `http://di.sandboxol.com/api/server-time` | Server time endpoint |
| `BMG_DEVICE_POOL_URL` | Repository default | Device-pool endpoint; may be unavailable |
| `BMG_USER_AGENT` | `okhttp/4.12.0` | Client user agent |
| `BMG_VERIFY_SSL` | `false` | Enable TLS certificate verification |
| `BMG_SESSION_CACHE` | `.sessions.json` | Session cache path |

The default `BMG_VERIFY_SSL=false` matches the existing client behavior but is not recommended for production. Set it to `true` when the server certificate chain works in your environment.

## Basic Usage

`login()` performs a fresh username/password login. It does not automatically restore `.sessions.json`.

```python
from blockmango import BmgAccount

account = BmgAccount("username", "password")
if not account.login():
    raise RuntimeError("Blockman GO login failed")

print(account.uid)
print(account.get_own_profile())
print(account.clan.get_own_clan())
print(account.friends.list_friends())
```

To reuse a cached session explicitly:

```python
from blockmango import BmgAccount

account = BmgAccount("username", "password")
session = account.load_session()
if not session or not account.restore_session(session) or not account.session_valid():
    if not account.login():
        raise RuntimeError("Blockman GO login failed")
```

The account object exposes the following groups:

- `account.user`
- `account.friends`
- `account.clan`
- `account.ranking`
- `account.game`
- `account.activity`
- `account.mailbox`
- `account.group`
- `account.decoration`
- `account.shop`
- `account.backpack`
- `account.bedwar`
- `account.pay`
- `account.video`
- `account.rongcloud`
- `account.gratitude`

Most methods have an async counterpart prefixed with `async_`. `account.request()` is available for endpoints not wrapped by a module.

## Limitations

- This project depends on a private, reverse-engineered API and is version-sensitive.
- Device credentials are inputs; the package does not create, forge, or recover `bm_ddh_id` from `BMG_DEVICE_ID`.
- Login from another account or emulator is possible, but that emulator still needs its own valid device values.
- Some server endpoints are removed, restricted, event-dependent, or behave differently by region.
- Methods that change account, friend, clan, inventory, or payment state should be treated as live operations. There is no dry-run layer.
- Sessions are written to `.sessions.json`, which is ignored by Git.

## License

MIT
