import unittest

from blockmango.client import BmgClient
from blockmango.models import UserProfile
from blockmango.transport import GroupMessageResult


class FakeFriends:
    def __init__(self, profiles: list[UserProfile]):
        self.profiles = profiles

    def find_friends(self, query, max_friends=500, force_refresh=False):
        needle = str(query).casefold()
        return [p for p in self.profiles if needle in p.nick_name.casefold()]

    async def async_find_friends(self, query, max_friends=500, force_refresh=False):
        return self.find_friends(query, max_friends, force_refresh)


class FakeGroup:
    def send_text(self, group_id, text, *, ext_content=None, timeout=10.0):
        return GroupMessageResult(group_id=str(group_id), message_id="m1")

    async def async_send_text(self, group_id, text, *, ext_content=None, timeout=10.0):
        return self.send_text(group_id, text, ext_content=ext_content, timeout=timeout)


class FakeAccount:
    def __init__(self, username: str, uid: int, names: list[str]):
        self.username = username
        self.uid = uid
        self.friends = FakeFriends([UserProfile(user_id=uid * 100 + i, nick_name=n) for i, n in enumerate(names)])
        self.group = FakeGroup()


class MultiAccountTests(unittest.TestCase):
    def setUp(self):
        self.a = FakeAccount("alpha", 1, ["Alice", "Bob"])
        self.b = FakeAccount("beta", 2, ["Alicia", "Carol"])
        self.client = BmgClient([])
        self.client._pool = [self.a, self.b]
        self.client._by_name = {"alpha": self.a, "beta": self.b}

    def test_accounts_and_lookup(self):
        self.assertEqual(self.client.accounts, (self.a, self.b))
        self.assertIs(self.client.get_account("ALPHA"), self.a)
        self.assertIsNone(self.client.get_account("missing"))

    def test_find_friends_across_accounts(self):
        matches = self.client.find_friends("ali")
        self.assertEqual([(m.username, m.friend.nick_name) for m in matches], [
            ("alpha", "Alice"),
            ("beta", "Alicia"),
        ])
        filtered = self.client.find_friends("ali", usernames=["beta"])
        self.assertEqual([m.username for m in filtered], ["beta"])

    def test_send_group_text_uses_selected_account(self):
        result = self.client.send_group_text("alpha", 7, "hello")
        self.assertEqual(result.group_id, "7")
        self.assertEqual(result.message_id, "m1")
        with self.assertRaises(ValueError):
            self.client.send_group_text("missing", 7, "hello")


class AsyncMultiAccountTests(unittest.IsolatedAsyncioTestCase):
    async def test_async_find_friends(self):
        a = FakeAccount("alpha", 1, ["Alice"])
        b = FakeAccount("beta", 2, ["Alicia"])
        client = BmgClient([])
        client._pool = [a, b]
        client._by_name = {"alpha": a, "beta": b}
        matches = await client.async_find_friends("ali")
        self.assertEqual([m.username for m in matches], ["alpha", "beta"])


if __name__ == "__main__":
    unittest.main()
