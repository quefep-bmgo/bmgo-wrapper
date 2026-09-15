# bmgo-wrapper

Blockman GO API wrapper with x-sign authentication.
Compatible with Blockman GO v3.28.2 (versionCode 5742).

## Setup

### 1. Install

```bash
pip install -e .
```

Requires Python 3.10+, `requests`, `httpx`, `pycryptodome`.

### 2. Get your device credentials

You need two values from a rooted Blockman GO emulator:

**`BMG_DEVICE_ID`** — your `android_id` (16 hex chars):
```bash
adb shell settings get secure android_id
```

**`BMG_BMDDH_ID`** — the `bm_ddh_id` value from MMKV storage:
```bash
adb shell "strings /data/data/com.sandboxol.blockymods/files/mmkv/bmg_cache | grep bm_ddh_id"
```
The value after `bm_ddh_id-,` is your `BMG_BMDDH_ID` (base64 string, ~44 chars).

### 3. Create `.env`

```bash
cp .env.example .env
```

Edit `.env`:
```
BMG_DEVICE_ID=your_16_hex_android_id
BMG_BMDDH_ID=your_base64_bmddh_id
```

### 4. Use

```python
from blockmango import BmgAccount

acc = BmgAccount("username", "password")
acc.login()

print(acc.uid, acc.nick)
clan = acc.clan.get_own_clan()
print(clan.name, clan.level)
```

Sessions are cached in `.sessions.json` (gitignored). On subsequent runs, `acc.login()` restores the cached session if valid.

## Modules

### Account (`BmgAccount`)

```python
acc = BmgAccount("user", "pass")
acc.login()                      # login with x-sign auth
acc.session_valid()              # check if token is still valid
acc.uid                          # user ID
acc.nick                         # nickname
acc.token                        # JWT access token
```

### Clan (`acc.clan`)

```python
acc.clan.get_own_clan()          # your clan info
acc.clan.get_info(clan_id)       # clan details
acc.clan.get_members()           # list members
acc.clan.get_clan_id()           # your clan ID
acc.clan.get_clan_currency()     # clan currency balance
acc.clan.get_bulletin()          # read bulletin
acc.clan.get_donation_info()     # donation stats
acc.clan.get_donation_history_page(page=0, size=50)  # donation history
acc.clan.get_donation_history_all()                   # all donation history
acc.clan.get_clan_rank_new()     # clan rankings
acc.clan.get_user_clan_rank()    # your clan contribution rank
acc.clan.get_recommendations()   # recommended clans
acc.clan.get_red_point()         # notifications
acc.clan.get_member_messages()   # member messages
acc.clan.get_personal_tasks()    # personal tasks
acc.clan.get_decorations_by_type(type_id)  # decorations
acc.clan.donate(currency=0, quantity=0)    # donate to clan
acc.clan.search(name)            # search clans
acc.clan.join(clan_id)           # apply to join
acc.clan.leave(clan_id)          # leave
acc.clan.invite(friend_ids)      # invite friends
acc.clan.approve_member(uid)     # approve join request
acc.clan.reject_member(uid)      # reject join request
acc.clan.remove_members(uids)    # remove members
acc.clan.mute_member(uid, mins)  # mute member
acc.clan.post_bulletin(text)     # post bulletin
acc.clan.edit(clan_id, ...)      # edit clan details
acc.clan.transfer_chief(uid)     # transfer chief role
```

### User (`acc.user`)

```python
acc.user.get_stats(uid)          # game stats
acc.user.get_avatar_frames()     # available avatar frames
acc.user.equip_avatar_frame(resource_id)  # equip frame
acc.user.get_colorful_nicknames()         # colorful name styles
acc.user.equip_colorful_nickname(resource_id)
acc.user.check_space_effects()   # personal space effects
acc.user.check_vip_personality() # VIP personality items
acc.user.get_daily_sign_in_v2()  # sign-in status
acc.user.daily_sign_in_v2()      # do daily sign-in
acc.user.get_account_settings()  # account settings
acc.user.get_profile_join_switch()  # show-friends toggle
acc.user.get_shop_info()         # shop/inventory
acc.user.get_month_card_info()   # subscription info
acc.user.get_payment_red_point() # payment notifications
acc.user.get_frequent_games()    # frequently played games
acc.user.is_nickname_free()      # check free name change
acc.user.change_name(name)       # change nickname
acc.user.change_avatar(pic)      # change avatar
acc.user.change_details(text)    # update bio
```

### Friends (`acc.friends`)

