from __future__ import annotations

from types import MappingProxyType

API_BASE = "https://gw.sandboxol.com"
TIME_API = "https://gw.sandboxol.com/server-time"
DEVICE_POOL_URL = "https://pastebin.com/raw/m4EZm0z5"

APP_VERSION = "5753"
APP_VERSION_NAME = "3.29.3"
ANDROID_VERSION = "32"
APP_MD5 = "5d0de77b0f4b93b44669f146e54b49d9"

KEY_PAIRS: tuple[tuple[str, str], ...] = (
    ("6aDtpIdzQdgGwrpP6HzuPA", "9EuDKGtoWAOWoQH1cRng-d5ihNN60hkGLaRiaZTk-6s"),
    ("h0jCHbhVd9Fpkx-FGkxeRw", "lOTB7DNdMMpdyUO-psJ5b2ivYGmU5RAy6j6bkpoMYcs"),
    ("dM9XM3sxjfVI6AC77GS9rw", "6aNQVhd8pP-Gg7_xM2PTEp92G-77tzHGnPKrwslxmAg"),
)

RSA_KEY = b"""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCLzlsA+3wXCAph80r/xs1bWhVrsJSOQmSBTA0GaBpVIzXqFBaibDmYA3WJDM9rcQ7KpYSyrJ02iFlsN43RnizrHfS+xPtdwuxBQ2Clow5cYPZucqQYL9HIlbBLoighH2eGQqGlVadL7r384iKTz9mmckSUa8hhJzS+WwUAqVO3DwIDAQAB
-----END PUBLIC KEY-----"""

DEFAULT_APP_HEADERS = MappingProxyType({
    "packagename": "blockymods",
    "packagenamefull": "com.sandboxol.blockymods",
    "package-name": "com.sandboxol.blockymods",
    "package_name_en": "com.sandboxol.blockymods",
    "androidversion": ANDROID_VERSION,
    "os": "android",
    "apptype": "android",
    "applanguage": "en",
    "appversion": APP_VERSION,
    "appversionname": APP_VERSION_NAME,
    "channel": "sandbox",
    "uid_register_ts": "0",
    "device_register_ts": "0",
    "eventtype": "app",
    "userlanguage": "en_US",
    "region": "sandbox",
    "clienttype": "client",
    "env": "prd",
    "content-type": "application/json; charset=UTF-8",
    "accept-encoding": "gzip",
    "user-agent": "okhttp/4.12.0",
})

DEFAULT_DEVICE_HEADERS = MappingProxyType({})

RAW_SIGN_PATH_PREFIXES: tuple[str, ...] = (
    "/config/files/",
    "/config/ml/files/",
)

DEVICE_HEADER_PATHS = frozenset({
    "/user/api/v4/account/login",
    "/user/api/v4/account/register",
    "/user/api/v3/register",
    "/user/api/v5/account/auth-token",
    "/user/api/v1/temporary/login",
    "/user/api/v2/login",
    "/user/api/v3/login",
    "/user/api/v2/app/login",
    "/user/api/v3/account/tourist/login",
})

