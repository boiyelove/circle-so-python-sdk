"""Admin API -- Events & Event Attendees."""
from __future__ import annotations
from typing import Any, Dict, Optional
from circle.http import AsyncTransport, SyncTransport
from circle.models.admin.events import Event, EventList, EventAttendee, EventAttendeeList

_P = "/api/admin/v2"


class EventsClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    def list_events(self, *, page: int = 1, per_page: int = 60, space_id: Optional[int] = None,
                    sort: Optional[str] = None, **kwargs: Any) -> EventList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page, **kwargs}
        if space_id: p["space_id"] = space_id
        if sort: p["sort"] = sort
        return EventList.model_validate(self._t.request("GET", f"{_P}/events", params=p))

    def create_event(self, *, space_id: int, **kwargs: Any) -> Event:
        return Event.model_validate(
            self._t.request("POST", f"{_P}/events", json={"event": kwargs, "space_id": space_id}))

    def get_event(self, event_id: int) -> Event:
        return Event.model_validate(self._t.request("GET", f"{_P}/events/{event_id}"))

    def update_event(self, event_id: int, *, space_id: int, **kwargs: Any) -> Event:
        return Event.model_validate(
            self._t.request("PUT", f"{_P}/events/{event_id}", json={"event": kwargs, "space_id": space_id}))

    def delete_event(self, event_id: int, *, space_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/events/{event_id}", params={"space_id": space_id})

    def duplicate_event(self, space_id: int, event_id: int, **kwargs: Any) -> Event:
        return Event.model_validate(
            self._t.request("POST", f"{_P}/spaces/{space_id}/events/{event_id}/duplicate", json=kwargs))

    def list_event_attendees(self, *, event_id: int, page: int = 1, per_page: int = 10) -> EventAttendeeList:
        return EventAttendeeList.model_validate(
            self._t.request("GET", f"{_P}/event_attendees",
                            params={"event_id": event_id, "page": page, "per_page": per_page}))

    def create_event_attendee(self, *, event_id: int, member_email: str) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/event_attendees",
                               json={"event_id": event_id, "member_email": member_email})

    def delete_event_attendee(self, *, event_id: int, member_email: str) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/event_attendees",
                               json={"event_id": event_id, "member_email": member_email})


class AsyncEventsClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def list_events(self, *, page: int = 1, per_page: int = 60, space_id: Optional[int] = None,
                          sort: Optional[str] = None, **kwargs: Any) -> EventList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page, **kwargs}
        if space_id: p["space_id"] = space_id
        if sort: p["sort"] = sort
        return EventList.model_validate(await self._t.request("GET", f"{_P}/events", params=p))

    async def create_event(self, *, space_id: int, **kwargs: Any) -> Event:
        return Event.model_validate(
            await self._t.request("POST", f"{_P}/events", json={"event": kwargs, "space_id": space_id}))

    async def get_event(self, event_id: int) -> Event:
        return Event.model_validate(await self._t.request("GET", f"{_P}/events/{event_id}"))

    async def update_event(self, event_id: int, *, space_id: int, **kwargs: Any) -> Event:
        return Event.model_validate(
            await self._t.request("PUT", f"{_P}/events/{event_id}", json={"event": kwargs, "space_id": space_id}))

    async def delete_event(self, event_id: int, *, space_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/events/{event_id}", params={"space_id": space_id})

    async def duplicate_event(self, space_id: int, event_id: int, **kwargs: Any) -> Event:
        return Event.model_validate(
            await self._t.request("POST", f"{_P}/spaces/{space_id}/events/{event_id}/duplicate", json=kwargs))

    async def list_event_attendees(self, *, event_id: int, page: int = 1, per_page: int = 10) -> EventAttendeeList:
        return EventAttendeeList.model_validate(
            await self._t.request("GET", f"{_P}/event_attendees",
                                  params={"event_id": event_id, "page": page, "per_page": per_page}))

    async def create_event_attendee(self, *, event_id: int, member_email: str) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/event_attendees",
                                     json={"event_id": event_id, "member_email": member_email})

    async def delete_event_attendee(self, *, event_id: int, member_email: str) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/event_attendees",
                                     json={"event_id": event_id, "member_email": member_email})
