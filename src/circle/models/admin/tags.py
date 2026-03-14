"""Member tag, tagged member, and profile field models."""
from __future__ import annotations
from typing import List, Optional
from circle.models.base import CircleModel, PaginatedResponse


class MemberTagDisplayLocations(CircleModel):
    post_bio: Optional[bool] = None
    profile_page: Optional[bool] = None
    member_directory: Optional[bool] = None


class MemberTag(CircleModel):
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    name: Optional[str] = None
    is_public: Optional[bool] = None
    is_background_enabled: Optional[bool] = None
    tagged_members_count: Optional[int] = None
    color: Optional[str] = None
    display_format: Optional[str] = None
    emoji: Optional[str] = None
    custom_emoji_url: Optional[str] = None
    custom_emoji_dark_url: Optional[str] = None
    display_locations: Optional[MemberTagDisplayLocations] = None

MemberTagList = PaginatedResponse[MemberTag]


class TaggedMember(CircleModel):
    id: Optional[int] = None
    member_tag_id: Optional[int] = None
    member_tag_name: Optional[str] = None
    member_tag_emoji: Optional[str] = None
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    lead_id: Optional[int] = None
    lead_email: Optional[str] = None
    community_member_id: Optional[int] = None
    contact_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

TaggedMemberList = PaginatedResponse[TaggedMember]


class ProfileFieldNumberOptions(CircleModel):
    id: Optional[int] = None
    format: Optional[str] = None
    decimal: Optional[int] = None


class ProfileFieldChoice(CircleModel):
    id: Optional[int] = None
    value: Optional[str] = None


class ProfileFieldPage(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    position: Optional[int] = None
    visible: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ProfileField(CircleModel):
    id: Optional[int] = None
    label: Optional[str] = None
    field_type: Optional[str] = None
    key: Optional[str] = None
    placeholder: Optional[str] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    allow_null: Optional[bool] = None
    platform_field: Optional[bool] = None
    archived: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    number_options: Optional[ProfileFieldNumberOptions] = None
    choices: Optional[List[ProfileFieldChoice]] = None
    pages: Optional[List[ProfileFieldPage]] = None

ProfileFieldList = PaginatedResponse[ProfileField]
