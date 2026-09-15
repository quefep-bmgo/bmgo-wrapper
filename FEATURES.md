# Blockman GO API Wrapper — Features

A Python wrapper for the Blockman GO (Blockman Multiplayer) API. Supports account login, clan management, friends, rankings, activities, group chat, mail, video, shop, and more.

## Installation

```bash
pip install -e .
```

## Setup

Copy `.env.example` to `.env` and fill in your device credentials:

```bash
cp .env.example .env
```

You need `BMG_DEVICE_ID` and `BMG_BMDDH_ID` from a rooted emulator. See `.env.example` for extraction instructions.

## Quick Start

```python
from blockmango import BmgAccount

acc = BmgAccount("username", "password")
acc.login()

# Get your clan
clan = acc.clan.get_own_clan()
print(clan.name, clan.level)

# Get donation history
history = acc.clan.get_donation_history_all()

# Look up a user
user = acc.user.lookup(1234567890)
print(user.nick, user.level)
```

---

## Modules

### Account (`BmgAccount`)

Core account management — login, session persistence, signed requests.

| Method | Description |
|--------|-------------|
| `login()` | Log in with username + password |
| `async_login()` | Async variant |
| `session_valid()` | Check if current session is still valid |
| `save_session()` | Persist session to disk |
| `load_session()` | Load saved session |
| `request(method, path, ...)` | Make a signed API request |

---

### Clan (`acc.clan`)

Full clan management — members, donations, rankings, decorations.

| Method | Description |
|--------|-------------|
| `get_own_clan()` | Get your clan info |
| `get_info(clan_id)` | Get clan details by ID |
| `get_members()` | List all clan members |
| `get_clan_id()` | Get your clan ID |
| `join(clan_id)` | Apply to join a clan |
| `leave(clan_id)` | Leave a clan |
| `search(name)` | Search clans by name |
| `create(name, ...)` | Create a new clan |
| `dissolve(clan_id)` | Dissolve a clan |
| `edit(clan_id, ...)` | Edit clan details |
| `invite(friend_ids)` | Invite friends to clan |
| `approve_member(other_id)` | Approve a join request |
| `reject_member(other_id)` | Reject a join request |
| `accept_invitation(id)` | Accept a clan invitation |
| `reject_invitation(id)` | Reject a clan invitation |
| `remove_members(member_ids)` | Remove members (batch) |
| `mute_member(member_id, minutes)` | Mute a member |
| `unmute_member(member_id)` | Unmute a member |
| `mute_all()` / `unmute_all()` | Mute/unmute entire clan |
| `edit_elders(type, ids)` | Manage elder roles |
| `set_verification(enabled)` | Toggle free verification |
| `buy_decoration(decoration_id)` | Buy a clan decoration |
| `get_decorations_by_type(type_id)` | List decorations by type |
| `accept_task(task_id, is_team)` | Accept a clan task |
| `claim_task(task_id, is_team)` | Claim a clan task |
| `get_personal_tasks(type)` | Get personal task list |
| `post_bulletin(content)` | Post a clan bulletin |
| `get_bulletin()` | Read the clan bulletin |
| `transfer_chief(new_chief_id)` | Transfer chief role |
| `get_donation_info()` | Get donation stats |
| `get_donation_history_page(page, size)` | Get donation history (paginated) |
| `get_donation_history_all()` | Get all donation history |
| `donate(currency, quantity)` | Donate to the clan |
| `get_clan_currency()` | Get clan currency balance |
| `get_clan_rank(type, page, size, rank_key)` | Get clan rankings |
| `get_clan_rank_new()` | Get new clan rankings |
| `get_user_clan_rank(type, rank_key)` | Get your clan contribution rank |
| `get_user_clan_rank_new(type)` | Get your new contribution rank |
| `get_recommendations()` | Get recommended clans |
| `get_member_messages()` | Get clan member messages |
| `get_red_point()` | Check clan notifications |
| `get_user_clan_role(uid)` | Get a user's clan role |
| `report_clan()` | Report a clan |

