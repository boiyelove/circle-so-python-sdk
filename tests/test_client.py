"""Tests for CircleClient facade and pagination helpers."""
import pytest
from circle.client import CircleClient, AsyncCircleClient
from circle.pagination import paginate, paginate_search_after
from circle.models.base import PaginatedResponse, CircleModel


class TestCircleClientFacade:
    def test_sync_client_has_all_namespaces(self):
        c = CircleClient(api_token="test")
        assert hasattr(c, "auth")
        assert hasattr(c, "admin")
        assert hasattr(c, "headless")
        c.close()

    def test_admin_has_all_sub_clients(self):
        c = CircleClient(api_token="test")
        for attr in ("access_groups", "community", "spaces", "posts", "events", "courses", "tags", "misc"):
            assert hasattr(c.admin, attr), f"Missing admin.{attr}"
        c.close()

    def test_headless_has_all_sub_clients(self):
        c = CircleClient(api_token="test")
        for attr in ("spaces_posts", "chat_notif_members", "misc"):
            assert hasattr(c.headless, attr), f"Missing headless.{attr}"
        c.close()

    def test_context_manager(self):
        with CircleClient(api_token="test") as c:
            assert c.admin is not None

    def test_custom_community_url(self):
        c = CircleClient(api_token="test", community_url="https://my.circle.so")
        assert c._admin_transport._base_url == "https://my.circle.so"
        c.close()


class TestAsyncCircleClientFacade:
    async def test_async_context_manager(self):
        async with AsyncCircleClient(api_token="test") as c:
            assert c.admin is not None
            assert c.headless is not None


class TestPagination:
    def _make_method(self, pages):
        """Create a mock paginated method that returns N pages."""
        call_count = [0]
        def method(*, page=1, per_page=10):
            idx = page - 1
            if idx < len(pages):
                records, has_next = pages[idx]
            else:
                records, has_next = [], False
            call_count[0] += 1
            return PaginatedResponse.model_validate({
                "page": page, "per_page": per_page, "has_next_page": has_next,
                "count": sum(len(r) for r, _ in pages), "page_count": len(pages),
                "records": [{"value": v} for v in records],
            })
        return method, call_count

    def test_single_page(self):
        method, calls = self._make_method([([1, 2, 3], False)])
        results = list(paginate(method, per_page=10))
        assert len(results) == 3
        assert calls[0] == 1

    def test_multiple_pages(self):
        method, calls = self._make_method([
            ([1, 2], True),
            ([3, 4], True),
            ([5], False),
        ])
        results = list(paginate(method, per_page=2))
        assert len(results) == 5
        assert calls[0] == 3

    def test_max_pages_limit(self):
        method, calls = self._make_method([
            ([1, 2], True),
            ([3, 4], True),
            ([5, 6], True),
        ])
        results = list(paginate(method, per_page=2, max_pages=2))
        assert len(results) == 4
        assert calls[0] == 2

    def test_empty_results(self):
        method, _ = self._make_method([([], False)])
        results = list(paginate(method))
        assert results == []
