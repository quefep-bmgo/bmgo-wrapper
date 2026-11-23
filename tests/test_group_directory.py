import unittest

from blockmango.submodules.group import GroupAPI
from blockmango.transport import FunctionGroupTransport, GroupMessageResult, GroupMessagingUnavailable


def group(gid: int, name: str, members: int = 0) -> dict:
    return {
        "groupId": gid,
        "groupName": name,
        "ownerId": 1,
        "memberCount": members,
        "maxMembers": 500,
        "inviteStatus": 1,
        "members": [
            {"userId": 10 + offset, "nickName": f"Member{offset}", "role": 0}
            for offset in range(members)
        ],
    }


class FakeGroupAccount:
    uid = 1

    def __init__(self, pages: dict[int, list[dict]]):
        self.pages = pages
        self.requests: list[tuple[str, str, dict]] = []

    def request(self, method, path, params=None, body=None, language=None, **kwargs):
        self.requests.append((method, path, dict(params or {})))
        if path.endswith("/list"):
            page = int((params or {}).get("pageNo", 1))
            items = self.pages.get(page, [])
            return {"code": 1, "data": {"data": items}}
        if path.endswith("/info"):
            gid = int((params or {}).get("groupId", 0))
            for items in self.pages.values():
                for item in items:
                    if int(item["groupId"]) == gid:
                        return {"code": 1, "data": item}
            return {"code": 1, "data": None}
        return {"code": 1, "data": {}}

    async def async_request(self, method, path, params=None, body=None, language=None, **kwargs):
        return self.request(method, path, params, body, language, **kwargs)


class FakeTransport:
    def __init__(self):
        self.sent: list[tuple] = []

    def send_text(self, group_id, text, *, ext_content=None, timeout=10.0):
        self.sent.append((group_id, text, ext_content, timeout))
        return GroupMessageResult(group_id=group_id, message_id="m1", message_uid="u1", timestamp=123)

    async def async_send_text(self, group_id, text, *, ext_content=None, timeout=10.0):
        return self.send_text(group_id, text, ext_content=ext_content, timeout=timeout)


class GroupDirectoryTests(unittest.TestCase):
    def test_group_pagination_search_and_find(self):
        account = FakeGroupAccount({
            0: [group(1, "Alpha"), group(2, "Beta")],
            1: [group(3, "Alphabet")],
            2: [],
        })
        api = GroupAPI(account)
        groups = api.list_all_groups(1000, page_size=2)
        self.assertEqual([g.group_id for g in groups], [1, 2, 3])
        self.assertEqual([g.group_id for g in api.search_groups("alpha")], [1, 3])
        self.assertEqual(api.find_group(name="ALPHA").group_id, 1)
        self.assertEqual(api.find_group(group_id=3).group_name, "Alphabet")

    def test_group_list_is_zero_based_and_parses_group_members(self):
        raw = {
            "groupId": 99,
            "groupName": "Live",
            "ownerId": 1,
            "inviteStatus": 1,
            "groupMembers": [
                {"userId": 7, "userName": "Owner", "identity": 2, "pic": "p.png"},
            ],
        }
        account = FakeGroupAccount({0: [raw], 1: []})
        api = GroupAPI(account)
        groups = api.list_all_groups()
        self.assertEqual([g.group_id for g in groups], [99])
        self.assertEqual(account.requests[0][2]["pageNo"], 0)
        self.assertEqual(groups[0].member_count, 1)
        self.assertEqual(groups[0].members[0].user_id, 7)
        self.assertEqual(groups[0].members[0].nick_name, "Owner")
        self.assertEqual(groups[0].members[0].role, 2)
        self.assertEqual(groups[0].members[0].pic_url, "p.png")

    def test_group_cache_and_refresh(self):
        account = FakeGroupAccount({0: [group(1, "Alpha")], 1: []})
        api = GroupAPI(account)
        api.list_all_groups()
        count = len(account.requests)
        api.list_all_groups()
        self.assertEqual(len(account.requests), count)
        api.refresh_groups()
        self.assertGreater(len(account.requests), count)

    def test_members_use_group_info(self):
        account = FakeGroupAccount({0: [group(1, "Alpha", members=2)], 1: []})
        api = GroupAPI(account)
        self.assertEqual([m.user_id for m in api.get_members(1)], [10, 11])

    def test_send_requires_transport(self):
        api = GroupAPI(FakeGroupAccount({0: [], 1: []}))
        with self.assertRaises(GroupMessagingUnavailable):
            api.send_text(1, "hello")

    def test_send_delegates_to_transport(self):
        api = GroupAPI(FakeGroupAccount({0: [], 1: []}))
        transport = FakeTransport()
        api.set_transport(transport)
        result = api.send_text(42, "hello", ext_content={"k": "v"})
        self.assertEqual(result.message_id, "m1")
        self.assertEqual(transport.sent, [("42", "hello", {"k": "v"}, 10.0)])

    def test_send_validates_empty_and_oversize_text(self):
        api = GroupAPI(FakeGroupAccount({0: [], 1: []}))
        with self.assertRaises(ValueError):
            api.send_text(1, "   ")
        with self.assertRaises(ValueError):
            api.send_text(1, "x" * 10_241)

    def test_function_transport_coerces_mapping(self):
        transport = FunctionGroupTransport(lambda **kwargs: {
            "messageId": "m2",
            "messageUId": "u2",
            "sentTime": 99,
        })
        result = transport.send_text("42", "hello")
        self.assertEqual(result.message_id, "m2")
        self.assertEqual(result.message_uid, "u2")
        self.assertEqual(result.timestamp, 99)


class AsyncGroupDirectoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_async_send_and_list(self):
        account = FakeGroupAccount({0: [group(1, "Alpha")], 1: []})
        api = GroupAPI(account)
        groups = await api.async_list_all_groups()
        self.assertEqual(len(groups), 1)
        api.set_transport(FakeTransport())
        result = await api.async_send_text(1, "hello")
        self.assertEqual(result.group_id, "1")


if __name__ == "__main__":
    unittest.main()
