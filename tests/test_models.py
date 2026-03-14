"""Tests for Pydantic models -- serialization, deserialization, extra fields."""
import pytest
from circle.models.base import PaginatedResponse, CircleModel, ErrorResponse
from circle.models.auth import HeadlessAuthToken, RefreshedAccessToken
from circle.models.admin.community import Community, ChatPreferences
from circle.models.admin.members import CommunityMember, CommunityMemberCreated
from circle.models.admin.spaces import Space, SpaceGroup, SpaceMember
from circle.models.admin.posts import BasicPost, ImagePost, Comment, Topic
from circle.models.admin.events import Event, EventAttendee
from circle.models.admin.courses import CourseSection, CourseLesson
from circle.models.admin.tags import MemberTag, TaggedMember, ProfileField
from circle.models.admin.misc import AccessGroup, Form, CommunitySegment, Embed, DirectUpload, FlaggedContent
from circle.models.headless.spaces import HeadlessSpace
from circle.models.headless.posts import HeadlessPost
from circle.models.headless.comments import HeadlessComment
from circle.models.headless.chat import ChatRoomMessage, ChatRoomParticipant
from circle.models.headless.notifications import Notification
from circle.models.headless.members import CurrentCommunityMember, PublicProfile
from circle.models.headless.courses import Section, Lesson, QuizAttempt
from circle.models.headless.misc import Bookmark, RecurringEvent, CommunityLink


class TestBaseModels:
    def test_circle_model_allows_extra_fields(self):
        m = CircleModel.model_validate({"unknown_field": "value", "another": 123})
        assert m.unknown_field == "value"

    def test_paginated_response_empty(self):
        data = {"page": 1, "per_page": 10, "has_next_page": False, "count": 0, "page_count": 0, "records": []}
        pr = PaginatedResponse.model_validate(data)
        assert pr.page == 1
        assert pr.records == []
        assert pr.has_next_page is False

    def test_error_response(self):
        er = ErrorResponse.model_validate({"success": False, "message": "Bad request", "error_details": {"key": "val"}})
        assert er.success is False
        assert er.message == "Bad request"


class TestAuthModels:
    def test_headless_auth_token(self):
        data = {
            "access_token": "eyJ...", "refresh_token": "abc",
            "access_token_expires_at": "2024-01-01T00:00:00Z",
            "refresh_token_expires_at": "2024-02-01T00:00:00Z",
            "community_member_id": 1, "community_id": 2,
        }
        t = HeadlessAuthToken.model_validate(data)
        assert t.access_token == "eyJ..."
        assert t.community_member_id == 1

    def test_refreshed_access_token(self):
        t = RefreshedAccessToken.model_validate({"access_token": "new", "access_token_expires_at": "2024-06-01"})
        assert t.access_token == "new"


class TestAdminModels:
    def test_community(self):
        c = Community.model_validate({"id": 1, "name": "Test", "slug": "test"})
        assert c.id == 1
        assert c.name == "Test"

    def test_community_member(self):
        m = CommunityMember.model_validate({"id": 1, "email": "a@b.com", "name": "Test User", "active": True})
        assert m.email == "a@b.com"
        assert m.active is True

    def test_space(self):
        s = Space.model_validate({"id": 1, "name": "General", "slug": "general", "space_type": "basic"})
        assert s.space_type == "basic"

    def test_basic_post(self):
        p = BasicPost.model_validate({"id": 42, "name": "Hello", "status": "published", "topics": [1, 2]})
        assert p.topics == [1, 2]

    def test_image_post_inherits_basic(self):
        p = ImagePost.model_validate({"id": 1, "name": "Photo", "gallery": {"id": 1, "images": []}})
        assert p.gallery.id == 1

    def test_comment(self):
        c = Comment.model_validate({"id": 1, "parent_comment_id": None, "likes_count": 5})
        assert c.likes_count == 5

    def test_event(self):
        e = Event.model_validate({"id": 1, "name": "Meetup", "starts_at": "2024-06-15T09:00:00Z"})
        assert e.name == "Meetup"

    def test_course_lesson(self):
        l = CourseLesson.model_validate({"id": 1, "name": "Intro", "status": "published", "section_id": 1})
        assert l.status == "published"

    def test_member_tag(self):
        t = MemberTag.model_validate({"id": 1, "name": "VIP", "color": "#FF0000"})
        assert t.color == "#FF0000"

    def test_access_group(self):
        ag = AccessGroup.model_validate({"id": 1, "name": "Premium", "status": "active"})
        assert ag.status == "active"

    def test_form(self):
        f = Form.model_validate({"id": 1, "name": "Contact", "status": "published", "uid": "abc"})
        assert f.uid == "abc"

    def test_embed(self):
        e = Embed.model_validate({"id": 1, "url": "https://youtube.com/watch?v=123", "type": "embed"})
        assert e.url == "https://youtube.com/watch?v=123"

    def test_flagged_content(self):
        fc = FlaggedContent.model_validate({"id": 1, "reported_reason_type": "spam", "content_type": "post"})
        assert fc.reported_reason_type == "spam"


class TestHeadlessModels:
    def test_headless_space(self):
        s = HeadlessSpace.model_validate({"id": 1, "name": "General", "is_member": True, "policies": {"can_view_space": True}})
        assert s.is_member is True
        assert s.policies.can_view_space is True

    def test_headless_post(self):
        p = HeadlessPost.model_validate({"id": 1, "post_type": "basic", "is_liked": False, "comment_count": 3})
        assert p.comment_count == 3

    def test_headless_comment(self):
        c = HeadlessComment.model_validate({"id": 1, "body_text": "Nice!", "is_liked": True})
        assert c.is_liked is True

    def test_notification(self):
        n = Notification.model_validate({"id": 1, "action": "add", "actor_name": "John", "read_at": None})
        assert n.read_at is None

    def test_chat_room_message(self):
        m = ChatRoomMessage.model_validate({"id": 1, "body": "Hello", "chat_room_uuid": "abc-123"})
        assert m.chat_room_uuid == "abc-123"

    def test_current_community_member(self):
        m = CurrentCommunityMember.model_validate({"id": 1, "name": "Me", "email": "me@example.com", "active": True})
        assert m.active is True

    def test_public_profile(self):
        p = PublicProfile.model_validate({"id": 1, "name": "User", "posts_count": 10})
        assert p.posts_count == 10

    def test_lesson(self):
        l = Lesson.model_validate({"id": 1, "name": "Lesson 1", "section_id": 1})
        assert l.section_id == 1

    def test_quiz_attempt(self):
        q = QuizAttempt.model_validate({"id": 1, "quiz_id": 1, "grade": 85, "result": "passed"})
        assert q.result == "passed"

    def test_bookmark(self):
        b = Bookmark.model_validate({"id": 1, "record_id": 42, "bookmarkable_type": "post"})
        assert b.record_id == 42

    def test_community_link(self):
        cl = CommunityLink.model_validate({"id": 1, "name": "Docs", "url": "https://docs.example.com"})
        assert cl.url == "https://docs.example.com"


class TestExtraFieldsForwardCompat:
    """Verify models don't break when API adds new fields."""

    def test_community_with_unknown_fields(self):
        c = Community.model_validate({"id": 1, "name": "Test", "brand_new_field": True, "nested_new": {"a": 1}})
        assert c.id == 1
        assert c.brand_new_field is True

    def test_headless_post_with_unknown_fields(self):
        p = HeadlessPost.model_validate({"id": 1, "future_feature": "enabled"})
        assert p.future_feature == "enabled"
