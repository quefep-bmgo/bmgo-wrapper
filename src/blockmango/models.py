from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class UserProfile:
    user_id: int
    nick_name: str
    pic_url: str | None = None
    level: int = 0
    vip_level: int = 0
    gender: int = 0
    birthday: str | None = None
    details: str | None = None
    clan_id: int | None = None
    clan_name: str | None = None
    clan_role: int | None = None
    friend_num: int | None = None
    family_num: int | None = None
    decoration_count: int | None = None
    suit_count: int | None = None
    atlas_count: int | None = None
    atlas_total: int | None = None
    career: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> UserProfile | None:
        if not data:
            return None
        return cls(
            user_id=int(data.get("userId", 0)),
            nick_name=data.get("nickName", ""),
            pic_url=data.get("picUrl"),
            level=int(data.get("level", 0)),
            vip_level=int(data.get("vipLevel", 0)),
            gender=int(data.get("gender", 0)),
            birthday=data.get("birthday"),
            details=data.get("details"),
            clan_id=int(data["clanId"]) if data.get("clanId") not in (None, "", 0, "0") else None,
            clan_name=data.get("clanName"),
            clan_role=int(data["clanRole"]) if data.get("clanRole") not in (None, "", 0, "0") else None,
            friend_num=data.get("friendNum"),
            family_num=data.get("familyNum"),
            decoration_count=data.get("decorationCount"),
            suit_count=data.get("suitCount"),
            atlas_count=data.get("ownedAtlasCount"),
            atlas_total=data.get("totalAtlasCount"),
        )


@dataclass(slots=True)
class UserStats:
    user_id: int
    career: dict[str, Any] = field(default_factory=dict)
    friend_num: int | None = None
    family_num: int | None = None
    decoration_count: int | None = None
    suit_count: int | None = None
    atlas_count: int | None = None
    atlas_total: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> UserStats | None:
        if not data:
            return None
        game = data.get("game") or {}
        friend = data.get("friend") or {}
        decoration = data.get("decoration") or {}
        return cls(
            user_id=int(data.get("userId", 0)),
            career=game,
            friend_num=friend.get("friendNum"),
            family_num=friend.get("familyNum"),
            decoration_count=decoration.get("decorationCount"),
            suit_count=decoration.get("suitCount"),
            atlas_count=decoration.get("ownedAtlasCount"),
            atlas_total=decoration.get("totalAtlasCount"),
        )


@dataclass(slots=True)
class ClanRole:
    clan_id: int
    clan_name: str
    role: int

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> ClanRole | None:
        if not data:
            return None
        cid = data.get("clanId")
        if cid in (None, "", 0, "0"):
            return None
        return cls(
            clan_id=int(cid),
            clan_name=data.get("clanName", ""),
            role=int(data.get("role", 0)),
        )


@dataclass(slots=True)
class ClanInfo:
    clan_id: int
    name: str
    level: int
    member_count: int
    max_members: int
    chief_id: int
    chief_name: str
    details: str | None = None
    head_pic: str | None = None
    tags: list[str] = field(default_factory=list)
    currency: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> ClanInfo | None:
        if not data:
            return None
        return cls(
            clan_id=int(data.get("clanId", 0)),
            name=data.get("name", ""),
            level=int(data.get("level", 0)),
            member_count=int(data.get("memberCount", 0)),
            max_members=int(data.get("maxMembers", 0)),
            chief_id=int(data.get("chiefId", 0)),
            chief_name=data.get("chiefName", ""),
            details=data.get("details"),
            head_pic=data.get("headPic"),
            tags=data.get("tags") or [],
            currency=int(data.get("currency", 0)),
        )


@dataclass(slots=True)
class ClanMember:
    user_id: int
    nick_name: str
    role: int
    level: int
    contribution: int
    last_online: int
    pic_url: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> ClanMember | None:
        if not data:
            return None
        return cls(
            user_id=int(data.get("userId", 0)),
            nick_name=data.get("nickName", ""),
            role=int(data.get("role", 0)),
            level=int(data.get("level", 0)),
            contribution=int(data.get("contribution", 0)),
            last_online=int(data.get("lastOnline", 0)),
            pic_url=data.get("picUrl"),
        )


