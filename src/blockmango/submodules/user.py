from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any

from ..models import UserProfile, UserStats


class UserAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def get_profile(self, uid: int) -> UserProfile | None:
        r = self._account.request("GET", f"/friend/api/v1/friends/info/id/{uid}")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    def get_own_profile(self) -> UserProfile | None:
        r = self._account.request("GET", "/user/api/v2/user/details/info")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    def get_stats(self, uid: int) -> UserStats | None:
        r = self._account.request("GET", "/user/api/v1/users/bg-careers", params={"userId": str(uid)})
        if r.get("code") == 1:
            return UserStats.from_dict(r.get("data"))
        return None

    def get_clan_role(self, uid: int) -> dict[str, Any] | None:
        r = self._account.request("GET", "/bedwar/api/v1/friends/clan/by/userIds", params={"userIds": str(uid)})
        if r.get("code") != 1:
            return None
        data = r.get("data")
        if not isinstance(data, list) or not data:
            return None
        role = (data[0] or {}).get("clanRole") or {}
        if role.get("clanId") in (None, "", 0, "0"):
            return None
        return role

    def lookup(self, uid: int) -> UserProfile | None:
        if uid == self._account.uid:
            profile = self.get_own_profile()
        else:
            profile = self.get_profile(uid)
        if not profile:
            return None
        stats = self.get_stats(uid)
        if stats:
            profile.career = stats.career
            profile.friend_num = stats.friend_num
            profile.decoration_count = stats.decoration_count
            profile.suit_count = stats.suit_count
            profile.atlas_count = stats.atlas_count
            profile.atlas_total = stats.atlas_total
        clan = self.get_clan_role(uid)
        if clan:
            profile.clan_id = clan.get("clanId")
            profile.clan_name = clan.get("clanName")
            profile.clan_role = clan.get("role")
        return profile

    def change_name(self, new_name: str, old_name: str) -> dict[str, Any]:
        return self._account.request("PUT", "/user/api/v3/user/nickName",
                                     params={"newName": new_name, "oldName": old_name})

    def change_details(self, details: str) -> dict[str, Any]:
        return self._account.request("PUT", "/user/api/v1/user/info", body={"details": details})

    def change_avatar(self, pic_url: str) -> dict[str, Any]:
        return self._account.request("PUT", "/user/api/v1/user/info", body={"picUrl": pic_url})

    def change_password(self, old_password: str, new_password: str) -> dict[str, Any]:
        return self._account.request("POST", "/user/api/v1/user/password/modify",
                                     body={"oldPassword": old_password, "newPassword": new_password, "confirmPassword": ""})

    def bind_email(self, email: str, verify_code: str) -> dict[str, Any]:
        return self._account.request("POST", "/user/api/v1/users/bind/email",
                                     body={"email": email, "verifyCode": verify_code})

    def unbind_email(self, email: str, verify_code: str) -> dict[str, Any]:
        return self._account.request("DELETE", f"/user/api/v2/users/{self._account.uid}/emails",
                                     params={"email": email, "verifyCode": verify_code})

    def set_birthday(self, birthday: str) -> dict[str, Any]:
        return self._account.request("PUT", "/user/api/v1/user/info", body={"birthday": birthday})

    async def async_get_profile(self, uid: int) -> UserProfile | None:
        r = await self._account.async_request("GET", f"/friend/api/v1/friends/info/id/{uid}")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    async def async_get_own_profile(self) -> UserProfile | None:
        r = await self._account.async_request("GET", "/user/api/v2/user/details/info")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    async def async_get_stats(self, uid: int) -> UserStats | None:
        r = await self._account.async_request("GET", "/user/api/v1/users/bg-careers", params={"userId": str(uid)})
        if r.get("code") == 1:
            return UserStats.from_dict(r.get("data"))
        return None

    async def async_get_clan_role(self, uid: int) -> dict[str, Any] | None:
        r = await self._account.async_request("GET", "/bedwar/api/v1/friends/clan/by/userIds", params={"userIds": str(uid)})
        if r.get("code") != 1:
            return None
        data = r.get("data")
        if not isinstance(data, list) or not data:
            return None
        role = (data[0] or {}).get("clanRole") or {}
        if role.get("clanId") in (None, "", 0, "0"):
            return None
        return role

    async def async_lookup(self, uid: int) -> UserProfile | None:
        if uid == self._account.uid:
            profile = await self.async_get_own_profile()
        else:
            profile = await self.async_get_profile(uid)
        if not profile:
            return None
        stats = await self.async_get_stats(uid)
        if stats:
            profile.career = stats.career
            profile.friend_num = stats.friend_num
            profile.decoration_count = stats.decoration_count
            profile.suit_count = stats.suit_count
            profile.atlas_count = stats.atlas_count
            profile.atlas_total = stats.atlas_total
        clan = await self.async_get_clan_role(uid)
        if clan:
            profile.clan_id = clan.get("clanId")
            profile.clan_name = clan.get("clanName")
            profile.clan_role = clan.get("role")
        return profile

    async def async_lookup_result(self, uid: int):
        return await self._account.async_lookup_result(uid)

    async def async_get_decorations_result(self, uid: int):
        return await self._account.async_get_decorations_result(uid)

    async def async_change_name(self, new_name: str, old_name: str) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/user/api/v3/user/nickName",
                                                 params={"newName": new_name, "oldName": old_name})

    async def async_change_details(self, details: str) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/user/api/v1/user/info", body={"details": details})

    async def async_change_avatar(self, pic_url: str) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/user/api/v1/user/info", body={"picUrl": pic_url})

    async def async_change_password(self, old_password: str, new_password: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/user/api/v1/user/password/modify",
                                                 body={"oldPassword": old_password, "newPassword": new_password, "confirmPassword": ""})

    async def async_bind_email(self, email: str, verify_code: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/user/api/v1/users/bind/email",
                                                 body={"email": email, "verifyCode": verify_code})

    async def async_unbind_email(self, email: str, verify_code: str) -> dict[str, Any]:
        return await self._account.async_request("DELETE", f"/user/api/v2/users/{self._account.uid}/emails",
                                                 params={"email": email, "verifyCode": verify_code})

    async def async_set_birthday(self, birthday: str) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/user/api/v1/user/info", body={"birthday": birthday})