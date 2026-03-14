"""Tests for Headless Client API clients."""
import pytest
from circle.api.headless_spaces_posts import HeadlessSpacesPostsClient
from circle.api.headless_chat_notif_members import HeadlessChatNotifMembersClient
from circle.api.headless_misc import HeadlessMiscClient
from circle.models.headless.spaces import HeadlessSpace
from circle.models.headless.posts import HeadlessPost, HeadlessPostList
from circle.models.headless.comments import HeadlessComment, HeadlessCommentList
from circle.models.headless.chat import ChatRoomMessages, ChatRoomMessage, UnreadChatRooms
from circle.models.headless.notifications import Notification, NotificationList, NewNotificationsCount
from circle.models.headless.members import CurrentCommunityMember, PublicProfile
from circle.models.headless.courses import Lesson
from circle.models.headless.misc import Bookmark, BookmarkList, SearchResults
from tests.conftest import MockSyncTransport

_P = "/api/headless/v1"


class TestHeadlessSpacesPosts:
    def _client(self, responses=None):
        return HeadlessSpacesPostsClient(MockSyncTransport(responses or {}))

    def test_list_spaces(self):
        c = self._client({("GET", f"{_P}/spaces"): [{"id": 1, "name": "General", "slug": "general"}]})
        result = c.list_spaces()
        assert len(result) == 1
        assert isinstance(result[0], HeadlessSpace)

    def test_get_space(self):
        c = self._client({("GET", f"{_P}/spaces/1"): {"id": 1, "name": "General", "is_member": True}})
        result = c.get_space(1)
        assert result.is_member is True

    def test_join_space(self):
        c = self._client({("POST", f"{_P}/spaces/1/join"): {"id": 1, "is_member": True}})
        result = c.join_space(1)
        assert result.is_member is True

    def test_list_posts(self):
        data = {"page": 1, "per_page": 10, "has_next_page": False, "count": 1, "sort": "latest",
                "records": [{"id": 1, "post_type": "basic", "name": "Hello"}]}
        c = self._client({("GET", f"{_P}/spaces/1/posts"): data})
        result = c.list_posts(1)
        assert isinstance(result, HeadlessPostList)
        assert result.records[0].name == "Hello"

    def test_create_post(self):
        c = self._client({("POST", f"{_P}/spaces/1/posts"): {"id": 2, "post_type": "basic", "name": "New"}})
        result = c.create_post(1, name="New")
        assert isinstance(result, HeadlessPost)

    def test_like_post(self):
        t = MockSyncTransport({("POST", f"{_P}/posts/1/user_likes"): {"success": True, "message": "Liked"}})
        c = HeadlessSpacesPostsClient(t)
        result = c.like_post(1)
        assert result["success"] is True

    def test_create_comment(self):
        c = self._client({("POST", f"{_P}/posts/1/comments"): {"id": 1, "body_text": "Nice!"}})
        result = c.create_comment(1, body="Nice!")
        assert isinstance(result, HeadlessComment)

    def test_create_reply(self):
        c = self._client({("POST", f"{_P}/comments/1/replies"): {"id": 2, "parent_comment_id": 1}})
        result = c.create_reply(1, body="Thanks!")
        assert result.parent_comment_id == 1

    def test_get_home_posts(self):
        data = {"page": 1, "per_page": 10, "has_next_page": False, "count": 0, "sort": "latest", "records": []}
        c = self._client({("GET", f"{_P}/home"): data})
        result = c.get_home_posts()
        assert isinstance(result, HeadlessPostList)


