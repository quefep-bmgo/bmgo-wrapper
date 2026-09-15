from __future__ import annotations

from .account import BmgAccount
from .client import BmgClient
from .config import Config
from .constants import (
    API_BASE,
    DEFAULT_APP_HEADERS,
    DEVICE_POOL_URL,
    KEY_PAIRS,
    RSA_KEY,
    TIME_API,
)
from .device import DevicePool, fetch_devices
from .exceptions import (
    AuthError, BlockmangoError, CryptoError, NetworkError,
    NotFoundError, RateLimitError, SessionError, SignError, ValidationError,
)
from .models import (
    ClanInfo, ClanMember, ClanRole, DecorationItem, GroupInfo, GroupMember,
    RankEntry, RongCloudToken, SignInStatus, TaskInfo, UserProfile, UserStats,
    Wardrobe,
)
from .session import SessionStore, load_session, save_session
from .submodules import (
    ActivityAPI, BackpackAPI, BedwarAPI, ClanAPI, DecorationAPI, FriendsAPI,
    GameAPI, GratitudeAPI, GroupAPI, MailboxAPI, PayAPI, RankingAPI,
    RongCloudAPI, ShopAPI, UserAPI, VideoAPI,
)
from .time_sync import TimeSyncer, sync_time

__version__ = "8202026.2"

__all__ = [
    "BmgAccount", "BmgClient", "Config",
    "API_BASE", "DEFAULT_APP_HEADERS", "DEVICE_POOL_URL", "KEY_PAIRS", "RSA_KEY", "TIME_API",
    "DevicePool", "fetch_devices",
    "AuthError", "BlockmangoError", "CryptoError", "NetworkError",
    "NotFoundError", "RateLimitError", "SessionError", "SignError", "ValidationError",
    "ClanInfo", "ClanMember", "ClanRole", "DecorationItem", "GroupInfo", "GroupMember",
    "RankEntry", "RongCloudToken", "SignInStatus", "TaskInfo", "UserProfile", "UserStats",
    "Wardrobe",
    "SessionStore", "load_session", "save_session",
    "ActivityAPI", "BackpackAPI", "BedwarAPI", "ClanAPI", "DecorationAPI",
    "FriendsAPI", "GameAPI", "GratitudeAPI", "GroupAPI", "MailboxAPI",
    "PayAPI", "RankingAPI", "RongCloudAPI", "ShopAPI", "UserAPI", "VideoAPI",
    "TimeSyncer", "sync_time",
    "__version__",
]