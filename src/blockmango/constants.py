from __future__ import annotations

from types import MappingProxyType

API_BASE = "https://gw.sandboxol.com"
TIME_API = "http://di.sandboxol.com/api/server-time"
DEVICE_POOL_URL = "https://pastebin.com/raw/m4EZm0z5"

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
    "androidversion": "30",
    "os": "android",
    "apptype": "android",
    "applanguage": "en",
    "appversion": "5711",
    "appversionname": "3.25.1",
    "channel": "sandbox",
    "env": "prd",
    "region": "sandbox",
    "userlanguage": "en_US",
    "clienttype": "client",
    "content-type": "application/json; charset=UTF-8",
    "accept-encoding": "gzip",
    "user-agent": "okhttp/4.12.0",
})

DEFAULT_SESSION_CACHE = ".sessions.json"
DEFAULT_USER_AGENT = "okhttp/4.12.0"