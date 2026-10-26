"""Remote configuration files served by the Blockman GO config endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class RemoteConfigAPI:
    """Read-only access to `/config/files` and `/config/ml/files` resources."""

    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def _get(self, name: str, client_md5: str | None = None,
             client_version: int | None = None, ml: bool = False) -> dict[str, Any]:
        prefix = "/config/ml/files/" if ml else "/config/files/"
        params: dict[str, Any] = {}
        if client_md5:
            params["clientMd5"] = client_md5
        if client_version is not None:
            params["clientVersion"] = client_version
        return self._account.request("GET", prefix + name, params=params or None)

    async def _async_get(self, name: str, client_md5: str | None = None,
                         client_version: int | None = None, ml: bool = False) -> dict[str, Any]:
        prefix = "/config/ml/files/" if ml else "/config/files/"
        params: dict[str, Any] = {}
        if client_md5:
            params["clientMd5"] = client_md5
        if client_version is not None:
            params["clientVersion"] = client_version
        return await self._account.async_request("GET", prefix + name, params=params or None)

    def get_config(self, name: str, client_md5: str | None = None,
                   client_version: int | None = None, ml: bool = False) -> dict[str, Any]:
        return self._get(name, client_md5, client_version, ml)

    async def async_get_config(self, name: str, client_md5: str | None = None,
                               client_version: int | None = None, ml: bool = False) -> dict[str, Any]:
        return await self._async_get(name, client_md5, client_version, ml)

    def check_version(self) -> dict[str, Any]:
        return self._get("blockymods-check-version")

    async def async_check_version(self) -> dict[str, Any]:
        return await self._async_get("blockymods-check-version")

    def get_deeplink_remote_config(self, client_md5: str = "590747fc8d5b438bd6d427e1003e0d1a",
                                   client_version: int = 67) -> dict[str, Any]:
        return self._get("deeplink-remote-config", client_md5, client_version)

    async def async_get_deeplink_remote_config(self, client_md5: str = "590747fc8d5b438bd6d427e1003e0d1a",
                                               client_version: int = 67) -> dict[str, Any]:
        return await self._async_get("deeplink-remote-config", client_md5, client_version)

    def get_event_blacklist_config(self, client_md5: str = "07322629b95adbe5171ce9be607d7b49",
                                   client_version: int = 16) -> dict[str, Any]:
        return self._get("event-blacklist-config", client_md5, client_version)

    async def async_get_event_blacklist_config(self, client_md5: str = "07322629b95adbe5171ce9be607d7b49",
                                               client_version: int = 16) -> dict[str, Any]:
        return await self._async_get("event-blacklist-config", client_md5, client_version)

    def get_common_lang_img_url_config(self, client_md5: str = "5f5aa2f16a9215d04c69775d5a34a241",
                                       client_version: int = 16) -> dict[str, Any]:
        return self._get("common_lang_img_url_config", client_md5, client_version, ml=True)

    async def async_get_common_lang_img_url_config(self, client_md5: str = "5f5aa2f16a9215d04c69775d5a34a241",
                                                   client_version: int = 16) -> dict[str, Any]:
        return await self._async_get("common_lang_img_url_config", client_md5, client_version, ml=True)

    def get_game_resource_config(self) -> dict[str, Any]:
        return self._get("game_resource_config")

    async def async_get_game_resource_config(self) -> dict[str, Any]:
        return await self._async_get("game_resource_config")

    def get_game_detail_to_editor(self) -> dict[str, Any]:
        return self._get("game-detail-to-editor")

    async def async_get_game_detail_to_editor(self) -> dict[str, Any]:
        return await self._async_get("game-detail-to-editor")

    def get_sharing_game_resource_config(self, client_md5: str = "ebbb5cd09b8cbdab4a60b6f89e6f5d9c",
                                         client_version: int = 16) -> dict[str, Any]:
        return self._get("sharing-game-resource-config", client_md5, client_version)

    async def async_get_sharing_game_resource_config(self, client_md5: str = "ebbb5cd09b8cbdab4a60b6f89e6f5d9c",
                                                     client_version: int = 16) -> dict[str, Any]:
        return await self._async_get("sharing-game-resource-config", client_md5, client_version)

    def get_sticker_config(self) -> dict[str, Any]:
        return self._get("app_sticker_config")

    async def async_get_sticker_config(self) -> dict[str, Any]:
        return await self._async_get("app_sticker_config")

    def get_blockmods_config(self, client_md5: str = "90b921c94343c316de3c2f14742e3f30",
                             client_version: int = 96) -> dict[str, Any]:
        return self._get("blockmods-config-v1", client_md5, client_version)

    async def async_get_blockmods_config(self, client_md5: str = "90b921c94343c316de3c2f14742e3f30",
                                         client_version: int = 96) -> dict[str, Any]:
        return await self._async_get("blockmods-config-v1", client_md5, client_version)

    def get_welcome_banner(self) -> dict[str, Any]:
        return self._get("blockmango_welcome_banner", ml=True)

    async def async_get_welcome_banner(self) -> dict[str, Any]:
        return await self._async_get("blockmango_welcome_banner", ml=True)

    def get_game_rank_title_config(self) -> dict[str, Any]:
        return self._get("game-rank-title-config", ml=True)

    async def async_get_game_rank_title_config(self) -> dict[str, Any]:
        return await self._async_get("game-rank-title-config", ml=True)

    def get_game_room_def_title_config(self) -> dict[str, Any]:
        return self._get("game_room_def_title_config", ml=True)

    async def async_get_game_room_def_title_config(self) -> dict[str, Any]:
        return await self._async_get("game_room_def_title_config", ml=True)

    def get_game_room_tab_config(self) -> dict[str, Any]:
        return self._get("game_room_tab_config", ml=True)

    async def async_get_game_room_tab_config(self) -> dict[str, Any]:
        return await self._async_get("game_room_tab_config", ml=True)

    def get_im_fraud_rule_config(self, client_md5: str = "4c76016c61747b68a6eaf908e73584c2",
                                 client_version: int = 2) -> dict[str, Any]:
        return self._get("im_fraud_rule_config", client_md5, client_version, ml=True)

    async def async_get_im_fraud_rule_config(self, client_md5: str = "4c76016c61747b68a6eaf908e73584c2",
                                             client_version: int = 2) -> dict[str, Any]:
        return await self._async_get("im_fraud_rule_config", client_md5, client_version, ml=True)

    def get_new_player_guide_config(self) -> dict[str, Any]:
        return self._get("new_player_guide_for_rbx_config", ml=True)

    async def async_get_new_player_guide_config(self) -> dict[str, Any]:
        return await self._async_get("new_player_guide_for_rbx_config", ml=True)

    def get_tribe_introduction_banner(self) -> dict[str, Any]:
        return self._get("tribe_introduction_banner", ml=True)

    async def async_get_tribe_introduction_banner(self) -> dict[str, Any]:
        return await self._async_get("tribe_introduction_banner", ml=True)