@dataclass(slots=True)
class DecorationItem:
    id: int
    name: str
    category: int
    icon: str | None = None
    is_suit: bool = False
    price: int = 0
    owned: bool = False
    using: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> DecorationItem | None:
        if not data:
            return None
        return cls(
            id=int(data.get("id", 0)),
            name=data.get("name", ""),
            category=int(data.get("category", 0)),
            icon=data.get("icon"),
            is_suit=bool(data.get("isSuit", False)),
            price=int(data.get("price", 0)),
            owned=bool(data.get("owned", False)),
            using=bool(data.get("using", False)),
        )


@dataclass(slots=True)
class Wardrobe:
    items: list[DecorationItem] = field(default_factory=list)

    @classmethod
    def from_list(cls, data: list[dict[str, Any]] | None) -> Wardrobe:
        if not data:
            return cls()
        items = [DecorationItem.from_dict(d) for d in data if d]
        return cls(items=[item for item in items if item is not None])


@dataclass(slots=True)
class GroupInfo:
    group_id: int
    group_name: str
    owner_id: int
    member_count: int
    max_members: int
    invite_status: int
    notice: str | None = None
    notice_pic: str | None = None
    members: list['GroupMember'] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> GroupInfo | None:
        if not data:
            return None
        from .models import GroupMember
        members_data = data.get("members") or data.get("memberList") or []
        members = [GroupMember.from_dict(m) for m in members_data if m]
        return cls(
            group_id=int(data.get("groupId", 0)),
            group_name=data.get("groupName", ""),
            owner_id=int(data.get("ownerId", 0)),
            member_count=int(data.get("memberCount", 0)),
            max_members=int(data.get("maxMembers", 0)),
            invite_status=int(data.get("inviteStatus", 0)),
            notice=data.get("groupNotice"),
            notice_pic=data.get("noticePic"),
            members=[m for m in members if m is not None],
        )


@dataclass(slots=True)
class GroupMember:
    user_id: int
    nick_name: str
    role: int
    pic_url: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> GroupMember | None:
        if not data:
            return None
        return cls(
            user_id=int(data.get("userId", 0)),
            nick_name=data.get("nickName", ""),
            role=int(data.get("role", 0)),
            pic_url=data.get("picUrl"),
        )


@dataclass(slots=True)
class RankEntry:
    user_id: int
    nick_name: str
    rank: int
    score: int
    level: int
    pic_url: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> RankEntry | None:
        if not data:
            return None
        return cls(
            user_id=int(data.get("userId", 0)),
            nick_name=data.get("nickName", ""),
            rank=int(data.get("rank", 0)),
            score=int(data.get("score", 0)),
            level=int(data.get("level", 0)),
            pic_url=data.get("picUrl"),
        )


@dataclass(slots=True)
class SignInStatus:
    signed: bool
    days: int
    rewards: list[dict[str, Any]] = field(default_factory=list)
    next_reward: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SignInStatus | None:
        if not data:
            return None
        signed = bool(data.get("signed", data.get("todaySigned", False)))
        return cls(
            signed=signed,
            days=int(data.get("days", 0)),
            rewards=data.get("rewards") or [],
            next_reward=data.get("nextReward"),
        )


@dataclass(slots=True)
class TaskInfo:
    task_id: int
    name: str
    description: str
    progress: int
    target: int
    completed: bool
    claimed: bool
    reward: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> TaskInfo | None:
        if not data:
            return None
        return cls(
            task_id=int(data.get("id", 0)),
            name=data.get("name", ""),
            description=data.get("description", ""),
            progress=int(data.get("progress", 0)),
            target=int(data.get("target", 0)),
            completed=bool(data.get("completed", False)),
            claimed=bool(data.get("claimed", False)),
            reward=data.get("reward") or {},
        )


@dataclass(slots=True)
class RongCloudToken:
    token: str
    nav_domain: str
    cfg_domain: str

    @classmethod
    def from_string(cls, s: str | None) -> RongCloudToken | None:
        if not s or "@" not in s:
            return None
        body, rest = s.split("@", 1)
        parts = rest.split(";")
        nav_domain = parts[0] if len(parts) > 0 else ""
        cfg_domain = parts[1] if len(parts) > 1 else ""
        return cls(token=body, nav_domain=nav_domain, cfg_domain=cfg_domain)