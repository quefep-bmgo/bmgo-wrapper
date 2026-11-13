# bmgo-wrapper

An unofficial Python client for Blockman GO's (BlockyMods) HTTP API. The
wrapper handles request signing, login, sessions, and typed helpers for common
player, clan, game, and leaderboard calls.

The API is private and can change without notice. A method being present does
not mean its endpoint has been verified against every app release.

## Quick start

You need Python 3.10+, a Blockman GO account, and device values from the same
app installation as that account.

```bash
python -m pip install -e .
cp .env.example .env
python tools/get_device_values.py --waydroid --output-env .env
```

The extractor reads the app's `android.id` and `bm_ddh_id` from its MMKV store.
For Waydroid it uses one `sudo waydroid shell` read because `adb root` is not
available there. For a conventional rooted emulator, omit `--waydroid`.

The official 3.31.1 app package is
`com.sandboxol.blockymods.channel.official`. Open the app once before extracting
values. `--output-env` preserves other settings and writes the file with
permissions `0600`.

The extractor updates only the two device-value lines and preserves the rest
of `.env`. Add your `BMG_USERNAME` and `BMG_PASSWORD` to that file before
signing in.

`.env` is ignored by Git. Never paste its contents into an issue or commit it.

## Sign in and make a request

```python
from blockmango import BmgAccount

account = BmgAccount.from_env()
try:
    if not account.login():
        raise RuntimeError(f"Blockman GO login failed (code {account.last_login_code})")
    print("Signed in as", account.uid)
    profile = account.get_own_profile()
    print(profile)
finally:
    account.close()
```

You can also provide the username and password explicitly with
`BmgAccount(username, password)`. Device values are still read from the
environment or a `Config` object.

Some accounts are bound to a particular installation. If login returns
`code 100008`, sign in to that account in the matching app installation and
use its device values. A session's `Access-Token` may require the app's
per-request native transform; see [Authentication](docs/authentication.md).
Login uses the configured device pair by default; the older remote device pool
is opt-in with `BMG_USE_DEVICE_POOL=true`.

## Look up players and clans

```python
# Lookup by numeric player ID.
target_uid = 123456789
player = account.user.lookup(target_uid)
if player:
    print(player.nick_name)
    print(player.clan_name)

# Nickname search is fuzzy; inspect candidates rather than assuming one match.
candidates = account.user.search_by_name("Player name", page=1, size=10)
for player in candidates:
    print(player.user_id, player.nick_name)

# Search clans by name or fetch one by its ID.
clans = account.clan.search("Clan name", page=0, size=10)
clan = account.clan.get_info(clan_id=12345)
```

`lookup()` returns `None` when the profile endpoint has no result. Nickname
search may return no matches or several fuzzy matches.

## Game leaderboards

Use a known game ID for the most reliable lookup:

```python
rows = account.ranking.get_game_leaderboard_entries(
    "g1019", period="all", page=0, size=10
)
for row in rows:
    print(row.rank, row.nick_name, row.score, row.display_value)
```

`period` accepts `all`, `week`, or `month`; `page` is zero-based. `score` is
kept as an exact Python integer, while `display_value` is the compact value
shown by the server.

For a title, the wrapper searches the current game catalogue:

```python
rows = account.ranking.get_game_leaderboard_entries_by_name(
    "Bed Wars", period="week", page=0, size=10
)
```

If a title has multiple IDs, the helper raises `ValueError`; pass the ID you
want instead. Titles absent from the current catalogue cannot be resolved by
name. See [Known game IDs](docs/games.md) for examples and ways to verify them.

## Async use

Most endpoint helpers have an `async_` counterpart. The account object's
session state is not designed for concurrent login/session mutation.

```python
import asyncio
from blockmango import BmgAccount

async def main():
    account = BmgAccount.from_env()
    try:
        if not await account.async_login():
            raise RuntimeError(f"Blockman GO login failed (code {account.last_login_code})")
        rows = await account.ranking.async_get_game_leaderboard_entries(
            "g1019", period="all", page=0, size=5
        )
        print(len(rows))
    finally:
        await account.async_close()

asyncio.run(main())
```

`account.extended` is synchronous; use `account.async_request()` for an async
raw endpoint call.

## Modules and documentation

The account exposes groups such as `account.user`, `friends`, `clan`,
`ranking`, `game`, `activity`, `mailbox`, `shop`, `pay`, and `remote_config`.
The full method index is in [API reference](docs/api-reference.md).

| Guide | What it covers |
| --- | --- |
| [Authentication](docs/authentication.md) | Device values, login, signing, tokens, and sessions |
| [API overview](docs/api-overview.md) | Module map, raw requests, and response/error behavior |
| [Leaderboards](docs/leaderboards.md) | Periods, pagination, models, and large scores |
| [Known game IDs](docs/games.md) | Example IDs and catalogue lookup |
| [3.31.1 path candidates](docs/api-candidates-3.31.1.csv) | Static APK string inventory; not an endpoint contract |

For an endpoint without a typed helper, use `account.request()`:

```python
response = account.request(
    "GET",
    "/game/api/v1/games/g1019/rank",
    params={"type": "all", "pageNo": 0, "pageSize": 10},
)
```

Use `account.async_request()` for the async equivalent. The server normally
returns a dictionary containing `code`, `message`, and `data`; check `code`
before treating `data` as a successful result. Transport failures use
`code == -1`.

## Tested scope

The current branch targets app version **3.31.1 / 5771**. The app fingerprint
and app-scoped signing ID were observed from the installed Waydroid app.

The latest live, read-only checks verified player profile lookup, clan search
and lookup by ID, and five-row leaderboards for three known game IDs. A game
catalogue page also returned successfully. The live catalogue did not contain
every documented title, so some title lookups still require a known game ID.
The API login call returned `100008` for the test account even though signing
into that account in the app worked. The verified API calls used the app's
per-request native token signer through the supported `token_encoder` callback;
the wrapper does not ship a standalone native encoder. These checks do not
certify every method in the package.

Offline tests:

```bash
python -m unittest discover -s tests -v
```

The tests cover configuration, signing, device-value parsing, nickname/title
helpers, and leaderboard parsing. They do not contact Blockman GO servers.

## Safety and limitations

- This is an unofficial client for a private, version-sensitive API.
- Read helpers are safe for exploration; methods named `buy`, `claim`, `join`,
  `send_request`, `change_*`, `delete_*`, `like`, or similar can change a live
  account or spend currency. Check the method before calling it.
- Payments, purchases, account changes, friend/clan mutations, and gameplay
  automation are not covered by the live smoke tests.
- Keep `.env`, `.sessions.json`, tokens, device values, and captured request
  data private. Extractor and session files are written with `0600` permissions
  on Unix. The wrapper does not print secrets, but your own logging code can.
- The API and its access-token requirements can change between app versions.

## Troubleshooting

| Result | What to check |
| --- | --- |
| `login()` returns `False` | Credentials, app version, region, and device values |
| `code 100008` | Device-bound access or rate limiting; use the matching app install |
| `code 6` or `code 37` | The session may need the app's native Access-Token transform |
| Empty player/clan search | Search is fuzzy; try an ID or a different spelling |
| Empty leaderboard | Confirm the game ID and try another period |
| `adb root` is unavailable | Use `python tools/get_device_values.py --waydroid` |
| `.env` is not loaded | Run from the repository root and install the package |

## Contributing

Run the offline test suite before submitting changes. Treat DEX string scans as
leads only; verify new endpoint behavior against the installed app before
describing it as live-tested.

## License

MIT.
