from __future__ import annotations
from .activity import ActivityAPI
from .backpack import BackpackAPI
from .bedwar import BedwarAPI
from .clan import ClanAPI
from .decoration import DecorationAPI
from .extended import ExtendedAPI
from .friends import FriendsAPI
from .game import GameAPI
from .gratitude import GratitudeAPI
from .group import GroupAPI
from .mailbox import MailboxAPI
from .notice import NoticeAPI
from .pay import PayAPI
from .ranking import RankingAPI
from .remote_config import RemoteConfigAPI
from .rongcloud import RongCloudAPI
from .shop import ShopAPI
from .user import UserAPI
from .video import VideoAPI

__all__ = [
    "ActivityAPI", "BackpackAPI", "BedwarAPI", "ClanAPI", "DecorationAPI",
    "ExtendedAPI", "FriendsAPI", "GameAPI", "GratitudeAPI", "GroupAPI", "MailboxAPI", "NoticeAPI",
    "PayAPI", "RankingAPI", "RemoteConfigAPI", "RongCloudAPI", "ShopAPI", "UserAPI", "VideoAPI",
]