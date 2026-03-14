"""Headless Client API -- Chat, Notifications, Members, Events."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.http import AsyncTransport, SyncTransport
from circle.models.headless.chat import (
    ChatRoom, ChatRoomList, ChatRoomMessage, ChatRoomMessages, ChatRoomParticipantList,
    ChatThread, ChatThreadList, UnreadChatRooms, CreateReactionResponse,
)
from circle.models.headless.notifications import (
    Notification, NotificationList, NewNotificationsCount, ResetNewNotificationsCount,
)
from circle.models.headless.members import (
    BasicCommunityMemberList, CurrentCommunityMember, PublicProfile, ProfileUpdateResponse, SearchedMemberList,
)
from circle.models.headless.posts import HeadlessPostList
from circle.models.headless.comments import HeadlessCommentList
from circle.models.headless.spaces import HeadlessSpaceList
from circle.models.headless.misc import (
    HeadlessEventAttendee, HeadlessEventAttendeeList, RecurringEventList,
)

_P = "/api/headless/v1"


class HeadlessChatNotifMembersClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    # -- Chat Rooms --
    def list_chat_rooms(self, *, page: int = 1, per_page: int = 10) -> ChatRoomList:
        return ChatRoomList.model_validate(
            self._t.request("GET", f"{_P}/messages", params={"page": page, "per_page": per_page}))

    def create_chat_room(self, **kwargs: Any) -> ChatRoom:
        return ChatRoom.model_validate(self._t.request("POST", f"{_P}/messages", json={"chat_room": kwargs}))

    def get_chat_room(self, uuid: str) -> ChatRoom:
        return ChatRoom.model_validate(self._t.request("GET", f"{_P}/messages/{uuid}"))

    def list_chat_messages(self, chat_room_uuid: str, *, id: Optional[int] = None,
                           previous_per_page: Optional[int] = None,
                           next_per_page: Optional[int] = None) -> ChatRoomMessages:
        p: Dict[str, Any] = {}
        if id is not None: p["id"] = id
        if previous_per_page is not None: p["previous_per_page"] = previous_per_page
        if next_per_page is not None: p["next_per_page"] = next_per_page
        return ChatRoomMessages.model_validate(
            self._t.request("GET", f"{_P}/messages/{chat_room_uuid}/chat_room_messages", params=p))

    def create_chat_message(self, chat_room_uuid: str, **kwargs: Any) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/messages/{chat_room_uuid}/chat_room_messages", json=kwargs)

    def get_chat_message(self, chat_room_uuid: str, message_id: int) -> ChatRoomMessage:
        return ChatRoomMessage.model_validate(
            self._t.request("GET", f"{_P}/messages/{chat_room_uuid}/chat_room_messages/{message_id}"))

    def update_chat_message(self, chat_room_uuid: str, message_id: int, **kwargs: Any) -> ChatRoomMessage:
        return ChatRoomMessage.model_validate(
            self._t.request("PUT", f"{_P}/messages/{chat_room_uuid}/chat_room_messages/{message_id}", json=kwargs))

    def delete_chat_message(self, chat_room_uuid: str, message_id: int) -> None:
        self._t.request("DELETE", f"{_P}/messages/{chat_room_uuid}/chat_room_messages/{message_id}")

    def list_chat_participants(self, chat_room_uuid: str, *, page: int = 1,
                               per_page: int = 50) -> ChatRoomParticipantList:
        return ChatRoomParticipantList.model_validate(
            self._t.request("GET", f"{_P}/messages/{chat_room_uuid}/chat_room_participants",
                            params={"page": page, "per_page": per_page}))

    def update_chat_participant(self, chat_room_uuid: str, participant_id: int, **kwargs: Any) -> ChatRoom:
        return ChatRoom.model_validate(
            self._t.request("PUT", f"{_P}/messages/{chat_room_uuid}/chat_room_participants/{participant_id}",
                            json=kwargs))

    def mark_chat_as_read(self, uuid: str) -> None:
        self._t.request("POST", f"{_P}/messages/{uuid}/mark_all_as_read")

    def get_unread_chat_rooms(self) -> UnreadChatRooms:
        return UnreadChatRooms.model_validate(self._t.request("GET", f"{_P}/messages/unread_chat_rooms"))

    # -- Chat Threads --
    def list_chat_threads(self, *, page: int = 1, per_page: int = 10) -> ChatThreadList:
        return ChatThreadList.model_validate(
            self._t.request("GET", f"{_P}/chat_threads", params={"page": page, "per_page": per_page}))

    def get_chat_thread(self, thread_id: int) -> ChatThread:
        return ChatThread.model_validate(self._t.request("GET", f"{_P}/chat_threads/{thread_id}"))

    def get_unread_chat_threads(self) -> Dict[str, Any]:
        return self._t.request("GET", f"{_P}/chat_threads/unread_chat_threads")

    # -- Reactions --
    def create_reaction(self, *, chat_room_message: int, emoji: str) -> CreateReactionResponse:
        return CreateReactionResponse.model_validate(
            self._t.request("POST", f"{_P}/reactions",
                            json={"chat_room_message": chat_room_message, "emoji": emoji}))

    def delete_reaction(self, *, chat_room_message: int, emoji: str) -> None:
        self._t.request("DELETE", f"{_P}/reactions",
                        json={"chat_room_message": chat_room_message, "emoji": emoji})

    # -- Notifications --
    def list_notifications(self, *, page: int = 1, per_page: int = 20, sort: Optional[str] = None,
                           status: Optional[str] = None) -> NotificationList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if sort: p["sort"] = sort
        if status: p["status"] = status
        return NotificationList.model_validate(self._t.request("GET", f"{_P}/notifications", params=p))

    def mark_notification_read(self, notification_id: int) -> Notification:
        return Notification.model_validate(
            self._t.request("POST", f"{_P}/notifications/{notification_id}/mark_as_read"))

    def mark_all_notifications_read(self, **kwargs: Any) -> None:
        self._t.request("POST", f"{_P}/notifications/mark_all_as_read", json=kwargs)

    def delete_notification(self, notification_id: int) -> Notification:
        return Notification.model_validate(self._t.request("DELETE", f"{_P}/notifications/{notification_id}"))

    def archive_notification(self, notification_id: int) -> Notification:
        return Notification.model_validate(
            self._t.request("POST", f"{_P}/notifications/{notification_id}/archive"))

    def get_new_notifications_count(self) -> NewNotificationsCount:
        return NewNotificationsCount.model_validate(
            self._t.request("GET", f"{_P}/notifications/new_notifications_count"))

    def reset_notifications_count(self) -> ResetNewNotificationsCount:
        return ResetNewNotificationsCount.model_validate(
            self._t.request("POST", f"{_P}/notifications/reset_new_notifications_count"))

    # -- Community Members --
    def list_community_members(self, *, page: int = 1, per_page: int = 10, space_id: Optional[int] = None,
                               sort: Optional[str] = None, search_text: Optional[str] = None,
                               search_after: Optional[List[Any]] = None) -> BasicCommunityMemberList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if space_id: p["space_id"] = space_id
        if sort: p["sort"] = sort
        if search_text: p["search_text"] = search_text
        if search_after: p["search_after"] = search_after
        return BasicCommunityMemberList.model_validate(
            self._t.request("GET", f"{_P}/community_members", params=p))

    def get_current_member(self) -> CurrentCommunityMember:
        return CurrentCommunityMember.model_validate(self._t.request("GET", f"{_P}/community_member"))

    def get_public_profile(self, community_member_id: int) -> PublicProfile:
        return PublicProfile.model_validate(
            self._t.request("GET", f"{_P}/community_members/{community_member_id}/public_profile"))

    def update_profile(self, **kwargs: Any) -> ProfileUpdateResponse:
        return ProfileUpdateResponse.model_validate(
            self._t.request("PUT", f"{_P}/profile", json={"community_member": kwargs}))

    def confirm_profile(self, **kwargs: Any) -> ProfileUpdateResponse:
        return ProfileUpdateResponse.model_validate(
            self._t.request("PUT", f"{_P}/signup/profile", json={"community_member": kwargs}))

    def deactivate_member(self) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/community_member/deactivate")

    def search_members(self, **kwargs: Any) -> SearchedMemberList:
        return SearchedMemberList.model_validate(
            self._t.request("POST", f"{_P}/search/community_members", json=kwargs))

    def get_member_posts(self, community_member_id: int, *, page: int = 1,
                         per_page: int = 10) -> HeadlessPostList:
        return HeadlessPostList.model_validate(
            self._t.request("GET", f"{_P}/community_members/{community_member_id}/posts",
                            params={"page": page, "per_page": per_page}))

    def get_member_comments(self, community_member_id: int, *, page: int = 1,
                            per_page: int = 10) -> HeadlessCommentList:
        return HeadlessCommentList.model_validate(
            self._t.request("GET", f"{_P}/community_members/{community_member_id}/comments",
                            params={"page": page, "per_page": per_page}))

    def get_member_spaces(self, community_member_id: int, *, page: int = 1,
                          per_page: int = 30) -> HeadlessSpaceList:
        return HeadlessSpaceList.model_validate(
            self._t.request("GET", f"{_P}/community_members/{community_member_id}/spaces",
                            params={"page": page, "per_page": per_page}))

    # -- Events --
    def list_community_events(self, *, page: int = 1, per_page: int = 10, **kwargs: Any) -> Dict[str, Any]:
        p: Dict[str, Any] = {"page": page, "per_page": per_page, **kwargs}
        return self._t.request("GET", f"{_P}/community_events", params=p)

    def create_event_attendee(self, event_id: int) -> HeadlessEventAttendee:
        return HeadlessEventAttendee.model_validate(
            self._t.request("POST", f"{_P}/events/{event_id}/event_attendees"))

    def delete_event_attendee(self, event_id: int) -> HeadlessEventAttendee:
        return HeadlessEventAttendee.model_validate(
            self._t.request("DELETE", f"{_P}/events/{event_id}/event_attendees"))

    def list_event_attendees(self, event_id: int, *, page: int = 1,
                             per_page: int = 10) -> HeadlessEventAttendeeList:
        return HeadlessEventAttendeeList.model_validate(
            self._t.request("GET", f"{_P}/events/{event_id}/event_attendees",
                            params={"page": page, "per_page": per_page}))

    def list_recurring_events(self, space_id: int, event_id: int, *, page: int = 1,
                              per_page: int = 10) -> RecurringEventList:
        return RecurringEventList.model_validate(
            self._t.request("GET", f"{_P}/spaces/{space_id}/events/{event_id}/recurring_events",
                            params={"page": page, "per_page": per_page}))

    def rsvp_recurring_events(self, space_id: int, event_id: int, *, event_ids: List[int]) -> Dict[str, Any]:
        return self._t.request("PUT", f"{_P}/spaces/{space_id}/events/{event_id}/recurring_events/rsvp",
                               json={"event_ids": event_ids})


class AsyncHeadlessChatNotifMembersClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def list_chat_rooms(self, *, page: int = 1, per_page: int = 10) -> ChatRoomList:
        return ChatRoomList.model_validate(
            await self._t.request("GET", f"{_P}/messages", params={"page": page, "per_page": per_page}))

    async def create_chat_room(self, **kwargs: Any) -> ChatRoom:
        return ChatRoom.model_validate(await self._t.request("POST", f"{_P}/messages", json={"chat_room": kwargs}))

    async def get_chat_room(self, uuid: str) -> ChatRoom:
        return ChatRoom.model_validate(await self._t.request("GET", f"{_P}/messages/{uuid}"))

    async def list_chat_messages(self, chat_room_uuid: str, *, id: Optional[int] = None,
                                 previous_per_page: Optional[int] = None,
                                 next_per_page: Optional[int] = None) -> ChatRoomMessages:
        p: Dict[str, Any] = {}
        if id is not None: p["id"] = id
        if previous_per_page is not None: p["previous_per_page"] = previous_per_page
        if next_per_page is not None: p["next_per_page"] = next_per_page
        return ChatRoomMessages.model_validate(
            await self._t.request("GET", f"{_P}/messages/{chat_room_uuid}/chat_room_messages", params=p))

    async def create_chat_message(self, chat_room_uuid: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/messages/{chat_room_uuid}/chat_room_messages", json=kwargs)

    async def get_chat_message(self, chat_room_uuid: str, message_id: int) -> ChatRoomMessage:
        return ChatRoomMessage.model_validate(
            await self._t.request("GET", f"{_P}/messages/{chat_room_uuid}/chat_room_messages/{message_id}"))

    async def update_chat_message(self, chat_room_uuid: str, message_id: int, **kwargs: Any) -> ChatRoomMessage:
        return ChatRoomMessage.model_validate(
            await self._t.request("PUT", f"{_P}/messages/{chat_room_uuid}/chat_room_messages/{message_id}",
                                  json=kwargs))

    async def delete_chat_message(self, chat_room_uuid: str, message_id: int) -> None:
        await self._t.request("DELETE", f"{_P}/messages/{chat_room_uuid}/chat_room_messages/{message_id}")

    async def list_chat_participants(self, chat_room_uuid: str, *, page: int = 1,
                                     per_page: int = 50) -> ChatRoomParticipantList:
        return ChatRoomParticipantList.model_validate(
            await self._t.request("GET", f"{_P}/messages/{chat_room_uuid}/chat_room_participants",
                                  params={"page": page, "per_page": per_page}))

    async def update_chat_participant(self, chat_room_uuid: str, participant_id: int, **kwargs: Any) -> ChatRoom:
        return ChatRoom.model_validate(
            await self._t.request("PUT", f"{_P}/messages/{chat_room_uuid}/chat_room_participants/{participant_id}",
                                  json=kwargs))

    async def mark_chat_as_read(self, uuid: str) -> None:
        await self._t.request("POST", f"{_P}/messages/{uuid}/mark_all_as_read")

    async def get_unread_chat_rooms(self) -> UnreadChatRooms:
        return UnreadChatRooms.model_validate(await self._t.request("GET", f"{_P}/messages/unread_chat_rooms"))

    async def list_chat_threads(self, *, page: int = 1, per_page: int = 10) -> ChatThreadList:
        return ChatThreadList.model_validate(
            await self._t.request("GET", f"{_P}/chat_threads", params={"page": page, "per_page": per_page}))

    async def get_chat_thread(self, thread_id: int) -> ChatThread:
        return ChatThread.model_validate(await self._t.request("GET", f"{_P}/chat_threads/{thread_id}"))

    async def get_unread_chat_threads(self) -> Dict[str, Any]:
        return await self._t.request("GET", f"{_P}/chat_threads/unread_chat_threads")

    async def create_reaction(self, *, chat_room_message: int, emoji: str) -> CreateReactionResponse:
        return CreateReactionResponse.model_validate(
            await self._t.request("POST", f"{_P}/reactions",
                                  json={"chat_room_message": chat_room_message, "emoji": emoji}))

    async def delete_reaction(self, *, chat_room_message: int, emoji: str) -> None:
        await self._t.request("DELETE", f"{_P}/reactions",
                              json={"chat_room_message": chat_room_message, "emoji": emoji})

    async def list_notifications(self, *, page: int = 1, per_page: int = 20, sort: Optional[str] = None,
                                 status: Optional[str] = None) -> NotificationList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if sort: p["sort"] = sort
        if status: p["status"] = status
        return NotificationList.model_validate(await self._t.request("GET", f"{_P}/notifications", params=p))

    async def mark_notification_read(self, notification_id: int) -> Notification:
        return Notification.model_validate(
            await self._t.request("POST", f"{_P}/notifications/{notification_id}/mark_as_read"))

    async def mark_all_notifications_read(self, **kwargs: Any) -> None:
        await self._t.request("POST", f"{_P}/notifications/mark_all_as_read", json=kwargs)

    async def delete_notification(self, notification_id: int) -> Notification:
        return Notification.model_validate(await self._t.request("DELETE", f"{_P}/notifications/{notification_id}"))

    async def archive_notification(self, notification_id: int) -> Notification:
        return Notification.model_validate(
            await self._t.request("POST", f"{_P}/notifications/{notification_id}/archive"))

    async def get_new_notifications_count(self) -> NewNotificationsCount:
        return NewNotificationsCount.model_validate(
            await self._t.request("GET", f"{_P}/notifications/new_notifications_count"))

    async def reset_notifications_count(self) -> ResetNewNotificationsCount:
        return ResetNewNotificationsCount.model_validate(
            await self._t.request("POST", f"{_P}/notifications/reset_new_notifications_count"))

    async def list_community_members(self, *, page: int = 1, per_page: int = 10, space_id: Optional[int] = None,
                                     sort: Optional[str] = None, search_text: Optional[str] = None,
                                     search_after: Optional[List[Any]] = None) -> BasicCommunityMemberList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if space_id: p["space_id"] = space_id
        if sort: p["sort"] = sort
        if search_text: p["search_text"] = search_text
        if search_after: p["search_after"] = search_after
        return BasicCommunityMemberList.model_validate(
            await self._t.request("GET", f"{_P}/community_members", params=p))

    async def get_current_member(self) -> CurrentCommunityMember:
        return CurrentCommunityMember.model_validate(await self._t.request("GET", f"{_P}/community_member"))

    async def get_public_profile(self, community_member_id: int) -> PublicProfile:
        return PublicProfile.model_validate(
            await self._t.request("GET", f"{_P}/community_members/{community_member_id}/public_profile"))

    async def update_profile(self, **kwargs: Any) -> ProfileUpdateResponse:
        return ProfileUpdateResponse.model_validate(
            await self._t.request("PUT", f"{_P}/profile", json={"community_member": kwargs}))

    async def confirm_profile(self, **kwargs: Any) -> ProfileUpdateResponse:
        return ProfileUpdateResponse.model_validate(
            await self._t.request("PUT", f"{_P}/signup/profile", json={"community_member": kwargs}))

    async def deactivate_member(self) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/community_member/deactivate")

    async def search_members(self, **kwargs: Any) -> SearchedMemberList:
        return SearchedMemberList.model_validate(
            await self._t.request("POST", f"{_P}/search/community_members", json=kwargs))

    async def get_member_posts(self, community_member_id: int, *, page: int = 1,
                               per_page: int = 10) -> HeadlessPostList:
        return HeadlessPostList.model_validate(
            await self._t.request("GET", f"{_P}/community_members/{community_member_id}/posts",
                                  params={"page": page, "per_page": per_page}))

    async def get_member_comments(self, community_member_id: int, *, page: int = 1,
                                  per_page: int = 10) -> HeadlessCommentList:
        return HeadlessCommentList.model_validate(
            await self._t.request("GET", f"{_P}/community_members/{community_member_id}/comments",
                                  params={"page": page, "per_page": per_page}))

    async def get_member_spaces(self, community_member_id: int, *, page: int = 1,
                                per_page: int = 30) -> HeadlessSpaceList:
        return HeadlessSpaceList.model_validate(
            await self._t.request("GET", f"{_P}/community_members/{community_member_id}/spaces",
                                  params={"page": page, "per_page": per_page}))

    async def list_community_events(self, *, page: int = 1, per_page: int = 10, **kwargs: Any) -> Dict[str, Any]:
        p: Dict[str, Any] = {"page": page, "per_page": per_page, **kwargs}
        return await self._t.request("GET", f"{_P}/community_events", params=p)

    async def create_event_attendee(self, event_id: int) -> HeadlessEventAttendee:
        return HeadlessEventAttendee.model_validate(
            await self._t.request("POST", f"{_P}/events/{event_id}/event_attendees"))

    async def delete_event_attendee(self, event_id: int) -> HeadlessEventAttendee:
        return HeadlessEventAttendee.model_validate(
            await self._t.request("DELETE", f"{_P}/events/{event_id}/event_attendees"))

    async def list_event_attendees(self, event_id: int, *, page: int = 1,
                                   per_page: int = 10) -> HeadlessEventAttendeeList:
        return HeadlessEventAttendeeList.model_validate(
            await self._t.request("GET", f"{_P}/events/{event_id}/event_attendees",
                                  params={"page": page, "per_page": per_page}))

    async def list_recurring_events(self, space_id: int, event_id: int, *, page: int = 1,
                                    per_page: int = 10) -> RecurringEventList:
        return RecurringEventList.model_validate(
            await self._t.request("GET", f"{_P}/spaces/{space_id}/events/{event_id}/recurring_events",
                                  params={"page": page, "per_page": per_page}))

    async def rsvp_recurring_events(self, space_id: int, event_id: int, *, event_ids: List[int]) -> Dict[str, Any]:
        return await self._t.request("PUT", f"{_P}/spaces/{space_id}/events/{event_id}/recurring_events/rsvp",
                                     json={"event_ids": event_ids})
