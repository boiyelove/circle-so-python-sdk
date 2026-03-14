"""Headless Auth API client."""

from __future__ import annotations

from typing import Any, Optional

from circle.http import AsyncTransport, SyncTransport
from circle.models.auth import HeadlessAuthToken, RefreshedAccessToken


class HeadlessAuthClient:
    """Sync client for Headless Auth endpoints."""

    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    def create_auth_token(
        self,
        *,
        sso_user_id: Optional[str] = None,
        community_member_id: Optional[int] = None,
        email: Optional[str] = None,
    ) -> HeadlessAuthToken:
        body: dict[str, Any] = {}
        if sso_user_id is not None:
            body["sso_user_id"] = sso_user_id
        elif community_member_id is not None:
            body["community_member_id"] = community_member_id
        elif email is not None:
            body["email"] = email
        data = self._t.request("POST", "/api/v1/headless/auth_token", json=body)
        return HeadlessAuthToken.model_validate(data)

    def refresh_access_token(self, refresh_token: str) -> RefreshedAccessToken:
        data = self._t.request("PATCH", "/api/v1/headless/access_token/refresh", json={"refresh_token": refresh_token})
        return RefreshedAccessToken.model_validate(data)

    def revoke_access_token(self, access_token: str) -> None:
        self._t.request("POST", "/api/v1/headless/access_token/revoke", json={"access_token": access_token})

    def revoke_refresh_token(self, refresh_token: str) -> None:
        self._t.request("POST", "/api/v1/headless/refresh_token/revoke", json={"refresh_token": refresh_token})


class AsyncHeadlessAuthClient:
    """Async client for Headless Auth endpoints."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def create_auth_token(
        self,
        *,
        sso_user_id: Optional[str] = None,
        community_member_id: Optional[int] = None,
        email: Optional[str] = None,
    ) -> HeadlessAuthToken:
        body: dict[str, Any] = {}
        if sso_user_id is not None:
            body["sso_user_id"] = sso_user_id
        elif community_member_id is not None:
            body["community_member_id"] = community_member_id
        elif email is not None:
            body["email"] = email
        data = await self._t.request("POST", "/api/v1/headless/auth_token", json=body)
        return HeadlessAuthToken.model_validate(data)

    async def refresh_access_token(self, refresh_token: str) -> RefreshedAccessToken:
        data = await self._t.request(
            "PATCH", "/api/v1/headless/access_token/refresh", json={"refresh_token": refresh_token}
        )
        return RefreshedAccessToken.model_validate(data)

    async def revoke_access_token(self, access_token: str) -> None:
        await self._t.request("POST", "/api/v1/headless/access_token/revoke", json={"access_token": access_token})

    async def revoke_refresh_token(self, refresh_token: str) -> None:
        await self._t.request("POST", "/api/v1/headless/refresh_token/revoke", json={"refresh_token": refresh_token})
