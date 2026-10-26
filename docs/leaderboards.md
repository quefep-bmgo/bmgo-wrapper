# Game leaderboards

The 3.29.x client uses two read-only game leaderboard endpoints.

## Game IDs

Known game IDs are listed in [games.md](games.md).

## Ranked list

`GET /game/api/v1/games/{gameId}/rank`

Headers:

- `language`: client language, e.g. `en_US`

Query parameters:

| Name | Type | Notes |
| --- | --- | --- |
| `type` | string | `all`, `week`, or `month` |
| `pageNo` | int | 0-based page index |
| `pageSize` | int | Page size; the client commonly uses 10 or 20 |

The endpoint is in `com.sandboxol.center.web.IGameApi.getGameRank` and returns
`RankInfo<CampaignRank>`.

Response shape:

```json
{
  "code": 1,
  "message": null,
  "data": {
    "pageInfo": {
      "pageNo": 0,
      "pageSize": 10,
      "totalPage": 10000,
      "totalSize": 99999,
      "data": [
        {
          "userId": 860875758,
          "nickName": "...",
          "rank": 1,
          "integral": 99994987733385001553625088,
          "displayValue": "99.99Y",
          "headPic": "http://...",
          "vip": 2,
          "avatarFrame": "frame_bronze.png",
          "colorfulNickName": null,
          "personalityItems": {}
        }
      ]
    },
    "remainTime": 459148000
  }
}
```

`remainTime` is a millisecond duration supplied by the server. A period can be
empty (`totalSize: 0`, `data: []`). An unsupported `type` returns `code: 3`
with `message: unsupported rank type: ...`.

## My rank

`GET /game/api/v1/games/{gameId}/uses/rank`

Headers:

- `language`: client language, e.g. `en_US`

Query parameters:

| Name | Type | Notes |
| --- | --- | --- |
| `type` | string | `all`, `week`, or `month` |

The endpoint is in `com.sandboxol.center.web.IGameApi.getGameMyRank` and returns
a single `CampaignRank`. An unranked account commonly returns `rank: 0` and
`integral: 0`.

## Score precision

`integral` is an integer. Some games, especially simulator-style games such as
WWE School Simulator (`g1055`), return values far above 64-bit range. Do not
convert these values to `float`; Python integers preserve them exactly.

`displayValue` is the server's compact display string (for example `"99.99Y"`)
and is kept separately by `RankEntry.display_value`.

## Python usage

```python
# Ranked list
for entry in account.ranking.get_game_leaderboard_entries(
    "g1055", period="all", page=0, size=10
):
    print(entry.rank, entry.nick_name, entry.score, entry.display_value)

# My rank for the same game and period
print(account.game.get_game_my_rank("g1055", period="all"))

# Raw page envelope, including pageInfo and remainTime
print(account.ranking.get_game_leaderboard("g1055", period="all", page=1, size=10))

# The game detail response also contains the top three for all/week/month
print(account.game.get_game_details("g1055")["data"]["gameRank"])
```

Async variants are available with the `async_` prefix.

## Observed WWE School Simulator (`g1055`) data

Captured on 2026-10-26. Leaderboards change continuously; figures are examples.

| Period | Ranked players | Pages | Top score | Display |
| --- | ---: | ---: | ---: | --- |
| `all` | 99,999 | 10,000 | 99,994,987,733,385,001,553,625,088 | `99.99Y` |
| `week` | 5,816 | 582 | 88,807,062,819,042,005,524,414,464 | `88.81Y` |
| `month` | 58,009 | 5,801 | 88,807,062,819,042,005,524,414,464 | `88.81Y` |

Page 1 of the all-time list started at rank 11 with a score of
`30,856,600,787,477,999,164,325,888` (`30.86Y`).
