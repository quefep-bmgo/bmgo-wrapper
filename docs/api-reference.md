# API reference

Generated from `src/blockmango/submodules/` by
`python tools/generate_api_docs.py`. The hand-written guides are:

- [api-overview.md](api-overview.md)
- [authentication.md](authentication.md)
- [leaderboards.md](leaderboards.md)
- [games.md](games.md)

Each row is a public method, its HTTP path when statically visible, and
its short description. Methods that delegate to another module show `—`.
`ExtendedAPI` is synchronous; use `account.async_request()` for async callers.

## `ActivityAPI`

Activity events, sign-in, ads, banners, and red packets.

| Method | Endpoint | Description |
| --- | --- | --- |
| `sign_in(language: str='en')` | `/activity/api/v1/signIn` |  |
| `get_sign_in_status(language: str='en')` | `/activity/api/v1/signIn` |  |
| `get_tasks(language: str='en')` | `/activity/api/v1/activity/task` |  |
| `claim_task_reward(task_id: int, language: str='en')` | `/activity/api/v1/activity/task/reward` |  |
| `async async_sign_in(language: str='en')` | `/activity/api/v1/signIn` |  |
| `async async_get_sign_in_status(language: str='en')` | `/activity/api/v1/signIn` |  |
| `async async_get_tasks(language: str='en')` | `/activity/api/v1/activity/task` |  |
| `async async_claim_task_reward(task_id: int, language: str='en')` | `/activity/api/v1/activity/task/reward` |  |
| `get_campaign_list(language: str='en')` | `/activity/api/v1/activity/worldCup` |  |
| `place_campaign_bet(body: dict[str, Any], language: str='en')` | `/activity/api/v1/activity/worldCup` |  |
| `get_campaign_history(language: str='en')` | `/activity/api/v1/activity/worldCup/history` |  |
| `get_campaign_notice(language: str='en')` | `/activity/api/v1/activity/worldCup/notice` |  |
| `get_campaign_integral(language: str='en')` | `/activity/api/v1/activity/worldCup/integral` |  |
| `get_my_integral_rank(language: str='en')` | `/activity/api/v1/activity/user/integral/rank` |  |
| `get_integral_leaderboard(page_no: int=1, page_size: int=20, language: str='en')` | `/activity/api/v1/activity/integral/rank` |  |
| `get_integral_rewards(type_: str='', language: str='en')` | `/activity/api/v1/activity/user/integral/reward` |  |
| `claim_integral_reward(type_: str='', decoration_id: int=0, language: str='en')` | `/activity/api/v1/activity/user/integral/reward` |  |
| `get_rank_reward_info(language: str='en')` | `/activity/api/v1/activity/user/rank/reward` |  |
| `get_activity_actions(title_type: str='', language: str='en')` | `/activity/api/v1/activity/action` |  |
| `receive_action_reward(title_type: str='', action_id: int=0, language: str='en')` | `/activity/api/v1/receive/reward` |  |
| `get_activity_titles(language: str='en')` | `/activity/api/v2/activity/title` |  |
| `get_treasure_info()` | `/activity/api/v1/treasure/bowl/info` |  |
| `buy_treasure()` | `/activity/api/v1/treasure/bowl/buy` |  |
| `get_seven_day_sign_data(activity_id: str, language: str='en')` | `/activity/api/v1/seven/day/sign/data/get` |  |
| `claim_seven_day_sign_reward(card_id: int=0, activity_id: str='', language: str='en')` | `/activity/api/v1/seven/day/sign/reward/receive` |  |
| `async async_get_campaign_list(language: str='en')` | `/activity/api/v1/activity/worldCup` |  |
| `async async_place_campaign_bet(body: dict[str, Any], language: str='en')` | `/activity/api/v1/activity/worldCup` |  |
| `async async_get_campaign_history(language: str='en')` | `/activity/api/v1/activity/worldCup/history` |  |
| `async async_get_campaign_notice(language: str='en')` | `/activity/api/v1/activity/worldCup/notice` |  |
| `async async_get_campaign_integral(language: str='en')` | `/activity/api/v1/activity/worldCup/integral` |  |
| `async async_get_my_integral_rank(language: str='en')` | `/activity/api/v1/activity/user/integral/rank` |  |
| `async async_get_integral_leaderboard(page_no: int=1, page_size: int=20, language: str='en')` | `/activity/api/v1/activity/integral/rank` |  |
| `async async_get_integral_rewards(type_: str='', language: str='en')` | `/activity/api/v1/activity/user/integral/reward` |  |
| `async async_claim_integral_reward(type_: str='', decoration_id: int=0, language: str='en')` | `/activity/api/v1/activity/user/integral/reward` |  |
| `async async_get_rank_reward_info(language: str='en')` | `/activity/api/v1/activity/user/rank/reward` |  |
| `async async_get_activity_actions(title_type: str='', language: str='en')` | `/activity/api/v1/activity/action` |  |
| `async async_receive_action_reward(title_type: str='', action_id: int=0, language: str='en')` | `/activity/api/v1/receive/reward` |  |
| `async async_get_activity_titles(language: str='en')` | `/activity/api/v2/activity/title` |  |
| `async async_get_treasure_info()` | `/activity/api/v1/treasure/bowl/info` |  |
| `async async_buy_treasure()` | `/activity/api/v1/treasure/bowl/buy` |  |
| `async async_get_seven_day_sign_data(activity_id: str, language: str='en')` | `/activity/api/v1/seven/day/sign/data/get` |  |
| `async async_claim_seven_day_sign_reward(card_id: int=0, activity_id: str='', language: str='en')` | `/activity/api/v1/seven/day/sign/reward/receive` |  |

## `BackpackAPI`

Backpack, pickaxe, and mining balances.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_backpack(version: str, user_id: str)` | `/backpack/api/{version}/backpack/{user_id}` |  |
| `get_candy_coupon_list()` | `/backpack/api/v1/candy-coupon/list` |  |
| `get_candy_coupon_address_list()` | `/backpack/api/v1/candy-coupon/address/list` |  |
| `exchange_candy_coupon(coupon_id: str, address_id: str)` | `/backpack/api/v1/candy-coupon/exchange` |  |
| `open_box_item(version: str, item_id: str, count: int=1)` | `/backpack/api/{version}/backpack/box/item` |  |
| `use_decoration_item(version: str, item_id: str)` | `/backpack/api/{version}/backpack/decoration/item` |  |
| `batch_fetch_item_details(item_ids: list[str])` | `/backpack/item/batch/fetch/details` |  |
| `check_duplicate_items(item_ids: list[str])` | `/backpack/repeat/item/check` |  |
| `async async_get_backpack(version: str, user_id: str)` | `/backpack/api/{version}/backpack/{user_id}` |  |
| `async async_get_candy_coupon_list()` | `/backpack/api/v1/candy-coupon/list` |  |
| `async async_get_candy_coupon_address_list()` | `/backpack/api/v1/candy-coupon/address/list` |  |
| `async async_exchange_candy_coupon(coupon_id: str, address_id: str)` | `/backpack/api/v1/candy-coupon/exchange` |  |
| `async async_open_box_item(version: str, item_id: str, count: int=1)` | `/backpack/api/{version}/backpack/box/item` |  |
| `async async_use_decoration_item(version: str, item_id: str)` | `/backpack/api/{version}/backpack/decoration/item` |  |
| `async async_batch_fetch_item_details(item_ids: list[str])` | `/backpack/item/batch/fetch/details` |  |
| `async async_check_duplicate_items(item_ids: list[str])` | `/backpack/repeat/item/check` |  |

## `BedwarAPI`

Bed Wars-specific endpoints.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_clan_role_for_users(user_ids: str)` | `/bedwar/api/v1/friends/clan/by/userIds` |  |
| `get_ranking(page: int=1, size: int=20)` | `/bedwar/api/v1/game/rank` |  |
| `get_game_info()` | `/bedwar/api/v1/game/info` |  |
| `get_match(match_id: str)` | `/bedwar/api/v1/game/match` |  |
| `get_recent(page: int=1, size: int=20)` | `/bedwar/api/v1/game/recent` |  |
| `get_team(team_id: str)` | `/bedwar/api/v1/game/team` |  |
| `like()` | `/bedwar/api/v1/game/like` |  |
| `get_season()` | `/bedwar/api/v1/game/season` |  |
| `get_achievement(user_id: int | None=None)` | `/bedwar/api/v1/game/achievement` |  |
| `get_match_name()` | `/bedwar/api/v1/contest/match-name` |  |
| `get_user_game_date_value(user_id: int)` | `/bedwar/api/v1/user/game/date/value/get` |  |
| `async async_get_clan_role_for_users(user_ids: str)` | `/bedwar/api/v1/friends/clan/by/userIds` |  |
| `async async_get_ranking(page: int=1, size: int=20)` | `/bedwar/api/v1/game/rank` |  |
| `async async_get_game_info()` | `/bedwar/api/v1/game/info` |  |
| `async async_get_match(match_id: str)` | `/bedwar/api/v1/game/match` |  |
| `async async_get_recent(page: int=1, size: int=20)` | `/bedwar/api/v1/game/recent` |  |
| `async async_get_team(team_id: str)` | `/bedwar/api/v1/game/team` |  |
| `async async_like()` | `/bedwar/api/v1/game/like` |  |
| `async async_get_season()` | `/bedwar/api/v1/game/season` |  |
| `async async_get_achievement(user_id: int | None=None)` | `/bedwar/api/v1/game/achievement` |  |
| `async async_get_match_name()` | `/bedwar/api/v1/contest/match-name` |  |
| `async async_get_user_game_date_value(user_id: int)` | `/bedwar/api/v1/user/game/date/value/get` |  |

## `ClanAPI`

