"""Headless Client API -- Spaces, Posts, Comments."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.constants import HEADLESS_V1_PREFIX as _P
from circle.http import AsyncTransport, SyncTransport
from circle.models.headless.spaces import (
    HeadlessSpace, HeadlessSpaceList, SpaceNotificationDetail, SpaceBookmarkList, HeadlessSpaceTopicList,
)
from circle.models.headless.posts import HeadlessPost, HeadlessPostList, HeadlessImagePost
from circle.models.headless.comments import HeadlessComment, HeadlessCommentList, UserLikeList


def _list_posts_params(page=1, per_page=10, sort=None, status=None, topics=None, **kw):
    p: Dict[str, Any] = {"page": page, "per_page": per_page, **kw}
    if sort: p["sort"] = sort
    if status: p["status"] = status
    if topics: p["topics"] = topics
    return p


def _comment_params(page=1, per_page=60, sort=None):
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if sort: p["sort"] = sort
    return p


def _home_params(page=1, per_page=10, sort=None):
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if sort: p["sort"] = sort
    return p


class HeadlessSpacesPostsClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    def list_spaces(self) -> List[HeadlessSpace]:
        return [HeadlessSpace.model_validate(s) for s in self._t.request("GET", f"{_P}/spaces")]

    def get_space(self, space_id: int) -> HeadlessSpace:
        return HeadlessSpace.model_validate(self._t.request("GET", f"{_P}/spaces/{space_id}"))

    def get_home_space(self) -> HeadlessSpace:
        return HeadlessSpace.model_validate(self._t.request("GET", f"{_P}/spaces/home"))

    def join_space(self, space_id: int) -> HeadlessSpace:
        return HeadlessSpace.model_validate(self._t.request("POST", f"{_P}/spaces/{space_id}/join"))

    def leave_space(self, space_id: int) -> HeadlessSpace:
        return HeadlessSpace.model_validate(self._t.request("POST", f"{_P}/spaces/{space_id}/leave"))

    def get_space_topics(self, space_id: int, *, page: int = 1, per_page: int = 10) -> HeadlessSpaceTopicList:
        return HeadlessSpaceTopicList.model_validate(
            self._t.request("GET", f"{_P}/spaces/{space_id}/topics", params={"page": page, "per_page": per_page}))

    def get_space_bookmarks(self, space_id: int, *, page: int = 1, per_page: int = 10) -> SpaceBookmarkList:
        return SpaceBookmarkList.model_validate(
            self._t.request("GET", f"{_P}/spaces/{space_id}/bookmarks", params={"page": page, "per_page": per_page}))

    def get_space_notification_details(self, *, space_ids: Optional[str] = None) -> List[SpaceNotificationDetail]:
        p: Dict[str, Any] = {}
        if space_ids: p["space_ids"] = space_ids
        return [SpaceNotificationDetail.model_validate(d) for d in
                self._t.request("GET", f"{_P}/space_notification_details", params=p)]

    def list_posts(self, space_id: int, **kw: Any) -> HeadlessPostList:
        return HeadlessPostList.model_validate(
            self._t.request("GET", f"{_P}/spaces/{space_id}/posts", params=_list_posts_params(**kw)))

    def create_post(self, space_id: int, **kw: Any) -> HeadlessPost:
        return HeadlessPost.model_validate(self._t.request("POST", f"{_P}/spaces/{space_id}/posts", json=kw))

    def get_post(self, space_id: int, post_id: int) -> HeadlessPost:
        return HeadlessPost.model_validate(self._t.request("GET", f"{_P}/spaces/{space_id}/posts/{post_id}"))

    def delete_post(self, space_id: int, post_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/spaces/{space_id}/posts/{post_id}")

    def create_image_post(self, space_id: int, **kw: Any) -> HeadlessImagePost:
        return HeadlessImagePost.model_validate(
            self._t.request("POST", f"{_P}/spaces/{space_id}/images/posts", json=kw))

    def update_image_post(self, space_id: int, post_id: int, **kw: Any) -> HeadlessImagePost:
        return HeadlessImagePost.model_validate(
            self._t.request("PUT", f"{_P}/spaces/{space_id}/images/posts/{post_id}", json=kw))

    def follow_post(self, post_id: int) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/posts/{post_id}/post_followers")

    def unfollow_post(self, post_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/posts/{post_id}/post_followers")

    def like_post(self, post_id: int) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/posts/{post_id}/user_likes")

    def unlike_post(self, post_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/posts/{post_id}/user_likes")

    def get_post_likes(self, post_id: int, *, page: int = 1, per_page: int = 10) -> UserLikeList:
        return UserLikeList.model_validate(
            self._t.request("GET", f"{_P}/posts/{post_id}/user_likes", params={"page": page, "per_page": per_page}))

    def get_home_posts(self, **kw: Any) -> HeadlessPostList:
        return HeadlessPostList.model_validate(self._t.request("GET", f"{_P}/home", params=_home_params(**kw)))

    def list_comments(self, post_id: int, **kw: Any) -> HeadlessCommentList:
        return HeadlessCommentList.model_validate(
            self._t.request("GET", f"{_P}/posts/{post_id}/comments", params=_comment_params(**kw)))

    def create_comment(self, post_id: int, **kw: Any) -> HeadlessComment:
        return HeadlessComment.model_validate(
            self._t.request("POST", f"{_P}/posts/{post_id}/comments", json={"comment": kw}))

    def get_comment(self, post_id: int, comment_id: int) -> HeadlessComment:
        return HeadlessComment.model_validate(
            self._t.request("GET", f"{_P}/posts/{post_id}/comments/{comment_id}"))

    def update_comment(self, post_id: int, comment_id: int, **kw: Any) -> HeadlessComment:
        return HeadlessComment.model_validate(
            self._t.request("PATCH", f"{_P}/posts/{post_id}/comments/{comment_id}", json={"comment": kw}))

    def delete_comment(self, post_id: int, comment_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/posts/{post_id}/comments/{comment_id}")

    def list_replies(self, comment_id: int, **kw: Any) -> HeadlessCommentList:
        return HeadlessCommentList.model_validate(
            self._t.request("GET", f"{_P}/comments/{comment_id}/replies", params=_comment_params(**kw)))

    def create_reply(self, comment_id: int, **kw: Any) -> HeadlessComment:
        return HeadlessComment.model_validate(
            self._t.request("POST", f"{_P}/comments/{comment_id}/replies", json={"comment": kw}))

    def get_reply(self, comment_id: int, reply_id: int) -> HeadlessComment:
        return HeadlessComment.model_validate(
            self._t.request("GET", f"{_P}/comments/{comment_id}/replies/{reply_id}"))

    def update_reply(self, comment_id: int, reply_id: int, **kw: Any) -> HeadlessComment:
        return HeadlessComment.model_validate(
            self._t.request("PATCH", f"{_P}/comments/{comment_id}/replies/{reply_id}", json={"comment": kw}))

    def delete_reply(self, comment_id: int, reply_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/comments/{comment_id}/replies/{reply_id}")

    def like_comment(self, comment_id: int) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/comments/{comment_id}/user_likes")

    def unlike_comment(self, comment_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/comments/{comment_id}/user_likes")

    def get_comment_likes(self, comment_id: int, *, page: int = 1, per_page: int = 10) -> UserLikeList:
        return UserLikeList.model_validate(
            self._t.request("GET", f"{_P}/comments/{comment_id}/user_likes",
                            params={"page": page, "per_page": per_page}))


class AsyncHeadlessSpacesPostsClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def list_spaces(self) -> List[HeadlessSpace]:
        return [HeadlessSpace.model_validate(s) for s in await self._t.request("GET", f"{_P}/spaces")]

    async def get_space(self, space_id: int) -> HeadlessSpace:
        return HeadlessSpace.model_validate(await self._t.request("GET", f"{_P}/spaces/{space_id}"))

    async def get_home_space(self) -> HeadlessSpace:
        return HeadlessSpace.model_validate(await self._t.request("GET", f"{_P}/spaces/home"))

    async def join_space(self, space_id: int) -> HeadlessSpace:
        return HeadlessSpace.model_validate(await self._t.request("POST", f"{_P}/spaces/{space_id}/join"))

    async def leave_space(self, space_id: int) -> HeadlessSpace:
        return HeadlessSpace.model_validate(await self._t.request("POST", f"{_P}/spaces/{space_id}/leave"))

    async def get_space_topics(self, space_id: int, *, page: int = 1, per_page: int = 10) -> HeadlessSpaceTopicList:
        return HeadlessSpaceTopicList.model_validate(
            await self._t.request("GET", f"{_P}/spaces/{space_id}/topics",
                                  params={"page": page, "per_page": per_page}))

    async def get_space_bookmarks(self, space_id: int, *, page: int = 1, per_page: int = 10) -> SpaceBookmarkList:
        return SpaceBookmarkList.model_validate(
            await self._t.request("GET", f"{_P}/spaces/{space_id}/bookmarks",
                                  params={"page": page, "per_page": per_page}))

    async def get_space_notification_details(self, *, space_ids: Optional[str] = None) -> List[SpaceNotificationDetail]:
        p: Dict[str, Any] = {}
        if space_ids: p["space_ids"] = space_ids
        return [SpaceNotificationDetail.model_validate(d) for d in
                await self._t.request("GET", f"{_P}/space_notification_details", params=p)]

    async def list_posts(self, space_id: int, **kw: Any) -> HeadlessPostList:
        return HeadlessPostList.model_validate(
            await self._t.request("GET", f"{_P}/spaces/{space_id}/posts", params=_list_posts_params(**kw)))

    async def create_post(self, space_id: int, **kw: Any) -> HeadlessPost:
        return HeadlessPost.model_validate(await self._t.request("POST", f"{_P}/spaces/{space_id}/posts", json=kw))

    async def get_post(self, space_id: int, post_id: int) -> HeadlessPost:
        return HeadlessPost.model_validate(await self._t.request("GET", f"{_P}/spaces/{space_id}/posts/{post_id}"))

    async def delete_post(self, space_id: int, post_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/spaces/{space_id}/posts/{post_id}")

    async def create_image_post(self, space_id: int, **kw: Any) -> HeadlessImagePost:
        return HeadlessImagePost.model_validate(
            await self._t.request("POST", f"{_P}/spaces/{space_id}/images/posts", json=kw))

    async def update_image_post(self, space_id: int, post_id: int, **kw: Any) -> HeadlessImagePost:
        return HeadlessImagePost.model_validate(
            await self._t.request("PUT", f"{_P}/spaces/{space_id}/images/posts/{post_id}", json=kw))

    async def follow_post(self, post_id: int) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/posts/{post_id}/post_followers")

    async def unfollow_post(self, post_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/posts/{post_id}/post_followers")

    async def like_post(self, post_id: int) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/posts/{post_id}/user_likes")

    async def unlike_post(self, post_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/posts/{post_id}/user_likes")

    async def get_post_likes(self, post_id: int, *, page: int = 1, per_page: int = 10) -> UserLikeList:
        return UserLikeList.model_validate(
            await self._t.request("GET", f"{_P}/posts/{post_id}/user_likes",
                                  params={"page": page, "per_page": per_page}))

    async def get_home_posts(self, **kw: Any) -> HeadlessPostList:
        return HeadlessPostList.model_validate(await self._t.request("GET", f"{_P}/home", params=_home_params(**kw)))

    async def list_comments(self, post_id: int, **kw: Any) -> HeadlessCommentList:
        return HeadlessCommentList.model_validate(
            await self._t.request("GET", f"{_P}/posts/{post_id}/comments", params=_comment_params(**kw)))

    async def create_comment(self, post_id: int, **kw: Any) -> HeadlessComment:
        return HeadlessComment.model_validate(
            await self._t.request("POST", f"{_P}/posts/{post_id}/comments", json={"comment": kw}))

    async def get_comment(self, post_id: int, comment_id: int) -> HeadlessComment:
        return HeadlessComment.model_validate(
            await self._t.request("GET", f"{_P}/posts/{post_id}/comments/{comment_id}"))

    async def update_comment(self, post_id: int, comment_id: int, **kw: Any) -> HeadlessComment:
        return HeadlessComment.model_validate(
            await self._t.request("PATCH", f"{_P}/posts/{post_id}/comments/{comment_id}", json={"comment": kw}))

    async def delete_comment(self, post_id: int, comment_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/posts/{post_id}/comments/{comment_id}")

    async def list_replies(self, comment_id: int, **kw: Any) -> HeadlessCommentList:
        return HeadlessCommentList.model_validate(
            await self._t.request("GET", f"{_P}/comments/{comment_id}/replies", params=_comment_params(**kw)))

    async def create_reply(self, comment_id: int, **kw: Any) -> HeadlessComment:
        return HeadlessComment.model_validate(
            await self._t.request("POST", f"{_P}/comments/{comment_id}/replies", json={"comment": kw}))

    async def get_reply(self, comment_id: int, reply_id: int) -> HeadlessComment:
        return HeadlessComment.model_validate(
            await self._t.request("GET", f"{_P}/comments/{comment_id}/replies/{reply_id}"))

    async def update_reply(self, comment_id: int, reply_id: int, **kw: Any) -> HeadlessComment:
        return HeadlessComment.model_validate(
            await self._t.request("PATCH", f"{_P}/comments/{comment_id}/replies/{reply_id}", json={"comment": kw}))

    async def delete_reply(self, comment_id: int, reply_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/comments/{comment_id}/replies/{reply_id}")

    async def like_comment(self, comment_id: int) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/comments/{comment_id}/user_likes")

    async def unlike_comment(self, comment_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/comments/{comment_id}/user_likes")

    async def get_comment_likes(self, comment_id: int, *, page: int = 1, per_page: int = 10) -> UserLikeList:
        return UserLikeList.model_validate(
            await self._t.request("GET", f"{_P}/comments/{comment_id}/user_likes",
                                  params={"page": page, "per_page": per_page}))
