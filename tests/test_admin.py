"""Tests for Admin API clients."""
import pytest
from circle.api.admin_access_groups import AccessGroupsClient
from circle.api.admin_community import CommunityClient
from circle.api.admin_spaces import SpacesClient
from circle.api.admin_posts import PostsClient
from circle.api.admin_events import EventsClient
from circle.api.admin_courses import CoursesClient
from circle.api.admin_tags import TagsClient
from circle.api.admin_misc import AdminMiscClient
from circle.models.admin.misc import AccessGroup, AccessGroupList
from circle.models.admin.community import Community
from circle.models.admin.members import CommunityMember, CommunityMemberList
from circle.models.admin.spaces import Space, SpaceList, SpaceGroup
from circle.models.admin.posts import BasicPost, PostList, Comment, Topic
from circle.models.admin.events import Event, EventList
from circle.models.admin.courses import CourseSection, CourseLesson
from circle.models.admin.tags import MemberTag, MemberTagList
from tests.conftest import MockSyncTransport

_P = "/api/admin/v2"


class TestAccessGroupsClient:
    def _client(self, responses=None):
        return AccessGroupsClient(MockSyncTransport(responses or {}))

    def test_list_access_groups(self):
        data = {"page": 1, "per_page": 60, "has_next_page": False, "count": 1, "page_count": 1,
                "records": [{"id": 1, "name": "VIP", "status": "active"}]}
        c = self._client({("GET", f"{_P}/access_groups"): data})
        result = c.list_access_groups()
        assert isinstance(result, AccessGroupList)
        assert len(result.records) == 1
        assert result.records[0].name == "VIP"

    def test_create_access_group(self):
        c = self._client({("POST", f"{_P}/access_groups"): {"id": 1, "name": "New", "status": "active"}})
        ag = c.create_access_group(name="New")
        assert isinstance(ag, AccessGroup)
        assert ag.name == "New"

    def test_archive_access_group(self):
        c = self._client({("DELETE", f"{_P}/access_groups/1"): {"success": True, "message": "Archived"}})
        result = c.archive_access_group(1)
        assert result["success"] is True

    def test_add_access_group_member(self):
        t = MockSyncTransport({("POST", f"{_P}/access_groups/1/community_members"): {"message": "Added"}})
        c = AccessGroupsClient(t)
        c.add_access_group_member(1, email="user@example.com")
        assert t._calls[0][2]["json"] == {"email": "user@example.com"}


class TestCommunityClient:
    def _client(self, responses=None):
        return CommunityClient(MockSyncTransport(responses or {}))

    def test_get_community(self):
        c = self._client({("GET", f"{_P}/community"): {"id": 1, "name": "My Community", "slug": "my-community"}})
        result = c.get_community()
        assert isinstance(result, Community)
        assert result.name == "My Community"

    def test_list_community_members(self):
        data = {"page": 1, "per_page": 10, "has_next_page": True, "count": 50, "page_count": 5,
                "records": [{"id": 1, "name": "User 1", "email": "u1@example.com"}]}
        c = self._client({("GET", f"{_P}/community_members"): data})
        result = c.list_community_members()
        assert result.has_next_page is True
        assert result.records[0].name == "User 1"

    def test_create_community_member(self):
        resp = {"message": "Invited", "community_member": {"id": 2, "email": "new@example.com", "name": "New"}}
        c = self._client({("POST", f"{_P}/community_members"): resp})
        result = c.create_community_member(email="new@example.com", name="New")
        assert result.community_member.email == "new@example.com"

    def test_search_community_member(self):
        c = self._client({("GET", f"{_P}/community_members/search"): {"id": 1, "email": "found@example.com"}})
        result = c.search_community_member(email="found@example.com")
        assert isinstance(result, CommunityMember)

    def test_ban_community_member(self):
        c = self._client({("PUT", f"{_P}/community_members/1/ban_member"): {"message": "Banned"}})
        result = c.ban_community_member(1)
        assert result["message"] == "Banned"


class TestSpacesClient:
    def _client(self, responses=None):
        return SpacesClient(MockSyncTransport(responses or {}))

    def test_list_spaces(self):
        data = {"page": 1, "per_page": 60, "has_next_page": False, "count": 1, "page_count": 1,
                "records": [{"id": 1, "name": "General", "slug": "general"}]}
        c = self._client({("GET", f"{_P}/spaces"): data})
        result = c.list_spaces()
        assert isinstance(result, SpaceList)

    def test_create_space(self):
        resp = {"success": True, "message": "Created", "space": {"id": 2, "name": "New", "slug": "new"}}
        c = self._client({("POST", f"{_P}/spaces"): resp})
        result = c.create_space(name="New", slug="new", space_group_id=1)
        assert result.space.name == "New"

    def test_show_space(self):
        c = self._client({("GET", f"{_P}/spaces/1"): {"id": 1, "name": "General", "space_type": "basic"}})
        result = c.show_space(1)
        assert isinstance(result, Space)

    def test_delete_space(self):
        c = self._client({("DELETE", f"{_P}/spaces/1"): {"success": True}})
        result = c.delete_space(1)
        assert result["success"] is True

    def test_add_space_member(self):
        t = MockSyncTransport({("POST", f"{_P}/space_members"): {"message": "Added"}})
        c = SpacesClient(t)
        c.add_space_member(email="user@example.com", space_id=1)
        assert t._calls[0][2]["json"] == {"email": "user@example.com", "space_id": 1}


