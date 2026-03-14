"""Shared test fixtures and mock transport."""
import pytest
from unittest.mock import MagicMock, AsyncMock
from circle.http import SyncTransport, AsyncTransport


class MockSyncTransport(SyncTransport):
    """SyncTransport that returns canned responses instead of making HTTP calls."""

    def __init__(self, responses=None):
        self._responses = responses or {}
        self._calls = []

    def request(self, method, path, **kwargs):
        self._calls.append((method, path, kwargs))
        key = (method, path)
        for (m, p), resp in self._responses.items():
            if m == method and (p == path or path.startswith(p)):
                if callable(resp):
                    return resp(method, path, kwargs)
                return resp
        return self._default_response(method, path)

    def _default_response(self, method, path):
        if method == "DELETE":
            return {"success": True, "message": "Deleted"}
        if method in ("POST", "PUT", "PATCH"):
            return {"id": 1, "message": "OK"}
        return {"page": 1, "per_page": 10, "has_next_page": False, "count": 0, "page_count": 0, "records": []}

    def close(self):
        pass


class MockAsyncTransport(AsyncTransport):
    """AsyncTransport that returns canned responses."""

    def __init__(self, responses=None):
        self._responses = responses or {}
        self._calls = []

    async def request(self, method, path, **kwargs):
        self._calls.append((method, path, kwargs))
        key = (method, path)
        for (m, p), resp in self._responses.items():
            if m == method and (p == path or path.startswith(p)):
                if callable(resp):
                    return resp(method, path, kwargs)
                return resp
        return self._default_response(method, path)

    def _default_response(self, method, path):
        if method == "DELETE":
            return {"success": True, "message": "Deleted"}
        if method in ("POST", "PUT", "PATCH"):
            return {"id": 1, "message": "OK"}
        return {"page": 1, "per_page": 10, "has_next_page": False, "count": 0, "page_count": 0, "records": []}

    async def close(self):
        pass


@pytest.fixture
def mock_transport():
    return MockSyncTransport()


@pytest.fixture
def mock_async_transport():
    return MockAsyncTransport()
