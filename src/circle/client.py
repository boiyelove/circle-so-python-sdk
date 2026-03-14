"""Stub top-level client -- will be completed in task 17."""

from __future__ import annotations

from typing import Optional

from circle.http import DEFAULT_BASE_URL, AsyncTransport, SyncTransport
from circle.api.auth import AsyncHeadlessAuthClient, HeadlessAuthClient


class CircleClient:
    """Synchronous Circle SDK client."""

    def __init__(
        self,
        api_token: str,
        base_url: str = DEFAULT_BASE_URL,
        community_url: Optional[str] = None,
    ) -> None:
        self._base_url = (community_url or base_url).rstrip("/")
        self._admin_transport = SyncTransport(
            api_token=api_token, base_url=self._base_url, auth_scheme="Token"
        )
        self._auth_transport = SyncTransport(
            api_token=api_token, base_url=self._base_url, auth_scheme="Bearer"
        )
        self.auth = HeadlessAuthClient(self._auth_transport)

    def close(self) -> None:
        self._admin_transport.close()
        self._auth_transport.close()

    def __enter__(self) -> CircleClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncCircleClient:
    """Asynchronous Circle SDK client."""

    def __init__(
        self,
        api_token: str,
        base_url: str = DEFAULT_BASE_URL,
        community_url: Optional[str] = None,
    ) -> None:
        self._base_url = (community_url or base_url).rstrip("/")
        self._admin_transport = AsyncTransport(
            api_token=api_token, base_url=self._base_url, auth_scheme="Token"
        )
        self._auth_transport = AsyncTransport(
            api_token=api_token, base_url=self._base_url, auth_scheme="Bearer"
        )
        self.auth = AsyncHeadlessAuthClient(self._auth_transport)

    async def close(self) -> None:
        await self._admin_transport.close()
        await self._auth_transport.close()

    async def __aenter__(self) -> AsyncCircleClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
