# bmgo-wrapper

[![Discord](https://img.shields.io/badge/Discord-Join%20Us-5865F2?logo=discord&logoColor=white)](https://discord.gg/PQhj8zcmBK)

A Python client for the Blockman GO (BlockyMods) HTTP API. It handles login, the
`x-sign` request format, session storage, and the calls this repository uses
most: profiles, game data, and leaderboards.

This is an unofficial client. The API is private, version-sensitive, and can
change without notice.

> **Version status:** this repository targets Blockman GO **3.29.3**
> (`appVersion 5753`). Support for 3.30.x is not confirmed.
> See [Tested scope](#tested-scope).

[Install](#install) | [Device values](#get-device-values) | [First login](#first-login) | [Leaderboards](#leaderboards) | [Documentation](#documentation) | [Troubleshooting](#troubleshooting)

## Before you start

- Python 3.10 or newer.
- A Blockman GO account.
- `BMG_DEVICE_ID` and `BMG_BMDDH_ID` from the same app installation. Some
  accounts are device-bound, so values from another installation may be
  rejected.
- `adb` and a rooted emulator if you use the bundled device extractor.

## Install

From a checkout:

```bash
python -m pip install -e .
```

This installs the runtime dependencies, including `requests`, `httpx`,
`pycryptodome`, and `python-dotenv`.

## Get device values

The API needs two values from the app installation:

| Variable | What it is |
| --- | --- |
| `BMG_DEVICE_ID` | Android `Settings.Secure.ANDROID_ID` |
| `BMG_BMDDH_ID` | the `bm_ddh_id` string stored by Blockman GO |

Start the emulator, open Blockman GO at least once, and run:

```bash
python tools/get_device_values.py
```

The tool uses `adb`, pulls the app's MMKV data, and prints the two `.env`
lines. It does not print tokens or passwords.

Create a local config and fill in the values:

```bash
cp .env.example .env
```

On PowerShell:

```powershell
Copy-Item .env.example .env
```

Add `BMG_USERNAME` and `BMG_PASSWORD` as well. `.env` is ignored by Git and is
loaded from the current working directory, so run commands from the repository
root.

If the extractor cannot find the value, see
[Authentication](docs/authentication.md) and `tools/get_device_values.py`.
A `code 100008` login error usually means the device values do not match the
account.

## First login

```python
from blockmango import BmgAccount

account = BmgAccount.from_env()
if not account.login():
    raise SystemExit("login failed")

print(account.uid, account.nick, account.region)
print(account.get_own_profile())
```

`BmgAccount.from_env()` reads `.env` or the same variables from the environment.
If you keep credentials elsewhere, pass them explicitly:

```python
account = BmgAccount("username", "password")
```

Device values still come from the environment or config. `login()` performs a
fresh login; session reuse is covered in
[Authentication](docs/authentication.md#5-sessions).

## Leaderboards

```python
game_id = "g1055"
period = "week"

rows = account.ranking.get_game_leaderboard_entries(
    game_id, period=period, page=0, size=5
)
for entry in rows:
    print(entry.rank, entry.nick_name, entry.score, entry.display_value)

my_rank = account.ranking.get_game_my_rank(game_id, period=period)
print(my_rank)
```

- `period` is `all`, `week`, or `month`.
- `page` is zero-based.
- `entry.score` keeps the exact integer, even for very large simulator scores.
- `entry.display_value` is the server's short form, such as `99.99Y`.

More detail, including response shapes and observed data:
[Leaderboards](docs/leaderboards.md).

## Async

Most module methods have an `async_` counterpart.

```python
import asyncio

from blockmango import BmgAccount


async def main():
    account = BmgAccount.from_env()
    if not await account.async_login():
        raise SystemExit("login failed")

    rows = await account.ranking.async_get_game_leaderboard_entries(
        "g1055", period="all", page=0, size=5
    )
    for entry in rows:
        print(entry.rank, entry.nick_name, entry.display_value)

    await account.async_close()


if __name__ == "__main__":
    asyncio.run(main())
```

`account.extended` is synchronous; use `account.async_request()` for those
endpoints in async code. See [API overview](docs/api-overview.md#async).

## Common calls

| Task | Call |
| --- | --- |
| Your profile | `account.get_own_profile()` |
| Your stats | `account.get_stats(account.uid)` |
| Game catalogue | `account.game.get_game_list()` |
| Game details | `account.game.get_game_details("g1055")` |
| Global leaderboard | `account.ranking.get_global_overall()` |
| Raw endpoint | `account.request("GET", "/path", params={"pageNo": 0})` |

Use `account.request()` for a new endpoint before adding a typed method. The
generated method index is in [API reference](docs/api-reference.md).

## Examples

Set up `.env` first.

```bash
python examples/leaderboards.py
```

Optional `BMG_GAME_ID` changes the example game (default `g1055`).

Discord:

```bash
python -m pip install discord.py
python examples/discord_leaderboard_bot.py
```

Set `DISCORD_TOKEN` and enable **Message Content Intent** in the Discord
developer portal. The bot command is `!rank [game_id] [period]`.

Telegram:

```bash
python -m pip install python-telegram-bot
python examples/telegram_leaderboard_bot.py
```

Set `TELEGRAM_TOKEN`. The command is `/rank [game_id] [period]`.

## Documentation

| Guide | Use it for |
| --- | --- |
| [Authentication](docs/authentication.md) | device values, login, signing, tokens, sessions |
| [API overview](docs/api-overview.md) | module map, important endpoints, raw requests, errors |
| [API reference](docs/api-reference.md) | generated list of methods, signatures, and endpoints |
| [Leaderboards](docs/leaderboards.md) | periods, response shapes, large scores, observed data |
| [Game IDs](docs/games.md) | known IDs and how to check them |

Regenerate the API reference after changing public methods:

```bash
python tools/generate_api_docs.py
```

## Tested scope

The live checks were read-only and intended to catch obvious endpoint drift, not
to certify every method:

- Offline tests: 9 passing.
- Live smoke: 91 captured GET endpoints; 83 returned `code 1`, 8 returned other
  codes. 30 module calls were also checked.
- Write, social, purchase, and account-changing endpoints were not executed.
- 3.30.x has not been tested. Treat untested methods as exploratory.

See [Limitations](#limitations) before using this with a real account.

## Project layout

```text
src/blockmango/
  account.py       login, requests, sessions, account facade
  crypto.py        signing and password encryption
  constants.py     app version, headers, endpoint rules
  submodules/      typed endpoint groups
tools/             device extractor and API-doc generator
examples/          runnable CLI, Discord, and Telegram examples
docs/              hand-written guides and generated API reference
tests/             offline unit tests
```

## Testing

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

The offline tests do not contact the API. For a live check:

```bash
python examples/leaderboards.py
```

Live checks need valid `.env` values.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `login()` returns `False` | credentials, device values, region, or rate limit |
| `code 100008` / access denied | device values from the account's own install; wait if rate-limited |
| `code 6` or `code 37` | re-login; check device values; see the Access-Token note in Authentication |
| `.env` not read | run from the repo root; install the package; check `python-dotenv` |
| `bm_ddh_id` not found | open the app once, use a rooted emulator, run the extractor |
| Empty leaderboard | try other periods; confirm the game ID with `get_game_details` |
| Score shows `99.99Y` | use `entry.score` for the exact integer |
| SSL warning | `BMG_VERIFY_SSL`; only enable verification if your certificate chain works |
| `adb root` fails | use a rooted emulator and enable USB debugging |

## Security

- Never commit `.env`, `.sessions.json`, or captured HTTP logs. They can contain
  live credentials, tokens, and device values.
- Use a test account for bots and experiments.
- Do not use this to bypass anti-cheat or automate unfair gameplay.

See [Authentication](docs/authentication.md) for session and token details.

## Limitations

- Targets Blockman GO 3.29.3; later clients may change headers, paths, or
  response shapes.
- Some accounts are device-bound and may require the native Access-Token
  transform.
- Write actions have no dry-run layer.
- Live coverage is partial; a method existing in the package does not mean it
  has been verified against the current server.
- `remote_config.get_game_resource_config()` returned `code 6`, and
  `game.get_update_tip()` returned an empty response in the last live run.

## License

MIT