```python
acc.friends.list_friends()       # friend list
acc.friends.search(name)         # search users
acc.friends.get_requests()       # pending requests
acc.friends.get_apply_count()    # request count
acc.friends.send_request(uid)    # send friend request
acc.friends.accept_request(uid)  # accept
acc.friends.reject_request(uid)  # reject
acc.friends.delete_friend(uid)   # remove friend
acc.friends.set_alias(uid, name) # set nickname
acc.friends.get_tags()           # friend tags
acc.friends.get_popularity(uid)  # popularity score
acc.friends.get_gaming_status(uid)  # is in-game
acc.friends.get_settings(uid)    # friend settings
acc.friends.get_recommendations()  # suggested friends
acc.friends.get_follow_list()    # following list
acc.friends.get_notice_list()    # friend notices
```

### Ranking (`acc.ranking`)

```python
acc.ranking.get_global_weekly()          # global weekly ranking
acc.ranking.get_global_overall()         # global overall
acc.ranking.get_region_weekly()          # regional weekly
acc.ranking.get_region_overall()         # regional overall
acc.ranking.get_clan_global_weekly()     # clan global weekly
acc.ranking.get_clan_global_overall()    # clan global overall
acc.ranking.get_gold_diamond_global_weekly()   # gold/diamond weekly
acc.ranking.get_gold_diamond_global_overall()  # gold/diamond overall
acc.ranking.get_gold_diamond_region_weekly()   # gold/diamond regional weekly
acc.ranking.get_gold_diamond_region_overall()  # gold/diamond regional overall
acc.ranking.get_region_home_page_info()  # ranking home page
```

### Game (`acc.game`)

```python
acc.game.get_game_categories()   # game categories
acc.game.get_hot_games()         # trending games
acc.game.get_recommended_games() # recommended games
acc.game.list_games()            # browse games
acc.game.get_game_details(game_id)  # game details
acc.game.get_recently_played()   # recently played
acc.game.search_games(query)     # search games
acc.game.create_room(...)        # create game room
acc.game.enter_room(room_id)     # join room
acc.game.list_rooms(...)         # list rooms
```

### Activity (`acc.activity`)

```python
acc.activity.get_sign_in_status()  # sign-in status
acc.activity.sign_in()             # do sign-in
acc.activity.get_tasks()           # activity tasks
acc.activity.claim_task_reward(task_id)  # claim reward
acc.activity.get_activity_titles() # activity categories
```

### Mailbox (`acc.mailbox`)

```python
acc.mailbox.list_mail()            # list all mail
acc.mailbox.get_new_mail_count()   # unread count
acc.mailbox.claim_attachment(mail_id)  # claim attachment
acc.mailbox.mark_read(mail_ids)    # mark as read
acc.mailbox.delete_mails(mail_ids) # delete mails
```

### Video (`acc.video`)

```python
acc.video.get_banner_config()      # video banner
acc.video.get_video_tags()         # available tags (game IDs)
acc.video.get_more_videos(...)     # browse videos
acc.video.get_video_detail_info(video_id)  # video details
acc.video.praise_video(video_id)   # like
acc.video.dislike_video(video_id)  # dislike
```

### Group Chat (`acc.group`)

```python
acc.group.list_groups()            # your groups
acc.group.get_creation_price()     # group creation cost
acc.group.get_join_requests()      # pending join requests
acc.group.create(name, ...)        # create group
acc.group.modify(group_id, ...)    # edit group
acc.group.invite(group_id, uids)   # invite members
acc.group.kick(group_id, uid)      # kick member
acc.group.quit(group_id)           # leave group
```

### Other Modules

```python
acc.decoration    # decorations shop
acc.shop          # in-game shop
acc.pay           # payments, month card
acc.rongcloud     # IM messaging token
acc.backpack      # inventory
acc.bedwar        # BedWar mode
acc.gratitude     # contributor recognitions
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BMG_DEVICE_ID` | Yes | `android_id` from emulator (16 hex chars) |
| `BMG_BMDDH_ID` | Yes | `bm_ddh_id` from MMKV (base64, ~44 chars) |
| `BMG_DEVICE_SIGN` | No | Device signature (defaults to BMG_BMDDH_ID) |
| `BMG_API_BASE` | No | API base URL |
| `BMG_USER_AGENT` | No | HTTP User-Agent |
| `BMG_VERIFY_SSL` | No | Enable SSL verification (default: false) |

## Notes

- The `bmg-sign` header must be the `bm_ddh_id` from MMKV, not the device signature from the device pool
- Sessions are cached in `.sessions.json` — delete it to force a fresh login
- All modules have async variants (prefix method with `async_`)
- The `language` parameter defaults to `"en_US"` on endpoints that require it
- Blocklist management (`get_blocklist`, `block_user`) is not supported — the server returns 400/405 on these endpoints
- Campaign/integral endpoints require an active event to return data

## License

MIT