Clan/tribe management and rankings.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_own_clan()` | `/clan/api/v1/clan/tribe/base` |  |
| `get_info(clan_id: int)` | `/clan/api/v2/clan/tribe` |  |
| `get_members()` | `/clan/api/v1/clan/tribe/member` |  |
| `join(clan_id: int, msg: str='')` | `/clan/api/v1/clan/tribe/member` |  |
| `leave(clan_id: int)` | `/clan/api/v1/clan/tribe/member` |  |
| `search(clan_name: str, page: int=0, size: int=20)` | `/clan/api/v1/clan/tribe/blurry/info` |  |
| `invite(friend_ids: list[int], msg: str='')` | `/clan/api/v1/clan/tribe/member/invite` |  |
| `approve_member(other_id: int)` | `/clan/api/v1/clan/tribe/member/agreement` |  |
| `reject_member(other_id: int)` | `/clan/api/v1/clan/tribe/member/rejection` |  |
| `mute_member(member_id: int, minutes: int)` | `/clan/api/v1/clan/tribe/mute/member` |  |
| `unmute_member(member_id: int)` | `/clan/api/v1/clan/tribe/mute/member` |  |
| `mute_all()` | `/clan/api/v1/clan/tribe/mute` |  |
| `unmute_all()` | `/clan/api/v1/clan/tribe/mute` |  |
| `remove_members(member_ids: list[int])` | `/clan/api/v1/clan/tribe/member/remove/batch` |  |
| `edit(clan_id: int, currency: int=0, details: str='', head_pic: str='', name: str='', tags: list[str] | None=None)` | `/clan/api/v1/clan/tribe` |  |
| `edit_elders(type_: int, elder_ids: list[int])` | `/clan/api/v1/clan/tribe/members` |  |
| `set_verification(enabled: bool)` | `/clan/api/v1/clan/free/verification` |  |
| `buy_decoration(decoration_id: int)` | `/clan/api/v1/clan/decorations/purchase` |  |
| `accept_task(task_id: int, is_team_task: bool)` | `/clan/api/v1/clan/tasks/accept` |  |
| `claim_task(task_id: int, is_team_task: bool)` | `/clan/api/v1/clan/tasks` |  |
| `get_personal_tasks(task_type: int=1)` | `/clan/api/v3/clan/personal/tasks` |  |
| `post_bulletin(content: str)` | `/clan/api/v1/clan/tribe/bulletin` |  |
| `transfer_chief(new_chief_id: int)` | `/clan/api/v1/clan/tribe/member` |  |
| `create(clan_id: int=0, currency: int=2, details: str='', head_pic: str='', name: str='', tags: list[str] | None=None)` | `/clan/api/v3/clan/tribe` |  |
| `dissolve(clan_id: int)` | `/clan/api/v1/clan/tribe` |  |
| `get_donation_info()` | `/clan/api/v1/clan/tribe/donation` |  |
| `get_donation_history_page(page: int=0, size: int=50)` | `/clan/api/v2/clan/tribe/donation/history` |  |
| `get_donation_history_all(size: int=50, delay: float=0.3)` | `—` |  |
| `get_user_clan_role(uid: int)` | `/bedwar/api/v1/friends/clan/by/userIds` |  |
| `apply_to_clan(clan_id: int, msg: str='')` | `—` |  |
| `leave_clan()` | `—` |  |
| `get_clan_info(clan_id: int)` | `—` |  |
| `get_clan_members()` | `—` |  |
| `async async_get_own_clan()` | `/clan/api/v1/clan/tribe/base` |  |
| `async async_get_info(clan_id: int)` | `/clan/api/v2/clan/tribe` |  |
| `async async_get_members()` | `/clan/api/v1/clan/tribe/member` |  |
| `async async_join(clan_id: int, msg: str='')` | `/clan/api/v1/clan/tribe/member` |  |
| `async async_leave(clan_id: int)` | `/clan/api/v1/clan/tribe/member` |  |
| `async async_search(clan_name: str, page: int=0, size: int=20)` | `/clan/api/v1/clan/tribe/blurry/info` |  |
| `async async_invite(friend_ids: list[int], msg: str='')` | `/clan/api/v1/clan/tribe/member/invite` |  |
| `async async_approve_member(other_id: int)` | `/clan/api/v1/clan/tribe/member/agreement` |  |
| `async async_reject_member(other_id: int)` | `/clan/api/v1/clan/tribe/member/rejection` |  |
| `async async_mute_member(member_id: int, minutes: int)` | `/clan/api/v1/clan/tribe/mute/member` |  |
| `async async_unmute_member(member_id: int)` | `/clan/api/v1/clan/tribe/mute/member` |  |
| `async async_mute_all()` | `/clan/api/v1/clan/tribe/mute` |  |
| `async async_unmute_all()` | `/clan/api/v1/clan/tribe/mute` |  |
| `async async_remove_members(member_ids: list[int])` | `/clan/api/v1/clan/tribe/member/remove/batch` |  |
| `async async_edit(clan_id: int, currency: int=0, details: str='', head_pic: str='', name: str='', tags: list[str] | None=None)` | `/clan/api/v1/clan/tribe` |  |
| `async async_edit_elders(type_: int, elder_ids: list[int])` | `/clan/api/v1/clan/tribe/members` |  |
| `async async_set_verification(enabled: bool)` | `/clan/api/v1/clan/free/verification` |  |
| `async async_buy_decoration(decoration_id: int)` | `/clan/api/v1/clan/decorations/purchase` |  |
| `async async_accept_task(task_id: int, is_team_task: bool)` | `/clan/api/v1/clan/tasks/accept` |  |
| `async async_claim_task(task_id: int, is_team_task: bool)` | `/clan/api/v1/clan/tasks` |  |
| `async async_get_personal_tasks(task_type: int=1)` | `/clan/api/v3/clan/personal/tasks` |  |
| `async async_post_bulletin(content: str)` | `/clan/api/v1/clan/tribe/bulletin` |  |
| `async async_transfer_chief(new_chief_id: int)` | `/clan/api/v1/clan/tribe/member` |  |
| `async async_create(clan_id: int=0, currency: int=2, details: str='', head_pic: str='', name: str='', tags: list[str] | None=None)` | `/clan/api/v3/clan/tribe` |  |
| `async async_dissolve(clan_id: int)` | `/clan/api/v1/clan/tribe` |  |
| `async async_get_donation_info()` | `/clan/api/v1/clan/tribe/donation` |  |
| `async async_get_donation_history_page(page: int=0, size: int=50)` | `/clan/api/v2/clan/tribe/donation/history` |  |
| `async async_get_donation_history_all(size: int=50, delay: float=0.3)` | `—` |  |
| `async async_get_user_clan_role(uid: int)` | `/bedwar/api/v1/friends/clan/by/userIds` |  |
| `async async_apply_to_clan(clan_id: int, msg: str='')` | `/clan/api/v1/clan/tribe/member` |  |
| `async async_leave_clan()` | `/clan/api/v1/clan/tribe/member` |  |
| `async async_get_clan_info(clan_id: int)` | `/clan/api/v2/clan/tribe` |  |
| `get_clan_rank(rank_type: str='weekly', page: int=0, size: int=20, rank_key: str='clanBattle')` | `/clan/api/v1/clan/rank` |  |
| `get_clan_rank_new()` | `/clan/api/v1/clan/rank/new` |  |
| `get_user_clan_rank(rank_type: str='weekly', rank_key: str='clanBattle')` | `/clan/api/v1/clan/user/rank` |  |
| `get_user_clan_rank_new(rank_type: str='weekly')` | `/clan/api/v1/clan/user/rank/new` |  |
| `get_clan_currency()` | `/clan/api/v1/clan/tribe/currency` |  |
| `donate(currency: int=0, quantity: int=0)` | `/clan/api/v3/clan/tribe/donation` |  |
| `get_bulletin()` | `/clan/api/v1/clan/tribe/bulletin` |  |
| `get_recommendations()` | `/clan/api/v1/clan/tribe/recommendation` |  |
| `get_clan_id()` | `/clan/api/v1/clan/tribe/id` |  |
| `accept_invitation(invitation_id: int)` | `/clan/api/v1/clan/tribe/member/agreement/invitation` |  |
| `reject_invitation(invitation_id: int)` | `/clan/api/v1/clan/tribe/member/rejection/invitation` |  |
| `get_member_messages()` | `/clan/api/v2/clan/tribe/member/message` |  |
| `get_red_point()` | `/clan/api/v1/red-point` |  |
| `get_decorations_by_type(type_id: int)` | `/clan/api/v1/clan/decorations/{type_id}` |  |
| `report_clan()` | `/clan/api/v1/clan/tribe/report` |  |
| `async async_get_clan_rank(rank_type: str='weekly', page: int=0, size: int=20, rank_key: str='clanBattle')` | `/clan/api/v1/clan/rank` |  |
| `async async_get_clan_rank_new()` | `/clan/api/v1/clan/rank/new` |  |
| `async async_get_user_clan_rank(rank_type: str='weekly', rank_key: str='clanBattle')` | `/clan/api/v1/clan/user/rank` |  |
| `async async_get_user_clan_rank_new(rank_type: str='weekly')` | `/clan/api/v1/clan/user/rank/new` |  |
| `async async_get_clan_currency()` | `/clan/api/v1/clan/tribe/currency` |  |
| `async async_donate(currency: int=0, quantity: int=0)` | `/clan/api/v3/clan/tribe/donation` |  |
| `async async_get_bulletin()` | `/clan/api/v1/clan/tribe/bulletin` |  |
| `async async_get_recommendations()` | `/clan/api/v1/clan/tribe/recommendation` |  |
| `async async_get_clan_id()` | `/clan/api/v1/clan/tribe/id` |  |
| `async async_accept_invitation(invitation_id: int)` | `/clan/api/v1/clan/tribe/member/agreement/invitation` |  |
| `async async_reject_invitation(invitation_id: int)` | `/clan/api/v1/clan/tribe/member/rejection/invitation` |  |
| `async async_get_member_messages()` | `/clan/api/v2/clan/tribe/member/message` |  |
| `async async_get_red_point()` | `/clan/api/v1/red-point` |  |
| `async async_get_decorations_by_type(type_id: int)` | `/clan/api/v1/clan/decorations/{type_id}` |  |
| `async async_report_clan()` | `/clan/api/v1/clan/tribe/report` |  |
| `async async_get_clan_members()` | `/clan/api/v1/clan/tribe/member` |  |

## `DecorationAPI`

Decoration resources and recommendations.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_wardrobe(uid: int)` | `/decoration/api/v1/new/decorations/users/{uid}/classify/all` |  |
| `get_current_price(skin_id: int, is_suit: bool)` | `/decoration/api/v1/decoration/current/price` |  |
| `buy(diamond: int, cloth_voucher: int, pay_type: int)` | `/shop/api/v1/new/shop/decorations/buy` |  |
| `get_shop_info()` | `/user/api/v1/user/shop/info` |  |
| `equip(skin_id: int)` | `/decoration/api/v1/decorations/using/new` |  |
| `get_skins(uid: int, engine_version: str='10105')` | `/decoration/api/v1/new/decorations/users/{uid}/classify/all` |  |
| `get_decorations_result(uid: int)` | `—` |  |
| `async async_get_wardrobe(uid: int)` | `/decoration/api/v1/new/decorations/users/{uid}/classify/all` |  |
| `async async_get_current_price(skin_id: int, is_suit: bool)` | `/decoration/api/v1/decoration/current/price` |  |
| `async async_buy(diamond: int, cloth_voucher: int, pay_type: int)` | `/shop/api/v1/new/shop/decorations/buy` |  |
| `async async_get_shop_info()` | `/user/api/v1/user/shop/info` |  |
| `async async_equip(skin_id: int)` | `/decoration/api/v1/decorations/using/new` |  |
| `async async_get_skins(uid: int, engine_version: str='10105')` | `/decoration/api/v1/new/decorations/users/{uid}/classify/all` |  |
| `async async_get_decorations_result(uid: int)` | `—` |  |

## `ExtendedAPI`

Wrappers for the newer 3.29.x endpoints captured from the Android client. These methods are intentionally thin: they return the raw API envelope. Most methods are synchronous; ``async_request`` remains available for async callers.

