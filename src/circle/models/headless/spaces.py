"""Headless space models."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse


class HeadlessSpacePolicies(CircleModel):
    can_manage_space: Optional[bool] = None
    can_view_space: Optional[bool] = None
    can_leave_space: Optional[bool] = None
    can_create_post: Optional[bool] = None
    can_invite_members: Optional[bool] = None


class HeadlessSpace(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    space_group_id: Optional[int] = None
    community_id: Optional[int] = None
    post_type: Optional[str] = None
    space_type: Optional[str] = None
    display_view: Optional[str] = None
    emoji: Optional[str] = None
    custom_emoji_url: Optional[str] = None
    custom_emoji_dark_url: Optional[str] = None
    is_private: Optional[bool] = None
    space_group_name: Optional[str] = None
    url: Optional[str] = None
    is_post_disabled: Optional[bool] = None
    hide_post_settings: Optional[bool] = None
    is_member: Optional[bool] = None
    default_tab: Optional[str] = None
    visible_tabs: Optional[Dict[str, bool]] = None
    default_sort: Optional[str] = None
    hide_sorting: Optional[bool] = None
    show_in_spaces_segment: Optional[bool] = None
    show_lock_icon_for_non_members: Optional[bool] = None
    space_member_id: Optional[int] = None
    policies: Optional[HeadlessSpacePolicies] = None
    require_topic_selection: Optional[bool] = None
    topics_count: Optional[int] = None
    display_space_welcome_banner: Optional[bool] = None
    cover_image: Optional[str] = None
    cover_image_url: Optional[str] = None

HeadlessSpaceList = PaginatedResponse[HeadlessSpace]


class SpaceNotificationDetail(CircleModel):
    id: Optional[int] = None
    unread_content_count: Optional[int] = None
    unread_notifications_count: Optional[int] = None


class SpaceBookmarkLink(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    display_type: Optional[str] = None
    url: Optional[str] = None
    emoji: Optional[str] = None
    custom_emoji_url: Optional[str] = None
    custom_emoji_dark_url: Optional[str] = None


class SpaceBookmark(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    display_type: Optional[str] = None
    links: Optional[List[SpaceBookmarkLink]] = None

SpaceBookmarkList = PaginatedResponse[SpaceBookmark]


class HeadlessSpaceTopic(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    admin_only: Optional[bool] = None

HeadlessSpaceTopicList = PaginatedResponse[HeadlessSpaceTopic]
