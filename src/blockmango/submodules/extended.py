"""Additional 3.29.x endpoint wrappers grouped by domain."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class ExtendedAPI:
    """Wrappers for the newer 3.29.x endpoints captured from the Android client.

    These methods are intentionally thin: they return the raw API envelope. Most
    methods are synchronous; ``async_request`` remains available for async callers.
    """

    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._account.request("GET", path, params=params)

    def _post(self, path: str, params: dict[str, Any] | None = None,
              body: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._account.request("POST", path, params=params, body=body)

    def _put(self, path: str, params: dict[str, Any] | None = None,
             body: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._account.request("PUT", path, params=params, body=body)

    # activity
    def activity_home_page(self) -> dict[str, Any]:
        return self._post("/activity/api/v1/activity/home/page")

    def ad_draw_info(self, activity_id: str = "ad_draw_activity1") -> dict[str, Any]:
        return self._get("/activity/api/v1/ad-draw/info", {"activityId": activity_id})

    def background_image(self) -> dict[str, Any]:
        return self._get("/activity/api/v1/background-image")

    def community_jump_info(self, activity_id: str = "community_jump_activity") -> dict[str, Any]:
        return self._get("/activity/api/v1/community-jump/info", {"activityId": activity_id})

    def direct_purchase_puzzles_popup(self) -> dict[str, Any]:
        return self._get("/activity/api/v1/direct-purchase/puzzles/popup")

    def game_banner_red_point(self) -> dict[str, Any]:
        return self._get("/activity/api/v1/game/banner/new/red-point")

    def holiday_score_info(self, activity_id: str = "holiday_score_202609") -> dict[str, Any]:
        return self._get("/activity/api/v1/holiday-score/info", {"activityId": activity_id})

    def preorder_holiday_score_pack(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._post("/activity/api/v1/holiday-score/pack/pre-order", body=body)

    def holiday_score_rank_period(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/activity/api/v1/holiday-score/rank/period", params)

    def holiday_score_rank_reward_preview(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/activity/api/v1/holiday-score/rank/reward-preview", params)

    def holiday_score_rank_total(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/activity/api/v1/holiday-score/rank/total", params)

    def homepage_ad_banner(self, language: str = "en_US", region: str | None = None,
                           tab_code: str = "") -> dict[str, Any]:
        return self._get("/activity/api/v1/homepage/ad-banner", {
            "language": language,
            "userId": self._account.uid,
            "region": region or self._account.region,
            "tabCode": tab_code,
        })

    def homepage_game_detail_icon_activity(self, game_id: str) -> dict[str, Any]:
        return self._get("/activity/api/v1/homepage/game-detail/icon-activity", {"gameId": game_id})

    def limit_gcube_pack_info(self, popup_scene: int | None = None) -> dict[str, Any]:
        params = {"popup_scene": popup_scene} if popup_scene is not None else None
        return self._get("/activity/api/v1/limit/gcube/pack/info", params)

    def receive_sub_pkg_transfer_reward(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._post("/activity/api/v1/sub-pkg-transfer/reward/receive", body=body)

    def tradplus_ad_config(self, force_update: bool = False) -> dict[str, Any]:
        return self._get("/activity/api/v1/tradplus/ad/open-config", {"forceUpdate": str(force_update).lower()})

    def treasure_bowl_survey_status(self) -> dict[str, Any]:
        return self._get("/activity/api/v1/treasure/bowl/rebate/survey/status")

    def homepage_activity_list_group(self, language: str = "en_US") -> dict[str, Any]:
        return self._get("/activity/api/v2/homepage/activity-list/group", {"language": language})

    def newbie_activity_status(self) -> dict[str, Any]:
        return self._get("/activity/api/v2/newbie/activity/status")

    def theme(self) -> dict[str, Any]:
        return self._get("/activity/api/v2/theme")

    def daily_ad_red_points(self) -> dict[str, Any]:
        return self._get("/activity/daily/ad/activity/red/points")

    # decoration
    def using_decorations(self, uid: int | None = None) -> dict[str, Any]:
        return self._get(f"/decoration/api/v1/decorations-v2/{uid or self._account.uid}/using")

    def check_new_decorations_resource(self, res_version: int,
                                       engine_version: int = 10114) -> dict[str, Any]:
        return self._get("/decoration/api/v1/new/decorations/check/resource", {
            "resVersion": res_version,
            "engineVersion": engine_version,
        })

    def recommended_decorations(self) -> dict[str, Any]:
        return self._get("/decoration/api/v1/recommend/get")

    def decoration_red_points(self) -> dict[str, Any]:
        return self._get("/decoration/api/v1/redpoints")

    def decoration_model_number(self) -> dict[str, Any]:
        return self._get("/decoration/api/v1/user/decoration/model/number")

    # friend
    def family_recruit_status(self) -> dict[str, Any]:
        return self._get("/friend/api/v1/family/recruit/status")

    def homeland_suspended_entrance(self) -> dict[str, Any]:
        return self._get("/friend/api/v1/homeland/suspended/entrance")

    def friends_v3(self, page: int = 0, size: int = 500, show_big_party: bool = True) -> dict[str, Any]:
        return self._get("/friend/api/v3/friends", {
            "pageNo": page,
            "pageSize": size,
            "showBigParty": 1 if show_big_party else 0,
        })

    def friend_v3(self, uid: int, show_big_party: bool = True) -> dict[str, Any]:
        return self._get(f"/friend/api/v3/friends/{uid}", {
            "showBigParty": 1 if show_big_party else 0,
        })

    def friend_tags(self) -> dict[str, Any]:
        return self._get("/friend/api/v1/tag/only")

    def friend_popularity(self, uid: int) -> dict[str, Any]:
        return self._get(f"/friend/api/v1/popularity/{uid}")

    # game
    def mining_token_balance_with_transform(self) -> dict[str, Any]:
        return self._get("/game/api/v1/backpack/mining-token/balance/with-transform")

    def bghall_game_entrance_ui_config(self) -> dict[str, Any]:
        return self._get("/game/api/v1/bghall/game-entrance/ui-config")

    def ping_server_list(self) -> dict[str, Any]:
        return self._get("/game/api/v1/ping/server/list")

    def user_highlight_data(self, target_id: int) -> dict[str, Any]:
        return self._get("/game/api/v1/user/highlight/data", {"targetId": target_id})

    def game_revision_combine(self, filter_type_id: int = 0, is_filter: int = 0,
                              os_name: str = "android", page: int = 0,
                              size: int = 20) -> dict[str, Any]:
        return self._get("/game/api/v2/game/revision/all/list/by/condition/combine", {
            "filterTypeId": filter_type_id,
            "isFilter": is_filter,
            "os": os_name,
            "pageNo": page,
            "pageSize": size,
        })

    def check_app_engine_update(self, engine_version: int = 10114,
                                common_res_version: int = 0,
                                game_res_version: int = 0,
                                game_type: str = "", engine_type: str = "v1") -> dict[str, Any]:
        return self._get("/game/api/v2/games/app-engine/check-update", {
            "engineVersion": engine_version,
            "commonResVersion": common_res_version,
            "gameResVersion": game_res_version,
            "gameType": game_type,
            "engineType": engine_type,
        })

    def clan_rank(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/clan/api/v1/clan/rank", params)

    def clan_rank_new(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/clan/api/v1/clan/rank/new", params)

    def clan_user_rank(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/clan/api/v1/clan/user/rank", params)

    def clan_user_rank_new(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/clan/api/v1/clan/user/rank/new", params)

    # mailbox / msg
    def redeem_cdkey(self, body: dict[str, Any] | None = None,
                     cdkey: str | None = None) -> dict[str, Any]:
        body = body or ({"cdkey": cdkey} if cdkey else None)
        return self._post("/mailbox/api/v1/cdkey/redeem", body=body)

    def mark_user_notifications_unread(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._post("/msg/api/v1/user-notification/unread", body=body)

    # pay
    def area_pack_popup_info(self) -> dict[str, Any]:
        return self._get("/pay/api/v1/area/pack/popup/info")

    def disposable_advance_order(self, product_id: str, data: str) -> dict[str, Any]:
        return self._put("/pay/api/v1/pay/disposable/advance/order", {
            "productId": product_id,
            "data": data,
        })

    def product_info_batch(self, product_ids: list[str] | str,
                           country: str = "US") -> dict[str, Any]:
        ids = product_ids if isinstance(product_ids, str) else ",".join(product_ids)
        return self._get("/pay/api/v1/product/info/batch/get", {
            "country": country,
            "productIds": ids,
        })

    def third_pay_access_status(self) -> dict[str, Any]:
        return self._get("/pay/api/v1/third-pay/user/access-status")

    def xsolla_billing_get(self) -> dict[str, Any]:
        return self._get("/pay/api/v1/xsolla/billing/get")

    def xsolla_enable(self) -> dict[str, Any]:
        return self._get("/pay/api/v1/xsolla/enable")

    # user
    def abtest_user_test(self) -> dict[str, Any]:
        return self._get("/user/api/v1/abtest/getUserTest")

    def chat_migrate_data(self) -> dict[str, Any]:
        return self._get("/user/api/v1/chat/migrate/data")

    def trigger_client_event(self, trigger_type: int = 1) -> dict[str, Any]:
        return self._post("/user/api/v1/client/trigger/event", {"triggerType": trigger_type})

    def sensitive_word_regions(self) -> dict[str, Any]:
        return self._get("/user/api/v1/sensitive/word/region/list")

    def collect_feedback_task(self) -> dict[str, Any]:
        return self._get("/user/api/v1/user-feedback/collect-task")

    def set_user_language(self, user_id: int | None = None, language: str = "en") -> dict[str, Any]:
        return self._post("/user/api/v1/user/language", {
            "userId": user_id or self._account.uid,
            "language": language,
        })

    def logout(self) -> dict[str, Any]:
        return self._put("/user/api/v1/user/login-out")

    def vip_customer_popup_needed(self) -> dict[str, Any]:
        return self._get("/user/api/v1/user/vip/customer/info/pop/up/needed")

    def web_auth_code(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._post("/user/api/v1/web/auth-code", body=body)

    def security_settings(self, user_id: int | None = None) -> dict[str, Any]:
        return self._get("/user/api/v2/users/verify/user/security/settings", {
            "userId": user_id or self._account.uid,
        })

    def user_details_v3(self) -> dict[str, Any]:
        return self._get("/user/api/v3/user/details/info")

    def auth_token(self, q: str) -> dict[str, Any]:
        return self._get("/user/api/v5/account/auth-token", {"q": q})
