"""Space, space group, and space member models."""
from __future__ import annotations
from typing import Any, List, Optional
from circle.models.base import CircleModel, PaginatedResponse


class SpaceGroupRef(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None


class CourseSetting(CircleModel):
    course_type: Optional[str] = None
    custom_lesson_label: Optional[str] = None
    custom_section_label: Optional[str] = None
    enforce_lessons_order: Optional[bool] = None
    new_comment_notification_enabled: Optional[bool] = None


class MetaTagAttributes(CircleModel):
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    opengraph_title: Optional[str] = None
    opengraph_description: Optional[str] = None
    opengraph_image: Optional[str] = None


class Space(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    cover_image_url: Optional[str] = None
    cover_image_visible: Optional[bool] = None
    cover_image_display_style: Optional[str] = None
    thumbnail_image_url: Optional[str] = None
    community_id: Optional[int] = None
    is_private: Optional[bool] = None
    is_hidden_from_non_members: Optional[bool] = None
    is_hidden: Optional[bool] = None
    emoji: Optional[str] = None
    custom_emoji_url: Optional[str] = None
    custom_emoji_dark_url: Optional[str] = None
    hide_post_settings: Optional[bool] = None
    display_view: Optional[str] = None
    is_post_disabled: Optional[bool] = None
    space_type: Optional[str] = None
    host: Optional[str] = None
    post_ids: Optional[List[int]] = None
    url: Optional[str] = None
    space_group: Optional[SpaceGroupRef] = None
    topics: Optional[List[int]] = None
    course_setting: Optional[CourseSetting] = None
    meta_tag_attributes: Optional[MetaTagAttributes] = None
    chat_room_show_history: Optional[bool] = None
    chat_room_description: Optional[str] = None
    default_in_app_notification_setting: Optional[str] = None
    default_mobile_notification_setting: Optional[str] = None
    default_notification_setting: Optional[str] = None
    default_mention_in_app_notification_setting: Optional[str] = None
    default_mention_mobile_notification_setting: Optional[str] = None
    event_auto_rsvp_enabled: Optional[bool] = None

SpaceList = PaginatedResponse[Space]


class SpaceCreateResponse(CircleModel):
    success: Optional[bool] = None
    message: Optional[str] = None
    space: Optional[Space] = None


class SpaceGroup(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    community_id: Optional[int] = None
    is_hidden_from_non_members: Optional[bool] = None
    hide_members_count: Optional[bool] = None
    allow_members_to_create_spaces: Optional[bool] = None
    automatically_add_members_to_new_spaces: Optional[bool] = None
    add_members_to_space_group_on_space_join: Optional[bool] = None
    hide_non_member_spaces_from_sidebar: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    space_group_members_count: Optional[int] = None
    spaces_count: Optional[int] = None

SpaceGroupList = PaginatedResponse[SpaceGroup]


class SpaceMemberCommunityMember(CircleModel):
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    headline: Optional[str] = None
    community_id: Optional[int] = None
    profile_url: Optional[str] = None
    public_uid: Optional[str] = None
    email: Optional[str] = None


class SpaceMember(CircleModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    space_id: Optional[int] = None
    notification_type: Optional[str] = None
    posts_read_count: Optional[int] = None
    in_app_notification_setting: Optional[str] = None
    community_member_id: Optional[int] = None
    moderator: Optional[bool] = None
    mobile_notification_setting: Optional[str] = None
    access_type: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    community_member: Optional[SpaceMemberCommunityMember] = None

SpaceMemberList = PaginatedResponse[SpaceMember]


class SpaceGroupMember(CircleModel):
    id: Optional[int] = None
    space_group_id: Optional[int] = None
    user_id: Optional[int] = None
    moderator: Optional[bool] = None
    community_member_id: Optional[int] = None
    access_type: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    community_member: Optional[SpaceMemberCommunityMember] = None

SpaceGroupMemberList = PaginatedResponse[SpaceGroupMember]


class SpaceAISummaryTopic(CircleModel):
    topic_name: Optional[str] = None
    summary: Optional[str] = None
    contributors: Optional[List[Any]] = None
    relevant_post_ids: Optional[List[int]] = None


class SpaceAISummary(CircleModel):
    overview: Optional[str] = None
    topics: Optional[List[SpaceAISummaryTopic]] = None
