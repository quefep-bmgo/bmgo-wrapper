# Authentication and request signing

This page explains how a Blockman GO session is built. It is intentionally
read-only: it does not create accounts or device values.

## 1. Device values

The API expects values from the same app installation:

- `BMG_DEVICE_ID`: Android `Settings.Secure.ANDROID_ID`.
- `BMG_BMDDH_ID`: the exact `bm_ddh_id` string stored by Blockman GO.

`BMG_DEVICE_SIGN` is only needed when a separate device-pool signature is used.
For a direct emulator setup, the login `bmg-sign` value is the `bm_ddh_id`.

Some accounts are device-bound. If login returns `code 100008` with
`access denied`, use the device values that belong to that account/install.
Do not reuse a device pair from a different account if the server rejects it.

The bundled extractor prints both values:

```bash
python tools/get_device_values.py
```

For a manual fallback, read the Android ID and pull the app's MMKV directory:

```bash
adb shell settings get secure android_id
adb root
adb pull /data/data/com.sandboxol.blockymods/files/mmkv ./mmkv
```

Open the app once before pulling. The value may be in any file under the
directory, not just `mutilProcessData`. The parser in
`tools/get_device_values.py` shows the MMKV string format.

## 2. Login

```python
from blockmango import BmgAccount

account = BmgAccount.from_env()  # reads .env / environment
if not account.login():
    raise RuntimeError("login failed")

print(account.uid, account.region)
```

You can also pass credentials explicitly with
`BmgAccount("username", "password")`.

Login uses `POST /user/api/v4/account/login`. The password is RSA-encrypted with
the public key embedded in the app. The response contains the raw access token,
user id, region, and registration timestamps.

The wrapper stores:

- `uid`
- the raw `accessToken`
- `region` (for example `RU` or `LATAM`)
- `uid_register_ts`
- `device_register_ts`
- the device values used for the session

These are included in later request headers.

## 3. Signing

The normal request signature is:

```text
base = api_key + path + nonce + time + sorted_params + body + secret_key
x-sign = md5(md5(base) + userdeviceid)
```

For account/auth paths and `/config/files/` or `/config/ml/files/` paths:

```text
x-sign = md5(base)
```

Header set for normal requests:

- `x-apikey`
- `x-nonce` (UUID)
- `x-time` (Unix seconds)
- `x-sign`
- `x-urlpath`
- `userdeviceid`
- `md5` (static app fingerprint, not the body MD5)
- `userid` and `access-token` when logged in

Login and auth-token requests additionally include `bmg-device-id` and
`bmg-sign`.

## 4. Access-Token caveat

The 3.29.x client normally transforms the login JWT into a 344-character,
native-encoded `access-token` value. In live testing on 2026-10-26 the server
also accepted the raw login JWT for the tested account, including profile, game
details, game auth, and leaderboards. Some accounts or sessions may require the
native value; those endpoints then return `code 6` or `code 37`.

If you have a working encoder, pass a callback:

```python
def encode_token(token, path, nonce, ts, params, body, region):
    # Return the 344-character Access-Token value for this request.
    return encoded_value

account = BmgAccount("username", "password", token_encoder=encode_token)
```

If the callback raises, the wrapper falls back to the raw JWT.

## 5. Sessions

Session data can be cached with `save_session()` / `load_session()` and
`restore_session()`. The default file is `.sessions.json`, which is ignored by
Git. It contains live credentials; never commit it.

## 6. Common errors

| Code | Meaning |
| --- | --- |
| `1` | Success |
| `3` | Missing authorization or unsupported option |
| `6` | Authentication/permission failure |
| `37` | Authorization check failed |
| `100001` | Server time mismatch; the wrapper retries after time sync |
| `100008` | Access denied / rate limited; login retries |
| `567` | Server-side retry condition |

## 7. Security

- Keep `.env`, `.sessions.json`, and captured request logs private.
- Do not commit device values, JWTs, access tokens, or passwords.
- Use test accounts for exploratory requests.
- Treat profile/friend/clan/inventory/payment mutations as live operations.
