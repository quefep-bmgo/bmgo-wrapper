import unittest

from blockmango.models import RankEntry
from blockmango.submodules.ranking import RankingAPI

SAMPLE = {
    "code": 1,
    "data": {
        "pageInfo": {
            "pageNo": 0,
            "pageSize": 10,
            "totalPage": 10000,
            "totalSize": 99999,
            "data": [
                {
                    "userId": 860875758,
                    "nickName": "cat",
                    "rank": 1,
                    "integral": 99994987733385001553625088,
                    "displayValue": "99.99Y",
                    "vip": 2,
                    "avatarFrame": "frame_bronze.png",
                },
                {
                    "userId": 734866064,
                    "nickName": "Nova",
                    "rank": 2,
                    "integral": 98979840858314995027410944,
                    "displayValue": "98.98Y",
                    "vip": 0,
                    "avatarFrame": "frame_blue_shine_ACW.svga",
                },
            ],
        },
        "remainTime": 459148000,
    },
}


class FakeGame:
    def get_game_leaderboard(self, game_id, period="all", page=0, size=10,
                             game_version=None, language="en_US"):
        return SAMPLE

    def get_game_my_rank(self, game_id, period="all", language="en_US"):
        return {"code": 1, "data": {"userId": 1, "rank": 5821, "integral": 0, "displayValue": "0"}}


class FakeAccount:
    def __init__(self):
        self.game = FakeGame()


class LeaderboardTests(unittest.TestCase):
    def test_large_integer_scores_are_exact(self):
        entry = RankEntry.from_dict(SAMPLE["data"]["pageInfo"]["data"][0])
        self.assertEqual(entry.score, 99994987733385001553625088)
        self.assertEqual(entry.display_value, "99.99Y")
        self.assertEqual(entry.vip, 2)
        self.assertEqual(entry.avatar_frame, "frame_bronze.png")

    def test_entries_parse_page_info_data(self):
        rows = RankingAPI(FakeAccount()).get_game_leaderboard_entries("g1055")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].rank, 1)
        self.assertEqual(rows[1].score, 98979840858314995027410944)

    def test_my_rank_is_a_single_object(self):
        data = RankingAPI(FakeAccount()).get_game_my_rank("g1055", period="week")["data"]
        self.assertEqual(data["rank"], 5821)
        self.assertEqual(data["integral"], 0)


if __name__ == "__main__":
    unittest.main()
