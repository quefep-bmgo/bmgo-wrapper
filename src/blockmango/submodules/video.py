from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..account import BmgAccount
else:
    BmgAccount = Any


class VideoAPI:
    __slots__ = ("_account",)

    def __init__(self, account: BmgAccount):
        self._account = account

    def list_videos(self, type_: str, page: int = 1, size: int = 20, tags: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size}
        if tags:
            params["tag"] = tags
        return self._account.request("GET", f"/video/api/v1/app/video/list/{type_}",
                                     params=params, language="en_US")

    def get_video_details(self, video_id: str) -> dict[str, Any]:
        return self._account.request("GET", f"/video/api/v1/videos/{video_id}")

    def like_video(self, video_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/video/api/v1/videos/like", body={"videoId": video_id})

    def share_video(self, video_id: str) -> dict[str, Any]:
        return self._account.request("POST", "/video/api/v1/videos/share", body={"videoId": video_id})

    def get_video_feed(self, page: int = 1, size: int = 20, author_id: int = 0,
                       video_id: int = 0, tags: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size, "authorId": author_id, "videoId": video_id}
        if tags:
            params["tag"] = tags
        return self._account.request("GET", "/video/api/v1/app/video/more/list",
                                     params=params, language="en_US")

    def get_user_videos(self, user_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", f"/video/api/v1/videos/user/{user_id}",
                                     params={"pageNo": page, "pageSize": size})

    def comment_video(self, video_id: str, content: str) -> dict[str, Any]:
        return self._account.request("POST", "/video/api/v1/videos/comment",
                                     body={"videoId": video_id, "content": content})

    def get_video_comments(self, video_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return self._account.request("GET", "/video/api/v1/videos/comments",
                                     params={"videoId": video_id, "pageNo": page, "pageSize": size})

    def get_banner_config(self) -> dict[str, Any]:
        return self._account.request("GET", "/video/api/v1/app/video/banner/config")

    def get_video_detail_info(self, video_id: str) -> dict[str, Any]:
        return self._account.request("GET", "/video/api/v1/app/video/detail/info",
                                     params={"videoId": video_id}, language="en_US")

    def get_video_list_by_type(self, type_: str, page: int = 1, size: int = 20, tags: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size}
        if tags:
            params["tag"] = tags
        return self._account.request("GET", f"/video/api/v1/app/video/list/{type_}",
                                     params=params, language="en_US")

    def get_more_videos(self, page: int = 1, size: int = 20, author_id: int = 0,
                         video_id: int = 0, tags: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size, "authorId": author_id, "videoId": video_id}
        if tags:
            params["tag"] = tags
        return self._account.request("GET", "/video/api/v1/app/video/more/list",
                                     params=params, language="en_US")

    def get_video_tags(self) -> dict[str, Any]:
        return self._account.request("GET", "/video/api/v1/app/video/tag/list", language="en_US")

    def praise_video(self, video_id: str) -> dict[str, Any]:
        return self._account.request("POST", f"/video/api/v1/app/video/praise/{video_id}")

    def dislike_video(self, video_id: str) -> dict[str, Any]:
        return self._account.request("POST", f"/video/api/v1/app/video/dislike/{video_id}")

    def report_play_amount(self, video_id: str, duration: int) -> dict[str, Any]:
        return self._account.request("POST", "/video/api/v1/app/video/report/play/amount",
                                     body={"videoId": video_id, "duration": duration})

    async def async_list_videos(self, type_: str, page: int = 1, size: int = 20, tags: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size}
        if tags:
            params["tag"] = tags
        return await self._account.async_request("GET", f"/video/api/v1/app/video/list/{type_}",
                                                 params=params, language="en_US")

    async def async_get_video_details(self, video_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/video/api/v1/videos/{video_id}")

    async def async_like_video(self, video_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/video/api/v1/videos/like", body={"videoId": video_id})

    async def async_share_video(self, video_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/video/api/v1/videos/share", body={"videoId": video_id})

    async def async_get_video_feed(self, page: int = 1, size: int = 20, author_id: int = 0,
                                    video_id: int = 0, tags: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size, "authorId": author_id, "videoId": video_id}
        if tags:
            params["tag"] = tags
        return await self._account.async_request("GET", "/video/api/v1/app/video/more/list",
                                                 params=params, language="en_US")

    async def async_get_user_videos(self, user_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", f"/video/api/v1/videos/user/{user_id}",
                                                 params={"pageNo": page, "pageSize": size})

    async def async_comment_video(self, video_id: str, content: str) -> dict[str, Any]:
        return await self._account.async_request("POST", "/video/api/v1/videos/comment",
                                                 body={"videoId": video_id, "content": content})

    async def async_get_video_comments(self, video_id: str, page: int = 1, size: int = 20) -> dict[str, Any]:
        return await self._account.async_request("GET", "/video/api/v1/videos/comments",
                                                 params={"videoId": video_id, "pageNo": page, "pageSize": size})

    async def async_get_banner_config(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/video/api/v1/app/video/banner/config")

    async def async_get_video_detail_info(self, video_id: str) -> dict[str, Any]:
        return await self._account.async_request("GET", "/video/api/v1/app/video/detail/info",
                                                 params={"videoId": video_id}, language="en_US")

    async def async_get_video_list_by_type(self, type_: str, page: int = 1, size: int = 20, tags: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size}
        if tags:
            params["tag"] = tags
        return await self._account.async_request("GET", f"/video/api/v1/app/video/list/{type_}",
                                                 params=params, language="en_US")

    async def async_get_more_videos(self, page: int = 1, size: int = 20, author_id: int = 0,
                                     video_id: int = 0, tags: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageNo": page, "pageSize": size, "authorId": author_id, "videoId": video_id}
        if tags:
            params["tag"] = tags
        return await self._account.async_request("GET", "/video/api/v1/app/video/more/list",
                                                 params=params, language="en_US")

    async def async_get_video_tags(self) -> dict[str, Any]:
        return await self._account.async_request("GET", "/video/api/v1/app/video/tag/list", language="en_US")

    async def async_praise_video(self, video_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", f"/video/api/v1/app/video/praise/{video_id}")

    async def async_dislike_video(self, video_id: str) -> dict[str, Any]:
        return await self._account.async_request("POST", f"/video/api/v1/app/video/dislike/{video_id}")

    async def async_report_play_amount(self, video_id: str, duration: int) -> dict[str, Any]:
        return await self._account.async_request("POST", "/video/api/v1/app/video/report/play/amount",
                                                 body={"videoId": video_id, "duration": duration})
