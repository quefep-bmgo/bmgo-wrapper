import asyncio
import tempfile
import unittest
from unittest.mock import patch

from blockmango.account import BmgAccount
from blockmango.config import Config
from blockmango.models import GroupInfo, UserProfile
from blockmango.social import SocialState


def friend(uid: int, name: str) -> UserProfile:
    return UserProfile(user_id=uid, nick_name=name)


def group(gid: int, name: str) -> GroupInfo:
    return GroupInfo(
        group_id=gid,
        group_name=name,
        owner_id=1,
        member_count=1,
        max_members=500,
        invite_status=1,
    )


class StubFriends:
    def __init__(self, items):
        self.items = list(items)
        self.calls = 0

    def list_all_friends(self, max_friends=500, page_size=50, ttl=300.0, force_refresh=False):
        self.calls += 1
        return list(self.items[:max_friends])

    async def async_list_all_friends(self, max_friends=500, page_size=50, ttl=300.0, force_refresh=False):
        return self.list_all_friends(max_friends, page_size, ttl, force_refresh)


class StubGroups:
    def __init__(self, items):
        self.items = list(items)
        self.calls = 0

    def list_all_groups(self, max_groups=1000, page_size=50, ttl=300.0, force_refresh=False):
        self.calls += 1
        return list(self.items[:max_groups])

    async def async_list_all_groups(self, max_groups=1000, page_size=50, ttl=300.0, force_refresh=False):
        return self.list_all_groups(max_groups, page_size, ttl, force_refresh)


class StubAccount:
    uid = 1

    def __init__(self, friends, groups):
        self.friends = StubFriends(friends)
        self.group = StubGroups(groups)


class SocialStateTests(unittest.TestCase):
    def test_initial_load_then_added_and_removed(self):
        one = friend(1, "One")
        two = friend(2, "Two")
        alpha = group(10, "Alpha")
        account = StubAccount([one, two], [alpha])
        state = SocialState(account)
        updates = []
        state.subscribe(updates.append)

        initial = state.refresh()
        self.assertTrue(initial.initial)
        self.assertTrue(initial.changed)
        self.assertEqual(initial.snapshot.groups, (alpha,))
        self.assertEqual(initial.snapshot.friends, (one, two))
        self.assertEqual(state.get_group(10), alpha)
        self.assertEqual(state.get_friend(2), two)
        self.assertEqual(updates, [])  # initial hydration is not an "added" event

        unchanged = state.refresh()
        self.assertFalse(unchanged.changed)
        self.assertEqual(unchanged.snapshot.revision, initial.snapshot.revision)
        self.assertEqual(updates, [])

        three = friend(3, "Three")
        beta = group(20, "Beta")
        account.friends.items = [one, three]
        account.group.items = [beta]
        changed = state.refresh()
        self.assertTrue(changed.changed)
        self.assertEqual(changed.group_ids_added, (20,))
        self.assertEqual(changed.group_ids_removed, (10,))
        self.assertEqual(changed.friend_ids_added, (3,))
        self.assertEqual(changed.friend_ids_removed, (2,))
        self.assertEqual(updates, [changed])
        self.assertEqual(changed.snapshot.revision, initial.snapshot.revision + 1)

    def test_search_and_unsubscribe(self):
        account = StubAccount(
            [friend(1, "Alice"), friend(2, "AliceInWonderland"), friend(3, "Bob")],
            [group(10, "Clan Alpha"), group(20, "Trading")],
        )
        state = SocialState(account)
        state.refresh()
        self.assertEqual([f.user_id for f in state.find_friends("alice")], [1, 2])
        self.assertEqual([g.group_id for g in state.find_groups("alpha")], [10])

        seen = []
        subscription = state.subscribe(seen.append)
        subscription.unsubscribe()
        account.group.items = []
        state.refresh()
        self.assertEqual(seen, [])

    def test_polling_emits_only_real_changes(self):
        account = StubAccount([friend(1, "One")], [group(10, "Alpha")])
        state = SocialState(account)
        state.refresh()
        state.start(interval=0.01, initial=False)
        try:
            account.group.items = [group(20, "Beta")]
            update = state.wait_for_update(timeout=2.0)
            self.assertIsNotNone(update)
            self.assertEqual(update.group_ids_added, (20,))
            self.assertEqual(update.group_ids_removed, (10,))
        finally:
            state.stop()
        self.assertFalse(state.is_running)

    def test_async_refresh(self):
        async def run():
            account = StubAccount([friend(1, "One")], [group(10, "Alpha")])
            state = SocialState(account)
            first = await state.async_refresh()
            self.assertTrue(first.initial)
            account.friends.items = [friend(2, "Two")]
            second = await state.async_refresh()
            self.assertEqual(second.friend_ids_added, (2,))
            self.assertEqual(second.friend_ids_removed, (1,))
            await state.async_start(interval=0.01, initial=False)
            self.assertTrue(state.is_running)
            await state.async_stop()
            self.assertFalse(state.is_running)

        asyncio.run(run())

    def test_account_login_hydrates_social_state(self):
        class DevicePool:
            def ensure_loaded(self):
                pass

            def get_random(self):
                return "device", "sign", "ddh"

        class Response:
            def json(self):
                return {
                    "code": 1,
                    "data": {
                        "userId": 99,
                        "accessToken": "token",
                        "nickName": "Tester",
                        "region": "sandbox",
                    },
                }

        class Session:
            def post(self, *args, **kwargs):
                return Response()

        with tempfile.TemporaryDirectory() as tmp:
            account = BmgAccount(
                "user",
                "pass",
                Config(session_cache_path=f"{tmp}/sessions.json"),
            )
            account.friends = StubFriends([friend(1, "One")])
            account.group = StubGroups([group(10, "Alpha")])
            account._device_pool = DevicePool()
            with patch.object(BmgAccount, "_sync_time", return_value=None), \
                    patch.object(BmgAccount, "_get_session", return_value=Session()):
                ok = account.login(start_sync=False)
            self.assertTrue(ok)
            self.assertTrue(account.social.loaded)
            self.assertEqual(account.social.groups[0].group_id, 10)
            self.assertEqual(account.social.friends[0].user_id, 1)
            account.close()

    def test_account_initialize_social_uses_account_state(self):
        account = BmgAccount("user", "pass", Config())
        account.friends = StubFriends([friend(1, "One")])
        account.group = StubGroups([group(10, "Alpha")])
        snapshot = account.initialize_social(start=False)
        self.assertEqual(snapshot.groups[0].group_id, 10)
        self.assertEqual(snapshot.friends[0].user_id, 1)
        self.assertIs(account.social.get_group(10), snapshot.groups[0])
        account.close()


if __name__ == "__main__":
    unittest.main()
