# Known game IDs

Game IDs are the values used in endpoints such as:

```text
GET /game/api/v1/games/{gameId}/rank
GET /game/api/v1/games/{gameId}/uses/rank
```

These IDs are examples captured from the current client. They can change, and
some IDs share a leaderboard.

| Game | ID |
| --- | --- |
| Bed Wars | `g1046` / `g1008` |
| Murder Mystery | `g1009` |
| TNT Run | `g1010` |
| Zombie Infecting | `g1013` |
| Borderline | `g1016` |
| Hide and Seek | `g1017` |
| Egg War | `g1018` |
| Aliens Attack | `g1019` |
| Build Battle | `g1023` |
| Hero Tycoon 2 | `g1025` |
| TNT Tag | `g1026` |
| Sky Royale | `g1027` |
| Snowman Defender | `g1030` |
| WWE School Simulator | `g1055` |

Use the API to confirm a title instead of trusting a hard-coded table:

```python
details = account.game.get_game_details("g1055")
print(details["data"]["gameTitle"])
```

You can also inspect the current game list:

```python
games = account.extended.game_revision_combine(page=0, size=20)
print(games)
```

The response shape of the game-list endpoint can vary. `get_game_details`
is the most reliable way to verify a known ID.

## Leaderboards

Use `all`, `week`, or `month`:

```python
for entry in account.ranking.get_game_leaderboard_entries(
    "g1055", period="all", page=0, size=10
):
    print(entry.rank, entry.nick_name, entry.score, entry.display_value)
```

WWE School Simulator is a simulator game and its scores can be enormous.
`score` is a Python integer and `display_value` is the short server string such
as `99.99Y`. See [leaderboards.md](leaderboards.md) for the full schema.

## Finding a game ID

1. Open the game detail page and look at the URL/route data.
2. Capture the app's HTTP traffic and find `/games/{gameId}`.
3. Call `get_game_details` for candidate IDs and check `gameTitle`.
4. Use `extended.game_revision_combine` for the current catalogue.

Avoid scraping every possible ID. Use the app's catalogue or a known ID first.
