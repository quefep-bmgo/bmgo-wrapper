# API overview

For the generated method/endpoint index, see [api-reference.md](api-reference.md).

The wrapper targets the Android client HTTP API at
`https://gw.sandboxol.com` and mirrors the v3.29.3 request headers and signing
rules. All responses use the same envelope:

```json
{ "code": 1, "message": "OK", "data": {}, "other": null }
```

Use the typed module methods when available. For anything not wrapped, use:

```python
account.request("GET", "/some/path", params={"pageNo": 0})
account.async_request("POST", "/some/path", body={"key": "value"})
```

## Account groups

| Group | Purpose |
| --- | --- |
| `account.user` | Profile, settings, VIP, feedback |
| `account.friends` | Friends, requests, tags, popularity |
| `account.clan` | Clan/tribe data, members, rankings |
| `account.ranking` | Global, clan, gold/diamond, and per-game ranks |
| `account.game` | Game catalogue, details, auth, rooms, leaderboards |
| `account.activity` | Home page, events, ads, red packets |
| `account.mailbox` | Mail and CD-key redemption |
| `account.group` | Chat groups and notifications |
| `account.decoration` | Decoration resources and recommendations |
| `account.shop` | Shop data |
| `account.backpack` | Backpack and mining balances |
| `account.bedwar` | Bed Wars-specific data |
| `account.pay` | Payment and Xsolla data |
| `account.video` | Video/ad endpoints |
| `account.rongcloud` | RongCloud IM token |
| `account.gratitude` | Contributor-recognition flow |
| `account.remote_config` | `/config/files` and `/config/ml/files` resources |
| `account.notice` | Server notices |
| `account.extended` | Additional 3.29.x activity/pay/user/game endpoints |

## Important new endpoints

| Method | Endpoint | Wrapper |
| --- | --- | --- |
| Game details | `GET /game/api/v3/games/{gameId}` | `game.get_game_details` |
| Game auth | `GET /game/api/v3/game/auth` | `game.game_auth` |
| Party auth | `GET /game/api/v3/party/auth` | `game.party_auth_v3` |
| Game leaderboard | `GET /game/api/v1/games/{gameId}/rank` | `game.get_game_leaderboard`, `ranking.get_game_leaderboard_entries` |
| My game rank | `GET /game/api/v1/games/{gameId}/uses/rank` | `game.get_game_my_rank` |
| Game revision list | `GET /game/api/v2/game/revision/all/list/by/condition/combine` | `extended.game_revision_combine` |
| App engine update | `GET /game/api/v2/games/app-engine/check-update` | `extended.check_app_engine_update` |
| Remote config | `GET /config/files/...`, `GET /config/ml/files/...` | `remote_config` |
| Server notice | `GET /notice/api/v1/server-notice/config` | `notice.get_server_notice_config` |
| Product info | `GET /pay/api/v1/product/info/batch/get` | `extended.product_info_batch` |
| CD-key redeem | `POST /mailbox/api/v1/cdkey/redeem` | `extended.redeem_cdkey` |

## Leaderboards

See [leaderboards.md](leaderboards.md) for parameters, pagination, large
integer scores, `displayValue`, my-rank behavior, and observed data.

## Async

Most module methods have an `async_` counterpart. `account.extended` is
synchronous; use `account.async_request()` for async callers. Only the HTTP calls
are asynchronous; the account object is not designed for concurrent mutation of
session state.

## Errors

The wrapper returns the server envelope for normal responses. Transport errors
are returned as `{"code": -1, "message": "..."}` by `request()`; the typed
modules generally follow the same convention. See
[authentication.md](authentication.md) for common server codes.

## Raw requests

`account.request()` uses the same header/sign/token machinery as the typed
methods, so any newly discovered endpoint can be called immediately:

```python
account.request(
    "GET",
    "/game/api/v1/games/g1055/rank",
    params={"type": "all", "pageNo": 0, "pageSize": 10},
    language="en_US",
)
```

Use this for exploratory work, then promote stable calls into a module.
