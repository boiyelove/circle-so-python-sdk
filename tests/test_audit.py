"""Tests for audit remediation: logging, User-Agent, retry control, constants."""
import logging
import pytest
from unittest.mock import MagicMock, patch
import httpx
from circle.http import SyncTransport, USER_AGENT, _parse_error
from circle.constants import ADMIN_V2_PREFIX, HEADLESS_V1_PREFIX, HEADLESS_AUTH_PREFIX
from circle.exceptions import CircleAPIError


class TestUserAgent:
    def test_user_agent_in_headers(self):
        t = SyncTransport(api_token="test", base_url="https://example.com")
        headers = t._build_headers()
        assert headers["User-Agent"] == USER_AGENT
        assert "circle-python-sdk/" in USER_AGENT
        assert "python/" in USER_AGENT

    def test_user_agent_format(self):
        import platform
        assert f"python/{platform.python_version()}" in USER_AGENT


class TestConstants:
    def test_admin_prefix(self):
        assert ADMIN_V2_PREFIX == "/api/admin/v2"

    def test_headless_prefix(self):
        assert HEADLESS_V1_PREFIX == "/api/headless/v1"

    def test_auth_prefix(self):
        assert HEADLESS_AUTH_PREFIX == "/api/v1/headless"


class TestLogging:
    def test_debug_log_on_request(self, caplog):
        t = SyncTransport(api_token="test", base_url="https://example.com")
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"ok": True}
        with patch.object(t._client, "request", return_value=mock_resp):
            with caplog.at_level(logging.DEBUG, logger="circle"):
                t.request("GET", "/test")
        assert any("request GET /test" in r.message for r in caplog.records)
        assert any("response GET /test -> 200" in r.message for r in caplog.records)

    def test_warning_log_on_retry(self, caplog):
        t = SyncTransport(api_token="test", base_url="https://example.com", max_retries=1)
        mock_resp_500 = MagicMock(spec=httpx.Response)
        mock_resp_500.status_code = 500
        mock_resp_500.text = "error"
        mock_resp_500.json.return_value = {"message": "error"}
        mock_resp_500.headers = {}
        mock_resp_200 = MagicMock(spec=httpx.Response)
        mock_resp_200.status_code = 200
        mock_resp_200.json.return_value = {"ok": True}
        with patch.object(t._client, "request", side_effect=[mock_resp_500, mock_resp_200]):
            with patch("circle.http.time.sleep"):
                with caplog.at_level(logging.WARNING, logger="circle"):
                    t.request("GET", "/test")
        assert any("retry" in r.message.lower() for r in caplog.records)

    def test_error_log_on_transport_failure(self, caplog):
        t = SyncTransport(api_token="test", base_url="https://example.com", max_retries=0)
        with patch.object(t._client, "request", side_effect=httpx.ConnectError("fail")):
            with caplog.at_level(logging.ERROR, logger="circle"):
                with pytest.raises(CircleAPIError):
                    t.request("GET", "/test")
        assert any("transport error" in r.message for r in caplog.records)


class TestRetryControl:
    def test_retry_false_no_retry_on_500(self):
        t = SyncTransport(api_token="test", base_url="https://example.com", max_retries=3)
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 500
        mock_resp.text = "error"
        mock_resp.json.return_value = {"message": "Server error"}
        mock_resp.headers = {}
        with patch.object(t._client, "request", return_value=mock_resp) as mock_req:
            with pytest.raises(CircleAPIError, match="Server error"):
                t.request("GET", "/test", retry=False)
        # Should only be called once (no retries)
        assert mock_req.call_count == 1

    def test_retry_true_retries_on_500(self):
        t = SyncTransport(api_token="test", base_url="https://example.com", max_retries=2)
        mock_resp_500 = MagicMock(spec=httpx.Response)
        mock_resp_500.status_code = 500
        mock_resp_500.text = "error"
        mock_resp_500.json.return_value = {"message": "error"}
        mock_resp_500.headers = {}
        mock_resp_200 = MagicMock(spec=httpx.Response)
        mock_resp_200.status_code = 200
        mock_resp_200.json.return_value = {"ok": True}
        with patch.object(t._client, "request", side_effect=[mock_resp_500, mock_resp_200]):
            with patch("circle.http.time.sleep"):
                result = t.request("GET", "/test", retry=True)
        assert result == {"ok": True}

    def test_retry_false_no_retry_on_transport_error(self):
        t = SyncTransport(api_token="test", base_url="https://example.com", max_retries=3)
        with patch.object(t._client, "request", side_effect=httpx.ConnectError("fail")) as mock_req:
            with pytest.raises(CircleAPIError):
                t.request("GET", "/test", retry=False)
        assert mock_req.call_count == 1


class TestEnvVarFallback:
    def test_raises_without_token(self, monkeypatch):
        monkeypatch.delenv("CIRCLE_API_TOKEN", raising=False)
        with pytest.raises(ValueError, match="api_token is required"):
            from circle import CircleClient
            CircleClient()

    def test_falls_back_to_env_token(self, monkeypatch):
        monkeypatch.setenv("CIRCLE_API_TOKEN", "env_token")
        from circle import CircleClient
        c = CircleClient()
        assert c._admin_transport._api_token == "env_token"
        c.close()

    def test_explicit_token_overrides_env(self, monkeypatch):
        monkeypatch.setenv("CIRCLE_API_TOKEN", "env_token")
        from circle import CircleClient
        c = CircleClient(api_token="explicit")
        assert c._admin_transport._api_token == "explicit"
        c.close()

    def test_community_url_from_env(self, monkeypatch):
        monkeypatch.setenv("CIRCLE_COMMUNITY_URL", "https://my.circle.so")
        from circle import CircleClient
        c = CircleClient(api_token="test")
        assert c._admin_transport._base_url == "https://my.circle.so"
        c.close()

    def test_base_url_from_env(self, monkeypatch):
        monkeypatch.setenv("CIRCLE_BASE_URL", "https://custom.circle.so")
        monkeypatch.delenv("CIRCLE_COMMUNITY_URL", raising=False)
        from circle import CircleClient
        c = CircleClient(api_token="test")
        assert c._admin_transport._base_url == "https://custom.circle.so"
        c.close()

    def test_explicit_url_overrides_env(self, monkeypatch):
        monkeypatch.setenv("CIRCLE_BASE_URL", "https://env.circle.so")
        from circle import CircleClient
        c = CircleClient(api_token="test", base_url="https://explicit.circle.so")
        assert c._admin_transport._base_url == "https://explicit.circle.so"
        c.close()
