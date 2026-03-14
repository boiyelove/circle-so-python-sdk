"""Event and event attendee models."""
from __future__ import annotations
from typing import List, Optional
from circle.models.base import CircleModel, PaginatedResponse


class EventSpace(CircleModel):
    id: Optional[int] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    community_id: Optional[int] = None


class Event(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    user_id: Optional[int] = None
    community_member_id: Optional[int] = None
    created_at: Optional[str] = None
    hide_meta_info: Optional[bool] = None
    confirmation_message_title: Optional[str] = None
    confirmation_message_button_title: Optional[str] = None
    confirmation_message_button_link: Optional[str] = None
    confirmation_message_description: Optional[str] = None
    in_person_location: Optional[str] = None
    host: Optional[str] = None
    comments_count: Optional[int] = None
    duration_in_seconds: Optional[int] = None
    enable_custom_thank_you_message: Optional[bool] = None
    send_in_app_notification_confirmation: Optional[bool] = None
    rsvp_disabled: Optional[bool] = None
    send_email_confirmation: Optional[bool] = None
    send_email_reminder: Optional[bool] = None
    send_in_app_notification_reminder: Optional[bool] = None
    virtual_location_url: Optional[str] = None
    starts_at: Optional[str] = None
    location_type: Optional[str] = None
    hide_attendees: Optional[bool] = None
    ends_at: Optional[str] = None
    updated_at: Optional[str] = None
    hide_location_from_non_attendees: Optional[bool] = None
    space: Optional[EventSpace] = None
    body: Optional[str] = None
    url: Optional[str] = None
    member_email: Optional[str] = None
    member_name: Optional[str] = None
    member_avatar_url: Optional[str] = None
    zapier_display_title: Optional[str] = None
    likes_count: Optional[int] = None
    cover_image_url: Optional[str] = None
    topics: Optional[List[int]] = None

EventList = PaginatedResponse[Event]


class EventAttendee(CircleModel):
    id: Optional[int] = None
    event_id: Optional[int] = None
    event_name: Optional[str] = None
    member_name: Optional[str] = None
    member_email: Optional[str] = None
    member_avatar_url: Optional[str] = None
    headline: Optional[str] = None
    rsvp_date: Optional[str] = None

EventAttendeeList = PaginatedResponse[EventAttendee]
