# bmgo-wrapper

[![Discord](https://img.shields.io/badge/Discord-Join%20Us-5865F2?logo=discord&logoColor=white)](https://discord.gg/PQhj8zcmBK)

A Python client for the Blockman GO (BlockyMods) HTTP API. It handles login, the
`x-sign` request format, the per-request access-token header, session storage,
profiles, games, leaderboards, friends, groups, and RongCloud group text
sending and listening.

This is an unofficial client. The API is private, version-sensitive, and can
change without notice.

> **Version status:** this repository targets Blockman GO **3.31.1**
> (`appVersion 5771`). The signing rules and device headers in this repository
> were checked against that build; older and newer clients are untested.
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
`pycryptodome`, `python-dotenv`, and `websocket-client`.

## Get device values

The API needs two values from the app installation:

| Variable | What it is |
| --- | --- |
| `BMG_DEVICE_ID` | the app's `android.id` from its MMKV store |
| `BMG_BMDDH_ID` | the `bm_ddh_id` string stored by Blockman GO |

`android.id` is written by the app, not by Android. Do not use
`Settings.Secure.ANDROID_ID` here; on the same device the two values differ, and
signing with the shell value makes the install look like a different device.

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
if not account.initialize():
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

## Friends and groups are loaded automatically

A successful `login()` collects the full friend list (up to 500) and every
group the account belongs to, then starts a lightweight background sync. The
default polling interval is 60 seconds and each account uses one daemon
thread.

```python
account = BmgAccount.from_env()
if not account.initialize():
    raise SystemExit("login failed")

print(account.social.groups)
print(account.social.friends)

def on_social_change(update):
    print("joined/added groups:", update.groups_added)
    print("left/removed groups:", update.groups_removed)
    print("added friends:", update.friends_added)
    print("removed friends:", update.friends_removed)

account.social.on_change(on_social_change)
```

`account.initialize()` is `login()` plus the directory snapshot and sync. If
you already call `login()`, that is enough: it hydrates and starts sync by
default. Use `account.login(load_social=False, start_sync=False)` when you want
to manage requests yourself.

```python
# Manual refresh / no background thread:
account.login(load_social=True, start_sync=False)
account.social.refresh()

# Script-style blocking wait for the next real change:
update = account.social.wait_for_update(timeout=30)
if update:
    print(update.group_ids_added, update.group_ids_removed)

# Stop polling before you discard the account:
account.social.stop()
account.close()
```

`SocialState` searches the loaded snapshot without another request:

```python
account.social.find_friends("alex")
account.social.find_groups("clan")
account.social.get_group(123456)
account.social.get_friend(654321)
```

After `restore_session()`, call `account.initialize_social()` (or
`await account.async_initialize_social()`). See
[Group chats and social state](docs/group-chat.md#account-social-state) for
the async and multi-account forms.

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

## Group chats and large friend lists

Group metadata and friend lists use the Blockman HTTP API. Both now use cached,
deduplicated snapshots instead of fetching one object at a time:

```python
groups = account.group.search_groups("clan")
group = account.group.find_group(name="My Clan")

friends = account.friends.list_all_friends()       # up to 500
alice = account.friends.find_friend("alice")
```

Group chat messages are carried by **RongCloud**, and sending works out of the
box. A normal `login()` installs the built-in pure-Python RongCloud transport:

```python
groups = account.social.groups
group_id = groups[0].group_id

result = account.group.send_text(group_id, "Hello group!")
print(result.message_uid)
```

There is no Android app, emulator, ADB, or Frida requirement. The transport
gets a RongCloud token from the Blockman account, resolves the RongCloud
WebSocket host, and publishes through the RongCloud RMTP protocol.

If you already have a different RongCloud client, `FunctionGroupTransport`
accepts any callable and returns a mapping or `GroupMessageResult`. Custom
transports can implement the same two-method contract. See
[Group chats](docs/group-chat.md) for the transport details and multi-account
examples.

### Incoming group messages

The RongCloud transport can also keep a listener open and deliver incoming
group messages:

```python
def on_message(message):
    if message.text == "!ping":
        account.group.send_text(message.group_id, "pong")

subscription = account.group.listen(
    on_message,
    group_ids=[123456],
    poll_interval=1.0,
)

# send while listening; this reuses the listener connection
account.group.send_text(123456, "hello")

subscription.stop()
```

Synchronous callbacks run on a worker thread, so a slow command handler does
not stop the socket from reading and `send_text()` is safe inside the callback.
The listener deduplicates by `message_uid` and advances its sync cursor. Image messages
arrive with `object_name="RC:ImgMsg"` and their URL is available as
`message.image_url`. `account.group.async_listen(...)` accepts an async
callback. Social-state polling is separate and still works normally. See
`examples/group_chat_listener.py` for a runnable example.

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
| [Group chats](docs/group-chat.md) | social state, built-in RongCloud sender, 500-friend caches, multi-account |

Regenerate the API reference after changing public methods:

```bash
python tools/generate_api_docs.py
```

## Tested scope

The main flows have been checked against Blockman GO 3.31.1:

- Unit tests: 77 passing, offline.
- Signing and access-token encoding reproduced from 3.31.1 client traffic.
- Device values read from the same 3.31.1 installation's MMKV store.
- Live friend and group snapshots loaded through the corrected endpoints.
- Live group text published through the pure-Python RongCloud transport, with
  a matching RongCloud message UID and `PubAck`.

The full 91-endpoint smoke sweep is still intentionally conservative; methods
not listed above remain exploratory until exercised against the current
server.

See [Limitations](#limitations) before using this with a real account.

## Project layout

```text
src/blockmango/
  account.py       login, requests, sessions, account facade
  crypto.py        signing and password encryption
  social.py        friend/group snapshots, diffs, polling
  rongcloud_transport.py
                   pure-Python RongCloud group sender
  rongcloud_listener.py
                   persistent incoming group-message listener
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
| `RongCloudTransportError` | log in first; check `BMG_RONG_APP_KEY`; close extra IM sessions on the same account |
| SSL warning | `BMG_VERIFY_SSL`; only enable verification if your certificate chain works |
| `adb root` fails | use a rooted emulator and enable USB debugging |

## Security

- Never commit `.env`, `.sessions.json`, or captured HTTP logs. They can contain
  live credentials, tokens, and device values.
- Use a test account for bots and experiments.
- Do not use this to bypass anti-cheat or automate unfair gameplay.

See [Authentication](docs/authentication.md) for session and token details.

## Limitations

- Targets Blockman GO 3.31.1; other builds may change headers, paths, or
  response shapes.
- Some accounts are device-bound. `android.id` and `bm_ddh_id` must come from the
  installation the account was registered on.
- The access-token header is generated locally, so it does not need the app at
  runtime, but it is still tied to the session token issued at login.
- Write actions have no dry-run layer.
- Live coverage is partial; a method existing in the package does not mean it
  has been verified against the current server.
- `remote_config.get_game_resource_config()` returned `code 6`, and
  `game.get_update_tip()` returned an empty response in the last live run.
- Group text sending and incoming group-message listening are built in and use
  RongCloud over WebSocket. Media messages and history sync are not included
  yet.

## License

MIT