| Method | Endpoint | Description |
| --- | --- | --- |
| `activity_home_page()` | `/activity/api/v1/activity/home/page` |  |
| `ad_draw_info(activity_id: str='ad_draw_activity1')` | `/activity/api/v1/ad-draw/info` |  |
| `background_image()` | `/activity/api/v1/background-image` |  |
| `community_jump_info(activity_id: str='community_jump_activity')` | `/activity/api/v1/community-jump/info` |  |
| `direct_purchase_puzzles_popup()` | `/activity/api/v1/direct-purchase/puzzles/popup` |  |
| `game_banner_red_point()` | `/activity/api/v1/game/banner/new/red-point` |  |
| `holiday_score_info(activity_id: str='holiday_score_202609')` | `/activity/api/v1/holiday-score/info` |  |
| `preorder_holiday_score_pack(body: dict[str, Any] | None=None)` | `/activity/api/v1/holiday-score/pack/pre-order` |  |
| `holiday_score_rank_period(params: dict[str, Any] | None=None)` | `/activity/api/v1/holiday-score/rank/period` |  |
| `holiday_score_rank_reward_preview(params: dict[str, Any] | None=None)` | `/activity/api/v1/holiday-score/rank/reward-preview` |  |
| `holiday_score_rank_total(params: dict[str, Any] | None=None)` | `/activity/api/v1/holiday-score/rank/total` |  |
| `homepage_ad_banner(language: str='en_US', region: str | None=None, tab_code: str='')` | `/activity/api/v1/homepage/ad-banner` |  |
| `homepage_game_detail_icon_activity(game_id: str)` | `/activity/api/v1/homepage/game-detail/icon-activity` |  |
| `limit_gcube_pack_info(popup_scene: int | None=None)` | `/activity/api/v1/limit/gcube/pack/info` |  |
| `return_activity_info()` | `/activity/api/v1/return-activity/info` |  |
| `receive_sub_pkg_transfer_reward(body: dict[str, Any] | None=None)` | `/activity/api/v1/sub-pkg-transfer/reward/receive` |  |
| `tradplus_ad_config(force_update: bool=False)` | `/activity/api/v1/tradplus/ad/open-config` |  |
| `treasure_bowl_survey_status()` | `/activity/api/v1/treasure/bowl/rebate/survey/status` |  |
| `homepage_activity_list_group(language: str='en_US')` | `/activity/api/v2/homepage/activity-list/group` |  |
| `newbie_activity_status()` | `/activity/api/v2/newbie/activity/status` |  |
| `theme()` | `/activity/api/v2/theme` |  |
| `daily_ad_red_points()` | `/activity/daily/ad/activity/red/points` |  |
| `using_decorations(uid: int | None=None)` | `/decoration/api/v1/decorations-v2/{uid or self._account.uid}/using` |  |
| `check_new_decorations_resource(res_version: int, engine_version: int=10114)` | `/decoration/api/v1/new/decorations/check/resource` |  |
| `recommended_decorations()` | `/decoration/api/v1/recommend/get` |  |
| `decoration_red_points()` | `/decoration/api/v1/redpoints` |  |
| `decoration_model_number()` | `/decoration/api/v1/user/decoration/model/number` |  |
| `family_recruit_status()` | `/friend/api/v1/family/recruit/status` |  |
| `homeland_suspended_entrance()` | `/friend/api/v1/homeland/suspended/entrance` |  |
| `friends_v3(page: int=0, size: int=500, show_big_party: bool=True)` | `/friend/api/v3/friends` |  |
| `friend_v3(uid: int, show_big_party: bool=True)` | `/friend/api/v3/friends/{uid}` |  |
| `friend_tags()` | `/friend/api/v1/tag/only` |  |
| `friend_popularity(uid: int)` | `/friend/api/v1/popularity/{uid}` |  |
| `mining_token_balance_with_transform()` | `/game/api/v1/backpack/mining-token/balance/with-transform` |  |
| `bghall_game_entrance_ui_config()` | `/game/api/v1/bghall/game-entrance/ui-config` |  |
| `ping_server_list()` | `/game/api/v1/ping/server/list` |  |
| `user_highlight_data(target_id: int)` | `/game/api/v1/user/highlight/data` |  |
| `game_revision_combine(filter_type_id: int=0, is_filter: int=0, os_name: str='android', page: int=0, size: int=20)` | `/game/api/v2/game/revision/all/list/by/condition/combine` |  |
| `check_app_engine_update(engine_version: int=10114, common_res_version: int=0, game_res_version: int=0, game_type: str='', engine_type: str='v1')` | `/game/api/v2/games/app-engine/check-update` |  |
| `clan_rank(params: dict[str, Any] | None=None)` | `/clan/api/v1/clan/rank` |  |
| `clan_rank_new(params: dict[str, Any] | None=None)` | `/clan/api/v1/clan/rank/new` |  |
| `clan_user_rank(params: dict[str, Any] | None=None)` | `/clan/api/v1/clan/user/rank` |  |
| `clan_user_rank_new(params: dict[str, Any] | None=None)` | `/clan/api/v1/clan/user/rank/new` |  |
| `redeem_cdkey(body: dict[str, Any] | None=None, cdkey: str | None=None)` | `/mailbox/api/v1/cdkey/redeem` |  |
| `mark_user_notifications_unread(body: dict[str, Any] | None=None)` | `/msg/api/v1/user-notification/unread` |  |
| `area_pack_popup_info()` | `/pay/api/v1/area/pack/popup/info` |  |
| `disposable_advance_order(product_id: str, data: str)` | `/pay/api/v1/pay/disposable/advance/order` |  |
| `product_info_batch(product_ids: list[str] | str, country: str='US')` | `/pay/api/v1/product/info/batch/get` |  |
| `third_pay_access_status()` | `/pay/api/v1/third-pay/user/access-status` |  |
| `xsolla_billing_get()` | `/pay/api/v1/xsolla/billing/get` |  |
| `xsolla_enable()` | `/pay/api/v1/xsolla/enable` |  |
| `abtest_user_test()` | `/user/api/v1/abtest/getUserTest` |  |
| `chat_migrate_data()` | `/user/api/v1/chat/migrate/data` |  |
| `trigger_client_event(trigger_type: int=1)` | `/user/api/v1/client/trigger/event` |  |
| `sensitive_word_regions()` | `/user/api/v1/sensitive/word/region/list` |  |
| `collect_feedback_task()` | `/user/api/v1/user-feedback/collect-task` |  |
| `set_user_language(user_id: int | None=None, language: str='en')` | `/user/api/v1/user/language` |  |
| `logout()` | `/user/api/v1/user/login-out` |  |
| `vip_customer_popup_needed()` | `/user/api/v1/user/vip/customer/info/pop/up/needed` |  |
| `web_auth_code(body: dict[str, Any] | None=None)` | `/user/api/v1/web/auth-code` |  |
| `security_settings(user_id: int | None=None)` | `/user/api/v2/users/verify/user/security/settings` |  |
| `user_details_v3()` | `/user/api/v3/user/details/info` |  |
| `auth_token(q: str)` | `/user/api/v5/account/auth-token` |  |

## `FriendsAPI`

Friends, requests, tags, and popularity.

| Method | Endpoint | Description |
| --- | --- | --- |
| `list_friends(page: int=1, size: int=50)` | `/friend/api/v1/friends/status` |  |
| `get_info(friend_id: int)` | `/friend/api/v1/friends/info/id/{friend_id}` |  |
| `send_request(friend_id: int, msg: str='Hello!')` | `/friend/api/v1/friends` |  |
| `accept_request(friend_id: int)` | `/friend/api/v1/friends/{friend_id}/agreement` |  |
| `reject_request(friend_id: int)` | `/friend/api/v1/friends/{friend_id}/rejection` |  |
| `delete_friend(friend_id: int)` | `/friend/api/v1/friends` |  |
| `set_alias(friend_id: int, alias: str)` | `/friend/api/v1/friends/{friend_id}/alias` |  |
| `get_status(uids: list[int])` | `/friend/api/v2/friends/status` |  |
| `add_popularity(friend_id: int)` | `/friend/api/v1/popularity` |  |
| `get_popularity(friend_id: int)` | `/friend/api/v1/popularity/{friend_id}` |  |
| `get_requests(page: int=1, size: int=50)` | `/friend/api/v1/friends/requests` |  |
| `approve_all_requests()` | `/friend/api/v1/friends/requests/approve-all` |  |
| `reject_all_requests()` | `/friend/api/v1/friends/requests/reject-all` |  |
| `search(query: str, page: int=1, size: int=20)` | `/friend/api/v1/friends/info/{query}` |  |
| `search_friends(query: str)` | `—` |  |
| `get_family_list(uid: int)` | `—` |  |
| `get_follow_list()` | `/friend/api/v1/friends/follow` |  |
| `get_notice_list(notice_type: int | None=None)` | `/friend/api/v1/friends/notice-list` |  |
| `get_recommendations()` | `/friend/api/v1/friends/recommendation` |  |
| `get_new_recommendations()` | `/friend/api/v2/friends/recommendation/new` |  |
| `get_settings(uid: int)` | `/friend/api/v1/friends/settings/{uid}` |  |
| `get_gaming_status(friend_id: int)` | `/friend/api/v1/friends/{friend_id}/gaming` |  |
| `get_friends_game_online()` | `/friend/api/v1/get/friends/game/online` |  |
| `get_apply_count()` | `/friend/api/v1/friends/apply/num` |  |
| `reject_request_by_id(request_id: int)` | `/friend/api/v1/friends/requests/{request_id}` |  |
| `remove_alias(friend_id: int)` | `/friend/api/v1/friends/{friend_id}/alias` |  |
| `get_popularity_list()` | `/friend/api/v1/popularity/list` |  |
| `get_popularity_props()` | `/friend/api/v1/popularity/props` |  |
| `get_tags()` | `/friend/api/v1/tag` |  |
| `get_tags_only()` | `/friend/api/v1/tag/only` |  |
| `async async_list_friends(page: int=1, size: int=50)` | `/friend/api/v1/friends/status` |  |
| `async async_get_info(friend_id: int)` | `/friend/api/v1/friends/info/id/{friend_id}` |  |
| `async async_send_request(friend_id: int, msg: str='Hello!')` | `/friend/api/v1/friends` |  |
| `async async_accept_request(friend_id: int)` | `/friend/api/v1/friends/{friend_id}/agreement` |  |
| `async async_reject_request(friend_id: int)` | `/friend/api/v1/friends/{friend_id}/rejection` |  |
| `async async_delete_friend(friend_id: int)` | `/friend/api/v1/friends` |  |
| `async async_set_alias(friend_id: int, alias: str)` | `/friend/api/v1/friends/{friend_id}/alias` |  |
| `async async_get_status(uids: list[int])` | `/friend/api/v2/friends/status` |  |
| `async async_add_popularity(friend_id: int)` | `—` |  |
| `async async_get_popularity(friend_id: int)` | `—` |  |
| `async async_get_requests(page: int=1, size: int=50)` | `—` |  |
| `async async_approve_all_requests()` | `—` |  |
| `async async_reject_all_requests()` | `—` |  |
| `async async_search(query: str, page: int=1, size: int=20)` | `/friend/api/v1/friends/info/{query}` |  |
| `async async_search_friends(query: str)` | `—` |  |
| `async async_get_family_list(uid: int)` | `—` |  |
| `async async_get_follow_list()` | `/friend/api/v1/friends/follow` |  |
| `async async_get_notice_list(notice_type: int | None=None)` | `/friend/api/v1/friends/notice-list` |  |
| `async async_get_recommendations()` | `/friend/api/v1/friends/recommendation` |  |
| `async async_get_new_recommendations()` | `/friend/api/v2/friends/recommendation/new` |  |
| `async async_get_settings(uid: int)` | `/friend/api/v1/friends/settings/{uid}` |  |
| `async async_get_gaming_status(friend_id: int)` | `/friend/api/v1/friends/{friend_id}/gaming` |  |
| `async async_get_friends_game_online()` | `/friend/api/v1/get/friends/game/online` |  |
| `async async_get_apply_count()` | `/friend/api/v1/friends/apply/num` |  |
| `async async_reject_request_by_id(request_id: int)` | `/friend/api/v1/friends/requests/{request_id}` |  |
| `async async_remove_alias(friend_id: int)` | `/friend/api/v1/friends/{friend_id}/alias` |  |
| `async async_get_popularity_list()` | `/friend/api/v1/popularity/list` |  |
| `async async_get_popularity_props()` | `/friend/api/v1/popularity/props` |  |
| `async async_get_tags()` | `/friend/api/v1/tag` |  |
| `async async_get_tags_only()` | `/friend/api/v1/tag/only` |  |

