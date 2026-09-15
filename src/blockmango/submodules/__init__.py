from __future__ import annotations
from .activity import ActivityAPI
from .backpack import BackpackAPI
from .bedwar import BedwarAPI
from .clan import ClanAPI
from .decoration import DecorationAPI
from .friends import FriendsAPI
from .game import GameAPI
from .gratitude import GratitudeAPI
from .group import GroupAPI
from .mailbox import MailboxAPI
from .pay import PayAPI
from .ranking import RankingAPI
from .rongcloud import RongCloudAPI
from .shop import ShopAPI
from .user import UserAPI
from .video import VideoAPI

__all__ = [
    "ActivityAPI", "BackpackAPI", "BedwarAPI", "ClanAPI", "DecorationAPI",
    "FriendsAPI", "GameAPI", "GratitudeAPI", "GroupAPI", "MailboxAPI",
    "PayAPI", "RankingAPI", "RongCloudAPI", "ShopAPI", "UserAPI", "VideoAPI",
]