---

### User (`acc.user`)

Profile, avatar, sign-in, shop, settings, decorations.

| Method | Description |
|--------|-------------|
| `get_profile(user_id)` | Get user profile |
| `get_stats(user_id)` | Get user game stats |
| `lookup(user_id)` | Full lookup (profile + stats + clan role) |
| `search_by_name(name)` | Search users by nickname |
| `get_random_nickname()` | Get a random nickname suggestion |
| `change_name(new_name)` | Change your nickname |
| `is_nickname_free()` | Check if name change is free |
| `change_avatar(head_pic)` | Change avatar |
| `change_details(details)` | Update bio/details |
| `update_profile_detail(body)` | Update full profile (bio, region, etc.) |
| `set_birthday(birthday)` | Set birthday |
| `update_engine(version)` | Update engine version |
| `get_avatar_frames()` | List available avatar frames |
| `equip_avatar_frame(resource_id)` | Equip an avatar frame |
| `check_avatar_frame_resources(res_version)` | Check frame resource updates |
| `get_colorful_nicknames()` | List colorful nickname styles |
| `equip_colorful_nickname(resource_id)` | Equip a colorful nickname |
| `check_space_effects(res_version)` | Check personal space effects |
| `check_vip_personality(res_version)` | Check VIP personality resources |
| `get_daily_sign_in_v2()` | Get daily sign-in status |
| `daily_sign_in_v2()` | Perform daily sign-in |
| `claim_sign_in_ad_reward()` | Claim ad sign-in reward |
| `get_account_settings()` | Get account settings |
| `get_profile_join_switch()` | Get show-friends-in-game state |
| `set_profile_join_switch()` | Toggle show-friends-in-game |
| `get_frequent_games(count)` | Get frequently played games |
| `get_security_email()` | Get security email |
| `get_shop_info()` | Get shop/inventory info |
| `get_decoration_details(decoration_id)` | Get decoration details |
| `get_suit_info(suit_id)` | Get dress suit info |
| `get_month_card_info()` | Get month card (subscription) info |
| `claim_month_card_reward(month_card_id)` | Claim month card daily reward |
| `get_payment_red_point()` | Check payment notifications |
| `get_task_activity_info(activity_id)` | Get task activity info |
| `claim_task_activity_reward(activity_id, reward_id)` | Claim activity reward |
| `claim_sharing_reward(type)` | Claim sharing reward |
| `get_new_daily_tasks()` | Get daily tasks |
| `get_daily_tasks(type)` | Get daily tasks by type |
| `delete_email()` | Delete account email |

---

### Friends (`acc.friends`)

Friend list, requests, tags, popularity, family system.

| Method | Description |
|--------|-------------|
| `get_friend_info(friend_id)` | Get friend details |
| `add_friend(friend_id)` | Send friend request |
| `remove_friend(friend_id)` | Remove a friend |
| `accept_request(friend_id)` | Accept friend request |
| `reject_request(friend_id)` | Reject friend request |
| `accept_all_requests()` | Accept all pending requests |
| `reject_all_requests()` | Reject all pending requests |
| `set_alias(friend_id, alias)` | Set friend nickname |
| `remove_alias(friend_id)` | Remove friend nickname |
| `block_user(user_id)` | Block a user |
| `unblock_user(user_id)` | Unblock a user |
| `search_by_name(name)` | Search friends by name |
| `get_requests()` | List pending friend requests |
| `get_request_count()` | Get pending request count |
| `get_recommendations()` | Get friend recommendations |
| `get_new_recommendations()` | Get new friend recommendations |
| `get_following()` | Get following list |
| `get_notices(type)` | Get friend notices |
| `get_settings(user_id)` | Get friend settings |
| `update_settings(body)` | Update friend settings |
| `get_gaming_status(friend_id)` | Check if friend is in-game |
| `get_popularity(target_id)` | Get popularity score |
| `add_popularity(target_id)` | Add popularity |
| `get_popularity_props()` | Get popularity props |
| `get_tags()` | Get friend tags |
| `get_tag_details(tag_id)` | Get tag details |
| `create_tag(name, ...)` | Create a friend tag |
| `delete_tag(tag_id)` | Delete a friend tag |
| `rename_tag(tag_id, name)` | Rename a friend tag |
| `apply_popularity(type, target_id)` | Apply popularity prop |

