# bmgo-wrapper

[![Discord](https://img.shields.io/badge/Discord-Join%20Us-5865F2?logo=discord&logoColor=white)](https://discord.gg/PQhj8zcmBK)

A Python client for the reverse-engineered Blockman GO (BlockyMods) HTTP API.
It handles login, the `x-sign` request format, sessions, the current 3.29.3
headers, and the game/leaderboard flows used by the Android client.

This is not an official SDK. The server, keys, headers, and endpoints can change
without notice. Use test accounts for exploratory work.

## Contents

- [What it does](#what-it-does)
- [Choose your path](#choose-your-path)
- [Requirements](#requirements)
- [Install](#install)
- [Quick start](#quick-start)
- [Device values](#device-values)
- [Configuration](#configuration)
- [Project map](#project-map)
- [Usage](#usage)
- [Leaderboards](#leaderboards)
- [Cookbook](#cookbook)
- [Known game IDs](#known-game-ids)
- [API reference](#api-reference)
- [Modules](#modules)
- [Authentication and signing](#authentication-and-signing)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Security](#security)
- [Limitations](#limitations)
- [License](#license)

## What it does

- Logs in with username/password and RSA-encrypted password.
- Builds the current Blockman GO headers and `x-sign`.
- Stores sessions and refreshes server time.
- Provides typed wrappers for user, friends, clan, game, activity, pay, mail,
  ranking, remote config, notices, and other modules.
- Supports async calls with `async_` methods.
- Parses game leaderboards, including very large simulator scores, without
  losing precision.

## Choose your path

**Just want a working bot or a quick leaderboard?** Follow [Quick
start](#quick-start), use 	ools/get_device_values.py to get your two device
values, then copy one of the examples in [Cookbook](#cookbook).

**Want to build on the API?** Read docs/api-overview.md and
docs/authentication.md, then use ccount.request() for new endpoints and
promote stable calls into a module under src/blockmango/submodules/.

The wrapper is deliberately boring: it gives you a signed HTTP client, typed
helpers, and JSON responses. You decide whether the output goes to Discord,
Telegram, a local dashboard, or an in-game companion tool.

## Requirements

- Python 3.10 or newer
- A Blockman GO installation, or a rooted Android emulator with the same app
- A Blockman GO account
- `BMG_DEVICE_ID` and `BMG_BMDDH_ID` from that app installation

## Install

```bash
python -m pip install -e .
```

## Quick start

This is the fastest path for a working setup.

1. Install the package:

   ```bash
   python -m pip install -e .
   ```

2. Get your device values while the emulator is running:

   ```bash
   python tools/get_device_values.py
   ```

   The tool prints two lines:

   ```text
   BMG_DEVICE_ID=...
   BMG_BMDDH_ID=...
   ```

3. Create your local configuration:

   ```bash
   cp .env.example .env
   ```

   PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

   Fill in `BMG_DEVICE_ID`, `BMG_BMDDH_ID`, `BMG_USERNAME`, and
   `BMG_PASSWORD`. The package loads `.env` automatically when
   `python-dotenv` is installed (it is a package dependency). `.env` is ignored
   by Git.

4. Log in and read a leaderboard:

   ```python
   from blockmango import BmgAccount

   account = BmgAccount.from_env()
   if not account.login():
       raise RuntimeError("Blockman GO login failed")

   print(account.uid, account.region)
   print(account.get_own_profile())
   for entry in account.ranking.get_game_leaderboard_entries(
       "g1055", period="all", page=0, size=5
   ):
       print(entry.rank, entry.nick_name, entry.score, entry.display_value)
   ```

If you prefer environment variables over `.env`, set `BMG_DEVICE_ID`,
`BMG_BMDDH_ID`, `BMG_USERNAME`, and `BMG_PASSWORD` in your shell. You can also
construct an account directly:

```python
from blockmango import BmgAccount

account = BmgAccount("username", "password")
```

`login()` performs a fresh login. To reuse a cached session explicitly:

```python
from blockmango import BmgAccount

account = BmgAccount.from_env()
session = account.load_session()
if not session or not account.restore_session(session) or not account.session_valid():
    if not account.login():
        raise RuntimeError("Blockman GO login failed")
```

`BMG_USERNAME` and `BMG_PASSWORD` are read by `BmgAccount.from_env()` and the
examples; `BmgAccount(...)` takes them as arguments.

## Device values

The API cannot log in with only a username and password. The device headers must
come from the same app installation as the account.

The quickest path is the bundled extractor while the emulator is running:

```bash
python tools/get_device_values.py
```

It restarts adbd as root, reads `Settings.Secure.ANDROID_ID`, pulls the app's
MMKV directory, finds `bm_ddh_id`, and prints the two `.env` lines. It does not
print tokens or passwords. If you prefer doing it manually, the file locations
are:

| Value | Where it lives |
| --- | --- |
| Android ID | `adb shell settings get secure android_id` |
| `bm_ddh_id` | `/data/data/com.sandboxol.blockymods/files/mmkv/` |
| Cached session | `.sessions.json` in the working directory |
| Wrapper settings | `.env` in the working directory, or environment variables |
| Account region | Returned by the login response; stored in the session cache |

`BMG_DEVICE_ID` is the emulator's `Settings.Secure.ANDROID_ID`:

```bash
adb shell settings get secure android_id
```

`BMG_BMDDH_ID` is the exact `bm_ddh_id` string stored by Blockman GO. It is not
derived from `ANDROID_ID`, and the wrapper cannot recreate it. For a rooted MuMu
instance:

```bash
adb root
adb pull /data/data/com.sandboxol.blockymods/files/mmkv/mutilProcessData ./mutilProcessData
```

The file name and layout can vary. Inspect the files under
`/data/data/com.sandboxol.blockymods/files/mmkv/` if the value is not in
`mutilProcessData`.

A small MMKV parser:

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

Some accounts are device-bound. If login returns `code 100008` with
`access denied`, use the device values that belong to that account/install.
`BMG_DEVICE_SIGN` is optional and only needed for a matching device-pool
signature.

The default device-pool URL is not a credential source. It may return no usable
devices, so set the device values explicitly.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `BMG_DEVICE_ID` | empty | Android ID for the session |
| `BMG_BMDDH_ID` | empty | `bm_ddh_id` / login `bmg-sign` value |
| `BMG_DEVICE_SIGN` | empty | Optional separate device-pool signature |
| `BMG_USERNAME` | empty | Account used by `BmgAccount.from_env()` and examples |
| `BMG_PASSWORD` | empty | Account password for `BmgAccount.from_env()` |
| `BMG_API_BASE` | `https://gw.sandboxol.com` | API base URL |
| `BMG_TIME_API` | `https://gw.sandboxol.com/server-time` | Server time endpoint |
| `BMG_DEVICE_POOL_URL` | repository default | Device-pool URL; may be unavailable |
| `BMG_REGION` | `sandbox` | Region before login; refreshed from login |
| `BMG_DEVICE_HEADERS_JSON` | empty | Optional JSON fingerprint headers, e.g. `{"manufacturer":"Samsung","model":"SM-S916U"}` |
| `BMG_USER_AGENT` | `okhttp/4.12.0` | Client user agent |
| `BMG_VERIFY_SSL` | `false` | Enable TLS certificate verification |
| `BMG_SESSION_CACHE` | `.sessions.json` | Session cache path |

`Config.from_env()` loads `.env` automatically when `python-dotenv` is installed.
If you do not use `.env`, export the same names in your shell or process
environment. `BMG_VERIFY_SSL=false` matches the app's behavior, but is not
recommended for production. Set it to `true` when the server certificate chain
works in your environment.

## Project map

| Path | What is there |
| --- | --- |
| `src/blockmango/account.py` | Login, requests, session state, account facade |
| `src/blockmango/crypto.py` | RSA password encryption, signatures, headers |
| `src/blockmango/constants.py` | API base, app headers, raw-sign paths, keys |
| `src/blockmango/config.py` | Environment and `.env` configuration |
| `src/blockmango/session.py` | `.sessions.json` cache |
| `src/blockmango/models.py` | `UserProfile`, `RankEntry`, and other models |
| `src/blockmango/submodules/` | Typed endpoint groups (`user`, `game`, `ranking`, ...) |
| `tools/get_device_values.py` | Android ID / `bm_ddh_id` extractor |
| `examples/` | CLI, Discord, and Telegram examples |
| `tests/` | Offline unit tests |
| `docs/` | API, authentication, leaderboard, and game-ID notes |

## Usage

### Login and sessions

`BmgAccount` stores the user id, access token, region, registration timestamps,
and the device values used for the session. The region is account-specific
(for example `RU` or `LATAM`) and is refreshed from the login response.

### Profiles and modules

```python
print(account.get_own_profile())
print(account.get_stats(account.uid))
print(account.friends.list_friends())
print(account.clan.get_own_clan())
```

The module list is in [Modules](#modules). `account.request()` is available for
any endpoint not wrapped by a module.

### Async

Most methods have an `async_` counterpart:

```python
import asyncio


async def main():
    account = BmgAccount("username", "password")
    if not await account.async_login():
        raise RuntimeError("login failed")
    profile = await account.async_get_own_profile()
    print(profile)
    await account.async_close()


asyncio.run(main())
```

## Leaderboards

Game leaderboard pages use:

```python
for entry in account.ranking.get_game_leaderboard_entries(
    "g1055", period="all", page=0, size=10
):
    print(entry.rank, entry.nick_name, entry.score, entry.display_value)

print(account.ranking.get_game_my_rank("g1055", period="week"))
```

- Periods: `all`, `week`, `month`.
- `page` is zero-based.
- `entry.score` is a Python integer, so scores above 64-bit range are exact.
- `entry.display_value` is the server's compact string such as `99.99Y`.
- `get_game_leaderboard()` returns the raw page envelope, including `pageInfo`
  and `remainTime`.
- `get_game_my_rank()` / `get_game_usage_leaderboard()` returns the account's
  own rank for the selected period.

See [docs/leaderboards.md](docs/leaderboards.md) for endpoint paths, parameter
details, response shapes, and observed WWE School Simulator data.

## Cookbook

### CLI / JSON output

`python
import dataclasses
import json

rows = account.ranking.get_game_leaderboard_entries(
    g1055, period=all, page=0, size=10
)
print(json.dumps([dataclasses.asdict(row) for row in rows], indent=2, ensure_ascii=False))
`

The JSON is ready to feed into a web dashboard, Discord webhook, Telegram
bridge, database, or another bot.

### Discord bot

`ash
python -m pip install discord.py
export DISCORD_TOKEN=your_bot_token
python examples/discord_leaderboard_bot.py
`

The example logs into Blockman GO with BmgAccount.from_env(), then serves
!rank [game_id] [period]. Enable **Message Content Intent** for the bot in
the Discord developer portal.

### Telegram bot

`ash
python -m pip install python-telegram-bot
export TELEGRAM_TOKEN=your_bot_token
python examples/telegram_leaderboard_bot.py
`

The example serves /rank [game_id] [period] and uses the async wrapper
methods.

### Other platforms

Any platform that can run Python can use the same calls. Return a JSON-safe
structure with dataclasses.asdict(), or call ccount.request() directly.
For async frameworks, use the sync_ methods and one BmgAccount per bot
process.

### Blockman Go itself

The wrapper is a normal HTTP client. For an in-game companion tool, run it as a
local service and feed results into the game's supported H5 bridge, overlay, or
chat/IM integration. Do not use it to bypass anti-cheat, automate unfair
gameplay, or spam chat. Follow the game's rules and use a test account for
development.

### Rate limits

Reuse the session, keep request rates low, and back off on code 100008,
code 567, and HTTP 429/5xx. Do not create a new login for every command.

## Known game IDs

Common IDs from the current client:

| Game | ID |
| --- | --- |
| Bed Wars | g1046 / g1008 |
| Murder Mystery | g1009 |
| TNT Run | g1010 |
| Hide and Seek | g1017 |
| Egg War | g1018 |
| Build Battle | g1023 |
| Hero Tycoon 2 | g1025 |
| Sky Royale | g1027 |
| WWE School Simulator | g1055 |

The full list and discovery notes are in [docs/games.md](docs/games.md). Use
ccount.game.get_game_list() for the current catalogue, and confirm an ID with
ccount.game.get_game_details(game_id) before relying on it.

## API reference

[docs/api-reference.md](docs/api-reference.md) is a generated index of every
public method, its HTTP endpoint, signature, and short description. Regenerate
it after adding or changing methods:

`ash
python tools/generate_api_docs.py
`

The hand-written guides are better for learning:

- [api-overview.md](docs/api-overview.md)
- [authentication.md](docs/authentication.md)
- [leaderboards.md](docs/leaderboards.md)
- [games.md](docs/games.md)

## Modules

| Module | What it covers |
| --- | --- |
| `account.user` | Profile, settings, VIP, feedback |
| `account.friends` | Friends, requests, tags, popularity |
| `account.clan` | Clan/tribe data and rankings |
| `account.ranking` | Global, clan, gold/diamond, and game rankings |
| `account.game` | Catalogue, details, auth, rooms, leaderboards |
| `account.activity` | Home page, events, ads, red packets |
| `account.mailbox` | Mail and CD-key redemption |
| `account.group` | Chat groups and notifications |
| `account.decoration` | Decorations and recommendations |
| `account.shop` | Shop data |
| `account.backpack` | Backpack and mining balances |
| `account.bedwar` | Bed Wars data |
| `account.pay` | Payments and Xsolla |
| `account.video` | Video/ad endpoints |
| `account.rongcloud` | RongCloud IM token |
| `account.gratitude` | Contributor recognitions |
| `account.remote_config` | Remote config files |
| `account.notice` | Server notices |
| `account.extended` | Additional 3.29.x endpoints |

`account.remote_config`, `account.notice`, and `account.extended` cover the
newer 3.29.x flows. `account.extended` methods are synchronous; use
`account.async_request()` inside async bots when a dedicated `async_` method does
not exist. See [docs/api-overview.md](docs/api-overview.md) for the important
endpoints and raw-request guidance.

## Authentication and signing

For normal requests:

```text
base = api_key + path + nonce + time + sorted_params + body + secret_key
x-sign = md5(md5(base) + userdeviceid)
```

For account/login paths and `/config/files/` or `/config/ml/files/` paths:

```text
x-sign = md5(base)
```

The wrapper also sends the current app headers (`appversion=5753`,
`appversionname=3.29.3`, Android `32`, package headers, `userdeviceid`, the
static `md5` fingerprint, and `userid`/`access-token` when logged in). Login and
auth-token calls include `bmg-device-id` and `bmg-sign`.

The 3.29.x client normally sends a 344-character native-encoded `access-token`.
In live testing the server accepted the raw login JWT for the tested account,
including profile, game details, game auth, config, and leaderboards. Some
accounts or sessions may require the native value; those endpoints return
`code 6` or `code 37`. A `token_encoder` callback can be passed to `BmgAccount`
when a working encoder is available.

See [docs/authentication.md](docs/authentication.md) for the full login,
signing, session, and access-token explanation.

## Testing

Install the package, then run the offline unit tests:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

The tests do not log in or contact the API. They cover signing paths, headers,
leaderboard parsing, and oversized scores.

Live checks:

```bash
python tools/get_device_values.py
python examples/leaderboards.py
```

Set `BMG_DEVICE_ID`, `BMG_BMDDH_ID`, `BMG_USERNAME`, and `BMG_PASSWORD` in
`.env` before running the live example. Optional bot examples:

```bash
python -m pip install discord.py
python examples/discord_leaderboard_bot.py

python -m pip install python-telegram-bot
python examples/telegram_leaderboard_bot.py
```

Set `DISCORD_TOKEN` or `TELEGRAM_TOKEN` in `.env` or the environment. On
PowerShell, use `$env:DISCORD_TOKEN="..."`.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `login()` returns `False` | Wrong password, wrong device values, region lock, or rate limit | Check credentials; run `tools/get_device_values.py`; wait if `100008` |
| `code 100008` / `access denied` | Account is device-bound, rate-limited, or blocked | Use the device values that belong to that account/install; wait and retry |
| `code 6` or `code 37` on authenticated calls | The session token/access-token is not accepted | Re-login; check device values; try `token_encoder` for that account |
| `code 100001` | Server time mismatch | The wrapper retries after time sync; check `BMG_TIME_API` |
| `code 567` | Server asks for a retry | Wait and retry with backoff |
| `bm_ddh_id was not found` | Wrong MMKV file or app not opened | Open the app once; inspect every file under the MMKV directory; run the extractor |
| `.env` is ignored | `python-dotenv` not installed or wrong working directory | `python -m pip install -e .`; run from the repo root; or export variables directly |
| Empty leaderboard | Account has no public rank for that period, or wrong game ID | Try `all`, `week`, `month`; confirm the ID with `get_game_details` |
| Scores look shortened (`99.99Y`) | `display_value` is a compact display string | Use `entry.score` for the exact Python integer |
| SSL warning | `BMG_VERIFY_SSL=false` | Set `BMG_VERIFY_SSL=true` if your certificate chain works |
| `adb root` fails | Production build or debugging disabled | Use a rooted emulator/image and enable USB debugging |

For a live login diagnosis, print the returned code and message instead of only
the boolean:

```python
account = BmgAccount("username", "password")
if not account.login():
    print("login failed; check code 100008 / 6 / 37 in docs/authentication.md")
```

## FAQ

**Do I need a rooted emulator?** You need the app's `bm_ddh_id`, which normally
comes from its MMKV data. A rooted emulator is the straightforward way. Use
device values from the same installation as the account.

**Can I use my main account?** You can, but use a test account for bots and
experiments. Automated writes and rate limits can affect a real account.

**Why are WWE School scores so large?** It is a simulator; the values are
legitimate. `entry.score` is exact. `entry.display_value` is the compact server
display such as `99.99Y`.

**Can I use this from Node.js, Go, or another language?** Yes. The wrapper is a
reference for the headers/signing; the API itself is HTTP/JSON. Use
`docs/authentication.md` to reproduce the headers, or run the Python client as a
local service.

**Can I make an in-game Blockman Go bot?** Use the game's supported H5/overlay or
chat/IM interfaces and follow its rules. The wrapper is not an anti-cheat
bypass and should not be used to automate unfair gameplay or spam.

**How do I add a new endpoint?** Call `account.request("GET", "/path", params=...)`
first. Once it is stable, add a method to the relevant module under
`src/blockmango/submodules/`, add an async counterpart, and a small offline test.

## Security

- Never commit `.env`, `.sessions.json`, or captured request logs. They can
  contain live credentials, device values, and tokens.
- Keep test credentials in environment variables or an ignored local file.
- Do not share raw captures; redact `access-token`, `q`, JWTs, and device values.
- Use test accounts for exploratory requests.

## Limitations

- The API is private and version-sensitive.
- Device values must match the account/install; some accounts are device-bound.
- Some accounts may require the native `Access-Token` transform.
- Region-specific endpoints and event endpoints can change or be unavailable.
- Methods that change account, friend, clan, inventory, or payment state are
  live operations; there is no dry-run layer.
- Sessions are written to `.sessions.json`, which is ignored by Git.

## License

MIT
