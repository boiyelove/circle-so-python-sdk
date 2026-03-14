"""Tests for error propagation, async clients, and pagination edge cases."""
import pytest
from circle.exceptions import NotFoundError, AuthenticationError, ValidationError
from circle.pagination import paginate, apaginate, paginate_search_after, apaginate_search_after
from circle.models.base import PaginatedResponse, CircleModel
from circle.api.admin_community import AsyncCommunityClient
from circle.api.admin_spaces import AsyncSpacesClient
from circle.api.admin_posts import AsyncPostsClient
from circle.api.admin_events import AsyncEventsClient
from circle.api.admin_courses import AsyncCoursesClient
from circle.api.admin_tags import AsyncTagsClient
from circle.api.admin_misc import AsyncAdminMiscClient
from circle.api.admin_access_groups import AsyncAccessGroupsClient
from circle.api.headless_spaces_posts import AsyncHeadlessSpacesPostsClient
from circle.api.headless_chat_notif_members import AsyncHeadlessChatNotifMembersClient
from circle.api.headless_misc import AsyncHeadlessMiscClient
from tests.conftest import MockSyncTransport, MockAsyncTransport


# -- Error propagation through full client stack --

class TestErrorPropagation:
    def test_404_propagates_from_community_client(self):
        t = MockSyncTransport()
        t.request = lambda *a, **kw: (_ for _ in ()).throw(NotFoundError("Missing record", status_code=404))
        from circle.api.admin_community import CommunityClient
        c = CommunityClient(t)
        with pytest.raises(NotFoundError, match="Missing record"):
            c.show_community_member(99999)

    def test_401_propagates_from_spaces_client(self):
        t = MockSyncTransport()
        t.request = lambda *a, **kw: (_ for _ in ()).throw(AuthenticationError("Invalid token", status_code=401))
        from circle.api.admin_spaces import SpacesClient
        c = SpacesClient(t)
        with pytest.raises(AuthenticationError):
            c.list_spaces()

    def test_422_propagates_from_posts_client(self):
        t = MockSyncTransport()
        t.request = lambda *a, **kw: (_ for _ in ()).throw(
            ValidationError("Name can't be blank", status_code=422, error_details={"name": ["can't be blank"]}))
        from circle.api.admin_posts import PostsClient
        c = PostsClient(t)
        with pytest.raises(ValidationError) as exc_info:
            c.create_post(space_id=1, name="")
        assert exc_info.value.error_details == {"name": ["can't be blank"]}

    def test_404_propagates_from_headless_client(self):
        t = MockSyncTransport()
        t.request = lambda *a, **kw: (_ for _ in ()).throw(NotFoundError("Post not found", status_code=404))
        from circle.api.headless_spaces_posts import HeadlessSpacesPostsClient
        c = HeadlessSpacesPostsClient(t)
        with pytest.raises(NotFoundError):
            c.get_post(1, 99999)

    def test_401_propagates_from_headless_chat(self):
        t = MockSyncTransport()
        t.request = lambda *a, **kw: (_ for _ in ()).throw(AuthenticationError("Expired", status_code=401))
        from circle.api.headless_chat_notif_members import HeadlessChatNotifMembersClient
        c = HeadlessChatNotifMembersClient(t)
        with pytest.raises(AuthenticationError):
            c.list_notifications()

    def test_404_propagates_from_headless_misc(self):
        t = MockSyncTransport()
        t.request = lambda *a, **kw: (_ for _ in ()).throw(NotFoundError("Lesson not found", status_code=404))
        from circle.api.headless_misc import HeadlessMiscClient
        c = HeadlessMiscClient(t)
        with pytest.raises(NotFoundError):
            c.get_lesson(1, 999)


# -- Async admin clients --

