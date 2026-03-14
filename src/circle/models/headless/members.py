"""Headless member models."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse


class BasicCommunityMember(CircleModel):
    community_member_id: Optional[int] = None
    name: Optional[str] = None
    headline: Optional[str] = None
    avatar_url: Optional[str] = None
    member_tags: Optional[List[Any]] = None
    can_receive_dm_from_current_member: Optional[bool] = None
    messaging_enabled: Optional[bool] = None
    email: Optional[str] = None

BasicCommunityMemberList = PaginatedResponse[BasicCommunityMember]


class ProfileFieldDetail(CircleModel):
    id: Optional[int] = None
    label: Optional[str] = None
    field_type: Optional[str] = None
    key: Optional[str] = None
    placeholder: Optional[str] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    platform_field: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    choices: Optional[List[Any]] = None
    number_options: Optional[Any] = None
    community_member_profile_field: Optional[Any] = None


class ProfileFields(CircleModel):
    visible: Optional[List[ProfileFieldDetail]] = None
    not_visible: Optional[List[ProfileFieldDetail]] = None


class CurrentCommunityMember(CircleModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    public_uid: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    large_avatar_url: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    posts_count: Optional[int] = None
    comments_count: Optional[int] = None
    spaces_count: Optional[int] = None
    bookmarks_count: Optional[int] = None
    default_space_id: Optional[int] = None
    active: Optional[bool] = None
    profile_info: Optional[Dict[str, Any]] = None
    roles: Optional[Dict[str, bool]] = None
    features: Optional[Dict[str, Any]] = None
    member_tags: Optional[List[Any]] = None
    profile_fields: Optional[ProfileFields] = None
    gamification_stats: Optional[Dict[str, Any]] = None


class PublicProfile(CircleModel):
    id: Optional[int] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    posts_count: Optional[int] = None
    comments_count: Optional[int] = None
    spaces_count: Optional[int] = None
    can_receive_dm_from_current_member: Optional[bool] = None
    messaging_enabled: Optional[bool] = None
    profile_info: Optional[Dict[str, Any]] = None
    roles: Optional[Dict[str, bool]] = None
    member_tags: Optional[List[Any]] = None
    avatar_url: Optional[str] = None
    large_avatar_url: Optional[str] = None
    gamification_stats: Optional[Dict[str, Any]] = None
    community_member_id: Optional[int] = None


class ProfileUpdateResponse(CircleModel):
    message: Optional[str] = None
    current_community_member: Optional[Any] = None


class SearchedMember(CircleModel):
    admin: Optional[bool] = None
    avatar_url: Optional[str] = None
    first_name: Optional[str] = None
    headline: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    public_uid: Optional[str] = None
    user_id: Optional[int] = None
    id: Optional[int] = None
    is_deleted: Optional[bool] = None
    community_member_id: Optional[int] = None

SearchedMemberList = PaginatedResponse[SearchedMember]
