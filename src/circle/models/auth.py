"""Headless Auth API models."""

from __future__ import annotations

from typing import Optional

from circle.models.base import CircleModel


class HeadlessAuthToken(CircleModel):
    access_token: str
    refresh_token: str
    access_token_expires_at: str
    refresh_token_expires_at: str
    community_member_id: int
    community_id: int


class RefreshedAccessToken(CircleModel):
    access_token: str
    access_token_expires_at: str