class TestAsyncAdminClients:
    async def test_async_community_get(self):
        t = MockAsyncTransport({("GET", "/api/admin/v2/community"): {"id": 1, "name": "Test"}})
        c = AsyncCommunityClient(t)
        result = await c.get_community()
        assert result.name == "Test"

    async def test_async_community_list_members(self):
        data = {"page": 1, "per_page": 10, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        t = MockAsyncTransport({("GET", "/api/admin/v2/community_members"): data})
        c = AsyncCommunityClient(t)
        result = await c.list_community_members()
        assert result.count == 0

    async def test_async_spaces_list(self):
        data = {"page": 1, "per_page": 60, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        t = MockAsyncTransport({("GET", "/api/admin/v2/spaces"): data})
        c = AsyncSpacesClient(t)
        result = await c.list_spaces()
        assert result.has_next_page is False

    async def test_async_posts_create(self):
        t = MockAsyncTransport({("POST", "/api/admin/v2/posts"): {"message": "Created", "post": {"id": 1, "name": "X"}}})
        c = AsyncPostsClient(t)
        result = await c.create_post(space_id=1, name="X")
        assert result.post.name == "X"

    async def test_async_events_list(self):
        data = {"page": 1, "per_page": 60, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        t = MockAsyncTransport({("GET", "/api/admin/v2/events"): data})
        c = AsyncEventsClient(t)
        result = await c.list_events()
        assert result.count == 0

    async def test_async_courses_create_section(self):
        t = MockAsyncTransport({("POST", "/api/admin/v2/course_sections"): {"id": 1, "name": "S1", "space_id": 1}})
        c = AsyncCoursesClient(t)
        result = await c.create_course_section(name="S1", space_id=1)
        assert result.name == "S1"

    async def test_async_tags_list(self):
        data = {"page": 1, "per_page": 10, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        t = MockAsyncTransport({("GET", "/api/admin/v2/member_tags"): data})
        c = AsyncTagsClient(t)
        result = await c.list_member_tags()
        assert result.count == 0

    async def test_async_access_groups_list(self):
        data = {"page": 1, "per_page": 60, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        t = MockAsyncTransport({("GET", "/api/admin/v2/access_groups"): data})
        c = AsyncAccessGroupsClient(t)
        result = await c.list_access_groups()
        assert result.count == 0

    async def test_async_misc_search(self):
        data = {"page": 1, "per_page": 20, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        t = MockAsyncTransport({("GET", "/api/admin/v2/advanced_search"): data})
        c = AsyncAdminMiscClient(t)
        result = await c.advanced_search(query="test")
        assert result.count == 0


# -- Async headless clients --

class TestAsyncHeadlessClients:
    async def test_async_headless_list_spaces(self):
        t = MockAsyncTransport({("GET", "/api/headless/v1/spaces"): [{"id": 1, "name": "G"}]})
        c = AsyncHeadlessSpacesPostsClient(t)
        result = await c.list_spaces()
        assert len(result) == 1

    async def test_async_headless_create_post(self):
        t = MockAsyncTransport({("POST", "/api/headless/v1/spaces/1/posts"): {"id": 1, "post_type": "basic"}})
        c = AsyncHeadlessSpacesPostsClient(t)
        result = await c.create_post(1, name="Test")
        assert result.id == 1

    async def test_async_headless_notifications(self):
        data = {"page": 1, "per_page": 20, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        t = MockAsyncTransport({("GET", "/api/headless/v1/notifications"): data})
        c = AsyncHeadlessChatNotifMembersClient(t)
        result = await c.list_notifications()
        assert result.count == 0

    async def test_async_headless_get_current_member(self):
        t = MockAsyncTransport({("GET", "/api/headless/v1/community_member"): {"id": 1, "name": "Me"}})
        c = AsyncHeadlessChatNotifMembersClient(t)
        result = await c.get_current_member()
        assert result.name == "Me"

    async def test_async_headless_search(self):
        data = {"page": 1, "per_page": 15, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        t = MockAsyncTransport({("GET", "/api/headless/v1/search"): data})
        c = AsyncHeadlessMiscClient(t)
        result = await c.search(search_text="test")
        assert result.count == 0

    async def test_async_headless_get_lesson(self):
        t = MockAsyncTransport({("GET", "/api/headless/v1/courses/1/lessons/2"): {"id": 2, "name": "L2"}})
        c = AsyncHeadlessMiscClient(t)
        result = await c.get_lesson(1, 2)
        assert result.name == "L2"


# -- Pagination edge cases --

class _FakeSearchAfterResult:
    def __init__(self, records, has_next_page, next_search_after=None):
        self.records = records
        self.has_next_page = has_next_page
        self.next_search_after = next_search_after


class TestPaginateSearchAfter:
    def test_single_page(self):
        def method(*, per_page=10):
            return _FakeSearchAfterResult([1, 2, 3], False)
        results = list(paginate_search_after(method))
        assert results == [1, 2, 3]

    def test_multiple_pages_with_cursor(self):
        call_count = [0]
        def method(*, per_page=10, search_after=None):
            call_count[0] += 1
            if search_after is None:
                return _FakeSearchAfterResult([1, 2], True, [100])
            elif search_after == [100]:
                return _FakeSearchAfterResult([3, 4], True, [200])
            else:
                return _FakeSearchAfterResult([5], False, None)
        results = list(paginate_search_after(method, per_page=2))
        assert results == [1, 2, 3, 4, 5]
        assert call_count[0] == 3

    def test_stops_when_no_next_search_after(self):
        def method(*, per_page=10, search_after=None):
            return _FakeSearchAfterResult([1], True, None)  # has_next but no cursor
        results = list(paginate_search_after(method))
        assert results == [1]

    def test_max_pages(self):
        def method(*, per_page=10, search_after=None):
            return _FakeSearchAfterResult([1], True, [999])
        results = list(paginate_search_after(method, max_pages=2))
        assert results == [1, 1]


class TestAsyncPaginate:
    async def test_apaginate_multiple_pages(self):
        call_count = [0]
        async def method(*, page=1, per_page=10):
            call_count[0] += 1
            if page == 1:
                return PaginatedResponse.model_validate(
                    {"page": 1, "per_page": 2, "has_next_page": True, "count": 3, "page_count": 2,
                     "records": [{"v": 1}, {"v": 2}]})
            return PaginatedResponse.model_validate(
                {"page": 2, "per_page": 2, "has_next_page": False, "count": 3, "page_count": 2,
                 "records": [{"v": 3}]})
        results = [r async for r in apaginate(method, per_page=2)]
        assert len(results) == 3
        assert call_count[0] == 2

    async def test_apaginate_empty(self):
        async def method(*, page=1, per_page=10):
            return PaginatedResponse.model_validate(
                {"page": 1, "per_page": 10, "has_next_page": False, "count": 0, "page_count": 0, "records": []})
        results = [r async for r in apaginate(method)]
        assert results == []

    async def test_apaginate_search_after(self):
        call_count = [0]
        async def method(*, per_page=10, search_after=None):
            call_count[0] += 1
            if search_after is None:
                return _FakeSearchAfterResult([1, 2], True, [100])
            return _FakeSearchAfterResult([3], False, None)
        results = [r async for r in apaginate_search_after(method, per_page=2)]
        assert results == [1, 2, 3]
        assert call_count[0] == 2
