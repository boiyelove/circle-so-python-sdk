"""Top-level CircleClient and AsyncCircleClient facade."""
from __future__ import annotations
import os
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
    """Synchronous Circle SDK client composing all three APIs.

    Provides access to the Headless Auth, Admin V2, and Headless Client V1
    APIs through the ``auth``, ``admin``, and ``headless`` namespaces.

    Args:
        api_token: Circle API token. Falls back to the ``CIRCLE_API_TOKEN``
            environment variable if not provided.
        base_url: Base URL for the Circle API. Falls back to the
            ``CIRCLE_BASE_URL`` environment variable, then the default
            ``https://app.circle.so``.
        community_url: Optional community-specific URL. Falls back to the
            ``CIRCLE_COMMUNITY_URL`` environment variable.
        rate_limit: Optional requests-per-second limit. When set, the client
            proactively throttles to avoid 429 responses.

    Raises:
        ValueError: If no api_token is provided and ``CIRCLE_API_TOKEN`` is
            not set.

    Examples:
        >>> client = CircleClient(api_token="YOUR_TOKEN")
        >>> community = client.admin.get_community()

        >>> # Using environment variables (CIRCLE_API_TOKEN must be set)
        >>> client = CircleClient()

        >>> # With rate limiting
        >>> client = CircleClient(api_token="YOUR_TOKEN", rate_limit=10)
    """

    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        community_url: Optional[str] = None,
        rate_limit: Optional[float] = None,
    ) -> None:
        token = api_token or os.environ.get("CIRCLE_API_TOKEN")
        if not token:
            raise ValueError(
                "api_token is required. Pass it directly or set the CIRCLE_API_TOKEN environment variable."
            )
        resolved_base = base_url or os.environ.get("CIRCLE_BASE_URL", DEFAULT_BASE_URL)
        resolved_community = community_url or os.environ.get("CIRCLE_COMMUNITY_URL")
        url = (resolved_community or resolved_base).rstrip("/")
        self._admin_transport = SyncTransport(api_token=token, base_url=url, auth_scheme="Token", rate_limit=rate_limit)
        self._bearer_transport = SyncTransport(api_token=token, base_url=url, auth_scheme="Bearer", rate_limit=rate_limit)
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
    """Asynchronous Circle SDK client composing all three APIs.

    Args:
        api_token: Circle API token. Falls back to ``CIRCLE_API_TOKEN`` env var.
        base_url: Base URL. Falls back to ``CIRCLE_BASE_URL`` env var.
        community_url: Community URL. Falls back to ``CIRCLE_COMMUNITY_URL`` env var.
        rate_limit: Optional requests-per-second limit.

    Raises:
        ValueError: If no api_token is provided and ``CIRCLE_API_TOKEN`` is not set.

    Examples:
        >>> async with AsyncCircleClient(api_token="YOUR_TOKEN") as client:
        ...     members = await client.admin.list_community_members()
    """

    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        community_url: Optional[str] = None,
        rate_limit: Optional[float] = None,
    ) -> None:
        token = api_token or os.environ.get("CIRCLE_API_TOKEN")
        if not token:
            raise ValueError(
                "api_token is required. Pass it directly or set the CIRCLE_API_TOKEN environment variable."
            )
        resolved_base = base_url or os.environ.get("CIRCLE_BASE_URL", DEFAULT_BASE_URL)
        resolved_community = community_url or os.environ.get("CIRCLE_COMMUNITY_URL")
        url = (resolved_community or resolved_base).rstrip("/")
        self._admin_transport = AsyncTransport(api_token=token, base_url=url, auth_scheme="Token", rate_limit=rate_limit)
        self._bearer_transport = AsyncTransport(api_token=token, base_url=url, auth_scheme="Bearer", rate_limit=rate_limit)
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
