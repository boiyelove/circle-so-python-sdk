"""Community member models."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse


class MemberTagRef(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None


class ProfileFieldChoice(CircleModel):
    id: Optional[int] = None
    value: Optional[str] = None


class CommunityMemberProfileField(CircleModel):
    id: Optional[int] = None
    text: Optional[str] = None
    textarea: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    display_value: Optional[Any] = None
    community_member_choices: Optional[List[Any]] = None
    number_options: Optional[Any] = None
    choices: Optional[List[ProfileFieldChoice]] = None


class ProfileFieldPage(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    position: Optional[int] = None
    visible: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class MemberProfileField(CircleModel):
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
    community_member_profile_field: Optional[CommunityMemberProfileField] = None
    number_options: Optional[Any] = None
    choices: Optional[List[ProfileFieldChoice]] = None
    pages: Optional[List[ProfileFieldPage]] = None


class GamificationStats(CircleModel):
    community_member_id: Optional[int] = None
    total_points: Optional[int] = None
    current_level: Optional[int] = None
    current_level_name: Optional[str] = None
    points_to_next_level: Optional[int] = None
    level_progress: Optional[int] = None


class ActivityScore(CircleModel):
    activity_score: Optional[str] = None
    presence: Optional[str] = None
    participation: Optional[str] = None
    contribution: Optional[str] = None
    connection: Optional[str] = None


class CommunityMember(CircleModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    headline: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    community_id: Optional[int] = None
    last_seen_at: Optional[str] = None
    profile_confirmed_at: Optional[str] = None
    profile_url: Optional[str] = None
    public_uid: Optional[str] = None
    avatar_url: Optional[str] = None
    user_id: Optional[int] = None
    name: Optional[str] = None
    accepted_invitation: Optional[str] = None
    active: Optional[bool] = None
    sso_provider_user_id: Optional[str] = None
    flattened_profile_fields: Optional[Dict[str, Any]] = None
    posts_count: Optional[int] = None
    comments_count: Optional[int] = None
    member_tags: Optional[List[MemberTagRef]] = None
    profile_fields: Optional[List[MemberProfileField]] = None
    gamification_stats: Optional[GamificationStats] = None
    activity_score: Optional[ActivityScore] = None


CommunityMemberList = PaginatedResponse[CommunityMember]


class CommunityMemberCreated(CircleModel):
    message: Optional[str] = None
    community_member: Optional[CommunityMember] = None
