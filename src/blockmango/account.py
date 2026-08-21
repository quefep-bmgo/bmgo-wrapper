from __future__ import annotations

import random
import time
from typing import Any

import requests

from .config import Config
from .constants import DEFAULT_APP_HEADERS, KEY_PAIRS
from .crypto import (
    _build_signed_headers, _compact, _enc_password,
    _flatten_params, _sign,
)
from .device import DevicePool
from .models import UserProfile, UserStats
from .session import SessionStore
from .submodules import (
    ActivityAPI, ClanAPI, DecorationAPI, FriendsAPI,
    GroupAPI, RankingAPI, RongCloudAPI, UserAPI,
)
from .time_sync import TimeSyncer


class BmgAccount:
    __slots__ = (
        "_ak", "_async_session", "_device_id", "_device_pool",
        "_device_sign", "_nick", "_session", "_session_store",
        "_sk", "_t_off", "_time_syncer", "_token", "_uid",
        "activity", "clan", "config", "decoration", "friends",
        "group", "password", "ranking", "rongcloud", "user", "username",
    )

    def __init__(self, username: str, password: str, config: Config | None = None):
        self.username = username
        self.password = password
        self.config = config or Config.from_env()
        self._session_store = SessionStore(self.config)
        self._time_syncer = TimeSyncer(self.config)
        self._device_pool = DevicePool(self.config)
        self._session: requests.Session | None = None
        self._async_session: Any = None
        self._uid: int | None = None
        self._token: str | None = None
        self._nick: str | None = None
        self._device_id: str | None = None
        self._device_sign: str | None = None
        self._ak: str = KEY_PAIRS[0][0]
        self._sk: str = KEY_PAIRS[0][1]
        self._t_off: int = 0
        self.user = UserAPI(self)
        self.friends = FriendsAPI(self)
        self.group = GroupAPI(self)
        self.clan = ClanAPI(self)
        self.decoration = DecorationAPI(self)
        self.ranking = RankingAPI(self)
        self.activity = ActivityAPI(self)
        self.rongcloud = RongCloudAPI(self)

    @property
    def uid(self) -> int | None:
        return self._uid

    @property
    def token(self) -> str | None:
        return self._token

    @property
    def nick(self) -> str | None:
        return self._nick

    @property
    def device_id(self) -> str | None:
        return self._device_id

    @property
    def is_logged_in(self) -> bool:
        return bool(self._uid and self._token)

    def _get_session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def _get_async_session(self) -> Any:
        if self._async_session is None:
            import httpx
            self._async_session = httpx.AsyncClient(verify=self.config.verify_ssl)
        return self._async_session

    def _session_dict(self) -> dict[str, Any]:
        return {
            "uid": self._uid, "token": self._token, "nick": self._nick,
            "device_id": self._device_id, "device_sign": self._device_sign,
            "ak": self._ak, "sk": self._sk,
        }

    def save_session(self) -> None:
        self._session_store.save(self.username, self._session_dict())

    def load_session(self) -> dict[str, Any]:
        return self._session_store.load(self.username)

    def restore_session(self, sess: dict[str, Any]) -> bool:
        self._uid = sess.get("uid")
        self._token = sess.get("token")
        self._nick = sess.get("nick")
        self._device_id = sess.get("device_id")
        self._device_sign = sess.get("device_sign")
        self._ak = sess.get("ak") or self._ak
        self._sk = sess.get("sk") or self._sk
        return bool(self._uid and self._token)

    def _sync_time(self) -> None:
        self._t_off = self._time_syncer.sync()

    def login(self, tries: int | None = None) -> bool:
        max_tries = tries or self.config.login_max_tries
        self._sync_time()
        self._device_pool.ensure_loaded()
        enc = _enc_password(self.password)
        rand = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
        for attempt in range(max_tries):
            dev_id, dev_sign = self._device_pool.get_random()
            ak, sk = random.choice(KEY_PAIRS)
            body = _compact({
                "account": self.username, "password": enc,
                "tsvAccount": "", "tsvPlatform": "", "tsvToken": "",
                "ticket": "", "randomstr": rand,
            })
            flat = _flatten_params({})
            nonce, ts, sign = _sign("/user/api/v4/account/login", flat, body, ak, sk, None, self._t_off)
            headers = {
                "Host": "gw.sandboxol.com", "bmg-device-id": dev_id, "bmg-sign": dev_sign,
                "os": "android", "apptype": "1", "x-apikey": ak, "x-nonce": nonce,
                "x-time": ts, "x-sign": sign, "x-urlpath": "/user/api/v4/account/login",
                "content-type": "application/json; charset=UTF-8", "user-agent": self.config.user_agent,
            }
            try:
                r = self._get_session().post(
                    self.config.api_base + "/user/api/v4/account/login",
                    headers=headers, data=body, timeout=self.config.login_timeout,
                    verify=self.config.verify_ssl,
                )
                data = r.json()
            except ValueError:
                if r is not None and r.status_code == 567:
                    return False
                time.sleep(0.5)
                continue
            except Exception:
                time.sleep(0.5)
                continue
            code = data.get("code")
            if code == 1:
                d = data.get("data", {})
                token = d.get("accessToken")
                if not token:
                    time.sleep(1)
                    continue
                self._uid = d.get("userId")
                self._token = token
                self._nick = d.get("nickName")
                self._device_id = dev_id
                self._device_sign = dev_sign
                self._ak = ak
                self._sk = sk
                self.save_session()
                return True
            if code == 100008:
                time.sleep(1)
            elif code == 100001:
                self._sync_time()
                time.sleep(0.5)
            elif code == 567:
                time.sleep(2)
            else:
                return False
        return False

    async def async_login(self, tries: int | None = None) -> bool:
        max_tries = tries or self.config.login_max_tries
        self._sync_time()
        self._device_pool.ensure_loaded()
        enc = _enc_password(self.password)
        rand = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
        for attempt in range(max_tries):
            dev_id, dev_sign = self._device_pool.get_random()
            ak, sk = random.choice(KEY_PAIRS)
            body = _compact({
                "account": self.username, "password": enc,
                "tsvAccount": "", "tsvPlatform": "", "tsvToken": "",
                "ticket": "", "randomstr": rand,
            })
            flat = _flatten_params({})
            nonce, ts, sign = _sign("/user/api/v4/account/login", flat, body, ak, sk, None, self._t_off)
            headers = {
                "Host": "gw.sandboxol.com", "bmg-device-id": dev_id, "bmg-sign": dev_sign,
                "os": "android", "apptype": "1", "x-apikey": ak, "x-nonce": nonce,
                "x-time": ts, "x-sign": sign, "x-urlpath": "/user/api/v4/account/login",
                "content-type": "application/json; charset=UTF-8", "user-agent": self.config.user_agent,
            }
            try:
                client = self._get_async_session()
                r = await client.post(
                    self.config.api_base + "/user/api/v4/account/login",
                    headers=headers, content=body, timeout=self.config.login_timeout,
                )
                data = r.json()
            except Exception:
                import asyncio
                await asyncio.sleep(0.5)
                continue
            code = data.get("code")
            if code == 1:
                d = data.get("data", {})
                token = d.get("accessToken")
                if not token:
                    import asyncio
                    await asyncio.sleep(1)
                    continue
                self._uid = d.get("userId")
                self._token = token
                self._nick = d.get("nickName")
                self._device_id = dev_id
                self._device_sign = dev_sign
                self._ak = ak
                self._sk = sk
                self.save_session()
                return True
            if code == 100008:
                import asyncio
                await asyncio.sleep(1)
            elif code == 100001:
                self._sync_time()
                import asyncio
                await asyncio.sleep(0.5)
            elif code == 567:
                import asyncio
                await asyncio.sleep(2)
            else:
                return False
        return False

    def session_valid(self) -> bool:
        if not self._token:
            return False
        try:
            self._sync_time()
            r = self.request("GET", "/user/api/v1/users/bg-careers", params={"userId": str(self._uid)})
            return r.get("code") == 1
        except Exception:
            return False

    async def async_session_valid(self) -> bool:
        if not self._token:
            return False
        try:
            self._sync_time()
            r = await self.async_request("GET", "/user/api/v1/users/bg-careers", params={"userId": str(self._uid)})
            return r.get("code") == 1
        except Exception:
            return False

    def request(self, method: str, path: str, params: dict[str, Any] | None = None,
                body: dict[str, Any] | None = None, language: str | None = None) -> dict[str, Any]:
        body_str = _compact(body)
        flat = _flatten_params(params or {})
        sp: dict[str, list[str]] = {}
        for k, v in flat:
            sp.setdefault(k, []).append(v)
        try:
            resp = self._signed_request(method, path, flat, sp, body_str, language)
        except Exception as e:
            return {"code": -1, "message": str(e)}
        if isinstance(resp, dict) and resp.get("code") == 100001:
            for _ in range(2):
                self._sync_time()
                try:
                    resp = self._signed_request(method, path, flat, sp, body_str, language)
                except Exception as e:
                    return {"code": -1, "message": str(e)}
                if not (isinstance(resp, dict) and resp.get("code") == 100001):
                    break
        return resp

    def _signed_request(self, method: str, path: str, flat: list[tuple[str, str]],
                        sp: dict[str, list[str]], body_str: str, language: str | None) -> dict[str, Any]:
        import copy
        headers = _build_signed_headers(
            path, flat, body_str, self._ak, self._sk,
            self._device_id or "", self._device_sign or "",
            self._t_off, self._uid, self._token, language,
            dict(DEFAULT_APP_HEADERS),
        )
        url = self.config.api_base + path
        if flat:
            url += "?" + "&".join(f"{k}={v}" for k, v in flat)
        session = self._get_session()
        if method == "GET":
            r = session.get(url, headers=headers, timeout=self.config.request_timeout, verify=self.config.verify_ssl)
        elif method == "POST":
            r = session.post(url, headers=headers, data=body_str, timeout=self.config.request_timeout, verify=self.config.verify_ssl)
        elif method == "PUT":
            r = session.put(url, headers=headers, data=body_str, timeout=self.config.request_timeout, verify=self.config.verify_ssl)
        elif method == "DELETE":
            r = session.delete(url, headers=headers, timeout=self.config.request_timeout, verify=self.config.verify_ssl)
        else:
            return {"code": -1, "message": "unsupported method"}
        return r.json() if r.text else {}

    async def async_request(self, method: str, path: str, params: dict[str, Any] | None = None,
                            body: dict[str, Any] | None = None, language: str | None = None) -> dict[str, Any]:
        body_str = _compact(body)
        flat = _flatten_params(params or {})
        sp: dict[str, list[str]] = {}
        for k, v in flat:
            sp.setdefault(k, []).append(v)
        try:
            resp = await self._async_signed_request(method, path, flat, sp, body_str, language)
        except Exception as e:
            return {"code": -1, "message": str(e)}
        if isinstance(resp, dict) and resp.get("code") == 100001:
            for _ in range(2):
                self._sync_time()
                try:
                    resp = await self._async_signed_request(method, path, flat, sp, body_str, language)
                except Exception as e:
                    return {"code": -1, "message": str(e)}
                if not (isinstance(resp, dict) and resp.get("code") == 100001):
                    break
        return resp

    async def _async_signed_request(self, method: str, path: str, flat: list[tuple[str, str]],
                                    sp: dict[str, list[str]], body_str: str, language: str | None) -> dict[str, Any]:
        headers = _build_signed_headers(
            path, flat, body_str, self._ak, self._sk,
            self._device_id or "", self._device_sign or "",
            self._t_off, self._uid, self._token, language,
            dict(DEFAULT_APP_HEADERS),
        )
        url = self.config.api_base + path
        if flat:
            url += "?" + "&".join(f"{k}={v}" for k, v in flat)
        client = self._get_async_session()
        if method == "GET":
            r = await client.get(url, headers=headers, timeout=self.config.request_timeout)
        elif method == "POST":
            r = await client.post(url, headers=headers, content=body_str, timeout=self.config.request_timeout)
        elif method == "PUT":
            r = await client.put(url, headers=headers, content=body_str, timeout=self.config.request_timeout)
        elif method == "DELETE":
            r = await client.delete(url, headers=headers, timeout=self.config.request_timeout)
        else:
            return {"code": -1, "message": "unsupported method"}
        return r.json() if r.text else {}

    def get_profile(self, uid: int) -> UserProfile | None:
        r = self.request("GET", f"/friend/api/v1/friends/info/id/{uid}")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    def get_own_profile(self) -> UserProfile | None:
        r = self.request("GET", "/user/api/v2/user/details/info")
        if r.get("code") == 1:
            return UserProfile.from_dict(r.get("data"))
        return None

    def get_stats(self, uid: int) -> UserStats | None:
        r = self.request("GET", "/user/api/v1/users/bg-careers", params={"userId": str(uid)})
        if r.get("code") == 1:
            return UserStats.from_dict(r.get("data"))
        return None

    def get_clan_role(self, uid: int) -> dict[str, Any] | None:
        r = self.request("GET", "/bedwar/api/v1/friends/clan/by/userIds", params={"userIds": str(uid)})
        if r.get("code") != 1:
            return None
        data = r.get("data")
        if not isinstance(data, list) or not data:
            return None
        role = (data[0] or {}).get("clanRole") or {}
        if role.get("clanId") in (None, "", 0, "0"):
            return None
        return role

    def get_own_clan(self) -> dict[str, Any] | None:
        r = self.request("GET", "/clan/api/v1/clan/tribe/base")
        return r.get("data") if r.get("code") == 1 else None

    def get_clan_info(self, clan_id: int) -> dict[str, Any] | None:
        r = self.request("GET", "/clan/api/v2/clan/tribe", params={"clanId": clan_id})
        return r.get("data") if r.get("code") == 1 else None

    def get_clan_members(self) -> list[dict[str, Any]]:
        r = self.request("GET", "/clan/api/v1/clan/tribe/member")
        return r.get("data") or []

    def apply_to_clan(self, clan_id: int, msg: str = "") -> dict[str, Any]:
        return self.request("POST", "/clan/api/v1/clan/tribe/member", body={"clanId": clan_id, "msg": msg or "Bot join request"})

    def leave_clan(self) -> dict[str, Any]:
        return self.request("DELETE", "/clan/api/v1/clan/tribe/member")

    def lookup(self, uid: int) -> UserProfile | None:
        if uid == self._uid:
            profile = self.get_own_profile()
        else:
            profile = self.get_profile(uid)
        if not profile:
            return None
        stats = self.get_stats(uid)
        if stats:
            profile.career = stats.career
            profile.friend_num = stats.friend_num
            profile.decoration_count = stats.decoration_count
            profile.suit_count = stats.suit_count
            profile.atlas_count = stats.atlas_count
            profile.atlas_total = stats.atlas_total
        clan = self.get_clan_role(uid)
        if clan:
            profile.clan_id = clan.get("clanId")
            profile.clan_name = clan.get("clanName")
            profile.clan_role = clan.get("role")
        return profile

    def lookup_result(self, uid: int):
        if uid == self._uid:
            profile = self.get_own_profile()
        else:
            profile = self.get_profile(uid)
        if profile:
            stats = self.get_stats(uid)
            if stats:
                profile.career = stats.career
                profile.friend_num = stats.friend_num
                profile.decoration_count = stats.decoration_count
                profile.suit_count = stats.suit_count
                profile.atlas_count = stats.atlas_count
                profile.atlas_total = stats.atlas_total
            clan = self.get_clan_role(uid)
            if clan:
                profile.clan_id = clan.get("clanId")
                profile.clan_name = clan.get("clanName")
                profile.clan_role = clan.get("role")
            return ("ok", profile)
        if uid == self._uid:
            r = self.request("GET", "/user/api/v2/user/details/info")
        else:
            r = self.request("GET", f"/friend/api/v1/friends/info/id/{uid}")
        if r.get("code") == 1:
            return ("notfound", None)
        return ("error", r.get("message") or "profile request failed")

    def get_decorations(self, uid: int) -> list[dict[str, Any]]:
        for path in (
            f"/decoration/api/v1/decorations-v2/users/{uid}/classify/all",
            f"/decoration/api/v1/new/decorations/users/{uid}/classify/all",
        ):
            r = self.request("GET", path, language="en_US")
            if r.get("code") == 1:
                return r.get("data") or []
            if r.get("code") == 3:
                continue
        return []

    def get_decorations_result(self, uid: int):
        for path in (
            f"/decoration/api/v1/decorations-v2/users/{uid}/classify/all",
            f"/decoration/api/v1/new/decorations/users/{uid}/classify/all",
        ):
            r = self.request("GET", path, language="en_US")
            if r.get("code") == 1:
                return True, r.get("data") or []
            if r.get("code") == 3:
                continue
        return False, "no items found"

    def get_family_list(self, uid: int) -> list[dict[str, Any]]:
        r = self.request("GET", "/friend/api/v1/friend/homepage/family/list", params={"userId": uid})
        return r.get("data") or []

    def search_friends(self, query: str, param: str = "keyword") -> list[dict[str, Any]]:
        for p in ("keyword", "name", "nickName", "key", "search"):
            r = self.request("GET", "/api/v1/friends/search", params={p: query})
            data = r.get("data")
            if data:
                results = data if isinstance(data, list) else (data.get("list") or data.get("users") or data.get("data") or [])
                if results:
                    return results
        return []

    def daily_sign_in(self) -> dict[str, Any]:
        return self.request("POST", "/activity/api/v1/signIn")

    def get_sign_in_status(self) -> dict[str, Any] | None:
        r = self.request("GET", "/activity/api/v1/signIn")
        return r.get("data") if r.get("code") == 1 else None

    def get_rongcloud_token(self) -> str | None:
        r = self.request("GET", "/user/api/v1/users/device/token")
        data = r.get("data")
        return data if isinstance(data, str) and "@" in data else None

    def get_group_info(self, group_id: int) -> dict[str, Any] | None:
        r = self.request("GET", "/msg/api/v1/msg/group/chat/info", params={"groupId": group_id})
        return r.get("data") if r.get("code") == 1 else None

    def kick_from_group(self, group_id: int, uids: list[int], group_name: str = "") -> dict[str, Any]:
        if not group_name:
            info = self.get_group_info(group_id)
            group_name = info.get("groupName") or "" if info else ""
        return self.request("PUT", "/msg/api/v1/msg/group/chat/kickOut",
                           body={"groupId": group_id, "groupName": group_name, "inviterId": self._uid, "memberIds": uids})

    def get_game_ranking(self, game_id: str, period: str = "all", page: int = 1, size: int = 10) -> dict[str, Any]:
        return self.request("GET", f"/game/api/v1/games/{game_id}/rank",
                           params={"type": period, "pageNo": page - 1, "pageSize": size})

    async def async_get_game_ranking(self, game_id: str, period: str = "all", page: int = 1, size: int = 10) -> dict[str, Any]:
        return await self.async_request("GET", f"/game/api/v1/games/{game_id}/rank",
                                       params={"type": period, "pageNo": page - 1, "pageSize": size})

    def party_auth(self, uid: int, psid: str, game_id: str = "g1008", is_new_engine: bool = True, engine4_version: int = 0) -> dict[str, Any]:
        return self.request("GET", "/game/api/v3/party/auth",
                           params={"userId": uid, "psid": psid, "isNewEngine": is_new_engine, "typeId": game_id, "engine4Version": engine4_version})

    async def async_party_auth(self, uid: int, psid: str, game_id: str = "g1008", is_new_engine: bool = True, engine4_version: int = 0) -> dict[str, Any]:
        return await self.async_request("GET", "/game/api/v3/party/auth",
                                       params={"userId": uid, "psid": psid, "isNewEngine": is_new_engine, "typeId": game_id, "engine4Version": engine4_version})

    def party_exists(self, psid: str) -> dict[str, Any]:
        return self.request("GET", "/api/v1/parties/exists", params={"psid": psid})

    async def async_party_exists(self, psid: str) -> dict[str, Any]:
        return await self.async_request("GET", "/api/v1/parties/exists", params={"psid": psid})

    def get_friend_popularity(self, friend_id: int) -> dict[str, Any]:
        return self.request("GET", f"/friend/api/v1/popularity/{friend_id}")

    async def async_get_friend_popularity(self, friend_id: int) -> dict[str, Any]:
        return await self.async_request("GET", f"/friend/api/v1/popularity/{friend_id}")

    def add_friend_popularity(self, friend_id: int) -> dict[str, Any]:
        return self.request("POST", "/friend/api/v1/popularity", params={"friendId": friend_id})

    async def async_add_friend_popularity(self, friend_id: int) -> dict[str, Any]:
        return await self.async_request("POST", "/friend/api/v1/popularity", params={"friendId": friend_id})

    def get_friend_requests(self, page: int = 1, size: int = 50) -> list[dict[str, Any]]:
        r = self.request("GET", "/friend/api/v1/friends/requests", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        return data.get("data") or data.get("list") or []

    async def async_get_friend_requests(self, page: int = 1, size: int = 50) -> list[dict[str, Any]]:
        r = await self.async_request("GET", "/friend/api/v1/friends/requests", params={"pageNo": page, "pageSize": size})
        data = r.get("data") or {}
        return data.get("data") or data.get("list") or []

    def approve_all_friend_requests(self) -> dict[str, Any]:
        return self.request("POST", "/friend/api/v1/friends/requests/approve-all")

    async def async_approve_all_friend_requests(self) -> dict[str, Any]:
        return await self.async_request("POST", "/friend/api/v1/friends/requests/approve-all")

    def reject_all_friend_requests(self) -> dict[str, Any]:
        return self.request("POST", "/friend/api/v1/friends/requests/reject-all")

    async def async_reject_all_friend_requests(self) -> dict[str, Any]:
        return await self.async_request("POST", "/friend/api/v1/friends/requests/reject-all")

    def register(self, account: str, password: str, captcha: str | None = None,
                 captcha_type: str = "geetest", scene: str = "register",
                 verify_code: str | None = None,
                 geetest_challenge: str | None = None,
                 geetest_validate: str | None = None,
                 geetest_seccode: str | None = None) -> dict[str, Any]:
        self._sync_time()
        self._device_pool.ensure_loaded()
        rand = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
        body_dict = {
            "account": account, "password": _enc_password(password),
            "tsvAccount": "", "tsvPlatform": "", "tsvToken": "", "ticket": "", "randomstr": rand,
        }
        if geetest_challenge and geetest_validate and geetest_seccode:
            body_dict["geetest_challenge"] = geetest_challenge
            body_dict["geetest_validate"] = geetest_validate
            body_dict["geetest_seccode"] = geetest_seccode
        elif captcha:
            body_dict["captcha"] = captcha
            body_dict["captchaType"] = captcha_type
            body_dict["scene"] = scene
        if verify_code:
            body_dict["verifyCode"] = verify_code
        body = _compact(body_dict)
        flat = _flatten_params({})
        nonce, ts, sign = _sign("/user/api/v4/account/register", flat, body, self._ak, self._sk, None, self._t_off)
        headers = {
            "Host": "gw.sandboxol.com", "bmg-device-id": self._device_id or "", "bmg-sign": self._device_sign or "",
            "os": "android", "apptype": "1", "x-apikey": self._ak, "x-nonce": nonce,
            "x-time": ts, "x-sign": sign, "x-urlpath": "/user/api/v4/account/register",
            "content-type": "application/json; charset=UTF-8", "user-agent": self.config.user_agent,
        }
        try:
            r = self._get_session().post(
                self.config.api_base + "/user/api/v4/account/register",
                headers=headers, data=body, timeout=self.config.login_timeout, verify=self.config.verify_ssl,
            )
            return r.json()
        except Exception as e:
            return {"code": -1, "message": str(e)}

    async def async_register(self, account: str, password: str, captcha: str | None = None,
                              captcha_type: str = "geetest", scene: str = "register",
                              verify_code: str | None = None,
                              geetest_challenge: str | None = None,
                              geetest_validate: str | None = None,
                              geetest_seccode: str | None = None) -> dict[str, Any]:
        self._sync_time()
        self._device_pool.ensure_loaded()
        rand = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
        body_dict = {
            "account": account, "password": _enc_password(password),
            "tsvAccount": "", "tsvPlatform": "", "tsvToken": "", "ticket": "", "randomstr": rand,
        }
        if geetest_challenge and geetest_validate and geetest_seccode:
            body_dict["geetest_challenge"] = geetest_challenge
            body_dict["geetest_validate"] = geetest_validate
            body_dict["geetest_seccode"] = geetest_seccode
        elif captcha:
            body_dict["captcha"] = captcha
            body_dict["captchaType"] = captcha_type
            body_dict["scene"] = scene
        if verify_code:
            body_dict["verifyCode"] = verify_code
        body = _compact(body_dict)
        flat = _flatten_params({})
        nonce, ts, sign = _sign("/user/api/v4/account/register", flat, body, self._ak, self._sk, None, self._t_off)
        headers = {
            "Host": "gw.sandboxol.com", "bmg-device-id": self._device_id or "", "bmg-sign": self._device_sign or "",
            "os": "android", "apptype": "1", "x-apikey": self._ak, "x-nonce": nonce,
            "x-time": ts, "x-sign": sign, "x-urlpath": "/user/api/v4/account/register",
            "content-type": "application/json; charset=UTF-8", "user-agent": self.config.user_agent,
        }
        try:
            client = self._get_async_session()
            r = await client.post(
                self.config.api_base + "/user/api/v4/account/register",
                headers=headers, content=body, timeout=self.config.login_timeout,
            )
            return r.json()
        except Exception as e:
            return {"code": -1, "message": str(e)}

    def get_captcha_challenge(self, scene: str = "register", captcha_type: str = "geetest") -> dict[str, Any]:
        self._sync_time()
        return self.request("GET", "/user/api/v4/captcha/get", params={"scene": scene, "type": captcha_type})

    async def async_get_captcha_challenge(self, scene: str = "register", captcha_type: str = "geetest") -> dict[str, Any]:
        self._sync_time()
        return await self.async_request("GET", "/user/api/v4/captcha/get", params={"scene": scene, "type": captcha_type})

    def verify_captcha(self, challenge: str, validate: str, seccode: str, scene: str = "register") -> dict[str, Any]:
        self._sync_time()
        return self.request("POST", "/user/api/v4/captcha/verify",
                           body={"challenge": challenge, "validate": validate, "seccode": seccode, "scene": scene})

    async def async_verify_captcha(self, challenge: str, validate: str, seccode: str, scene: str = "register") -> dict[str, Any]:
        self._sync_time()
        return await self.async_request("POST", "/user/api/v4/captcha/verify",
                                       body={"challenge": challenge, "validate": validate, "seccode": seccode, "scene": scene})

    def send_verification_code(self, account: str, code_type: str = "email", scene: str = "register") -> dict[str, Any]:
        self._sync_time()
        return self.request("POST", "/user/api/v4/account/sendCode",
                           body={"account": account, "type": code_type, "scene": scene})

    async def async_send_verification_code(self, account: str, code_type: str = "email", scene: str = "register") -> dict[str, Any]:
        self._sync_time()
        return await self.async_request("POST", "/user/api/v4/account/sendCode",
                                       body={"account": account, "type": code_type, "scene": scene})

    def verify_code(self, account: str, code: str, code_type: str = "email", scene: str = "register") -> dict[str, Any]:
        self._sync_time()
        return self.request("POST", "/user/api/v4/account/verifyCode",
                           body={"account": account, "code": code, "type": code_type, "scene": scene})

    async def async_verify_code(self, account: str, code: str, code_type: str = "email", scene: str = "register") -> dict[str, Any]:
        self._sync_time()
        return await self.async_request("POST", "/user/api/v4/account/verifyCode",
                                       body={"account": account, "code": code, "type": code_type, "scene": scene})

    async def async_leave_clan(self) -> dict[str, Any]:
        return await self.async_request("DELETE", "/clan/api/v1/clan/tribe/member")

    async def async_get_clan_members(self) -> list[dict[str, Any]]:
        r = await self.async_request("GET", "/clan/api/v1/clan/tribe/member")
        return r.get("data") or []

    async def async_get_own_clan(self) -> dict[str, Any] | None:
        r = await self.async_request("GET", "/clan/api/v1/clan/tribe/base")
        return r.get("data") if r.get("code") == 1 else None

    async def async_get_clan_info(self, clan_id: int) -> dict[str, Any] | None:
        r = await self.async_request("GET", "/clan/api/v2/clan/tribe", params={"clanId": clan_id})
        return r.get("data") if r.get("code") == 1 else None

    def close(self) -> None:
        if self._session:
            self._session.close()
            self._session = None

    async def async_close(self) -> None:
        if self._async_session:
            await self._async_session.aclose()
            self._async_session = None

    def logout(self) -> None:
        self._token = None
        self._uid = None
        self._nick = None
        self._device_id = None
        self._device_sign = None
        self.close()

    async def async_logout(self) -> None:
        self._token = None
        self._uid = None
        self._nick = None
        self._device_id = None
        self._device_sign = None
        await self.async_close()

    def __enter__(self) -> 'BmgAccount':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    async def __aenter__(self) -> 'BmgAccount':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.async_close()