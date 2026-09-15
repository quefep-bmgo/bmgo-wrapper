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

    def get_online_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/online/info")

    def update_engine(self, engine_version: str) -> dict[str, Any]:
        return self._account.request("PUT", "/user/api/v1/user/engine", body={"engineVersion": engine_version})

    def get_friend_count(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/friend/num")

    def get_report_info(self, uid: int) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/report/info", params={"userId": uid})

    def report_user(self, uid: int, reason: str, content: str = "") -> dict[str, Any]:
        return self._account.request("POST", "/user/api/v1/user/report", body={"userId": uid, "reason": reason, "content": content})

    def get_simple_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/simple/info")

    def get_vip_info(self, uid: int) -> dict[str, Any]:
        return self._account.request("GET", f"/user/api/v1/vip/users/{uid}")

    def get_player_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/player/info")

    def get_random_nickname(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/random/nickname")

    def check_nickname_exist(self, nickname: str) -> dict[str, Any]:
        return self._account.request("GET", "/api/v1/temporary/check/nickname/exist", params={"nickname": nickname})

    def get_daily_tasks(self, task_type: int = 1) -> dict[str, Any]:
        return self._account.request("GET", f"/user/api/v1/users/dairy/tasks/{task_type}")

    def get_new_daily_tasks(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/users/new/daily/tasks")

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

    async def async_get_online_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/online/info")

    async def async_update_engine(self, engine_version: str) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/user/api/v1/user/engine", body={"engineVersion": engine_version})

    async def async_get_friend_count(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/friend/num")

    async def async_get_report_info(self, uid: int) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/report/info", params={"userId": uid})

    async def async_report_user(self, uid: int, reason: str, content: str = "") -> dict[str, Any]:
        return await self._account.async_request("POST", "/user/api/v1/user/report", body={"userId": uid, "reason": reason, "content": content})

    async def async_get_simple_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/simple/info")

    async def async_get_vip_info(self, uid: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/user/api/v1/vip/users/{uid}")

    async def async_get_player_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/player/info")

    async def async_get_random_nickname(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/random/nickname")

    async def async_check_nickname_exist(self, nickname: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/api/v1/temporary/check/nickname/exist", params={"nickname": nickname})

    async def async_get_daily_tasks(self, task_type: int = 1) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/user/api/v1/users/dairy/tasks/{task_type}")

    async def async_get_new_daily_tasks(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/users/new/daily/tasks")

    # --- Avatar frames ---

    def get_avatar_frames(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/avatar/frame")

    def equip_avatar_frame(self, resource_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/user/api/v1/user/avatar/frame", params={"resourceId": resource_id})

    def check_avatar_frame_resources(self, res_version: int = 0) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/avatar/frame/resource/check", params={"resVersion": res_version})

    # --- Colorful nicknames ---

    def get_colorful_nicknames(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/colorful/nickName")

    def equip_colorful_nickname(self, resource_id: int) -> dict[str, Any]:
        return self._account.request("PUT", "/user/api/v1/user/colorful/nickName", params={"resourceId": resource_id})

    # --- Personal space effects ---

    def check_space_effects(self, res_version: int = 0) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/personal/space/effect/resource/check", params={"resVersion": res_version})

    # --- VIP ---

    def check_vip_personality(self, res_version: int = 0) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/vip/personality/resource/check", params={"resVersion": res_version})

    # --- Sign-in v2 ---

    def get_daily_sign_in_v2(self) -> dict[str, Any]:
        return self._account.request("GET", f"/user/api/v2/users/{self._account.uid}/daily/sign/in")

    def daily_sign_in_v2(self) -> dict[str, Any]:
        return self._account.request("PUT", f"/user/api/v2/users/{self._account.uid}/daily/sign/in")

    def claim_sign_in_ad_reward(self) -> dict[str, Any]:
        return self._account.request("PUT", "/user/api/v1/users/daily/sign/ads")

    # --- Profile ---

    def update_profile_detail(self, body: dict[str, Any]) -> dict[str, Any]:
        return self._account.request("PUT", f"/user/api/v1/profile/detail/{self._account.uid}", body=body)

    def get_account_settings(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/account/settings")

    def get_profile_join_switch(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/profile/join/switch")

    def set_profile_join_switch(self) -> dict[str, Any]:
        return self._account.request("POST", "/user/api/v1/user/profile/join/switch")

    def is_nickname_free(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/nickName/free")

    def get_frequent_games(self, count: int = 5) -> dict[str, Any]:
        return self._account.request("GET", f"/user/api/v1/data/frequently/game/{self._account.uid}", params={"count": count})

    # --- Shop ---

    def get_shop_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/user/shop/info")

    def get_decoration_details(self, decoration_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/shop/api/v1/shop/decorations/details/{decoration_id}")

    def get_suit_info(self, suit_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/shop/api/v1/new/shop/suit/info/{suit_id}")

    # --- Pay / Month card ---

    def get_month_card_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v2/monthcard/info")

    def claim_month_card_reward(self, month_card_id: int) -> dict[str, Any]:
        return self._account.request("POST", "/pay/api/v2/monthcard/receive", params={"monthCardId": month_card_id})

    def get_payment_red_point(self) -> dict[str, Any]:
        return self._account.request("GET", "/pay/api/v1/red-point")

    # --- Activity ---

    def get_task_activity_info(self, activity_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/activity/api/v1/task/activity/info", params={"activityId": activity_id})

    def claim_task_activity_reward(self, activity_id: str, task_reward_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/activity/api/v1/task/activity/reward/receive",
                                     params={"activityId": activity_id, "taskRewardId": task_reward_id})

    def claim_sharing_reward(self, type_: int = 0) -> dict[str, Any]:
        return self._account.request("POST", "/user/api/v1/users/sharing/reward", params={"type": type_})

    def get_security_email(self) -> dict[str, Any]:
        return self._account.request("GET", "/user/api/v1/users/security/bind/email", params={"userId": self._account.uid})

    # --- Async: Avatar frames ---

    async def async_get_avatar_frames(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/avatar/frame")

    async def async_equip_avatar_frame(self, resource_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/user/api/v1/user/avatar/frame", params={"resourceId": resource_id})

    async def async_check_avatar_frame_resources(self, res_version: int = 0) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/avatar/frame/resource/check", params={"resVersion": res_version})

    # --- Async: Colorful nicknames ---

    async def async_get_colorful_nicknames(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/colorful/nickName")

    async def async_equip_colorful_nickname(self, resource_id: int) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/user/api/v1/user/colorful/nickName", params={"resourceId": resource_id})

    # --- Async: Personal space effects ---

    async def async_check_space_effects(self, res_version: int = 0) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/personal/space/effect/resource/check", params={"resVersion": res_version})

    # --- Async: VIP ---

    async def async_check_vip_personality(self, res_version: int = 0) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/vip/personality/resource/check", params={"resVersion": res_version})

    # --- Async: Sign-in v2 ---

    async def async_get_daily_sign_in_v2(self) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/user/api/v2/users/{self._account.uid}/daily/sign/in")

    async def async_daily_sign_in_v2(self) -> dict[str, Any]:
        return await self._account.async_request("PUT", f"/user/api/v2/users/{self._account.uid}/daily/sign/in")

    async def async_claim_sign_in_ad_reward(self) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/user/api/v1/users/daily/sign/ads")

    # --- Async: Profile ---

    async def async_update_profile_detail(self, body: dict[str, Any]) -> dict[str, Any]:
        return await self._account.async_request("PUT", f"/user/api/v1/profile/detail/{self._account.uid}", body=body)

    async def async_get_account_settings(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/account/settings")

    async def async_get_profile_join_switch(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/profile/join/switch")

    async def async_set_profile_join_switch(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/user/api/v1/user/profile/join/switch")

    async def async_is_nickname_free(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/nickName/free")

    async def async_get_frequent_games(self, count: int = 5) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/user/api/v1/data/frequently/game/{self._account.uid}", params={"count": count})

    # --- Async: Shop ---

    async def async_get_shop_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/user/shop/info")

    async def async_get_decoration_details(self, decoration_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/shop/api/v1/shop/decorations/details/{decoration_id}")

    async def async_get_suit_info(self, suit_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/shop/api/v1/new/shop/suit/info/{suit_id}")

    # --- Async: Pay / Month card ---

    async def async_get_month_card_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v2/monthcard/info")

    async def async_claim_month_card_reward(self, month_card_id: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/pay/api/v2/monthcard/receive", params={"monthCardId": month_card_id})

    async def async_get_payment_red_point(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/pay/api/v1/red-point")

    # --- Async: Activity ---

    async def async_get_task_activity_info(self, activity_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/activity/api/v1/task/activity/info", params={"activityId": activity_id})

    async def async_claim_task_activity_reward(self, activity_id: str, task_reward_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/activity/api/v1/task/activity/reward/receive",
                                                  params={"activityId": activity_id, "taskRewardId": task_reward_id})

    async def async_claim_sharing_reward(self, type_: int = 0) -> dict[str, Any]:
        return await self._account.async_request("POST", "/user/api/v1/users/sharing/reward", params={"type": type_})

    async def async_get_security_email(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/user/api/v1/users/security/bind/email", params={"userId": self._account.uid})