## `GameAPI`

Game catalogue, launch/auth, rooms, and leaderboards.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_game_list(page: int=0, size: int=20, filter_type_id: int=0, filter_tag_id: int=0, is_filter: int=0, sort_type: str='', ram: int=0, language: str='en_US')` | `/game/api/v2/game/revision/list/by/condition` | Return the current game catalogue using the v2 condition endpoint. |
| `async async_get_game_list(page: int=0, size: int=20, filter_type_id: int=0, filter_tag_id: int=0, is_filter: int=0, sort_type: str='', ram: int=0, language: str='en_US')` | `/game/api/v2/game/revision/list/by/condition` |  |
| `list_games(page: int=1, size: int=20, order_type: str='', type_id: int=0, order: str='', is_publish: int=1)` | `/game/api/v1/games` | Legacy v1 game list; prefer :meth:get_game_list. |
| `get_game_details(game_id: str, app_version: int=5753, engine_version: int=0, ram: int=0)` | `/game/api/v3/games/{game_id}` |  |
| `get_game_ranking(game_id: str, period: str='all', page: int=1, size: int=10, game_version: int | None=None)` | `—` |  |
| `get_usage_ranking(game_id: str, page: int=1, size: int=10)` | `/game/api/v1/games/{game_id}/uses/rank` |  |
| `get_hot_games()` | `/game/api/v1/game-list/homepage/hot` |  |
| `get_recommended_games()` | `/game/api/v2/game-list/homepage/recommend` |  |
| `get_game_categories()` | `/game/api/v1/game-list/category/list` |  |
| `get_games_by_category(category_id: str, page: int=1, size: int=20)` | `/game/api/v1/game-list/by/category` |  |
| `get_app_categories()` | `/game/api/v1/app/categories` |  |
| `get_categories_by_language(language: str='en_US')` | `/game/api/v1/category/list/by/language` |  |
| `get_game_config(game_id: str)` | `/game/api/v1/games/config/app/{game_id}` |  |
| `get_game_mode_config(game_id: str)` | `/game/api/v1/games/mode/config/app/{game_id}` |  |
| `get_resource_version()` | `/game/api/v1/games/resource/version` |  |
| `search_games(keyword: str, page: int=1, size: int=20)` | `/game/api/v1/game/info/search` |  |
| `get_update_tip(game_id: str, engine_version: int=10114, is_new: int=0)` | `/game/api/v1/games/update/tip/info/app/{game_id}` |  |
| `get_update_list(user_id: int, old_engine_version: int=10114, new_engine_version: int=20084)` | `/game/api/v1/games/update/list/{user_id}` |  |
| `get_warmup_info(game_id: str, language: str='en_US')` | `/game/api/v1/games/warmup/{game_id}/languages/{language}` |  |
| `get_all_open_parties(app_version: int=5753)` | `/game/api/v1/games/all/open/party` |  |
| `get_team_members(team_id: str)` | `/game/api/v1/games/team/member/{team_id}` |  |
| `get_turntable_info(game_id: str)` | `/game/api/v1/game/{game_id}/turntable` |  |
| `claim_turntable(game_id: str)` | `/game/api/v1/game/{game_id}/turntable` |  |
| `get_praise_online_info(game_ids: str | list[str] | None=None)` | `/game/api/v1/game/praise/online/info` |  |
| `update_engine(engine_version: str)` | `/game/api/v1/games/engine` |  |
| `like_game(game_id: str)` | `/game/api/v1/games/like` |  |
| `post_comment(game_id: str, content: str)` | `/game/api/v1/comment` |  |
| `get_svip_game_list()` | `/game/api/v1/vip-privilege-game/svip-game-list` |  |
| `get_vip_game_list()` | `/game/api/v1/vip-privilege-game/vip-game-list` |  |
| `create_room(game_id: str, room_name: str='', max_players: int=0, is_private: bool=False, password: str='')` | `/game/api/v4/gameroom/create` |  |
| `list_rooms(game_id: str, page: int=1, size: int=20)` | `/game/api/v2/gameroom/list` |  |
| `list_rooms_v4(game_id: str, page: int=1, size: int=20)` | `/game/api/v4/gameroom/list` |  |
| `get_room_details(room_id: str)` | `/game/api/v1/gameroom/details` |  |
| `get_room_details_v3(room_id: str)` | `/game/api/v3/gameroom/details` |  |
| `enter_room(room_id: str)` | `/game/api/v1/gameroom/enter` |  |
| `exit_room(room_id: str)` | `/game/api/v1/gameroom/exit` |  |
| `check_room(room_id: str)` | `/game/api/v1/gameroom/check` |  |
| `share_room(room_id: str)` | `/game/api/v1/gameroom/share` |  |
| `enter_game(room_id: str)` | `/game/api/v1/gameroom/enter-game` |  |
| `like_work(work_id: str)` | `/game/api/v1/gameroom/work/{work_id}/like` |  |
| `unlike_work(work_id: str)` | `/game/api/v1/gameroom/work/{work_id}/unlike` |  |
| `get_random_work()` | `/game/api/v1/gameroom/work/random` |  |
| `get_random_feed()` | `/game/api/v1/gameroom/work/random-feed` |  |
| `get_recently_created(page: int=1)` | `/game/api/v1/gameroom/recent/created` |  |
| `get_recently_played(page: int=1)` | `/game/api/v1/gameroom/recent/played` |  |
| `get_creative_list(page: int=1, size: int=20)` | `/game/api/v1/gameroom/creative/list` |  |
| `get_creative_detail(creative_id: str)` | `/game/api/v1/gameroom/creative/{creative_id}` |  |
| `get_room_permissions()` | `/game/api/v1/gameroom/permissions` |  |
| `assign_preview(work_id: str, preview_url: str)` | `/game/api/v1/gameroom/work/{work_id}/preview/assign` |  |
| `set_room_password(room_id: str, password: str)` | `/game/api/v1/room/password/set` |  |
| `clear_room_password(room_id: str)` | `/game/api/v1/room/password/clear` |  |
| `get_mining_room_list(page: int=1, size: int=20)` | `/game/api/v1/mining/room/list` |  |
| `get_running_mining_rooms()` | `/game/api/v1/mining/room/running` |  |
| `get_mining_record_summary()` | `/game/api/v1/mining/record/summary` |  |
| `get_mining_shop_info()` | `/game/api/v1/mining/shop/info` |  |
| `exchange_mining_currency(amount: int)` | `/game/api/v1/mining/shop/currency/exchange` |  |
| `exchange_mining_token(amount: int)` | `/game/api/v1/mining/shop/sub-token/exchange` |  |
| `purchase_mining_decoration(decoration_id: int)` | `/game/api/v1/mining/shop/decoration/purchase` |  |
| `refresh_mining_decoration()` | `/game/api/v1/mining/shop/decoration/refresh` |  |
| `get_pickaxe_balance()` | `/game/api/v1/pickaxe/balance` |  |
| `get_mining_token_balance()` | `/game/api/v1/mining/token/balance` |  |
| `game_auth_v2(game_id: str)` | `/game/api/v2/flow/game/auth` |  |
| `async async_list_games(page: int=1, size: int=20, order_type: str='', type_id: int=0, order: str='', is_publish: int=1)` | `/game/api/v1/games` |  |
| `async async_get_game_details(game_id: str, app_version: int=5753, engine_version: int=0, ram: int=0)` | `/game/api/v3/games/{game_id}` |  |
| `async async_get_game_ranking(game_id: str, period: str='all', page: int=1, size: int=10, game_version: int | None=None)` | `—` |  |
| `async async_get_usage_ranking(game_id: str, page: int=1, size: int=10)` | `/game/api/v1/games/{game_id}/uses/rank` |  |
| `async async_get_hot_games()` | `/game/api/v1/game-list/homepage/hot` |  |
| `async async_get_recommended_games()` | `/game/api/v2/game-list/homepage/recommend` |  |
| `async async_get_game_categories()` | `/game/api/v1/game-list/category/list` |  |
| `async async_get_games_by_category(category_id: str, page: int=1, size: int=20)` | `/game/api/v1/game-list/by/category` |  |
| `async async_get_app_categories()` | `/game/api/v1/app/categories` |  |
| `async async_get_categories_by_language(language: str='en_US')` | `/game/api/v1/category/list/by/language` |  |
| `async async_get_game_config(game_id: str)` | `/game/api/v1/games/config/app/{game_id}` |  |
| `async async_get_game_mode_config(game_id: str)` | `/game/api/v1/games/mode/config/app/{game_id}` |  |
| `async async_get_resource_version()` | `/game/api/v1/games/resource/version` |  |
| `async async_search_games(keyword: str, page: int=1, size: int=20)` | `/game/api/v1/game/info/search` |  |
| `async async_get_update_tip(game_id: str, engine_version: int=10114, is_new: int=0)` | `/game/api/v1/games/update/tip/info/app/{game_id}` |  |
| `async async_get_update_list(user_id: int, old_engine_version: int=10114, new_engine_version: int=20084)` | `/game/api/v1/games/update/list/{user_id}` |  |
| `async async_get_warmup_info(game_id: str, language: str='en_US')` | `/game/api/v1/games/warmup/{game_id}/languages/{language}` |  |
| `async async_get_all_open_parties(app_version: int=5753)` | `/game/api/v1/games/all/open/party` |  |
| `async async_get_team_members(team_id: str)` | `/game/api/v1/games/team/member/{team_id}` |  |
| `async async_get_turntable_info(game_id: str)` | `/game/api/v1/game/{game_id}/turntable` |  |
| `async async_claim_turntable(game_id: str)` | `/game/api/v1/game/{game_id}/turntable` |  |
| `async async_get_praise_online_info(game_ids: str | list[str] | None=None)` | `/game/api/v1/game/praise/online/info` |  |
| `async async_update_engine(engine_version: str)` | `/game/api/v1/games/engine` |  |
| `async async_like_game(game_id: str)` | `/game/api/v1/games/like` |  |
| `async async_post_comment(game_id: str, content: str)` | `/game/api/v1/comment` |  |
| `async async_get_svip_game_list()` | `/game/api/v1/vip-privilege-game/svip-game-list` |  |
| `async async_get_vip_game_list()` | `/game/api/v1/vip-privilege-game/vip-game-list` |  |
| `async async_create_room(game_id: str, room_name: str='', max_players: int=0, is_private: bool=False, password: str='')` | `/game/api/v4/gameroom/create` |  |
| `async async_list_rooms(game_id: str, page: int=1, size: int=20)` | `/game/api/v2/gameroom/list` |  |
| `async async_list_rooms_v4(game_id: str, page: int=1, size: int=20)` | `/game/api/v4/gameroom/list` |  |
| `async async_get_room_details(room_id: str)` | `/game/api/v1/gameroom/details` |  |
| `async async_get_room_details_v3(room_id: str)` | `/game/api/v3/gameroom/details` |  |
| `async async_enter_room(room_id: str)` | `/game/api/v1/gameroom/enter` |  |
| `async async_exit_room(room_id: str)` | `/game/api/v1/gameroom/exit` |  |
| `async async_check_room(room_id: str)` | `/game/api/v1/gameroom/check` |  |
| `async async_share_room(room_id: str)` | `/game/api/v1/gameroom/share` |  |
| `async async_enter_game(room_id: str)` | `/game/api/v1/gameroom/enter-game` |  |
| `async async_like_work(work_id: str)` | `/game/api/v1/gameroom/work/{work_id}/like` |  |
| `async async_unlike_work(work_id: str)` | `/game/api/v1/gameroom/work/{work_id}/unlike` |  |
| `async async_get_random_work()` | `/game/api/v1/gameroom/work/random` |  |
| `async async_get_random_feed()` | `/game/api/v1/gameroom/work/random-feed` |  |
| `async async_get_recently_created(page: int=1)` | `/game/api/v1/gameroom/recent/created` |  |
| `async async_get_recently_played(page: int=1)` | `/game/api/v1/gameroom/recent/played` |  |
| `async async_get_creative_list(page: int=1, size: int=20)` | `/game/api/v1/gameroom/creative/list` |  |
| `async async_get_creative_detail(creative_id: str)` | `/game/api/v1/gameroom/creative/{creative_id}` |  |
| `async async_get_room_permissions()` | `/game/api/v1/gameroom/permissions` |  |
| `async async_assign_preview(work_id: str, preview_url: str)` | `/game/api/v1/gameroom/work/{work_id}/preview/assign` |  |
| `async async_set_room_password(room_id: str, password: str)` | `/game/api/v1/room/password/set` |  |
| `async async_clear_room_password(room_id: str)` | `/game/api/v1/room/password/clear` |  |
| `async async_get_mining_room_list(page: int=1, size: int=20)` | `/game/api/v1/mining/room/list` |  |
| `async async_get_running_mining_rooms()` | `/game/api/v1/mining/room/running` |  |
| `async async_get_mining_record_summary()` | `/game/api/v1/mining/record/summary` |  |
| `async async_get_mining_shop_info()` | `/game/api/v1/mining/shop/info` |  |
| `async async_exchange_mining_currency(amount: int)` | `/game/api/v1/mining/shop/currency/exchange` |  |
| `async async_exchange_mining_token(amount: int)` | `/game/api/v1/mining/shop/sub-token/exchange` |  |
| `async async_purchase_mining_decoration(decoration_id: int)` | `/game/api/v1/mining/shop/decoration/purchase` |  |
| `async async_refresh_mining_decoration()` | `/game/api/v1/mining/shop/decoration/refresh` |  |
| `async async_get_pickaxe_balance()` | `/game/api/v1/pickaxe/balance` |  |
| `async async_get_mining_token_balance()` | `/game/api/v1/mining/token/balance` |  |
| `async async_game_auth_v2(game_id: str)` | `/game/api/v2/flow/game/auth` |  |
| `get_game_leaderboard(game_id: str, period: str='all', page: int=0, size: int=10, game_version: int | None=None, language: str='en_US')` | `/game/api/v1/games/{game_id}/rank` | Return one raw page of a game leaderboard. `period` is `all`, `week`, or `month`. `page` is zero-based. Use :meth:get_game_leaderboard_entries for parsed `RankEntry` rows. |
| `async async_get_game_leaderboard(game_id: str, period: str='all', page: int=0, size: int=10, game_version: int | None=None, language: str='en_US')` | `/game/api/v1/games/{game_id}/rank` |  |
| `get_game_leaderboard_entries(game_id: str, period: str='all', page: int=0, size: int=10, game_version: int | None=None, language: str='en_US')` | `—` | Return parsed leaderboard rows from :class:RankingAPI. |
| `async async_get_game_leaderboard_entries(game_id: str, period: str='all', page: int=0, size: int=10, game_version: int | None=None, language: str='en_US')` | `—` |  |
| `get_game_usage_leaderboard(game_id: str, period: str='all', language: str='en_US')` | `/game/api/v1/games/{game_id}/uses/rank` | Return the logged-in account's rank for a game and period. |
| `async async_get_game_usage_leaderboard(game_id: str, period: str='all', language: str='en_US')` | `/game/api/v1/games/{game_id}/uses/rank` |  |
| `get_game_my_rank(game_id: str, period: str='all', language: str='en_US')` | `—` | Alias for :meth:get_game_usage_leaderboard. |
| `async async_get_game_my_rank(game_id: str, period: str='all', language: str='en_US')` | `—` |  |
| `game_auth(game_id: str, game_version: int=10114)` | `—` |  |
| `async async_game_auth(game_id: str, game_version: int=10114)` | `—` |  |
| `party_auth_v3(game_id: str='', engine4_version: int=40040, is_new_engine: bool=False)` | `/game/api/v3/party/auth` |  |
| `async async_party_auth_v3(game_id: str='', engine4_version: int=40040, is_new_engine: bool=False)` | `/game/api/v3/party/auth` |  |
| `get_ping_server_list()` | `/game/api/v1/ping/server/list` |  |
| `async async_get_ping_server_list()` | `/game/api/v1/ping/server/list` |  |
| `get_game_entrance_ui_config()` | `/game/api/v1/bghall/game-entrance/ui-config` |  |
| `get_user_highlight_data(target_id: int)` | `/game/api/v1/user/highlight/data` |  |
| `get_game_revision_combine(filter_type_id: int=0, is_filter: int=0, page: int=0, size: int=20)` | `/game/api/v2/game/revision/all/list/by/condition/combine` |  |
| `check_app_engine_update(engine_version: int=10114, common_res_version: int=0, game_res_version: int=0, game_type: str='', engine_type: str='v1')` | `/game/api/v2/games/app-engine/check-update` |  |
| `get_mining_token_balance_with_transform()` | `/game/api/v1/backpack/mining-token/balance/with-transform` |  |

## `GratitudeAPI`

Contributor-recognition endpoints.

| Method | Endpoint | Description |
| --- | --- | --- |
| `list(category_id: int | None=None, page: int=1, size: int=20, language: str | None=None)` | `/user/api/v1/contributor-recognitions` |  |
| `like(target_uid: int)` | `/user/api/v1/contributor-recognitions/likes` |  |
| `unlike(target_uid: int)` | `/user/api/v1/contributor-recognitions/likes` |  |
| `async async_list(category_id: int | None=None, page: int=1, size: int=20, language: str | None=None)` | `/user/api/v1/contributor-recognitions` |  |
| `async async_like(target_uid: int)` | `/user/api/v1/contributor-recognitions/likes` |  |
| `async async_unlike(target_uid: int)` | `/user/api/v1/contributor-recognitions/likes` |  |

## `GroupAPI`

Chat groups and notifications.

| Method | Endpoint | Description |
| --- | --- | --- |
| `create(member_ids: list[int], cost: int=0)` | `/msg/api/v2/msg/group/chat` |  |
| `get_info(group_id: int)` | `/msg/api/v1/msg/group/chat/info` |  |
| `list_groups(page: int=1, size: int=50)` | `/msg/api/v1/msg/group/chat/list` |  |
| `rename(group_id: int, name: str)` | `/msg/api/v1/msg/group/chat/modify` |  |
| `edit(group_id: int, name: str, notice: str, invite_status: int, notice_pics: list[str] | None=None)` | `/msg/api/v1/msg/group/chat/modify` |  |
| `invite(group_id: int, member_ids: list[int])` | `/msg/api/v1/msg/group/chat/invite` |  |
| `kick(group_id: int, member_ids: list[int], group_name: str | None=None)` | `/msg/api/v1/msg/group/chat/kickOut` |  |
| `set_admin(group_id: int, member_id: int, operation_type: int)` | `/msg/api/v1/msg/group/chat/member` |  |
| `mute(group_id: int, member_id: int, minutes: int)` | `/msg/api/v1/msg/group/chat/forbidden/member` |  |
| `approve_join(group_id: int, operate_id: int, join_type: int)` | `/msg/api/v1/msg/group/chat/agreement` |  |
| `quit(group_id: int, group_name: str)` | `/msg/api/v1/msg/group/chat/quit` |  |
| `apply(group_id: int, msg: str)` | `/msg/api/v1/msg/group/chat/apply` |  |
| `transfer_ownership(group_id: int, new_owner_id: int)` | `/msg/api/v1/msg/group/chat/transfer` |  |
| `allow_invite(group_id: int, group_name: str, invite_status: int)` | `/msg/api/v1/msg/group/chat/modify` |  |
| `get_creation_price()` | `/msg/api/v1/group/chat/price` |  |
| `get_invite_count(group_id: int, language: str='en')` | `/msg/api/v1/msg/group/chat/invite/count` |  |
| `get_join_requests()` | `/msg/api/v1/msg/group/chat/request/list` |  |
| `get_vip_group_info(group_id: str)` | `/msg/api/v1/vip-group/info` |  |
| `approve_all_join_requests()` | `/msg/api/v1/msg/group/chat/agreement-all` |  |
| `reject_all_join_requests()` | `/msg/api/v1/msg/group/chat/reject-all` |  |
| `recall_message(message_id: str)` | `/msg/api/v1/msg/group/chat/recall/message` |  |
| `mute_all_members()` | `/msg/api/v1/msg/group/chat/forbidden` |  |
| `unmute_all_members()` | `/msg/api/v1/msg/group/chat/forbidden` |  |
| `remove_member_ban(member_id: int)` | `/msg/api/v1/msg/group/chat/remove/forbidden/member` |  |
| `add_member_by_email(email: str)` | `/msg/api/v1/msg/group/chat/mail/add` |  |
| `async async_create(member_ids: list[int], cost: int=0)` | `/msg/api/v2/msg/group/chat` |  |
| `async async_get_info(group_id: int)` | `/msg/api/v1/msg/group/chat/info` |  |
| `async async_list_groups(page: int=1, size: int=50)` | `/msg/api/v1/msg/group/chat/list` |  |
| `async async_rename(group_id: int, name: str)` | `/msg/api/v1/msg/group/chat/modify` |  |
| `async async_edit(group_id: int, name: str, notice: str, invite_status: int, notice_pics: list[str] | None=None)` | `/msg/api/v1/msg/group/chat/modify` |  |
| `async async_invite(group_id: int, member_ids: list[int])` | `/msg/api/v1/msg/group/chat/invite` |  |
| `async async_kick(group_id: int, member_ids: list[int], group_name: str | None=None)` | `/msg/api/v1/msg/group/chat/kickOut` |  |
| `async async_set_admin(group_id: int, member_id: int, operation_type: int)` | `/msg/api/v1/msg/group/chat/member` |  |
| `async async_mute(group_id: int, member_id: int, minutes: int)` | `/msg/api/v1/msg/group/chat/forbidden/member` |  |
| `async async_approve_join(group_id: int, operate_id: int, join_type: int)` | `/msg/api/v1/msg/group/chat/agreement` |  |
| `async async_quit(group_id: int, group_name: str)` | `/msg/api/v1/msg/group/chat/quit` |  |
| `async async_apply(group_id: int, msg: str)` | `/msg/api/v1/msg/group/chat/apply` |  |
| `async async_transfer_ownership(group_id: int, new_owner_id: int)` | `/msg/api/v1/msg/group/chat/transfer` |  |
| `async async_allow_invite(group_id: int, group_name: str, invite_status: int)` | `/msg/api/v1/msg/group/chat/modify` |  |
| `async async_get_creation_price()` | `/msg/api/v1/group/chat/price` |  |
| `async async_get_invite_count(group_id: int, language: str='en')` | `/msg/api/v1/msg/group/chat/invite/count` |  |
| `async async_get_join_requests()` | `/msg/api/v1/msg/group/chat/request/list` |  |
| `async async_get_vip_group_info(group_id: str)` | `/msg/api/v1/vip-group/info` |  |
| `async async_approve_all_join_requests()` | `/msg/api/v1/msg/group/chat/agreement-all` |  |
| `async async_reject_all_join_requests()` | `/msg/api/v1/msg/group/chat/reject-all` |  |
| `async async_recall_message(message_id: str)` | `/msg/api/v1/msg/group/chat/recall/message` |  |
| `async async_mute_all_members()` | `/msg/api/v1/msg/group/chat/forbidden` |  |
| `async async_unmute_all_members()` | `/msg/api/v1/msg/group/chat/forbidden` |  |
| `async async_remove_member_ban(member_id: int)` | `/msg/api/v1/msg/group/chat/remove/forbidden/member` |  |
| `async async_add_member_by_email(email: str)` | `/msg/api/v1/msg/group/chat/mail/add` |  |

## `MailboxAPI`

Mail and CD-key rewards.

| Method | Endpoint | Description |
| --- | --- | --- |
| `list_mail(page_no: int=1, page_size: int=20)` | `/mailbox/api/v1/mail` |  |
| `get_new_mail_count()` | `/mailbox/api/v1/mail/new` |  |
| `claim_attachment(mail_id: str)` | `/mailbox/api/v1/mail/attachment` |  |
| `mark_read(mail_ids: list[int])` | `/mailbox/api/v1/mail` |  |
| `delete_mails(mail_ids: list[int])` | `/mailbox/api/v1/mail` |  |
| `async async_list_mail(page_no: int=1, page_size: int=20)` | `/mailbox/api/v1/mail` |  |
| `async async_get_new_mail_count()` | `/mailbox/api/v1/mail/new` |  |
| `async async_claim_attachment(mail_id: str)` | `/mailbox/api/v1/mail/attachment` |  |
| `async async_mark_read(mail_ids: list[int])` | `/mailbox/api/v1/mail` |  |
| `async async_delete_mails(mail_ids: list[int])` | `/mailbox/api/v1/mail` |  |

## `NoticeAPI`

Server notice configuration.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_server_notice_config()` | `/notice/api/v1/server-notice/config` |  |
| `async async_get_server_notice_config()` | `/notice/api/v1/server-notice/config` |  |

