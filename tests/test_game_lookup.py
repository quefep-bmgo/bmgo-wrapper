import asyncio
import unittest

from blockmango.submodules.game import GameAPI
from blockmango.submodules.ranking import RankingAPI


CATALOGUE = {
    "code": 1,
    "data": {
        "list": [
            {"gameId": "g1019", "gameTitle": "Alien Attack"},
            {"gameId": "g1008", "gameTitle": "Bed Wars"},
            {"gameId": "g1046", "gameTitle": "Bed Wars"},
            {"gameId": "g1009", "gameTitle": "Murder Mystery"},
        ]
    },
}


class FakeAccount:
    uid = 42

    def __init__(self):
        self.calls = []
        self.game = GameAPI(self)

    def request(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs))
        if path == "/game/api/v2/game/revision/list/by/condition":
            return CATALOGUE
        if path.endswith("/rank"):
            return {
                "code": 1,
                "data": {"pageInfo": {"data": [{
                    "userId": 7, "nickName": "Player", "rank": 1,
                    "integral": 12, "displayValue": "12",
                }]}},
            }
        return {"code": 1, "data": {}}

    async def async_request(self, method, path, **kwargs):
        return self.request(method, path, **kwargs)


class GameLookupTests(unittest.TestCase):
    def test_game_id_skips_catalogue_request(self):
        account = FakeAccount()
        self.assertEqual(account.game.resolve_game_id("G1019"), "g1019")
        self.assertEqual(account.calls, [])

    def test_resolves_exact_or_unique_partial_title(self):
        api = FakeAccount().game
        self.assertEqual(api.resolve_game_id("alien attack"), "g1019")
        self.assertEqual(api.resolve_game_id("murder"), "g1009")

    def test_catalogue_uses_live_default_sort_and_page_size(self):
        account = FakeAccount()
        account.game.get_game_list()
        _, _, kwargs = account.calls[-1]
        self.assertEqual(kwargs["params"]["sortType"], "complex")
        self.assertEqual(kwargs["params"]["pageSize"], 20)

    def test_ambiguous_title_requires_a_game_id(self):
        with self.assertRaisesRegex(ValueError, "g1008.*g1046"):
            FakeAccount().game.resolve_game_id("Bed Wars")

    def test_unknown_title_is_reported(self):
        with self.assertRaises(LookupError):
            FakeAccount().game.resolve_game_id("not a real game")

    def test_leaderboard_by_title_resolves_and_fetches_rows(self):
        account = FakeAccount()
        rows = RankingAPI(account).get_game_leaderboard_entries_by_name("Alien Attack")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].user_id, 7)
        rank_calls = [call for call in account.calls if call[1].endswith("/rank")]
        self.assertEqual(rank_calls[0][1], "/game/api/v1/games/g1019/rank")

    def test_async_resolves_title(self):
        api = FakeAccount().game
        self.assertEqual(asyncio.run(api.async_resolve_game_id("Alien Attack")), "g1019")


if __name__ == "__main__":
    unittest.main()