class TestHeadlessChatNotifMembers:
    def _client(self, responses=None):
        return HeadlessChatNotifMembersClient(MockSyncTransport(responses or {}))

    def test_list_chat_messages(self):
        data = {"id": 10, "has_next_page": False, "has_previous_page": False,
                "first_id": 1, "last_id": 10, "total_count": 10, "records": []}
        c = self._client({("GET", f"{_P}/messages/uuid-123/chat_room_messages"): data})
        result = c.list_chat_messages("uuid-123")
        assert isinstance(result, ChatRoomMessages)
        assert result.total_count == 10

    def test_get_unread_chat_rooms(self):
        c = self._client({("GET", f"{_P}/messages/unread_chat_rooms"): {"chat_rooms": ["uuid-1", "uuid-2"]}})
        result = c.get_unread_chat_rooms()
        assert isinstance(result, UnreadChatRooms)
        assert len(result.chat_rooms) == 2

    def test_list_notifications(self):
        data = {"page": 1, "per_page": 20, "has_next_page": False, "count": 1, "page_count": 1,
                "records": [{"id": 1, "action": "add", "actor_name": "John"}]}
        c = self._client({("GET", f"{_P}/notifications"): data})
        result = c.list_notifications()
        assert isinstance(result, NotificationList)
        assert result.records[0].actor_name == "John"

    def test_get_new_notifications_count(self):
        c = self._client({("GET", f"{_P}/notifications/new_notifications_count"):
                          {"new_notifications_count": 5, "new_mentions_count": 2, "new_inbox_count": 1}})
        result = c.get_new_notifications_count()
        assert isinstance(result, NewNotificationsCount)
        assert result.new_notifications_count == 5

    def test_get_current_member(self):
        c = self._client({("GET", f"{_P}/community_member"):
                          {"id": 1, "name": "Me", "email": "me@example.com", "active": True}})
        result = c.get_current_member()
        assert isinstance(result, CurrentCommunityMember)
        assert result.name == "Me"

    def test_get_public_profile(self):
        c = self._client({("GET", f"{_P}/community_members/2/public_profile"):
                          {"id": 2, "name": "Other", "posts_count": 10}})
        result = c.get_public_profile(2)
        assert isinstance(result, PublicProfile)

    def test_create_event_attendee(self):
        c = self._client({("POST", f"{_P}/events/1/event_attendees"):
                          {"id": 1, "community_member_id": 1, "rsvp_status": "yes"}})
        result = c.create_event_attendee(1)
        assert result.rsvp_status == "yes"


class TestHeadlessMisc:
    def _client(self, responses=None):
        return HeadlessMiscClient(MockSyncTransport(responses or {}))

    def test_get_lesson(self):
        c = self._client({("GET", f"{_P}/courses/1/lessons/2"):
                          {"id": 2, "name": "Lesson 2", "section_id": 1}})
        result = c.get_lesson(1, 2)
        assert isinstance(result, Lesson)
        assert result.name == "Lesson 2"

    def test_search(self):
        data = {"page": 1, "per_page": 15, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        c = self._client({("GET", f"{_P}/search"): data})
        result = c.search(search_text="python")
        assert isinstance(result, SearchResults)

    def test_list_bookmarks(self):
        data = {"page": 1, "per_page": 10, "has_next_page": False, "count": 1, "page_count": 1,
                "records": [{"id": 1, "record_id": 42, "bookmarkable_type": "post"}]}
        c = self._client({("GET", f"{_P}/bookmarks"): data})
        result = c.list_bookmarks()
        assert isinstance(result, BookmarkList)
        assert result.records[0].record_id == 42

    def test_create_bookmark(self):
        c = self._client({("POST", f"{_P}/bookmarks"): {"id": 1, "record_id": 42, "bookmarkable_type": "post"}})
        result = c.create_bookmark(record_id=42, bookmark_type="post")
        assert isinstance(result, Bookmark)

    def test_get_community_links(self):
        c = self._client({("GET", f"{_P}/community_links"): [
            {"id": 1, "name": "Docs", "url": "https://docs.example.com"}
        ]})
        result = c.get_community_links()
        assert len(result) == 1
        assert result[0].name == "Docs"

    def test_update_lesson_progress(self):
        t = MockSyncTransport({("PATCH", f"{_P}/courses/1/lessons/2/progress"): {"status": "completed"}})
        c = HeadlessMiscClient(t)
        result = c.update_lesson_progress(1, 2, status="completed")
        assert result["status"] == "completed"
