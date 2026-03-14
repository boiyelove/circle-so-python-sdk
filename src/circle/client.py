"""Top-level CircleClient and AsyncCircleClient facade."""
from __future__ import annotations
from typing import Optional

from circle.http import DEFAULT_BASE_URL, AsyncTransport, SyncTransport
from circle.api.auth import AsyncHeadlessAuthClient, HeadlessAuthClient
from circle.api.admin_access_groups import AccessGroupsClient, AsyncAccessGroupsClient
from circle.api.admin_community import CommunityClient, AsyncCommunityClient
from circle.api.admin_spaces import SpacesClient, AsyncSpacesClient
from circle.api.admin_posts import PostsClient, AsyncPostsClient
from circle.api.admin_events import EventsClient, AsyncEventsClient
from circle.api.admin_courses import CoursesClient, AsyncCoursesClient
from circle.api.admin_tags import TagsClient, AsyncTagsClient
from circle.api.admin_misc import AdminMiscClient, AsyncAdminMiscClient
from circle.api.headless_spaces_posts import HeadlessSpacesPostsClient, AsyncHeadlessSpacesPostsClient
from circle.api.headless_chat_notif_members import HeadlessChatNotifMembersClient, AsyncHeadlessChatNotifMembersClient
from circle.api.headless_misc import HeadlessMiscClient, AsyncHeadlessMiscClient


class _AdminNamespace:
    """Groups all Admin API V2 sub-clients under client.admin.*"""
    def __init__(self, transport: SyncTransport) -> None:
        self.access_groups = AccessGroupsClient(transport)
        self.community = CommunityClient(transport)
        self.spaces = SpacesClient(transport)
        self.posts = PostsClient(transport)
        self.events = EventsClient(transport)
        self.courses = CoursesClient(transport)
        self.tags = TagsClient(transport)
        self.misc = AdminMiscClient(transport)

    # Convenience delegates to community sub-client
    def get_community(self, **kw):
        return self.community.get_community(**kw)

    def list_community_members(self, **kw):
        return self.community.list_community_members(**kw)


class _AsyncAdminNamespace:
    def __init__(self, transport: AsyncTransport) -> None:
        self.access_groups = AsyncAccessGroupsClient(transport)
        self.community = AsyncCommunityClient(transport)
        self.spaces = AsyncSpacesClient(transport)
        self.posts = AsyncPostsClient(transport)
        self.events = AsyncEventsClient(transport)
        self.courses = AsyncCoursesClient(transport)
        self.tags = AsyncTagsClient(transport)
        self.misc = AsyncAdminMiscClient(transport)

    async def get_community(self, **kw):
        return await self.community.get_community(**kw)

    async def list_community_members(self, **kw):
        return await self.community.list_community_members(**kw)


class _HeadlessNamespace:
    """Groups all Headless Client V1 sub-clients under client.headless.*"""
    def __init__(self, transport: SyncTransport) -> None:
        self.spaces_posts = HeadlessSpacesPostsClient(transport)
        self.chat_notif_members = HeadlessChatNotifMembersClient(transport)
        self.misc = HeadlessMiscClient(transport)

    # Convenience delegates
    def list_spaces(self, **kw):
        return self.spaces_posts.list_spaces(**kw)

    def list_posts(self, space_id, **kw):
        return self.spaces_posts.list_posts(space_id, **kw)


class _AsyncHeadlessNamespace:
    def __init__(self, transport: AsyncTransport) -> None:
        self.spaces_posts = AsyncHeadlessSpacesPostsClient(transport)
        self.chat_notif_members = AsyncHeadlessChatNotifMembersClient(transport)
        self.misc = AsyncHeadlessMiscClient(transport)

    async def list_spaces(self, **kw):
        return await self.spaces_posts.list_spaces(**kw)

    async def list_posts(self, space_id, **kw):
        return await self.spaces_posts.list_posts(space_id, **kw)


class CircleClient:
    """Synchronous Circle SDK client composing all three APIs."""

    def __init__(
        self,
        api_token: str,
        base_url: str = DEFAULT_BASE_URL,
        community_url: Optional[str] = None,
    ) -> None:
        url = (community_url or base_url).rstrip("/")
        self._admin_transport = SyncTransport(api_token=api_token, base_url=url, auth_scheme="Token")
        self._bearer_transport = SyncTransport(api_token=api_token, base_url=url, auth_scheme="Bearer")
        self.auth = HeadlessAuthClient(self._bearer_transport)
        self.admin = _AdminNamespace(self._admin_transport)
        self.headless = _HeadlessNamespace(self._bearer_transport)

    def close(self) -> None:
        self._admin_transport.close()
        self._bearer_transport.close()

    def __enter__(self) -> CircleClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncCircleClient:
    """Asynchronous Circle SDK client composing all three APIs."""

    def __init__(
        self,
        api_token: str,
        base_url: str = DEFAULT_BASE_URL,
        community_url: Optional[str] = None,
    ) -> None:
        url = (community_url or base_url).rstrip("/")
        self._admin_transport = AsyncTransport(api_token=api_token, base_url=url, auth_scheme="Token")
        self._bearer_transport = AsyncTransport(api_token=api_token, base_url=url, auth_scheme="Bearer")
        self.auth = AsyncHeadlessAuthClient(self._bearer_transport)
        self.admin = _AsyncAdminNamespace(self._admin_transport)
        self.headless = _AsyncHeadlessNamespace(self._bearer_transport)

    async def close(self) -> None:
        await self._admin_transport.close()
        await self._bearer_transport.close()

    async def __aenter__(self) -> AsyncCircleClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