## `PayAPI`

Payments, products, and Xsolla.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_pay_info()` | `/pay/api/v1/pay/info` |  |
| `create_payment(item_id: str, pay_type: int, amount: int)` | `/pay/api/v1/pay/create` |  |
| `get_payment_status(order_id: str)` | `/pay/api/v1/pay/status` |  |
| `verify_payment(order_id: str, receipt: str)` | `/pay/api/v1/pay/verify` |  |
| `get_order_list(page_no: int=1, page_size: int=20)` | `/pay/api/v1/pay/orders` |  |
| `get_payment_receipt(order_id: str)` | `/pay/api/v1/pay/receipt` |  |
| `request_refund(order_id: str, reason: str)` | `/pay/api/v1/pay/refund` |  |
| `get_growth_fund_info()` | `/pay/api/v1/growth/fund/info` |  |
| `get_recharge_recommendations()` | `/pay/api/v1/recharge/recommend/gcube-gear` |  |
| `get_subscription_info()` | `/pay/api/v1/sub/info/get` |  |
| `get_user_wealth()` | `/pay/api/v1/wealth/user` |  |
| `get_monthly_card_info()` | `/pay/api/v2/monthcard/info` |  |
| `receive_monthly_card_reward()` | `/pay/api/v2/monthcard/receive` |  |
| `get_vip_gift_products()` | `/pay/api/v1/vip/gift/all/product/info` |  |
| `get_gdiamond_exchange_rate()` | `/pay/api/v1/pay/gdiamond/cloth-voucher/exchange/rate` |  |
| `exchange_gdiamond()` | `/pay/api/v1/pay/gdiamond/cloth-voucher/exchange` |  |
| `async async_get_pay_info()` | `/pay/api/v1/pay/info` |  |
| `async async_create_payment(item_id: str, pay_type: int, amount: int)` | `/pay/api/v1/pay/create` |  |
| `async async_get_payment_status(order_id: str)` | `/pay/api/v1/pay/status` |  |
| `async async_verify_payment(order_id: str, receipt: str)` | `/pay/api/v1/pay/verify` |  |
| `async async_get_order_list(page_no: int=1, page_size: int=20)` | `/pay/api/v1/pay/orders` |  |
| `async async_get_payment_receipt(order_id: str)` | `/pay/api/v1/pay/receipt` |  |
| `async async_request_refund(order_id: str, reason: str)` | `/pay/api/v1/pay/refund` |  |
| `async async_get_growth_fund_info()` | `/pay/api/v1/growth/fund/info` |  |
| `async async_get_recharge_recommendations()` | `/pay/api/v1/recharge/recommend/gcube-gear` |  |
| `async async_get_subscription_info()` | `/pay/api/v1/sub/info/get` |  |
| `async async_get_user_wealth()` | `/pay/api/v1/wealth/user` |  |
| `async async_get_monthly_card_info()` | `/pay/api/v2/monthcard/info` |  |
| `async async_receive_monthly_card_reward()` | `/pay/api/v2/monthcard/receive` |  |
| `async async_get_vip_gift_products()` | `/pay/api/v1/vip/gift/all/product/info` |  |
| `async async_get_gdiamond_exchange_rate()` | `/pay/api/v1/pay/gdiamond/cloth-voucher/exchange/rate` |  |
| `async async_exchange_gdiamond()` | `/pay/api/v1/pay/gdiamond/cloth-voucher/exchange` |  |

## `RankingAPI`

Global, clan, gold/diamond, and per-game leaderboards.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_user_rank(uid: int, rank_type: str='active', rank_kind: str='overall', is_region: bool=False)` | `/ranking/api/v1/ranking/user/info` |  |
| `get_global_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/active/global/weekly/rank` |  |
| `get_game_ranking(game_id: str, period: str='all', page: int=1, size: int=10)` | `—` |  |
| `get_ranking_list(rank_type: str='active', page: int=1, size: int=10)` | `/ranking/api/v1/ranking/list` |  |
| `get_friend_ranking(page: int=1, size: int=10)` | `/ranking/api/v1/ranking/friends` |  |
| `get_clan_ranking(rank_type: str='active', page: int=1, size: int=10)` | `/ranking/api/v1/ranking/clan` |  |
| `get_global_overall(page: int=1, size: int=10)` | `/ranking/api/v1/active/global/overall/rank` |  |
| `get_region_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/active/region/weekly/rank` |  |
| `get_region_overall(page: int=1, size: int=10)` | `/ranking/api/v1/active/region/overall/rank` |  |
| `get_clan_global_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/clan/global/weekly/rank` |  |
| `get_clan_global_overall(page: int=1, size: int=10)` | `/ranking/api/v1/clan/global/overall/rank` |  |
| `get_clan_region_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/clan/region/weekly/rank` |  |
| `get_clan_region_overall(page: int=1, size: int=10)` | `/ranking/api/v1/clan/region/overall/rank` |  |
| `get_gold_diamond_global_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/gold/diamond/global/weekly/rank` |  |
| `get_gold_diamond_global_overall(page: int=1, size: int=10)` | `/ranking/api/v1/gold/diamond/global/overall/rank` |  |
| `get_gold_diamond_region_overall(page: int=1, size: int=10)` | `/ranking/api/v1/gold/diamond/region/overall/rank` |  |
| `get_gold_diamond_region_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/gold/diamond/region/weekly/rank` |  |
| `get_region_home_page_info(rank_type: str='active')` | `/ranking/api/v1/ranking/region/home/page/info` |  |
| `async async_get_user_rank(uid: int, rank_type: str='active', rank_kind: str='overall', is_region: bool=False)` | `/ranking/api/v1/ranking/user/info` |  |
| `async async_get_global_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/active/global/weekly/rank` |  |
| `async async_get_game_ranking(game_id: str, period: str='all', page: int=1, size: int=10)` | `—` |  |
| `async async_get_ranking_list(rank_type: str='active', page: int=1, size: int=10)` | `/ranking/api/v1/ranking/list` |  |
| `async async_get_friend_ranking(page: int=1, size: int=10)` | `/ranking/api/v1/ranking/friends` |  |
| `async async_get_clan_ranking(rank_type: str='active', page: int=1, size: int=10)` | `/ranking/api/v1/ranking/clan` |  |
| `async async_get_global_overall(page: int=1, size: int=10)` | `/ranking/api/v1/active/global/overall/rank` |  |
| `async async_get_region_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/active/region/weekly/rank` |  |
| `async async_get_region_overall(page: int=1, size: int=10)` | `/ranking/api/v1/active/region/overall/rank` |  |
| `async async_get_clan_global_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/clan/global/weekly/rank` |  |
| `async async_get_clan_global_overall(page: int=1, size: int=10)` | `/ranking/api/v1/clan/global/overall/rank` |  |
| `async async_get_clan_region_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/clan/region/weekly/rank` |  |
| `async async_get_clan_region_overall(page: int=1, size: int=10)` | `/ranking/api/v1/clan/region/overall/rank` |  |
| `async async_get_gold_diamond_global_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/gold/diamond/global/weekly/rank` |  |
| `async async_get_gold_diamond_global_overall(page: int=1, size: int=10)` | `/ranking/api/v1/gold/diamond/global/overall/rank` |  |
| `async async_get_gold_diamond_region_overall(page: int=1, size: int=10)` | `/ranking/api/v1/gold/diamond/region/overall/rank` |  |
| `async async_get_gold_diamond_region_weekly(page: int=1, size: int=10)` | `/ranking/api/v1/gold/diamond/region/weekly/rank` |  |
| `async async_get_region_home_page_info(rank_type: str='active')` | `/ranking/api/v1/ranking/region/home/page/info` |  |
| `get_game_leaderboard(game_id: str, period: str='all', page: int=0, size: int=10, game_version: int | None=None, language: str='en_US')` | `—` |  |
| `async async_get_game_leaderboard(game_id: str, period: str='all', page: int=0, size: int=10, game_version: int | None=None, language: str='en_US')` | `—` |  |
| `get_game_usage_leaderboard(game_id: str, period: str='all', language: str='en_US')` | `—` |  |
| `async async_get_game_usage_leaderboard(game_id: str, period: str='all', language: str='en_US')` | `—` |  |
| `get_game_my_rank(game_id: str, period: str='all', language: str='en_US')` | `—` | Return the logged-in account's rank for a game and period. |
| `async async_get_game_my_rank(game_id: str, period: str='all', language: str='en_US')` | `—` |  |
| `get_game_leaderboard_entries(game_id: str, period: str='all', page: int=0, size: int=10, game_version: int | None=None, language: str='en_US')` | `—` | Return a page of game leaderboard rows as :class:RankEntry objects. Scores are Python integers and keep full precision; `display_value` contains the server's compact display string (for example `99.99Y`). |
| `async async_get_game_leaderboard_entries(game_id: str, period: str='all', page: int=0, size: int=10, game_version: int | None=None, language: str='en_US')` | `—` |  |

