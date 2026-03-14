"""Headless notification models."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse


class NotificationNotifiable(CircleModel):
    id: Optional[int] = None
    community_id: Optional[int] = None
    space_id: Optional[int] = None
    parent_comment_id: Optional[int] = None
    post_id: Optional[int] = None


class Notification(CircleModel):
    id: Optional[int] = None
    created_at: Optional[str] = None
    read_at: Optional[str] = None
    action: Optional[str] = None
    notifiable_id: Optional[int] = None
    space_title: Optional[str] = None
    display_action: Optional[str] = None
    space_id: Optional[int] = None
    notification_text_structure: Optional[List[str]] = None
    actor_name: Optional[str] = None
    notifiable_title: Optional[str] = None
    actor_image: Optional[str] = None
    notifiable_type: Optional[str] = None
    action_web_url: Optional[str] = None
    notifiable: Optional[NotificationNotifiable] = None

NotificationList = PaginatedResponse[Notification]


class NewNotificationsCount(CircleModel):
    new_notifications_count: Optional[int] = None
    new_mentions_count: Optional[int] = None
    new_inbox_count: Optional[int] = None


class ResetNewNotificationsCount(CircleModel):
    new_notifications_count: Optional[int] = None


class NotificationPreference(CircleModel):
    type: Optional[Any] = None
    name: Optional[str] = None
    enabled: Optional[bool] = None


class SpacePreference(CircleModel):
    id: Optional[int] = None
    space_id: Optional[int] = None
    space_name: Optional[str] = None
    choice: Optional[str] = None
    is_chat_space: Optional[bool] = None


class MediumNotificationPreferences(CircleModel):
    notification_preferences: Optional[List[NotificationPreference]] = None
    space_preferences: Optional[List[SpacePreference]] = None


class SpaceMemberNotificationPreferences(CircleModel):
    in_app: Optional[str] = None
    push: Optional[str] = None
