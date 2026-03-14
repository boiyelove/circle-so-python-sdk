"""Misc admin models: access groups, forms, segments, invitations, embeds, uploads, live rooms, flagged content, search, leaderboard."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse


# -- Access Groups --

class AccessGroup(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    community_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

AccessGroupList = PaginatedResponse[AccessGroup]


class AccessGroupCommunityMember(CircleModel):
    id: Optional[int] = None
    access_group_id: Optional[int] = None
    community_member_id: Optional[int] = None
    community_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

AccessGroupCommunityMemberList = PaginatedResponse[AccessGroupCommunityMember]


# -- Forms --

class FormEmbedStyles(CircleModel):
    form: Optional[Dict[str, str]] = None
    button: Optional[Dict[str, str]] = None


class Form(CircleModel):
    id: Optional[int] = None
    uid: Optional[str] = None
    after_submission_action: Optional[str] = None
    embed_display_format: Optional[str] = None
    popup_delay: Optional[int] = None
    popup_frequency: Optional[int] = None
    name: Optional[str] = None
    redirect_url: Optional[str] = None
    status: Optional[str] = None
    thank_you_page_body: Optional[str] = None
    thank_you_page_title: Optional[str] = None
    updated_at: Optional[str] = None
    submissions_count: Optional[int] = None
    embed_styles: Optional[FormEmbedStyles] = None
    standalone_page_styles: Optional[FormEmbedStyles] = None
    elements: Optional[List[Any]] = None

FormList = PaginatedResponse[Form]


class FormSubmissionField(CircleModel):
    field_id: Optional[int] = None
    label: Optional[str] = None
    value: Optional[Any] = None
    hidden: Optional[bool] = None


class FormSubmission(CircleModel):
    id: Optional[int] = None
    created_at: Optional[str] = None
    fields: Optional[List[FormSubmissionField]] = None

FormSubmissionList = PaginatedResponse[FormSubmission]


# -- Community Segments --

class SegmentCreatedBy(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    public_uid: Optional[str] = None


class CommunitySegment(CircleModel):
    id: Optional[int] = None
    title: Optional[str] = None
    rules: Optional[Dict[str, Any]] = None
    visible: Optional[bool] = None
    audience_count: Optional[int] = None
    created_by: Optional[SegmentCreatedBy] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

CommunitySegmentList = PaginatedResponse[CommunitySegment]


# -- Invitation Links --

class InvitationLink(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    active: Optional[bool] = None
    members_joined_count: Optional[int] = None
    redirect_space_id: Optional[int] = None

InvitationLinkList = PaginatedResponse[InvitationLink]


# -- Embeds --

class Embed(CircleModel):
    id: Optional[int] = None
    url: Optional[str] = None
    sgid: Optional[str] = None
    type: Optional[str] = None
    embed_type: Optional[str] = None
    embed_provider: Optional[str] = None
    circle_embed_url: Optional[str] = None
    html: Optional[str] = None
    title: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    version: Optional[str] = None
    author_url: Optional[str] = None
    author_name: Optional[str] = None
    description: Optional[str] = None
    provider_url: Optional[str] = None
    provider_name: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail_width: Optional[int] = None
    thumbnail_height: Optional[int] = None


# -- Direct Uploads --

class DirectUploadInfo(CircleModel):
    url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None


class DirectUpload(CircleModel):
    id: Optional[int] = None
    key: Optional[str] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None
    byte_size: Optional[int] = None
    checksum: Optional[str] = None
    created_at: Optional[str] = None
    metadata: Optional[Any] = None
    service_name: Optional[str] = None
    signed_id: Optional[str] = None
    attachable_sgid: Optional[str] = None
    direct_upload: Optional[DirectUploadInfo] = None
    url: Optional[str] = None


# -- Live Rooms --

class LiveRoom(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[str] = None
    room_type: Optional[str] = None
    created_at: Optional[str] = None
    live_at: Optional[str] = None
    closed_at: Optional[str] = None
    recording_enabled: Optional[bool] = None
    slug: Optional[str] = None

LiveRoomList = PaginatedResponse[LiveRoom]


# -- Flagged Content --

class FlaggedContent(CircleModel):
    id: Optional[int] = None
    status: Optional[str] = None
    reported_reason_type: Optional[str] = None
    reported_reason_body: Optional[str] = None
    reported_at: Optional[str] = None
    action_taken_at: Optional[str] = None
    action_reason_body: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    content_id: Optional[int] = None
    content_type: Optional[str] = None
    content_authored_by_id: Optional[int] = None
    content_authored_by_name: Optional[str] = None
    content_authored_by_email: Optional[str] = None
    reported_by_id: Optional[int] = None
    reported_by_name: Optional[str] = None
    reported_by_email: Optional[str] = None
    action_by_id: Optional[int] = None
    action_by_name: Optional[str] = None
    action_by_email: Optional[str] = None

FlaggedContentList = PaginatedResponse[FlaggedContent]


# -- Leaderboard --

class LeaderboardMember(CircleModel):
    community_member_id: Optional[int] = None
    name: Optional[str] = None
    public_uid: Optional[str] = None
    headline: Optional[str] = None
    avatar_url: Optional[str] = None
    total_points: Optional[int] = None


# -- Advanced Search --

class AdvancedSearchedPost(CircleModel):
    id: Optional[int] = None
    type: Optional[str] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None
    status: Optional[str] = None
    highlighted_name: Optional[str] = None
    cover_image_url: Optional[str] = None
    body: Optional[str] = None
    highlighted_body: Optional[str] = None
    sgid: Optional[str] = None
    starts_at: Optional[str] = None
    author: Optional[Dict[str, Any]] = None
    space: Optional[Dict[str, Any]] = None


class AdvancedSearchResults(CircleModel):
    page: Optional[int] = None
    per_page: Optional[int] = None
    has_next_page: Optional[bool] = None
    count: Optional[int] = None
    page_count: Optional[int] = None
    records: Optional[List[Any]] = None
