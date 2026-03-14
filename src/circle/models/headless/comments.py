"""Headless comment models."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse
from circle.models.headless.posts import SharedCommunityMember
from circle.models.admin.posts import TiptapBody


class HeadlessCommentPolicies(CircleModel):
    can_bookmark: Optional[bool] = None
    can_destroy: Optional[bool] = None
    can_edit: Optional[bool] = None
    can_manage: Optional[bool] = None
    can_report: Optional[bool] = None


class HeadlessCommentBody(CircleModel):
    attachments: Optional[Any] = None
    attachments_array: Optional[List[Any]] = None
    html: Optional[str] = None


class HeadlessComment(CircleModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    post_id: Optional[int] = None
    user_likes_count: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    parent_comment_id: Optional[int] = None
    replies_count: Optional[int] = None
    removed_at: Optional[str] = None
    community_member_id: Optional[int] = None
    editor: Optional[str] = None
    topic_id: Optional[int] = None
    space_id: Optional[int] = None
    post_name: Optional[str] = None
    body: Optional[HeadlessCommentBody] = None
    tiptap_body: Optional[TiptapBody] = None
    body_text: Optional[str] = None
    is_liked: Optional[bool] = None
    bookmark_id: Optional[int] = None
    flagged_for_approval_at: Optional[str] = None
    unresolved_flagged_reports_count: Optional[int] = None
    author: Optional[SharedCommunityMember] = None
    policies: Optional[HeadlessCommentPolicies] = None
    replies: Optional[List[HeadlessComment]] = None

HeadlessCommentList = PaginatedResponse[HeadlessComment]


class UserLike(CircleModel):
    headline: Optional[str] = None
    member_tags: Optional[List[Any]] = None
    name: Optional[str] = None
    roles: Optional[Any] = None
    community_member_id: Optional[int] = None
    avatar_url: Optional[str] = None

UserLikeList = PaginatedResponse[UserLike]
