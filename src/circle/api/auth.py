"""Headless Auth API client."""
from __future__ import annotations
from typing import Any, Dict, Optional
from circle.constants import HEADLESS_AUTH_PREFIX as _P
from circle.http import AsyncTransport, SyncTransport
from circle.models.auth import HeadlessAuthToken, RefreshedAccessToken


def _auth_body(sso_user_id=None, community_member_id=None, email=None):
    body: Dict[str, Any] = {}
    if sso_user_id is not None:
        body["sso_user_id"] = sso_user_id
    elif community_member_id is not None:
        body["community_member_id"] = community_member_id
    elif email is not None:
        body["email"] = email
    return body


class HeadlessAuthClient:
    """Sync client for Headless Auth endpoints."""

    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    def create_auth_token(self, *, sso_user_id: Optional[str] = None,
                          community_member_id: Optional[int] = None,
                          email: Optional[str] = None) -> HeadlessAuthToken:
        return HeadlessAuthToken.model_validate(
            self._t.request("POST", f"{_P}/auth_token", json=_auth_body(sso_user_id, community_member_id, email)))

    def refresh_access_token(self, refresh_token: str) -> RefreshedAccessToken:
        return RefreshedAccessToken.model_validate(
            self._t.request("PATCH", f"{_P}/access_token/refresh", json={"refresh_token": refresh_token}))

    def revoke_access_token(self, access_token: str) -> None:
        self._t.request("POST", f"{_P}/access_token/revoke", json={"access_token": access_token})

    def revoke_refresh_token(self, refresh_token: str) -> None:
        self._t.request("POST", f"{_P}/refresh_token/revoke", json={"refresh_token": refresh_token})


class AsyncHeadlessAuthClient:
    """Async client for Headless Auth endpoints."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def create_auth_token(self, *, sso_user_id: Optional[str] = None,
                                community_member_id: Optional[int] = None,
                                email: Optional[str] = None) -> HeadlessAuthToken:
        return HeadlessAuthToken.model_validate(
            await self._t.request("POST", f"{_P}/auth_token", json=_auth_body(sso_user_id, community_member_id, email)))

    async def refresh_access_token(self, refresh_token: str) -> RefreshedAccessToken:
        return RefreshedAccessToken.model_validate(
            await self._t.request("PATCH", f"{_P}/access_token/refresh", json={"refresh_token": refresh_token}))

    async def revoke_access_token(self, access_token: str) -> None:
        await self._t.request("POST", f"{_P}/access_token/revoke", json={"access_token": access_token})

    async def revoke_refresh_token(self, refresh_token: str) -> None:
        await self._t.request("POST", f"{_P}/refresh_token/revoke", json={"refresh_token": refresh_token})