---

### Ranking (`acc.ranking`)

Global, regional, clan, and gold/diamond leaderboards.

| Method | Description |
|--------|-------------|
| `get_user_info()` | Get your ranking info |
| `get_global_weekly(page, size)` | Global weekly ranking |
| `get_global_overall(page, size)` | Global overall ranking |
| `get_region_weekly(page, size)` | Regional weekly ranking |
| `get_region_overall(page, size)` | Regional overall ranking |
| `get_clan_global_weekly(page, size)` | Clan global weekly |
| `get_clan_global_overall(page, size)` | Clan global overall |
| `get_clan_region_weekly(page, size)` | Clan regional weekly |
| `get_clan_region_overall(page, size)` | Clan regional overall |
| `get_gold_diamond_global_weekly(page, size)` | Gold/diamond global weekly |
| `get_gold_diamond_global_overall(page, size)` | Gold/diamond global overall |
| `get_gold_diamond_region_weekly(page, size)` | Gold/diamond regional weekly |
| `get_gold_diamond_region_overall(page, size)` | Gold/diamond regional overall |
| `get_home_page_info()` | Get ranking home page |

---

### Activity (`acc.activity`)

Sign-in, campaigns, WorldCup betting, treasure, 7-day rewards.

| Method | Description |
|--------|-------------|
| `sign_in()` | Sign in (POST) |
| `get_sign_in_status()` | Get sign-in status |
| `get_tasks()` | Get activity tasks |
| `claim_task_reward(task_id)` | Claim task reward |
| `get_campaign_list()` | Get WorldCup campaign list |
| `place_campaign_bet(body)` | Place a campaign bet |
| `get_campaign_history()` | Get bet history |
| `get_campaign_notice()` | Get campaign notifications |
| `get_campaign_integral()` | Get campaign integral |
| `get_my_integral_rank()` | Get your integral rank |
| `get_integral_leaderboard()` | Get integral leaderboard |
| `get_integral_rewards()` | List integral rewards |
| `claim_integral_reward()` | Claim integral reward |
| `get_rank_reward_info()` | Get rank reward info |
| `get_activity_actions()` | Get activity actions |
| `receive_action_reward()` | Receive action reward |
| `get_activity_titles()` | Get activity categories |
| `get_treasure_info()` | Get GCube/treasure info |
| `buy_treasure()` | Buy GCube/treasure |
| `get_seven_day_sign_data()` | Get 7-day sign-in data |
| `claim_seven_day_sign_reward()` | Claim 7-day sign reward |

---

### Group Chat (`acc.group`)

Group creation, messaging, member management, moderation.

| Method | Description |
|--------|-------------|
| `create(name, ...)` | Create a group chat |
| `get_info(group_id)` | Get group info |
| `list_groups()` | List your groups |
| `modify(group_id, ...)` | Modify group settings |
| `invite(group_id, user_ids)` | Invite users to group |
| `kick(group_id, member_id)` | Kick a member |
| `approve(group_id, member_id)` | Approve join request |
| `approve_all_join_requests()` | Approve all join requests |
| `reject_all_join_requests()` | Reject all join requests |
| `get_join_requests()` | List pending join requests |
| `quit(group_id)` | Leave a group |
| `transfer(group_id, user_id)` | Transfer group ownership |
| `mute_member(group_id, member_id)` | Mute a member |
| `remove_member_ban(member_id)` | Remove member ban |
| `mute_all_members()` | Mute all members |
| `unmute_all_members()` | Unmute all members |
| `recall_message(message_id)` | Recall a message |
| `add_member_by_email(email)` | Add member by email |
| `get_creation_price()` | Get group creation price |
| `get_invite_count()` | Get invite count |
| `get_vip_group_info()` | Get VIP group info |

