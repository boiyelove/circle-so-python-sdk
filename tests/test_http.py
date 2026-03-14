"""Tests for HTTP transport layer -- error parsing, retry logic, headers."""
import pytest
import httpx
from unittest.mock import patch, MagicMock
from circle.http import SyncTransport, AsyncTransport, _parse_error, _retry_delay, DEFAULT_BASE_URL
from circle.exceptions import (
    CircleAPIError, AuthenticationError, ForbiddenError, NotFoundError, ValidationError, RateLimitError,
)


class TestParseError:
    def _make_response(self, status_code, json_data=None, text=""):
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = status_code
        resp.text = text
        if json_data is not None:
            resp.json.return_value = json_data
        else:
            resp.json.side_effect = Exception("no json")
        return resp

    def test_401_raises_authentication_error(self):
        resp = self._make_response(401, {"message": "Invalid token", "error_details": {}})
        err = _parse_error(resp)
        assert isinstance(err, AuthenticationError)
        assert "Invalid token" in str(err)
        assert err.status_code == 401

    def test_403_raises_forbidden_error(self):
        resp = self._make_response(403, {"message": "Not eligible"})
        err = _parse_error(resp)
        assert isinstance(err, ForbiddenError)

    def test_404_raises_not_found_error(self):
        resp = self._make_response(404, {"message": "Missing record", "error_details": {"message": "Missing record: post"}})
        err = _parse_error(resp)
        assert isinstance(err, NotFoundError)
        assert err.error_details == {"message": "Missing record: post"}

    def test_422_raises_validation_error(self):
        resp = self._make_response(422, {"message": "Name can't be blank"})
        err = _parse_error(resp)
        assert isinstance(err, ValidationError)

    def test_429_raises_rate_limit_error(self):
        resp = self._make_response(429, {"message": "Too many requests"})
        err = _parse_error(resp)
        assert isinstance(err, RateLimitError)

    def test_500_raises_base_error(self):
        resp = self._make_response(500, None, "Internal Server Error")
        err = _parse_error(resp)
        assert isinstance(err, CircleAPIError)
        assert err.status_code == 500

    def test_error_with_list_message(self):
        resp = self._make_response(403, {"errors": ["Limit exceeded", "Plan upgrade required"]})
        err = _parse_error(resp)
        assert "Limit exceeded" in str(err)


class TestRetryDelay:
    def test_exponential_backoff(self):
        assert _retry_delay(0, None) == 1
        assert _retry_delay(1, None) == 2
        assert _retry_delay(2, None) == 4
        assert _retry_delay(10, None) == 30  # capped at 30

    def test_retry_after_header(self):
        resp = MagicMock()
        resp.status_code = 429
        resp.headers = {"Retry-After": "5"}
        assert _retry_delay(0, resp) == 5.0


class TestSyncTransportHeaders:
    def test_token_auth_scheme(self):
        t = SyncTransport(api_token="test123", base_url="https://example.com", auth_scheme="Token")
        headers = t._build_headers()
        assert headers["Authorization"] == "Token test123"

    def test_bearer_auth_scheme(self):
        t = SyncTransport(api_token="abc", base_url="https://example.com", auth_scheme="Bearer")
        headers = t._build_headers()
        assert headers["Authorization"] == "Bearer abc"

    def test_full_url(self):
        t = SyncTransport(api_token="x", base_url="https://app.circle.so")
        assert t._full_url("/api/v1/test") == "https://app.circle.so/api/v1/test"

    def test_trailing_slash_stripped(self):
        t = SyncTransport(api_token="x", base_url="https://app.circle.so/")
        assert t._full_url("/api") == "https://app.circle.so/api"