class TestPostsClient:
    def _client(self, responses=None):
        return PostsClient(MockSyncTransport(responses or {}))

    def test_list_posts(self):
        data = {"page": 1, "per_page": 60, "has_next_page": False, "count": 1, "page_count": 1,
                "records": [{"id": 1, "name": "Post 1", "status": "published"}]}
        c = self._client({("GET", f"{_P}/posts"): data})
        result = c.list_posts(space_id=1)
        assert len(result.records) == 1

    def test_create_post(self):
        resp = {"message": "Created", "post": {"id": 1, "name": "New Post", "status": "published"}}
        c = self._client({("POST", f"{_P}/posts"): resp})
        result = c.create_post(space_id=1, name="New Post")
        assert result.post.name == "New Post"

    def test_create_comment(self):
        c = self._client({("POST", f"{_P}/comments"): {"id": 1, "body": {"body": "Nice"}}})
        result = c.create_comment(body="Nice", post_id=1)
        assert isinstance(result, Comment)

    def test_create_topic(self):
        c = self._client({("POST", f"{_P}/topics"): {"id": 1, "name": "Python", "admin_only": False}})
        result = c.create_topic(name="Python")
        assert isinstance(result, Topic)
        assert result.name == "Python"


class TestEventsClient:
    def _client(self, responses=None):
        return EventsClient(MockSyncTransport(responses or {}))

    def test_list_events(self):
        data = {"page": 1, "per_page": 60, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        c = self._client({("GET", f"{_P}/events"): data})
        result = c.list_events()
        assert isinstance(result, EventList)

    def test_create_event(self):
        c = self._client({("POST", f"{_P}/events"): {"id": 1, "name": "Meetup"}})
        result = c.create_event(space_id=1, name="Meetup", status="published")
        assert isinstance(result, Event)


class TestCoursesClient:
    def _client(self, responses=None):
        return CoursesClient(MockSyncTransport(responses or {}))

    def test_create_course_section(self):
        c = self._client({("POST", f"{_P}/course_sections"): {"id": 1, "name": "Section 1", "space_id": 1}})
        result = c.create_course_section(name="Section 1", space_id=1)
        assert isinstance(result, CourseSection)

    def test_create_course_lesson(self):
        c = self._client({("POST", f"{_P}/course_lessons"): {"id": 1, "name": "Lesson 1", "section_id": 1}})
        result = c.create_course_lesson(name="Lesson 1", section_id=1)
        assert isinstance(result, CourseLesson)

    def test_update_lesson_progress(self):
        t = MockSyncTransport({("PUT", f"{_P}/course_lesson_progress"): {"success": True}})
        c = CoursesClient(t)
        c.update_course_lesson_progress(lesson_id=1, member_email="u@example.com", status="completed")
        assert t._calls[0][2]["json"]["status"] == "completed"


class TestTagsClient:
    def _client(self, responses=None):
        return TagsClient(MockSyncTransport(responses or {}))

    def test_list_member_tags(self):
        data = {"page": 1, "per_page": 10, "has_next_page": False, "count": 1, "page_count": 1,
                "records": [{"id": 1, "name": "VIP"}]}
        c = self._client({("GET", f"{_P}/member_tags"): data})
        result = c.list_member_tags()
        assert isinstance(result, MemberTagList)

    def test_create_tagged_member(self):
        t = MockSyncTransport({("POST", f"{_P}/tagged_members"): {"message": "Tagged"}})
        c = TagsClient(t)
        c.create_tagged_member(member_tag_id=1, user_email="u@example.com")
        assert t._calls[0][2]["json"]["member_tag_id"] == 1


class TestAdminMiscClient:
    def _client(self, responses=None):
        return AdminMiscClient(MockSyncTransport(responses or {}))

    def test_advanced_search(self):
        data = {"page": 1, "per_page": 20, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        c = self._client({("GET", f"{_P}/advanced_search"): data})
        result = c.advanced_search(query="test")
        assert result.count == 0

    def test_get_leaderboard(self):
        c = self._client({("GET", f"{_P}/gamification/leaderboard"): [
            {"community_member_id": 1, "name": "Top", "total_points": 100}
        ]})
        result = c.get_leaderboard()
        assert len(result) == 1
        assert result[0].total_points == 100

    def test_create_embed(self):
        c = self._client({("POST", f"{_P}/embeds"): {"id": 1, "url": "https://youtube.com/123", "type": "embed"}})
        result = c.create_embed(url="https://youtube.com/123")
        assert result.url == "https://youtube.com/123"