---

### Mailbox (`acc.mailbox`)

Mail management — read, claim attachments, delete.

| Method | Description |
|--------|-------------|
| `list_mails()` | List all mails |
| `get_new_mails()` | Get new/unread mails |
| `claim_attachment(mail_id)` | Claim mail attachment |
| `mark_read(mail_ids)` | Mark mails as read |
| `delete_mails(mail_ids)` | Delete mails |

---

### Video (`acc.video`)

Video feed, details, tags, reactions.

| Method | Description |
|--------|-------------|
| `get_video_list(type)` | Get video list by type |
| `get_more_videos(page, size)` | Get more videos |
| `get_banner()` | Get video banner config |
| `get_video_detail(video_id)` | Get video details |
| `get_tags()` | Get video tags |
| `praise_video(video_id)` | Like a video |
| `dislike_video(video_id)` | Dislike a video |
| `report_play_amount(video_id)` | Report play count |

---

### Other Modules

| Module | Methods | Description |
|--------|---------|-------------|
| `acc.game` | `get_game_list`, `get_game_info`, `get_engine_config`, ... | Game catalog and engine management |
| `acc.decoration` | `get_decorations`, `get_suits`, `buy_decoration`, ... | Decoration/suit shop |
| `acc.shop` | `get_shop_info`, `buy_item`, ... | In-game shop |
| `acc.backpack` | `get_items`, `use_item`, ... | Inventory/backpack |
| `acc.bedwar` | `get_stats`, `get_rankings`, ... | BedWar game mode |
| `acc.gratitude` | `get_gratitude_list`, ... | Gratitude system |
| `acc.mailbox` | `list_mails`, `claim_attachment`, ... | Mail management |
| `acc.pay` | `get_month_card_info`, `claim_reward`, ... | Payments and subscriptions |
| `acc.rongcloud` | `get_token`, ... | RongCloud messaging token |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BMG_DEVICE_ID` | Yes | Your android_id (16 hex chars) |
| `BMG_BMDDH_ID` | Yes | bmg-sign value from MMKV |
| `BMG_DEVICE_SIGN` | No | Device signature (defaults to BMG_BMDDH_ID) |
| `BMG_API_BASE` | No | API base URL |
| `BMG_TIME_API` | No | Time sync endpoint |
| `BMG_DEVICE_POOL_URL` | No | Device pool URL |
| `BMG_USER_AGENT` | No | HTTP User-Agent string |
| `BMG_VERIFY_SSL` | No | Enable SSL verification (default: false) |

---

## API Coverage

~160 endpoints across 16 modules covering:

- **Clan**: 49 methods — full management, rankings, donations, decorations
- **User**: 51 methods — profile, avatar, sign-in, shop, settings, month card
- **Friends**: 34 methods — friend list, tags, popularity, family system
- **Activity**: 22 methods — campaigns, WorldCup, integral, treasure, 7-day sign
- **Group**: 26 methods — chat, moderation, member management
- **Ranking**: 19 methods — global, regional, clan, gold/diamond leaderboards
- **Video**: 17 methods — feed, details, reactions
- **Mailbox**: 6 methods — read, claim, delete

## Notes

- The `bmg-sign` header must be the `bm_ddh_id` from MMKV, NOT the device signature
- Sessions are cached in `.sessions.json` (gitignored)
- All modules have async variants (prefix with `async_`)
- The `language` parameter defaults to `"en_US"` on endpoints that require it
