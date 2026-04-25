"""Headless chat models."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse
from circle.models.admin.posts import TiptapBody


class ChatRoomParticipant(CircleModel):
    id: Optional[int] = None
    community_member_id: Optional[int] = None
    name: Optional[str] = None
    user_public_uid: Optional[str] = None
    avatar_url: Optional[str] = None
    muted: Optional[bool] = None
    archived: Optional[bool] = None
    last_seen_text: Optional[str] = None
    status: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    user_id: Optional[int] = None
    admin: Optional[bool] = None
    community_admin: Optional[bool] = None
    moderator: Optional[bool] = None
    deleted_at: Optional[str] = None
    can_send_message: Optional[bool] = None

ChatRoomParticipantList = PaginatedResponse[ChatRoomParticipant]


class ChatRoomMessageSender(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    community_member_id: Optional[int] = None
    user_public_uid: Optional[str] = None
    avatar_url: Optional[str] = None


class ChatRoomReaction(CircleModel):
    emoji: Optional[str] = None
    count: Optional[int] = None
    community_member_ids: Optional[List[int]] = None


class ChatRoomMessage(CircleModel):
    id: Optional[int] = None
    parent_message_id: Optional[int] = None
    edited_at: Optional[str] = None
    created_at: Optional[str] = None
    chat_room_uuid: Optional[str] = None
    chat_room_participant_id: Optional[int] = None
    body: Optional[str] = None
    bookmark_id: Optional[int] = None
    rich_text_body: Optional[TiptapBody] = None
    sent_at: Optional[str] = None
    replies_count: Optional[int] = None
    last_reply_at: Optional[str] = None
    total_thread_participants_count: Optional[int] = None
    thread_participants_preview: Optional[List[Any]] = None
    sender: Optional[ChatRoomMessageSender] = None
    chat_thread_id: Optional[int] = None
    reactions: Optional[List[ChatRoomReaction]] = None
    embedded_chat_message_access: Optional[List[Any]] = None


class ChatRoomMessages(CircleModel):
    id: Optional[int] = None
    has_next_page: Optional[bool] = None
    has_previous_page: Optional[bool] = None
    first_id: Optional[int] = None
    last_id: Optional[int] = None
    total_count: Optional[int] = None
    records: Optional[List[ChatRoomMessage]] = None


class ChatRoomLastMessage(CircleModel):
    id: Optional[int] = None
    parent_message_id: Optional[int] = None
    edited_at: Optional[str] = None
    created_at: Optional[str] = None
    chat_room_uuid: Optional[str] = None
    chat_room_participant_id: Optional[int] = None
    body: Optional[str] = None
    bookmark_id: Optional[int] = None
    rich_text_body: Optional[TiptapBody] = None


class ChatRoomDetail(CircleModel):
    id: Optional[int] = None
    uuid: Optional[str] = None
    identifier: Optional[str] = None
    unread_messages_count: Optional[int] = None
    chat_room_kind: Optional[str] = None
    chat_room_name: Optional[str] = None
    chat_room_description: Optional[str] = None
    chat_room_show_history: Optional[bool] = None
    chat_room_participants_count: Optional[int] = None
    other_participants_preview: Optional[List[ChatRoomParticipant]] = None
    current_participant: Optional[ChatRoomParticipant] = None
    last_message: Optional[ChatRoomLastMessage] = None
    first_unread_message_id: Optional[int] = None


class ChatRoom(CircleModel):
    """Deprecated: use ChatRoomDetail directly. Kept for backward compatibility."""
    chat_room: Optional[ChatRoomDetail] = None

ChatRoomList = PaginatedResponse[ChatRoomDetail]


class ChatThreadRoom(CircleModel):
    kind: Optional[str] = None
    name: Optional[str] = None
    embedded_space: Optional[Any] = None
    lesson: Optional[Any] = None


class ChatThread(CircleModel):
    id: Optional[int] = None
    parent_message: Optional[ChatRoomMessage] = None
    replies: Optional[List[ChatRoomMessage]] = None
    chat_room: Optional[ChatThreadRoom] = None

ChatThreadList = PaginatedResponse[ChatThread]


class UnreadChatRooms(CircleModel):
    chat_rooms: Optional[List[str]] = None


class CreateReactionResponse(CircleModel):
    success: Optional[bool] = None
    message: Optional[str] = None
    reaction: Optional[Dict[str, Any]] = None
