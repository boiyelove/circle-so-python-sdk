"""Headless misc models: bookmarks, search, events, direct uploads, community links."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse


class BookmarkRecord(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    created_at: Optional[str] = None
    url: Optional[str] = None
    body: Optional[str] = None
    attachment_count: Optional[int] = None
    author: Optional[Dict[str, Any]] = None
    space: Optional[Dict[str, Any]] = None
    is_deleted: Optional[bool] = None


class Bookmark(CircleModel):
    id: Optional[int] = None
    record_id: Optional[int] = None
    bookmarkable_type: Optional[str] = None
    created_at: Optional[str] = None
    community_id: Optional[int] = None
    community_member_id: Optional[int] = None
    bookmark_record: Optional[BookmarkRecord] = None

BookmarkList = PaginatedResponse[Bookmark]


class HeadlessEventAttendee(CircleModel):
    id: Optional[int] = None
    community_member_id: Optional[int] = None
    contact_id: Optional[int] = None
    contact_type: Optional[str] = None
    avatar_url: Optional[str] = None
    rsvp_date: Optional[str] = None
    rsvp_status: Optional[str] = None
    name: Optional[str] = None

HeadlessEventAttendeeList = PaginatedResponse[HeadlessEventAttendee]


class RecurringEvent(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    start_date: Optional[str] = None
    time_zone_abbreviations: Optional[str] = None
    time_zone: Optional[str] = None
    rsvped_event: Optional[bool] = None
    rsvp_count: Optional[int] = None
    rsvp_limit: Optional[int] = None

RecurringEventList = PaginatedResponse[RecurringEvent]


class SearchResultRecord(CircleModel):
    id: Optional[Any] = None
    type: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

SearchResults = PaginatedResponse[SearchResultRecord]


class HeadlessAdvancedSearchResults(CircleModel):
    page: Optional[int] = None
    per_page: Optional[int] = None
    has_next_page: Optional[bool] = None
    count: Optional[int] = None
    page_count: Optional[int] = None
    records: Optional[List[Any]] = None


class CommunityLink(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    community_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class HeadlessDirectUploadInfo(CircleModel):
    url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None


class HeadlessDirectUpload(CircleModel):
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
    direct_upload: Optional[HeadlessDirectUploadInfo] = None
    url: Optional[str] = None


class HeadlessPageProfileField(CircleModel):
    id: Optional[int] = None
    label: Optional[str] = None
    field_type: Optional[str] = None
    key: Optional[str] = None
    placeholder: Optional[str] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    allow_null: Optional[bool] = None
    platform_field: Optional[bool] = None
    number_options: Optional[Any] = None
    choices: Optional[List[Any]] = None

HeadlessPageProfileFieldList = PaginatedResponse[HeadlessPageProfileField]