RAW_SIGN_PATHS = frozenset("""
/user/api/v1/account/email/tp-auth/login/code/send
/user/api/v1/account/tp/list-public
/user/api/v1/account/email/reset-pwd/code/send
/user/api/v1/account/email/reset-pwd/code/verify
/user/api/v1/account/email/reset-password
/user/api/v1/account/email/register/code/send
/user/api/v1/account/email/register/code/verify
/user/api/v1/account/email/register
/user/api/v1/account/email/login/code/send
/user/api/v1/account/email/login/code/verify
/user/api/v1/account/email/login
/user/api/v1/account/invalid/check
/game/api/v1/appeal/game/list/get
/user/api/v1/appeal/info/handle
/user/api/v1/appeal/other/info/save
/user/api/v1/appeal/password/reset
/user/api/v1/user/random/nickname
/user/api/v3/users/verify/user/security/settings
/user/api/v1/vc/cimage
/user/api/v1/user/details/info/get
/pay/api/v1/coda/shop/top/up/verify
/pay/api/v1/xiao/mi/pay/notify
/editorproxy/community-api/v1/pub/community_news/detail
/editorproxy/meditor-api/v1/pub/lang_config_info
/activity/api/v1/garena/user/wealth
/user/api/v1/temporary/login
/editorproxy/community-api/v1/pub/community_news/list
/clan/api/v3/clan/tribe/recommendation
/user/api/v1/app/renew
/user/api/v1/user/data/delete
/editorproxy/meditor-api/v1/editor/version
/user/api/v1/temporary/uniworlds/login
/user/api/v1/login/encrypt
/pay/api/v1/xsolla/pay/billing/update
/user/api/v1/user/nickname/exist
/user/api/v1/users/third-part/info
/editorproxy/gamedata-api/v2/pub/game_manage/new_game_types
/user/api/v3/register
/user/api/v4/account/login
/editorproxy/meditor-api/v1/pub/meditor_templates
/user/api/v1/new/appeal/status
/user/api/v1/bmx/users/security/bind/email
/activity/api/v1/garena/user/game/data
/editorproxy/community-api/v1/pub/community_course/details
/editorproxy/gamedata-api/v1/pub/game_manage/game_types
/pay/api/v1/xsolla/enable
/editorproxy/gamedata-api/v1/game_show/find_game
/editorproxy/meditor-api/v1/pub/temporary_service/info
/user/api/v1/vc/validate
/user/api/v1/ip/region/get
/editorproxy/meditor-api/v1/pub/game/app_engine/check_update
/pay/api/v1/subscribe/notify/ios
/decoration/api/v1/decoration/versions
/user/api/v1/emails/reset-pwd
/user/api/v1/check/region/status
/user/api/v1/users/question/reset/password
/user/api/v1/xiao/mi/login
/pay/api/v1/subscribe/notify/google
/api/v1/users/third-part/info
/editorproxy/community-api/v1/pub/community_news/cumulative_view
/activity/api/v1/garena/user/info
/user/api/v1/pre-registration
/user/api/v1/users/security/verify/email/reset
/editorproxy/meditor-api/v1/pub/config/account_retrieve
/editorproxy/community-api/v1/pub/community_course/cumulative_view
/pay/api/v1/xsolla/billing/update
/user/api/v1/users/third-part/info/
/clan/api/v1/clan/tribe/recommendation
/activity/api/v1/recharge/count/info
/user/api/v5/account/auth-token
/user/api/v1/temporary/uniworlds/register
/user/api/v1/new/appeal/info/handle
/editorproxy/community-api/v1/pub/material/query_recommended_materials
/user/api/v1/token/info/get
/user/api/v1/emails/reset-pwd/auth
/user/api/v1/emails/password/reset
/datareport/api/v1/inner/statistics/userGameActionData
/datareport/api/v1/app/google/pay/process/get
/user/api/v2/app/renew
/decoration/api/v1/decorations/user-decoration
/user/api/v2/temporary/login
/user/api/v1/visitor
/user/api/v1/users/secret/question
/mailbox/api/v1/garena/mail/send
/notice/api/v1/server-notice/config
/auth/api/v1/users/third-part/info/
/pay/public/pay/api/v1/public/pay/testCountry
/editorproxy/community-api/v1/pub/community_news_sort/list
/user/api/v1/hua/wei/login
/editorproxy/community-api/v1/pub/community_course/list
/editorproxy/meditor-api/v1/pub/meditor_template
/user/api/v1/temporary/lock/region
/user/api/v2/login
/user/api/v1/user/login/change/record
/pay/api/v1/xsolla/validateuser
/user/api/v1/user/mac/id
/msg/api/v1/msg/receive_message
/pay/api/v1/xsolla/verifyuser
/user/api/v3/login
/user/api/v1/temporary/check/nickname/exist
/pay/api/v1/hua/wei/pay/notify
/pay/api/v1/public/pay/notify
/pay/api/v1/subscribe/google/msg/receive
/editorproxy/community-api/v1/pub/material/list
/editorproxy/community-api/v1/pub/material/production_guide_url
/pay/api/v1/codapay/notify
/pay/api/v1/razer/notify
/user/api/v1/lock/region
/pay/api/v1/public/pay/centili/notify
/pay/api/v1/coda/shop/validate/verify
/user/api/v1/check/account/source
/user/api/v3/account/tourist/login
/editorproxy/community-api/v1/pub/community_course_sort/list
/user/api/v1/temporary/register
/editorproxy/version-api/v1/check_launcher_update
/pay/api/v1/xsolla/billing/get
/datareport/api/v1/inner/statistics/userActionData
/msg/api/v1/msg/app/status
/statistic/api/v1/statistic/user/new/add/country
/pay/api/v1/xsolla/verifyUser
/user/api/v2/users/verify/user/security/settings
/pay/api/v1/xsolla/pay
/pay/api/v1/subscribe/ios/msg/receive
/editorproxy/meditor-api/v1/pub/lang_map/list
/user/api/v4/account/register
/editorproxy/community-api/v1/pub/community_course/list/with_page
/game/api/v1/games/so-resource/upgrade
/user/api/v1/users/security/bind/email
/activity/api/v1/garena/web/config
/user/api/v1/alerts/phones
/user/api/v1/region/recommend/list
/activity/api/v1/garena/user/item
/user/api/v1/sms/send/refound
/activity/api/v1/tradplus/reward-video/verify
/user/api/v2/app/login
/api/v1/users/third-part/info
/user/api/v1/user/password
/pay/api/v1/subscribe/garena/notify
/user/api/v1/device/bind/info/get
/user/api/v1/check/region/open/status
/config/files/game/pkg/check-version
/config/files/game/pkg/ad
/user/api/v1/account/tp/login
/user/api/v1/account/pkg/grant-login
""".split())

DEFAULT_SESSION_CACHE = ".sessions.json"
DEFAULT_USER_AGENT = "okhttp/4.12.0"
