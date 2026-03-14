"""Admin API -- Posts, Comments, Topics."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.http import AsyncTransport, SyncTransport
from circle.models.admin.posts import (
    BasicPost, PostList, BasicPostCreatedResponse, BasicPostUpdatedResponse, BasicPostDeletedResponse,
    ImagePost, ImagePostCreatedResponse, AISummary, Comment, CommentList, Topic, TopicList,
)

_P = "/api/admin/v2"


class PostsClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    # -- Posts --
    def list_posts(self, *, page: int = 1, per_page: int = 60, space_id: Optional[int] = None,
                   space_group_id: Optional[int] = None, status: Optional[str] = None,
                   search_text: Optional[str] = None, sort: Optional[str] = None) -> PostList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if space_id: p["space_id"] = space_id
        if space_group_id: p["space_group_id"] = space_group_id
        if status: p["status"] = status
        if search_text: p["search_text"] = search_text
        if sort: p["sort"] = sort
        return PostList.model_validate(self._t.request("GET", f"{_P}/posts", params=p))

    def create_post(self, *, space_id: int, name: str, **kwargs: Any) -> BasicPostCreatedResponse:
        return BasicPostCreatedResponse.model_validate(
            self._t.request("POST", f"{_P}/posts", json={"space_id": space_id, "name": name, **kwargs}))

    def show_post(self, post_id: int) -> BasicPost:
        return BasicPost.model_validate(self._t.request("GET", f"{_P}/posts/{post_id}"))

    def update_post(self, post_id: int, **kwargs: Any) -> BasicPostUpdatedResponse:
        return BasicPostUpdatedResponse.model_validate(
            self._t.request("PUT", f"{_P}/posts/{post_id}", json=kwargs))

    def delete_post(self, post_id: int) -> BasicPostDeletedResponse:
        return BasicPostDeletedResponse.model_validate(self._t.request("DELETE", f"{_P}/posts/{post_id}"))

    def get_post_summary(self, post_id: int) -> AISummary:
        return AISummary.model_validate(self._t.request("GET", f"{_P}/posts/{post_id}/summary"))

    # -- Image Posts --
    def create_image_post(self, space_id: int, **kwargs: Any) -> ImagePostCreatedResponse:
        return ImagePostCreatedResponse.model_validate(
            self._t.request("POST", f"{_P}/spaces/{space_id}/images/posts", json=kwargs))

    def delete_image_post(self, space_id: int, post_id: int) -> BasicPostDeletedResponse:
        return BasicPostDeletedResponse.model_validate(
            self._t.request("DELETE", f"{_P}/spaces/{space_id}/images/posts/{post_id}"))

    def duplicate_image_post(self, space_id: int, post_id: int, **kwargs: Any) -> ImagePostCreatedResponse:
        return ImagePostCreatedResponse.model_validate(
            self._t.request("POST", f"{_P}/spaces/{space_id}/images/posts/{post_id}/duplicate", json=kwargs))

    # -- Post Followers --
    def unfollow_post(self, post_id: int, *, community_member_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/posts/{post_id}/post_followers",
                               params={"community_member_id": community_member_id})

    # -- Comments --
    def list_comments(self, *, page: int = 1, per_page: int = 10, space_id: Optional[int] = None,
                      post_id: Optional[int] = None, search_text: Optional[str] = None) -> CommentList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if space_id: p["space_id"] = space_id
        if post_id: p["post_id"] = post_id
        if search_text: p["search_text"] = search_text
        return CommentList.model_validate(self._t.request("GET", f"{_P}/comments", params=p))

    def create_comment(self, *, body: str, post_id: int, **kwargs: Any) -> Comment:
        return Comment.model_validate(
            self._t.request("POST", f"{_P}/comments", json={"body": body, "post_id": post_id, **kwargs}))

    def show_comment(self, comment_id: int) -> Comment:
        return Comment.model_validate(self._t.request("GET", f"{_P}/comments/{comment_id}"))

    def delete_comment(self, comment_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/comments/{comment_id}")

    # -- Topics --
    def list_topics(self, *, page: int = 1, per_page: int = 10, name: Optional[str] = None,
                    sort: Optional[str] = None) -> TopicList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if name: p["name"] = name
        if sort: p["sort"] = sort
        return TopicList.model_validate(self._t.request("GET", f"{_P}/topics", params=p))

    def create_topic(self, *, name: str, **kwargs: Any) -> Topic:
        return Topic.model_validate(self._t.request("POST", f"{_P}/topics", json={"name": name, **kwargs}))

    def show_topic(self, topic_id: int) -> Topic:
        return Topic.model_validate(self._t.request("GET", f"{_P}/topics/{topic_id}"))

    def update_topic(self, topic_id: int, **kwargs: Any) -> Topic:
        return Topic.model_validate(self._t.request("PUT", f"{_P}/topics/{topic_id}", json=kwargs))

    def delete_topic(self, topic_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/topics/{topic_id}")


class AsyncPostsClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def list_posts(self, *, page: int = 1, per_page: int = 60, space_id: Optional[int] = None,
                         space_group_id: Optional[int] = None, status: Optional[str] = None,
                         search_text: Optional[str] = None, sort: Optional[str] = None) -> PostList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if space_id: p["space_id"] = space_id
        if space_group_id: p["space_group_id"] = space_group_id
        if status: p["status"] = status
        if search_text: p["search_text"] = search_text
        if sort: p["sort"] = sort
        return PostList.model_validate(await self._t.request("GET", f"{_P}/posts", params=p))

    async def create_post(self, *, space_id: int, name: str, **kwargs: Any) -> BasicPostCreatedResponse:
        return BasicPostCreatedResponse.model_validate(
            await self._t.request("POST", f"{_P}/posts", json={"space_id": space_id, "name": name, **kwargs}))

    async def show_post(self, post_id: int) -> BasicPost:
        return BasicPost.model_validate(await self._t.request("GET", f"{_P}/posts/{post_id}"))

    async def update_post(self, post_id: int, **kwargs: Any) -> BasicPostUpdatedResponse:
        return BasicPostUpdatedResponse.model_validate(
            await self._t.request("PUT", f"{_P}/posts/{post_id}", json=kwargs))

    async def delete_post(self, post_id: int) -> BasicPostDeletedResponse:
        return BasicPostDeletedResponse.model_validate(await self._t.request("DELETE", f"{_P}/posts/{post_id}"))

    async def get_post_summary(self, post_id: int) -> AISummary:
        return AISummary.model_validate(await self._t.request("GET", f"{_P}/posts/{post_id}/summary"))

    async def create_image_post(self, space_id: int, **kwargs: Any) -> ImagePostCreatedResponse:
        return ImagePostCreatedResponse.model_validate(
            await self._t.request("POST", f"{_P}/spaces/{space_id}/images/posts", json=kwargs))

    async def delete_image_post(self, space_id: int, post_id: int) -> BasicPostDeletedResponse:
        return BasicPostDeletedResponse.model_validate(
            await self._t.request("DELETE", f"{_P}/spaces/{space_id}/images/posts/{post_id}"))

    async def duplicate_image_post(self, space_id: int, post_id: int, **kwargs: Any) -> ImagePostCreatedResponse:
        return ImagePostCreatedResponse.model_validate(
            await self._t.request("POST", f"{_P}/spaces/{space_id}/images/posts/{post_id}/duplicate", json=kwargs))

    async def unfollow_post(self, post_id: int, *, community_member_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/posts/{post_id}/post_followers",
                                     params={"community_member_id": community_member_id})

    async def list_comments(self, *, page: int = 1, per_page: int = 10, space_id: Optional[int] = None,
                            post_id: Optional[int] = None, search_text: Optional[str] = None) -> CommentList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if space_id: p["space_id"] = space_id
        if post_id: p["post_id"] = post_id
        if search_text: p["search_text"] = search_text
        return CommentList.model_validate(await self._t.request("GET", f"{_P}/comments", params=p))

    async def create_comment(self, *, body: str, post_id: int, **kwargs: Any) -> Comment:
        return Comment.model_validate(
            await self._t.request("POST", f"{_P}/comments", json={"body": body, "post_id": post_id, **kwargs}))

    async def show_comment(self, comment_id: int) -> Comment:
        return Comment.model_validate(await self._t.request("GET", f"{_P}/comments/{comment_id}"))

    async def delete_comment(self, comment_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/comments/{comment_id}")

    async def list_topics(self, *, page: int = 1, per_page: int = 10, name: Optional[str] = None,
                          sort: Optional[str] = None) -> TopicList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if name: p["name"] = name
        if sort: p["sort"] = sort
        return TopicList.model_validate(await self._t.request("GET", f"{_P}/topics", params=p))

    async def create_topic(self, *, name: str, **kwargs: Any) -> Topic:
        return Topic.model_validate(await self._t.request("POST", f"{_P}/topics", json={"name": name, **kwargs}))

    async def show_topic(self, topic_id: int) -> Topic:
        return Topic.model_validate(await self._t.request("GET", f"{_P}/topics/{topic_id}"))

    async def update_topic(self, topic_id: int, **kwargs: Any) -> Topic:
        return Topic.model_validate(await self._t.request("PUT", f"{_P}/topics/{topic_id}", json=kwargs))

    async def delete_topic(self, topic_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/topics/{topic_id}")
