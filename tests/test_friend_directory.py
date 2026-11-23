import unittest

from blockmango.models import UserProfile
from blockmango.submodules.friends import FriendsAPI


def friend(uid: int, name: str) -> dict:
    return {"userId": uid, "nickName": name}


class FakeFriendsAccount:
    def __init__(self, pages: dict[int, list[dict]]):
        self.pages = pages
        self.requests: list[tuple[str, dict]] = []

    def request(self, method, path, params=None, body=None, language=None, **kwargs):
        self.requests.append((path, dict(params or {})))
        page = int((params or {}).get("pageNo", 1))
        items = self.pages.get(page, [])
        return {"code": 1, "data": {"data": items}}

    async def async_request(self, method, path, params=None, body=None, language=None, **kwargs):
        return self.request(method, path, params, body, language, **kwargs)


def pages_of(count: int, page_size: int = 50) -> dict[int, list[dict]]:
    pages: dict[int, list[dict]] = {}
    for index in range(0, count, page_size):
        page = index // page_size
        pages[page] = [friend(index + offset + 1, f"Player{index + offset + 1}") for offset in range(page_size)]
    return pages


class FriendDirectoryTests(unittest.TestCase):
    def test_paginates_and_caps_at_500(self):
        account = FakeFriendsAccount(pages_of(620))
        friends = FriendsAPI(account).list_all_friends(500)
        self.assertEqual(len(friends), 500)
        self.assertEqual(len(account.requests), 10)
        self.assertEqual(friends[0].user_id, 1)
        self.assertEqual(friends[-1].user_id, 500)

    def test_friend_list_is_zero_based_and_uses_list_endpoint(self):
        account = FakeFriendsAccount({0: [friend(1, "One")], 1: []})
        api = FriendsAPI(account)
        friends = api.list_all_friends()
        self.assertEqual([f.user_id for f in friends], [1])
        self.assertEqual(account.requests[0][0], "/friend/api/v1/friends")
        self.assertEqual(account.requests[0][1]["pageNo"], 0)

    def test_deduplicates_across_pages(self):
        account = FakeFriendsAccount({
            0: [friend(1, "One"), friend(2, "Two")],
            1: [friend(2, "Two"), friend(3, "Three")],
            2: [],
        })
        friends = FriendsAPI(account).list_all_friends(50, page_size=2)
        self.assertEqual([item.user_id for item in friends], [1, 2, 3])

    def test_cache_avoids_repeated_requests(self):
        account = FakeFriendsAccount(pages_of(120))
        api = FriendsAPI(account)
        first = api.list_all_friends(500)
        request_count = len(account.requests)
        second = api.list_all_friends(500)
        self.assertEqual([f.user_id for f in first], [f.user_id for f in second])
        self.assertEqual(len(account.requests), request_count)
        api.list_all_friends(500, force_refresh=True)
        self.assertGreater(len(account.requests), request_count)

    def test_search_is_exact_then_prefix_then_substring(self):
        account = FakeFriendsAccount({0: [
            friend(1, "Alice"),
            friend(2, "AliceInWonderland"),
            friend(3, "Malice"),
            friend(4, "Bob"),
        ], 1: []})
        api = FriendsAPI(account)
        self.assertEqual([f.user_id for f in api.find_friends("alice")], [1, 2, 3])
        self.assertEqual(api.find_friend("ALICE").user_id, 1)
        self.assertEqual(api.find_friend("4").user_id, 4)

    def test_invalidate_forces_refresh(self):
        account = FakeFriendsAccount(pages_of(60))
        api = FriendsAPI(account)
        api.list_all_friends(500)
        count = len(account.requests)
        api.invalidate_cache()
        api.list_all_friends(500)
        self.assertGreater(len(account.requests), count)

    def test_user_profile_parsing(self):
        profile = UserProfile.from_dict(friend(7, "Seven"))
        self.assertEqual(profile.user_id, 7)
        self.assertEqual(profile.nick_name, "Seven")

    def test_user_profile_parses_live_level_and_vip_fields(self):
        profile = UserProfile.from_dict({
            "userId": 8,
            "nickName": "Eight",
            "userLevel": 12,
            "vipLv": 6,
            "sex": 1,
        })
        self.assertEqual(profile.level, 12)
        self.assertEqual(profile.vip_level, 6)
        self.assertEqual(profile.gender, 1)


class AsyncFriendDirectoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_async_list_and_find(self):
        account = FakeFriendsAccount({0: [friend(1, "Alice"), friend(2, "Bob")], 1: []})
        api = FriendsAPI(account)
        friends = await api.async_list_all_friends(500)
        self.assertEqual(len(friends), 2)
        matches = await api.async_find_friends("ali")
        self.assertEqual(matches[0].user_id, 1)


if __name__ == "__main__":
    unittest.main()
