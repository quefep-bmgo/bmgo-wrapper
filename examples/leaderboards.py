"""Print a game leaderboard and the current account's rank.

Set the device and login values in the environment; do not hard-code them:

    BMG_DEVICE_ID=...
    BMG_BMDDH_ID=...
    BMG_USERNAME=...
    BMG_PASSWORD=...

Optional: ``BMG_GAME_ID`` (defaults to ``g1055``, WWE School Simulator).
"""

import os

from blockmango import BmgAccount


def main() -> None:
    username = os.environ.get("BMG_USERNAME")
    password = os.environ.get("BMG_PASSWORD")
    if not username or not password:
        raise SystemExit("Set BMG_USERNAME and BMG_PASSWORD in the environment")

    account = BmgAccount(username, password)
    if not account.login():
        raise SystemExit("Blockman GO login failed")

    game_id = os.environ.get("BMG_GAME_ID", "g1055")
    for period in ("all", "week", "month"):
        print(f"\n{game_id} / {period}")
        rows = account.ranking.get_game_leaderboard_entries(
            game_id, period=period, page=0, size=5
        )
        for entry in rows:
            print(f"  #{entry.rank:<3} {entry.nick_name!r}  {entry.score}  ({entry.display_value})")
        my_rank = account.game.get_game_my_rank(game_id, period=period).get("data") or {}
        print(f"  my rank: {my_rank.get('rank')}  score: {my_rank.get('integral')}")


if __name__ == "__main__":
    main()