## `RemoteConfigAPI`

Read-only access to `/config/files` and `/config/ml/files` resources.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_config(name: str, client_md5: str | None=None, client_version: int | None=None, ml: bool=False)` | `—` |  |
| `async async_get_config(name: str, client_md5: str | None=None, client_version: int | None=None, ml: bool=False)` | `—` |  |
| `check_version()` | `—` |  |
| `async async_check_version()` | `—` |  |
| `get_deeplink_remote_config(client_md5: str='590747fc8d5b438bd6d427e1003e0d1a', client_version: int=67)` | `—` |  |
| `async async_get_deeplink_remote_config(client_md5: str='590747fc8d5b438bd6d427e1003e0d1a', client_version: int=67)` | `—` |  |
| `get_event_blacklist_config(client_md5: str='07322629b95adbe5171ce9be607d7b49', client_version: int=16)` | `—` |  |
| `async async_get_event_blacklist_config(client_md5: str='07322629b95adbe5171ce9be607d7b49', client_version: int=16)` | `—` |  |
| `get_common_lang_img_url_config(client_md5: str='5f5aa2f16a9215d04c69775d5a34a241', client_version: int=16)` | `—` |  |
| `async async_get_common_lang_img_url_config(client_md5: str='5f5aa2f16a9215d04c69775d5a34a241', client_version: int=16)` | `—` |  |
| `get_game_resource_config()` | `—` |  |
| `async async_get_game_resource_config()` | `—` |  |
| `get_game_detail_to_editor()` | `—` |  |
| `async async_get_game_detail_to_editor()` | `—` |  |
| `get_sharing_game_resource_config(client_md5: str='ebbb5cd09b8cbdab4a60b6f89e6f5d9c', client_version: int=16)` | `—` |  |
| `async async_get_sharing_game_resource_config(client_md5: str='ebbb5cd09b8cbdab4a60b6f89e6f5d9c', client_version: int=16)` | `—` |  |
| `get_sticker_config()` | `—` |  |
| `async async_get_sticker_config()` | `—` |  |
| `get_blockmods_config(client_md5: str='90b921c94343c316de3c2f14742e3f30', client_version: int=96)` | `—` |  |
| `async async_get_blockmods_config(client_md5: str='90b921c94343c316de3c2f14742e3f30', client_version: int=96)` | `—` |  |
| `get_welcome_banner()` | `—` |  |
| `async async_get_welcome_banner()` | `—` |  |
| `get_game_rank_title_config()` | `—` |  |
| `async async_get_game_rank_title_config()` | `—` |  |
| `get_game_room_def_title_config()` | `—` |  |
| `async async_get_game_room_def_title_config()` | `—` |  |
| `get_game_room_tab_config()` | `—` |  |
| `async async_get_game_room_tab_config()` | `—` |  |
| `get_im_fraud_rule_config(client_md5: str='4c76016c61747b68a6eaf908e73584c2', client_version: int=2)` | `—` |  |
| `async async_get_im_fraud_rule_config(client_md5: str='4c76016c61747b68a6eaf908e73584c2', client_version: int=2)` | `—` |  |
| `get_new_player_guide_config()` | `—` |  |
| `async async_get_new_player_guide_config()` | `—` |  |
| `get_tribe_introduction_banner()` | `—` |  |
| `async async_get_tribe_introduction_banner()` | `—` |  |

## `RongCloudAPI`

RongCloud IM token.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_token()` | `/user/api/v1/users/device/token` |  |
| `get_raw_token()` | `/user/api/v1/users/device/token` |  |
| `async async_get_token()` | `/user/api/v1/users/device/token` |  |
| `async async_get_raw_token()` | `/user/api/v1/users/device/token` |  |

