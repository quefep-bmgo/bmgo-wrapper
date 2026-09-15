from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class GameAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def list_games(self, page: int = 1, size: int = 20, order_type: str = "",
                   type_id: int = 0, order: str = "", is_publish: int = 1) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size, "isPublish": is_publish}
        if order_type:
            params["orderType"] = order_type
        if type_id:
            params["typeId"] = type_id
        if order:
            params["order"] = order
        return self._account.request("GET", "/game/api/v1/games",
                                     params=params, language="en_US")

    def get_game_details(self, game_id: str, app_version: int = 0,
                         engine_version: int = 0, ram: int = 0) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if app_version:
            params["appVersion"] = app_version
        return self._account.request("GET", f"/game/api/v3/games/{game_id}",
                                     params=params, language="en_US")

    def get_game_ranking(self, game_id: str, period: str = "all", page: int = 1, size: int = 10) -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/games/{game_id}/rank",
                                     params={"type": period, "pageNo": page - 1, "pageSize": size})

    def get_usage_ranking(self, game_id: str, page: int = 1, size: int = 10) -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/games/{game_id}/uses/rank",
                                     params={"pageNo": page, "pageSize": size})

    def get_hot_games(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/game-list/homepage/hot")

    def get_recommended_games(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v2/game-list/homepage/recommend")

    def get_game_categories(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/game-list/category/list")

    def get_games_by_category(self, category_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/game-list/by/category",
                                     params={"categoryId": category_id, "pageNo": page, "pageSize": size})

    def get_app_categories(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/app/categories")

    def get_categories_by_language(self, language: str = "en_US") -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/category/list/by/language",
                                     params={"language": language})

    def get_game_config(self, game_id: str) -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/games/config/app/{game_id}")

    def get_game_mode_config(self, game_id: str) -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/games/mode/config/app/{game_id}")

    def get_resource_version(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/games/resource/version")

    def search_games(self, keyword: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/game/info/search",
                                     params={"keyword": keyword, "pageNo": page, "pageSize": size})

    def get_update_tip(self, game_id: str) -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/games/update/tip/info/app/{game_id}")

    def get_update_list(self, user_id: int) -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/games/update/list/{user_id}")

    def get_warmup_info(self, game_id: str, language: str = "en_US") -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/games/warmup/{game_id}/languages/{language}")

    def get_all_open_parties(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/games/all/open/party")

    def get_team_members(self, team_id: str) -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/games/team/member/{team_id}")

    def get_turntable_info(self, game_id: str) -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/game/{game_id}/turntable")

    def claim_turntable(self, game_id: str) -> dict[str, Any]:
        return self._account.request("PUT", f"/game/api/v1/game/{game_id}/turntable")

    def get_praise_online_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/game/praise/online/info")

    def update_engine(self, engine_version: str) -> dict[str, Any]:
        return self._account.request("PUT", "/game/api/v1/games/engine",
                                     body={"engineVersion": engine_version})

    def like_game(self, game_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/games/like",
                                     body={"gameId": game_id})

    def post_comment(self, game_id: str, content: str) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/comment",
                                     body={"gameId": game_id, "content": content})

    def get_svip_game_list(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/vip-privilege-game/svip-game-list")

    def get_vip_game_list(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/vip-privilege-game/vip-game-list")

    def create_room(self, game_id: str, room_name: str = "", max_players: int = 0,
                    is_private: bool = False, password: str = "") -> dict[str, Any]:
        body: dict[str, Any] = {"gameId": game_id}
        if room_name:
            body["roomName"] = room_name
        if max_players:
            body["maxPlayers"] = max_players
        if is_private:
            body["isPrivate"] = True
        if password:
            body["password"] = password
        return self._account.request("POST", "/game/api/v4/gameroom/create", body=body)

    def list_rooms(self, game_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v2/gameroom/list",
                                     params={"gameId": game_id, "pageNo": page, "pageSize": size})

    def list_rooms_v4(self, game_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v4/gameroom/list",
                                     params={"gameId": game_id, "pageNo": page, "pageSize": size})

    def get_room_details(self, room_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/details",
                                     params={"roomId": room_id})

    def get_room_details_v3(self, room_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v3/gameroom/details",
                                     params={"roomId": room_id})

    def enter_room(self, room_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/enter",
                                     params={"roomId": room_id})

    def exit_room(self, room_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/exit",
                                     params={"roomId": room_id})

    def check_room(self, room_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/check",
                                     params={"roomId": room_id})

    def share_room(self, room_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/gameroom/share",
                                     body={"roomId": room_id})

    def enter_game(self, room_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/gameroom/enter-game",
                                     body={"roomId": room_id})

    def like_work(self, work_id: str) -> dict[str, Any]:
        return self._account.request("POST", f"/game/api/v1/gameroom/work/{work_id}/like")

    def unlike_work(self, work_id: str) -> dict[str, Any]:
        return self._account.request("POST", f"/game/api/v1/gameroom/work/{work_id}/unlike")

    def get_random_work(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/work/random")

    def get_random_feed(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/work/random-feed")

    def get_recently_created(self, page: int = 1) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/recent/created",
                                     params={"pageNo": page})

    def get_recently_played(self, page: int = 1) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/recent/played",
                                     params={"pageNo": page})

    def get_creative_list(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/creative/list",
                                     params={"pageNo": page, "pageSize": size})

    def get_creative_detail(self, creative_id: str) -> dict[str, Any]:
        return self._account.request("GET", f"/game/api/v1/gameroom/creative/{creative_id}")

    def get_room_permissions(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/gameroom/permissions")

    def assign_preview(self, work_id: str, preview_url: str) -> dict[str, Any]:
        return self._account.request("POST", f"/game/api/v1/gameroom/work/{work_id}/preview/assign",
                                     body={"previewUrl": preview_url})

    def set_room_password(self, room_id: str, password: str) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/room/password/set",
                                     body={"roomId": room_id, "password": password})

    def clear_room_password(self, room_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/room/password/clear",
                                     body={"roomId": room_id})

    def get_mining_room_list(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/mining/room/list",
                                     params={"pageNo": page, "pageSize": size})

    def get_running_mining_rooms(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/mining/room/running")

    def get_mining_record_summary(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/mining/record/summary")

    def get_mining_shop_info(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/mining/shop/info")

    def exchange_mining_currency(self, amount: int) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/mining/shop/currency/exchange",
                                     body={"amount": amount})

    def exchange_mining_token(self, amount: int) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/mining/shop/sub-token/exchange",
                                     body={"amount": amount})

    def purchase_mining_decoration(self, decoration_id: int) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/mining/shop/decoration/purchase",
                                     body={"decorationId": decoration_id})

    def refresh_mining_decoration(self) -> dict[str, Any]:
        return self._account.request("POST", "/game/api/v1/mining/shop/decoration/refresh")

    def get_pickaxe_balance(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/pickaxe/balance")

    def get_mining_token_balance(self) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v1/mining/token/balance")

    def game_auth_v2(self, game_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/game/api/v2/flow/game/auth",
                                     params={"gameId": game_id})

    async def async_list_games(self, page: int = 1, size: int = 20, order_type: str = "",
                                type_id: int = 0, order: str = "", is_publish: int = 1) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size, "isPublish": is_publish}
        if order_type:
            params["orderType"] = order_type
        if type_id:
            params["typeId"] = type_id
        if order:
            params["order"] = order
        return await self._account.async_request("GET", "/game/api/v1/games",
                                                 params=params, language="en_US")

    async def async_get_game_details(self, game_id: str, app_version: int = 0,
                                      engine_version: int = 0, ram: int = 0) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if app_version:
            params["appVersion"] = app_version
        return await self._account.async_request("GET", f"/game/api/v3/games/{game_id}",
                                                 params=params, language="en_US")

    async def async_get_game_ranking(self, game_id: str, period: str = "all", page: int = 1, size: int = 10) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/games/{game_id}/rank",
                                                 params={"type": period, "pageNo": page - 1, "pageSize": size})

    async def async_get_usage_ranking(self, game_id: str, page: int = 1, size: int = 10) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/games/{game_id}/uses/rank",
                                                 params={"pageNo": page, "pageSize": size})

    async def async_get_hot_games(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/game-list/homepage/hot")

    async def async_get_recommended_games(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v2/game-list/homepage/recommend")

    async def async_get_game_categories(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/game-list/category/list")

    async def async_get_games_by_category(self, category_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/game-list/by/category",
                                                 params={"categoryId": category_id, "pageNo": page, "pageSize": size})

    async def async_get_app_categories(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/app/categories")

    async def async_get_categories_by_language(self, language: str = "en_US") -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/category/list/by/language",
                                                 params={"language": language})

    async def async_get_game_config(self, game_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/games/config/app/{game_id}")

    async def async_get_game_mode_config(self, game_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/games/mode/config/app/{game_id}")

    async def async_get_resource_version(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/games/resource/version")

    async def async_search_games(self, keyword: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/game/info/search",
                                                 params={"keyword": keyword, "pageNo": page, "pageSize": size})

    async def async_get_update_tip(self, game_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/games/update/tip/info/app/{game_id}")

    async def async_get_update_list(self, user_id: int) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/games/update/list/{user_id}")

    async def async_get_warmup_info(self, game_id: str, language: str = "en_US") -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/games/warmup/{game_id}/languages/{language}")

    async def async_get_all_open_parties(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/games/all/open/party")

    async def async_get_team_members(self, team_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/games/team/member/{team_id}")

    async def async_get_turntable_info(self, game_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/game/{game_id}/turntable")

    async def async_claim_turntable(self, game_id: str) -> dict[str, Any]:
        return await self._account.async_request("PUT", f"/game/api/v1/game/{game_id}/turntable")

    async def async_get_praise_online_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/game/praise/online/info")

    async def async_update_engine(self, engine_version: str) -> dict[str, Any]:
        return await self._account.async_request("PUT", "/game/api/v1/games/engine",
                                                 body={"engineVersion": engine_version})

    async def async_like_game(self, game_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/games/like",
                                                 body={"gameId": game_id})

    async def async_post_comment(self, game_id: str, content: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/comment",
                                                 body={"gameId": game_id, "content": content})

    async def async_get_svip_game_list(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/vip-privilege-game/svip-game-list")

    async def async_get_vip_game_list(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/vip-privilege-game/vip-game-list")

    async def async_create_room(self, game_id: str, room_name: str = "", max_players: int = 0,
                                is_private: bool = False, password: str = "") -> dict[str, Any]:
        body: dict[str, Any] = {"gameId": game_id}
        if room_name:
            body["roomName"] = room_name
        if max_players:
            body["maxPlayers"] = max_players
        if is_private:
            body["isPrivate"] = True
        if password:
            body["password"] = password
        return await self._account.async_request("POST", "/game/api/v4/gameroom/create", body=body)

    async def async_list_rooms(self, game_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v2/gameroom/list",
                                                 params={"gameId": game_id, "pageNo": page, "pageSize": size})

    async def async_list_rooms_v4(self, game_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v4/gameroom/list",
                                                 params={"gameId": game_id, "pageNo": page, "pageSize": size})

    async def async_get_room_details(self, room_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/details",
                                                 params={"roomId": room_id})

    async def async_get_room_details_v3(self, room_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v3/gameroom/details",
                                                 params={"roomId": room_id})

    async def async_enter_room(self, room_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/enter",
                                                 params={"roomId": room_id})

    async def async_exit_room(self, room_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/exit",
                                                 params={"roomId": room_id})

    async def async_check_room(self, room_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/check",
                                                 params={"roomId": room_id})

    async def async_share_room(self, room_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/gameroom/share",
                                                 body={"roomId": room_id})

    async def async_enter_game(self, room_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/gameroom/enter-game",
                                                 body={"roomId": room_id})

    async def async_like_work(self, work_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", f"/game/api/v1/gameroom/work/{work_id}/like")

    async def async_unlike_work(self, work_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", f"/game/api/v1/gameroom/work/{work_id}/unlike")

    async def async_get_random_work(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/work/random")

    async def async_get_random_feed(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/work/random-feed")

    async def async_get_recently_created(self, page: int = 1) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/recent/created",
                                                 params={"pageNo": page})

    async def async_get_recently_played(self, page: int = 1) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/recent/played",
                                                 params={"pageNo": page})

    async def async_get_creative_list(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/creative/list",
                                                 params={"pageNo": page, "pageSize": size})

    async def async_get_creative_detail(self, creative_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/game/api/v1/gameroom/creative/{creative_id}")

    async def async_get_room_permissions(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/gameroom/permissions")

    async def async_assign_preview(self, work_id: str, preview_url: str) -> dict[str, Any]:
        return await self._account.async_request("POST", f"/game/api/v1/gameroom/work/{work_id}/preview/assign",
                                                 body={"previewUrl": preview_url})

    async def async_set_room_password(self, room_id: str, password: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/room/password/set",
                                                 body={"roomId": room_id, "password": password})

    async def async_clear_room_password(self, room_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/room/password/clear",
                                                 body={"roomId": room_id})

    async def async_get_mining_room_list(self, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/mining/room/list",
                                                 params={"pageNo": page, "pageSize": size})

    async def async_get_running_mining_rooms(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/mining/room/running")

    async def async_get_mining_record_summary(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/mining/record/summary")

    async def async_get_mining_shop_info(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/mining/shop/info")

    async def async_exchange_mining_currency(self, amount: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/mining/shop/currency/exchange",
                                                 body={"amount": amount})

    async def async_exchange_mining_token(self, amount: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/mining/shop/sub-token/exchange",
                                                 body={"amount": amount})

    async def async_purchase_mining_decoration(self, decoration_id: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/mining/shop/decoration/purchase",
                                                 body={"decorationId": decoration_id})

    async def async_refresh_mining_decoration(self) -> dict[str, Any]:
        return await self._account.async_request("POST", "/game/api/v1/mining/shop/decoration/refresh")

    async def async_get_pickaxe_balance(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/pickaxe/balance")

    async def async_get_mining_token_balance(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v1/mining/token/balance")

    async def async_game_auth_v2(self, game_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/game/api/v2/flow/game/auth",
                                                 params={"gameId": game_id})
