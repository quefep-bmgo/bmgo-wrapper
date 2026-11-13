import unittest

from blockmango.submodules.user import UserAPI


class FakeFriends:
    def search(self, query, page=1, size=10):
        return [(query, page, size)]

    async def async_search(self, query, page=1, size=10):
        return [(query, page, size)]


class FakeAccount:
    def __init__(self):
        self.friends = FakeFriends()


class UserSearchTests(unittest.TestCase):
    def test_search_by_name_delegates_to_fuzzy_profile_search(self):
        api = UserAPI(FakeAccount())
        self.assertEqual(api.search_by_name("Player One", page=2, size=5),
                         [("Player One", 2, 5)])

    def test_async_search_by_name_delegates_to_fuzzy_profile_search(self):
        import asyncio

        api = UserAPI(FakeAccount())
        self.assertEqual(asyncio.run(api.async_search_by_name("Player One", page=3, size=7)),
                         [("Player One", 3, 7)])


if __name__ == "__main__":
    unittest.main()