## `ShopAPI`

Shop catalogue.

| Method | Endpoint | Description |
| --- | --- | --- |
| `list_shop_items(page: int=1, size: int=20)` | `/shop/api/v1/new/shop/list` |  |
| `get_shop_info()` | `/shop/api/v1/new/shop/info` |  |
| `buy_decoration(diamond: int, gold: int, cloth_voucher: int, pay_type: int)` | `/shop/api/v1/new/shop/decorations/buy` |  |
| `list_shop_decorations(page: int=1, size: int=20)` | `/shop/api/v1/shop/decorations/list` |  |
| `get_shop_banners()` | `/shop/api/v1/shop/banners` |  |
| `get_recommended_items()` | `/shop/api/v1/shop/recommend` |  |
| `purchase(item_id: int, quantity: int=1, pay_type: int=0)` | `/shop/api/v1/shop/purchase` |  |
| `get_currency_balance()` | `/shop/api/v1/shop/currency/balance` |  |
| `get_vip_info()` | `/shop/api/v1/shop/vip/info` |  |
| `purchase_vip(vip_type: int, pay_type: int=0)` | `/shop/api/v1/shop/vip/purchase` |  |
| `get_decorations_by_classify(classify_id: int)` | `/shop/api/v1/new/shop/decorations/classify/{classify_id}` |  |
| `get_decoration_by_type(type_id: int)` | `/shop/api/v1/new/shop/decorations/{type_id}` |  |
| `get_suit_list_info()` | `/shop/api/v1/new/shop/suit/list/info` |  |
| `get_suit_info(suit_id: int)` | `/shop/api/v1/new/shop/suit/info/{suit_id}` |  |
| `get_suit_decorations()` | `/shop/api/v1/new/shop/suit/decorations` |  |
| `get_recommend_decorations()` | `/shop/api/v1/new/shop/recommend-decorations` |  |
| `get_recommend_decorations_alt()` | `/shop/api/v1/new/shop/recommend/decorations` |  |
| `get_v2_decorations_by_classify(classify_id: int)` | `/shop/api/v1/shop-v2/decorations/classify/{classify_id}` |  |
| `get_v2_decoration_details(decoration_id: int)` | `/shop/api/v1/shop-v2/decorations/details/{decoration_id}` |  |
| `get_v2_suit_decorations()` | `/shop/api/v1/shop-v2/suit/decorations` |  |
| `get_v2_suit_decorations_by_ids(suit_ids: str)` | `/shop/api/v1/shop-v2/suit/decorations/by/suitIds` |  |
| `get_game_props_shop()` | `/shop/api/v2/shop/game/props/new` |  |
| `async async_list_shop_items(page: int=1, size: int=20)` | `/shop/api/v1/new/shop/list` |  |
| `async async_get_shop_info()` | `/shop/api/v1/new/shop/info` |  |
| `async async_buy_decoration(diamond: int, gold: int, cloth_voucher: int, pay_type: int)` | `/shop/api/v1/new/shop/decorations/buy` |  |
| `async async_list_shop_decorations(page: int=1, size: int=20)` | `/shop/api/v1/shop/decorations/list` |  |
| `async async_get_shop_banners()` | `/shop/api/v1/shop/banners` |  |
| `async async_get_recommended_items()` | `/shop/api/v1/shop/recommend` |  |
| `async async_purchase(item_id: int, quantity: int=1, pay_type: int=0)` | `/shop/api/v1/shop/purchase` |  |
| `async async_get_currency_balance()` | `/shop/api/v1/shop/currency/balance` |  |
| `async async_get_vip_info()` | `/shop/api/v1/shop/vip/info` |  |
| `async async_purchase_vip(vip_type: int, pay_type: int=0)` | `/shop/api/v1/shop/vip/purchase` |  |
| `async async_get_decorations_by_classify(classify_id: int)` | `/shop/api/v1/new/shop/decorations/classify/{classify_id}` |  |
| `async async_get_decoration_by_type(type_id: int)` | `/shop/api/v1/new/shop/decorations/{type_id}` |  |
| `async async_get_suit_list_info()` | `/shop/api/v1/new/shop/suit/list/info` |  |
| `async async_get_suit_info(suit_id: int)` | `/shop/api/v1/new/shop/suit/info/{suit_id}` |  |
| `async async_get_suit_decorations()` | `/shop/api/v1/new/shop/suit/decorations` |  |
| `async async_get_recommend_decorations()` | `/shop/api/v1/new/shop/recommend-decorations` |  |
| `async async_get_recommend_decorations_alt()` | `/shop/api/v1/new/shop/recommend/decorations` |  |
| `async async_get_v2_decorations_by_classify(classify_id: int)` | `/shop/api/v1/shop-v2/decorations/classify/{classify_id}` |  |
| `async async_get_v2_decoration_details(decoration_id: int)` | `/shop/api/v1/shop-v2/decorations/details/{decoration_id}` |  |
| `async async_get_v2_suit_decorations()` | `/shop/api/v1/shop-v2/suit/decorations` |  |
| `async async_get_v2_suit_decorations_by_ids(suit_ids: str)` | `/shop/api/v1/shop-v2/suit/decorations/by/suitIds` |  |
| `async async_get_game_props_shop()` | `/shop/api/v2/shop/game/props/new` |  |

## `UserAPI`

Profile, settings, VIP, and feedback.

