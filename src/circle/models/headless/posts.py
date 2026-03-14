"""Headless post models."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse
from circle.models.admin.posts import TiptapBody


class SharedCommunityMember(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    headline: Optional[str] = None
    avatar_url: Optional[str] = None
    roles: Optional[Any] = None
    rich_text_field_sgid: Optional[str] = None
    member_tags: Optional[List[Any]] = None
    community_member_id: Optional[int] = None


class HeadlessPostPolicies(CircleModel):
    can_destroy_post: Optional[bool] = None
    can_duplicate_post: Optional[bool] = None
    can_manage_post: Optional[bool] = None
    can_report_post: Optional[bool] = None
    can_update_post: Optional[bool] = None


class HeadlessPostBody(CircleModel):
    attachments: Optional[Any] = None
    attachments_array: Optional[List[Any]] = None
    html: Optional[str] = None


class HeadlessPostSpace(CircleModel):
    id: Optional[int] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    emoji: Optional[str] = None
    custom_emoji_url: Optional[str] = None
    custom_emoji_dark_url: Optional[str] = None


class HeadlessPostTopic(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    admin_only: Optional[bool] = None


class HeadlessPostAction(CircleModel):
    user_name: Optional[str] = None
    created_at: Optional[str] = None
    type: Optional[str] = None


class HeadlessPost(CircleModel):
    post_type: Optional[str] = None
    space_type: Optional[str] = None
    status: Optional[str] = None
    id: Optional[int] = None
    name: Optional[str] = None
    display_title: Optional[str] = None
    slug: Optional[str] = None
    cover_image: Optional[str] = None
    cardview_image: Optional[str] = None
    is_comments_closed: Optional[bool] = None
    is_comments_enabled: Optional[bool] = None
    is_liking_enabled: Optional[bool] = None
    is_pinned_at_top_of_space: Optional[bool] = None
    comment_count: Optional[int] = None
    user_likes_count: Optional[int] = None
    hide_meta_info: Optional[bool] = None
    is_liked: Optional[bool] = None
    is_truncation_disabled: Optional[bool] = None
    bookmark_id: Optional[int] = None
    flagged_for_approval_at: Optional[str] = None
    unresolved_flagged_reports_count: Optional[int] = None
    first_liked_by: Optional[List[SharedCommunityMember]] = None
    editor: Optional[str] = None
    body: Optional[HeadlessPostBody] = None
    tiptap_body: Optional[TiptapBody] = None
    body_plain_text: Optional[str] = None
    body_plain_text_without_attachments: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    space: Optional[HeadlessPostSpace] = None
    post_follower_id: Optional[int] = None
    topic_follower_id: Optional[int] = None
    author: Optional[SharedCommunityMember] = None
    topics: Optional[List[HeadlessPostTopic]] = None
    action: Optional[HeadlessPostAction] = None
    custom_html: Optional[str] = None
    policies: Optional[HeadlessPostPolicies] = None

HeadlessPostList = PaginatedResponse[HeadlessPost]


class HeadlessImageGalleryImage(CircleModel):
    id: Optional[int] = None
    url: Optional[str] = None
    signed_id: Optional[str] = None
    filename: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class HeadlessImageGallery(CircleModel):
    id: Optional[int] = None
    downloadable_images: Optional[bool] = None
    images: Optional[List[HeadlessImageGalleryImage]] = None


class HeadlessImagePost(HeadlessPost):
    gallery: Optional[HeadlessImageGallery] = None


class HeadlessEventSetting(CircleModel):
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    in_person_location: Optional[str] = None
    hide_location_from_non_attendees: Optional[bool] = None
    duration_in_seconds: Optional[int] = None
    rsvp_disabled: Optional[bool] = None
    hide_attendees: Optional[bool] = None
    location_type: Optional[str] = None
    virtual_location_url: Optional[str] = None
    rsvp_limit: Optional[int] = None
    rsvp_count: Optional[int] = None
    event_type: Optional[str] = None


class HeadlessEventPost(HeadlessPost):
    event_setting_attributes: Optional[HeadlessEventSetting] = None
    rsvped_event: Optional[bool] = None
    rsvp_status: Optional[str] = None
    invited_attendee: Optional[bool] = None
    event_attendees: Optional[Dict[str, Any]] = None
    recurring_setting_attributes: Optional[Dict[str, Any]] = None
