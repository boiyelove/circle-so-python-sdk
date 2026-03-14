"""Tests for Headless Auth API client."""
import pytest
from circle.api.auth import HeadlessAuthClient, AsyncHeadlessAuthClient
from circle.models.auth import HeadlessAuthToken, RefreshedAccessToken
from tests.conftest import MockSyncTransport, MockAsyncTransport

AUTH_RESPONSE = {
    "access_token": "eyJ_access", "refresh_token": "ref_token",
    "access_token_expires_at": "2024-06-01T00:00:00Z",
    "refresh_token_expires_at": "2024-07-01T00:00:00Z",
    "community_member_id": 1, "community_id": 2,
}
REFRESH_RESPONSE = {"access_token": "eyJ_new", "access_token_expires_at": "2024-06-02T00:00:00Z"}


class TestHeadlessAuthClient:
    def _client(self, responses=None):
        return HeadlessAuthClient(MockSyncTransport(responses or {}))

    def test_create_auth_token_by_email(self):
        c = self._client({("POST", "/api/v1/headless/auth_token"): AUTH_RESPONSE})
        token = c.create_auth_token(email="user@example.com")
        assert isinstance(token, HeadlessAuthToken)
        assert token.access_token == "eyJ_access"
        assert token.community_member_id == 1

    def test_create_auth_token_by_sso(self):
        c = self._client({("POST", "/api/v1/headless/auth_token"): AUTH_RESPONSE})
        token = c.create_auth_token(sso_user_id="sso123")
        assert token.refresh_token == "ref_token"

    def test_create_auth_token_by_member_id(self):
        c = self._client({("POST", "/api/v1/headless/auth_token"): AUTH_RESPONSE})
        token = c.create_auth_token(community_member_id=42)
        assert token.community_id == 2

    def test_refresh_access_token(self):
        c = self._client({("PATCH", "/api/v1/headless/access_token/refresh"): REFRESH_RESPONSE})
        result = c.refresh_access_token("ref_token")
        assert isinstance(result, RefreshedAccessToken)
        assert result.access_token == "eyJ_new"

    def test_revoke_access_token(self):
        t = MockSyncTransport({("POST", "/api/v1/headless/access_token/revoke"): None})
        c = HeadlessAuthClient(t)
        c.revoke_access_token("token123")
        assert len(t._calls) == 1
        assert t._calls[0][0] == "POST"

    def test_revoke_refresh_token(self):
        t = MockSyncTransport({("POST", "/api/v1/headless/refresh_token/revoke"): None})
        c = HeadlessAuthClient(t)
        c.revoke_refresh_token("ref123")
        assert t._calls[0][2]["json"] == {"refresh_token": "ref123"}


@pytest.mark.asyncio
class TestAsyncHeadlessAuthClient:
    def _client(self, responses=None):
        return AsyncHeadlessAuthClient(MockAsyncTransport(responses or {}))

    async def test_create_auth_token(self):
        c = self._client({("POST", "/api/v1/headless/auth_token"): AUTH_RESPONSE})
        token = await c.create_auth_token(email="user@example.com")
        assert isinstance(token, HeadlessAuthToken)
        assert token.access_token == "eyJ_access"

    async def test_refresh_access_token(self):
        c = self._client({("PATCH", "/api/v1/headless/access_token/refresh"): REFRESH_RESPONSE})
        result = await c.refresh_access_token("ref")
        assert result.access_token == "eyJ_new"