| Method | Endpoint | Description |
| --- | --- | --- |
| `get_profile(uid: int)` | `/friend/api/v1/friends/info/id/{uid}` |  |
| `get_own_profile()` | `/user/api/v2/user/details/info` |  |
| `get_stats(uid: int)` | `/user/api/v1/users/bg-careers` |  |
| `get_clan_role(uid: int)` | `/bedwar/api/v1/friends/clan/by/userIds` |  |
| `lookup(uid: int)` | `—` |  |
| `change_name(new_name: str, old_name: str)` | `/user/api/v3/user/nickName` |  |
| `change_details(details: str)` | `/user/api/v1/user/info` |  |
| `change_avatar(pic_url: str)` | `/user/api/v1/user/info` |  |
| `change_password(old_password: str, new_password: str)` | `/user/api/v1/user/password/modify` |  |
| `bind_email(email: str, verify_code: str)` | `/user/api/v1/users/bind/email` |  |
| `unbind_email(email: str, verify_code: str)` | `/user/api/v2/users/{self._account.uid}/emails` |  |
| `set_birthday(birthday: str)` | `/user/api/v1/user/info` |  |
| `get_online_info()` | `/user/api/v1/user/online/info` |  |
| `update_engine(engine_version: str)` | `/user/api/v1/user/engine` |  |
| `get_friend_count()` | `/user/api/v1/user/friend/num` |  |
| `get_report_info(uid: int)` | `/user/api/v1/user/report/info` |  |
| `report_user(uid: int, reason: str, content: str='')` | `/user/api/v1/user/report` |  |
| `get_simple_info()` | `/user/api/v1/simple/info` |  |
| `get_vip_info(uid: int)` | `/user/api/v1/vip/users/{uid}` |  |
| `get_player_info()` | `/user/api/v1/user/player/info` |  |
| `get_random_nickname(language: str='en')` | `/user/api/v1/user/random/nickname` |  |
| `check_nickname_exist(nickname: str)` | `/api/v1/temporary/check/nickname/exist` |  |
| `get_daily_tasks(task_type: int=1)` | `/user/api/v1/users/dairy/tasks/{task_type}` |  |
| `get_new_daily_tasks()` | `/user/api/v1/users/new/daily/tasks` |  |
| `async async_get_profile(uid: int)` | `/friend/api/v1/friends/info/id/{uid}` |  |
| `async async_get_own_profile()` | `/user/api/v2/user/details/info` |  |
| `async async_get_stats(uid: int)` | `/user/api/v1/users/bg-careers` |  |
| `async async_get_clan_role(uid: int)` | `/bedwar/api/v1/friends/clan/by/userIds` |  |
| `async async_lookup(uid: int)` | `—` |  |
| `async async_lookup_result(uid: int)` | `—` |  |
| `async async_get_decorations_result(uid: int)` | `—` |  |
| `async async_change_name(new_name: str, old_name: str)` | `/user/api/v3/user/nickName` |  |
| `async async_change_details(details: str)` | `/user/api/v1/user/info` |  |
| `async async_change_avatar(pic_url: str)` | `/user/api/v1/user/info` |  |
| `async async_change_password(old_password: str, new_password: str)` | `/user/api/v1/user/password/modify` |  |
| `async async_bind_email(email: str, verify_code: str)` | `/user/api/v1/users/bind/email` |  |
| `async async_unbind_email(email: str, verify_code: str)` | `/user/api/v2/users/{self._account.uid}/emails` |  |
| `async async_set_birthday(birthday: str)` | `/user/api/v1/user/info` |  |
| `async async_get_online_info()` | `/user/api/v1/user/online/info` |  |
| `async async_update_engine(engine_version: str)` | `/user/api/v1/user/engine` |  |
| `async async_get_friend_count()` | `/user/api/v1/user/friend/num` |  |
| `async async_get_report_info(uid: int)` | `/user/api/v1/user/report/info` |  |
| `async async_report_user(uid: int, reason: str, content: str='')` | `/user/api/v1/user/report` |  |
| `async async_get_simple_info()` | `/user/api/v1/simple/info` |  |
| `async async_get_vip_info(uid: int)` | `/user/api/v1/vip/users/{uid}` |  |
| `async async_get_player_info()` | `/user/api/v1/user/player/info` |  |
| `async async_get_random_nickname(language: str='en')` | `/user/api/v1/user/random/nickname` |  |
| `async async_check_nickname_exist(nickname: str)` | `/api/v1/temporary/check/nickname/exist` |  |
| `async async_get_daily_tasks(task_type: int=1)` | `/user/api/v1/users/dairy/tasks/{task_type}` |  |
| `async async_get_new_daily_tasks()` | `/user/api/v1/users/new/daily/tasks` |  |
| `get_avatar_frames(language: str='en')` | `/user/api/v1/user/avatar/frame` |  |
| `equip_avatar_frame(resource_id: int, language: str='en')` | `/user/api/v1/user/avatar/frame` |  |
| `check_avatar_frame_resources(res_version: int=0)` | `/user/api/v1/user/avatar/frame/resource/check` |  |
| `get_colorful_nicknames()` | `/user/api/v1/user/colorful/nickName` |  |
| `equip_colorful_nickname(resource_id: int)` | `/user/api/v1/user/colorful/nickName` |  |
| `check_space_effects(res_version: int=0)` | `/user/api/v1/user/personal/space/effect/resource/check` |  |
| `check_vip_personality(res_version: int=0)` | `/user/api/v1/user/vip/personality/resource/check` |  |
| `get_daily_sign_in_v2(language: str='en')` | `/user/api/v2/users/{self._account.uid}/daily/sign/in` |  |
| `daily_sign_in_v2(language: str='en')` | `/user/api/v2/users/{self._account.uid}/daily/sign/in` |  |
| `claim_sign_in_ad_reward()` | `/user/api/v1/users/daily/sign/ads` |  |
| `update_profile_detail(body: dict[str, Any])` | `/user/api/v1/profile/detail/{self._account.uid}` |  |
| `get_account_settings()` | `/user/api/v1/account/settings` |  |
| `get_profile_join_switch()` | `/user/api/v1/user/profile/join/switch` |  |
| `set_profile_join_switch()` | `/user/api/v1/user/profile/join/switch` |  |
| `is_nickname_free()` | `/user/api/v1/user/nickName/free` |  |
| `get_frequent_games(count: int=5)` | `/user/api/v1/data/frequently/game/{self._account.uid}` |  |
| `get_shop_info()` | `/user/api/v1/user/shop/info` |  |
| `get_decoration_details(decoration_id: int)` | `/shop/api/v1/shop/decorations/details/{decoration_id}` |  |
| `get_suit_info(suit_id: int)` | `/shop/api/v1/new/shop/suit/info/{suit_id}` |  |
| `get_month_card_info()` | `/pay/api/v2/monthcard/info` |  |
| `claim_month_card_reward(month_card_id: int)` | `/pay/api/v2/monthcard/receive` |  |
| `get_payment_red_point()` | `/pay/api/v1/red-point` |  |
| `get_task_activity_info(activity_id: str)` | `/activity/api/v1/task/activity/info` |  |
| `claim_task_activity_reward(activity_id: str, task_reward_id: str)` | `/activity/api/v1/task/activity/reward/receive` |  |
| `claim_sharing_reward(type_: int=0)` | `/user/api/v1/users/sharing/reward` |  |
| `get_security_email(language: str='en')` | `/user/api/v1/users/security/bind/email` |  |
| `async async_get_avatar_frames(language: str='en')` | `/user/api/v1/user/avatar/frame` |  |
| `async async_equip_avatar_frame(resource_id: int, language: str='en')` | `/user/api/v1/user/avatar/frame` |  |
| `async async_check_avatar_frame_resources(res_version: int=0)` | `/user/api/v1/user/avatar/frame/resource/check` |  |
| `async async_get_colorful_nicknames()` | `/user/api/v1/user/colorful/nickName` |  |
| `async async_equip_colorful_nickname(resource_id: int)` | `/user/api/v1/user/colorful/nickName` |  |
| `async async_check_space_effects(res_version: int=0)` | `/user/api/v1/user/personal/space/effect/resource/check` |  |
| `async async_check_vip_personality(res_version: int=0)` | `/user/api/v1/user/vip/personality/resource/check` |  |
| `async async_get_daily_sign_in_v2(language: str='en')` | `/user/api/v2/users/{self._account.uid}/daily/sign/in` |  |
| `async async_daily_sign_in_v2(language: str='en')` | `/user/api/v2/users/{self._account.uid}/daily/sign/in` |  |
| `async async_claim_sign_in_ad_reward()` | `/user/api/v1/users/daily/sign/ads` |  |
| `async async_update_profile_detail(body: dict[str, Any])` | `/user/api/v1/profile/detail/{self._account.uid}` |  |
| `async async_get_account_settings()` | `/user/api/v1/account/settings` |  |
| `async async_get_profile_join_switch()` | `/user/api/v1/user/profile/join/switch` |  |
| `async async_set_profile_join_switch()` | `/user/api/v1/user/profile/join/switch` |  |
| `async async_is_nickname_free()` | `/user/api/v1/user/nickName/free` |  |
| `async async_get_frequent_games(count: int=5)` | `/user/api/v1/data/frequently/game/{self._account.uid}` |  |
| `async async_get_shop_info()` | `/user/api/v1/user/shop/info` |  |
| `async async_get_decoration_details(decoration_id: int)` | `/shop/api/v1/shop/decorations/details/{decoration_id}` |  |
| `async async_get_suit_info(suit_id: int)` | `/shop/api/v1/new/shop/suit/info/{suit_id}` |  |
| `async async_get_month_card_info()` | `/pay/api/v2/monthcard/info` |  |
| `async async_claim_month_card_reward(month_card_id: int)` | `/pay/api/v2/monthcard/receive` |  |
| `async async_get_payment_red_point()` | `/pay/api/v1/red-point` |  |
| `async async_get_task_activity_info(activity_id: str)` | `/activity/api/v1/task/activity/info` |  |
| `async async_claim_task_activity_reward(activity_id: str, task_reward_id: str)` | `/activity/api/v1/task/activity/reward/receive` |  |
| `async async_claim_sharing_reward(type_: int=0)` | `/user/api/v1/users/sharing/reward` |  |
| `async async_get_security_email(language: str='en')` | `/user/api/v1/users/security/bind/email` |  |

## `VideoAPI`

Video and ad endpoints.

| Method | Endpoint | Description |
| --- | --- | --- |
| `list_videos(type_: str, page: int=1, size: int=20, tags: list[str] | None=None)` | `/video/api/v1/app/video/list/{type_}` |  |
| `get_video_details(video_id: str)` | `/video/api/v1/videos/{video_id}` |  |
| `like_video(video_id: str)` | `/video/api/v1/videos/like` |  |
| `share_video(video_id: str)` | `/video/api/v1/videos/share` |  |
| `get_video_feed(page: int=1, size: int=20, author_id: int=0, video_id: int=0, tags: list[str] | None=None)` | `/video/api/v1/app/video/more/list` |  |
| `get_user_videos(user_id: str, page: int=1, size: int=20)` | `/video/api/v1/videos/user/{user_id}` |  |
| `comment_video(video_id: str, content: str)` | `/video/api/v1/videos/comment` |  |
| `get_video_comments(video_id: str, page: int=1, size: int=20)` | `/video/api/v1/videos/comments` |  |
| `get_banner_config()` | `/video/api/v1/app/video/banner/config` |  |
| `get_video_detail_info(video_id: str)` | `/video/api/v1/app/video/detail/info` |  |
| `get_video_list_by_type(type_: str, page: int=1, size: int=20, tags: list[str] | None=None)` | `/video/api/v1/app/video/list/{type_}` |  |
| `get_more_videos(page: int=1, size: int=20, author_id: int=0, video_id: int=0, tags: list[str] | None=None)` | `/video/api/v1/app/video/more/list` |  |
| `get_video_tags()` | `/video/api/v1/app/video/tag/list` |  |
| `praise_video(video_id: str)` | `/video/api/v1/app/video/praise/{video_id}` |  |
| `dislike_video(video_id: str)` | `/video/api/v1/app/video/dislike/{video_id}` |  |
| `report_play_amount(video_id: str, duration: int)` | `/video/api/v1/app/video/report/play/amount` |  |
| `async async_list_videos(type_: str, page: int=1, size: int=20, tags: list[str] | None=None)` | `/video/api/v1/app/video/list/{type_}` |  |
| `async async_get_video_details(video_id: str)` | `/video/api/v1/videos/{video_id}` |  |
| `async async_like_video(video_id: str)` | `/video/api/v1/videos/like` |  |
| `async async_share_video(video_id: str)` | `/video/api/v1/videos/share` |  |
| `async async_get_video_feed(page: int=1, size: int=20, author_id: int=0, video_id: int=0, tags: list[str] | None=None)` | `/video/api/v1/app/video/more/list` |  |
| `async async_get_user_videos(user_id: str, page: int=1, size: int=20)` | `/video/api/v1/videos/user/{user_id}` |  |
| `async async_comment_video(video_id: str, content: str)` | `/video/api/v1/videos/comment` |  |
| `async async_get_video_comments(video_id: str, page: int=1, size: int=20)` | `/video/api/v1/videos/comments` |  |
| `async async_get_banner_config()` | `/video/api/v1/app/video/banner/config` |  |
| `async async_get_video_detail_info(video_id: str)` | `/video/api/v1/app/video/detail/info` |  |
| `async async_get_video_list_by_type(type_: str, page: int=1, size: int=20, tags: list[str] | None=None)` | `/video/api/v1/app/video/list/{type_}` |  |
| `async async_get_more_videos(page: int=1, size: int=20, author_id: int=0, video_id: int=0, tags: list[str] | None=None)` | `/video/api/v1/app/video/more/list` |  |
| `async async_get_video_tags()` | `/video/api/v1/app/video/tag/list` |  |
| `async async_praise_video(video_id: str)` | `/video/api/v1/app/video/praise/{video_id}` |  |
| `async async_dislike_video(video_id: str)` | `/video/api/v1/app/video/dislike/{video_id}` |  |
| `async async_report_play_amount(video_id: str, duration: int)` | `/video/api/v1/app/video/report/play/amount` |  |
