"""Admin API -- Spaces, Space Groups, Space Members."""
from __future__ import annotations
from typing import Any, Dict, Optional, Tuple
from circle.constants import ADMIN_V2_PREFIX as _P
from circle.http import AsyncTransport, SyncTransport
from circle.models.admin.spaces import (
    Space, SpaceList, SpaceCreateResponse, SpaceGroup, SpaceGroupList,
    SpaceMember, SpaceMemberList, SpaceGroupMember, SpaceGroupMemberList, SpaceAISummary,
)

# -- Request descriptor type: (method, path, kwargs) --
_Req = Tuple[str, str, Dict[str, Any]]


# -- Spaces helpers --

def _list_spaces(page: int, per_page: int, sort: Optional[str]) -> _Req:
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if sort:
        p["sort"] = sort
    return "GET", f"{_P}/spaces", {"params": p}


def _create_space(kwargs: Dict[str, Any]) -> _Req:
    return "POST", f"{_P}/spaces", {"json": kwargs}


def _show_space(space_id: int) -> _Req:
    return "GET", f"{_P}/spaces/{space_id}", {}


def _update_space(space_id: int, kwargs: Dict[str, Any]) -> _Req:
    return "PUT", f"{_P}/spaces/{space_id}", {"json": kwargs}


def _delete_space(space_id: int) -> _Req:
    return "DELETE", f"{_P}/spaces/{space_id}", {}


def _get_space_ai_summary(space_id: int, date_from: Optional[str],
                           first_unread_message_id: Optional[int]) -> _Req:
    p: Dict[str, Any] = {}
    if date_from:
        p["date_from"] = date_from
    if first_unread_message_id:
        p["first_unread_message_id"] = first_unread_message_id
    return "GET", f"{_P}/spaces/{space_id}/ai_summaries", {"params": p}


# -- Space Groups helpers --

def _list_space_groups(page: int, per_page: int, name: Optional[str]) -> _Req:
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if name:
        p["name"] = name
    return "GET", f"{_P}/space_groups", {"params": p}


def _create_space_group(name: str, slug: str, kwargs: Dict[str, Any]) -> _Req:
    return "POST", f"{_P}/space_groups", {"json": {"name": name, "slug": slug, **kwargs}}


def _show_space_group(space_group_id: int) -> _Req:
    return "GET", f"{_P}/space_groups/{space_group_id}", {}


def _update_space_group(space_group_id: int, kwargs: Dict[str, Any]) -> _Req:
    return "PUT", f"{_P}/space_groups/{space_group_id}", {"json": kwargs}


def _delete_space_group(space_group_id: int) -> _Req:
    return "DELETE", f"{_P}/space_groups/{space_group_id}", {}


# -- Space Members helpers --

def _list_space_members(space_id: int, page: int, per_page: int,
                        status: Optional[str]) -> _Req:
    p: Dict[str, Any] = {"space_id": space_id, "page": page, "per_page": per_page}
    if status:
        p["status"] = status
    return "GET", f"{_P}/space_members", {"params": p}


def _show_space_member(email: str, space_id: int) -> _Req:
    return "GET", f"{_P}/space_member", {"params": {"email": email, "space_id": space_id}}


def _add_space_member(email: str, space_id: int) -> _Req:
    return "POST", f"{_P}/space_members", {"json": {"email": email, "space_id": space_id}}


def _remove_space_member(email: str, space_id: int) -> _Req:
    return "DELETE", f"{_P}/space_members", {"params": {"email": email, "space_id": space_id}}


# -- Space Group Members helpers --

def _list_space_group_members(space_group_id: int, page: int, per_page: int,
                              status: Optional[str]) -> _Req:
    p: Dict[str, Any] = {"space_group_id": space_group_id, "page": page, "per_page": per_page}
    if status:
        p["status"] = status
    return "GET", f"{_P}/space_group_members", {"params": p}


def _show_space_group_member(email: str, space_group_id: int) -> _Req:
    return "GET", f"{_P}/space_group_member", {"params": {"email": email, "space_group_id": space_group_id}}


def _create_space_group_member(email: str, space_group_id: int) -> _Req:
    return "POST", f"{_P}/space_group_members", {"json": {"email": email, "space_group_id": space_group_id}}


def _destroy_space_group_member(email: str, space_group_id: int) -> _Req:
    return "DELETE", f"{_P}/space_group_members", {"params": {"email": email, "space_group_id": space_group_id}}


# ---------------------------------------------------------------------------
# Sync client
# ---------------------------------------------------------------------------

class SpacesClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    # -- Spaces --
    def list_spaces(self, *, page: int = 1, per_page: int = 60, sort: Optional[str] = None) -> SpaceList:
        m, p, kw = _list_spaces(page, per_page, sort)
        return SpaceList.model_validate(self._t.request(m, p, **kw))

    def create_space(self, **kwargs: Any) -> SpaceCreateResponse:
        m, p, kw = _create_space(kwargs)
        return SpaceCreateResponse.model_validate(self._t.request(m, p, **kw))

    def show_space(self, space_id: int) -> Space:
        m, p, kw = _show_space(space_id)
        return Space.model_validate(self._t.request(m, p, **kw))

    def update_space(self, space_id: int, **kwargs: Any) -> Space:
        m, p, kw = _update_space(space_id, kwargs)
        return Space.model_validate(self._t.request(m, p, **kw))

    def delete_space(self, space_id: int) -> Dict[str, Any]:
        m, p, kw = _delete_space(space_id)
        return self._t.request(m, p, **kw)

    def get_space_ai_summary(self, space_id: int, *, date_from: Optional[str] = None,
                             first_unread_message_id: Optional[int] = None) -> SpaceAISummary:
        m, p, kw = _get_space_ai_summary(space_id, date_from, first_unread_message_id)
        return SpaceAISummary.model_validate(self._t.request(m, p, **kw))

    # -- Space Groups --
    def list_space_groups(self, *, page: int = 1, per_page: int = 60, name: Optional[str] = None) -> SpaceGroupList:
        m, p, kw = _list_space_groups(page, per_page, name)
        return SpaceGroupList.model_validate(self._t.request(m, p, **kw))

    def create_space_group(self, *, name: str, slug: str, **kwargs: Any) -> SpaceGroup:
        m, p, kw = _create_space_group(name, slug, kwargs)
        return SpaceGroup.model_validate(self._t.request(m, p, **kw))

    def show_space_group(self, space_group_id: int) -> SpaceGroup:
        m, p, kw = _show_space_group(space_group_id)
        return SpaceGroup.model_validate(self._t.request(m, p, **kw))

    def update_space_group(self, space_group_id: int, **kwargs: Any) -> SpaceGroup:
        m, p, kw = _update_space_group(space_group_id, kwargs)
        return SpaceGroup.model_validate(self._t.request(m, p, **kw))

    def delete_space_group(self, space_group_id: int) -> Dict[str, Any]:
        m, p, kw = _delete_space_group(space_group_id)
        return self._t.request(m, p, **kw)

    # -- Space Members --
    def list_space_members(self, *, space_id: int, page: int = 1, per_page: int = 60,
                           status: Optional[str] = None) -> SpaceMemberList:
        m, p, kw = _list_space_members(space_id, page, per_page, status)
        return SpaceMemberList.model_validate(self._t.request(m, p, **kw))

    def show_space_member(self, *, email: str, space_id: int) -> SpaceMember:
        m, p, kw = _show_space_member(email, space_id)
        return SpaceMember.model_validate(self._t.request(m, p, **kw))

    def add_space_member(self, *, email: str, space_id: int) -> Dict[str, Any]:
        m, p, kw = _add_space_member(email, space_id)
        return self._t.request(m, p, **kw)

    def remove_space_member(self, *, email: str, space_id: int) -> Dict[str, Any]:
        m, p, kw = _remove_space_member(email, space_id)
        return self._t.request(m, p, **kw)

    # -- Space Group Members --
    def list_space_group_members(self, *, space_group_id: int, page: int = 1, per_page: int = 60,
                                 status: Optional[str] = None) -> SpaceGroupMemberList:
        m, p, kw = _list_space_group_members(space_group_id, page, per_page, status)
        return SpaceGroupMemberList.model_validate(self._t.request(m, p, **kw))

    def show_space_group_member(self, *, email: str, space_group_id: int) -> SpaceGroupMember:
        m, p, kw = _show_space_group_member(email, space_group_id)
        return SpaceGroupMember.model_validate(self._t.request(m, p, **kw))

    def create_space_group_member(self, *, email: str, space_group_id: int) -> Dict[str, Any]:
        m, p, kw = _create_space_group_member(email, space_group_id)
        return self._t.request(m, p, **kw)

    def destroy_space_group_member(self, *, email: str, space_group_id: int) -> Dict[str, Any]:
        m, p, kw = _destroy_space_group_member(email, space_group_id)
        return self._t.request(m, p, **kw)


# ---------------------------------------------------------------------------
# Async client
# ---------------------------------------------------------------------------

class AsyncSpacesClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    # -- Spaces --
    async def list_spaces(self, *, page: int = 1, per_page: int = 60, sort: Optional[str] = None) -> SpaceList:
        m, p, kw = _list_spaces(page, per_page, sort)
        return SpaceList.model_validate(await self._t.request(m, p, **kw))

    async def create_space(self, **kwargs: Any) -> SpaceCreateResponse:
        m, p, kw = _create_space(kwargs)
        return SpaceCreateResponse.model_validate(await self._t.request(m, p, **kw))

    async def show_space(self, space_id: int) -> Space:
        m, p, kw = _show_space(space_id)
        return Space.model_validate(await self._t.request(m, p, **kw))

    async def update_space(self, space_id: int, **kwargs: Any) -> Space:
        m, p, kw = _update_space(space_id, kwargs)
        return Space.model_validate(await self._t.request(m, p, **kw))

    async def delete_space(self, space_id: int) -> Dict[str, Any]:
        m, p, kw = _delete_space(space_id)
        return await self._t.request(m, p, **kw)

    async def get_space_ai_summary(self, space_id: int, *, date_from: Optional[str] = None,
                                   first_unread_message_id: Optional[int] = None) -> SpaceAISummary:
        m, p, kw = _get_space_ai_summary(space_id, date_from, first_unread_message_id)
        return SpaceAISummary.model_validate(await self._t.request(m, p, **kw))

    # -- Space Groups --
    async def list_space_groups(self, *, page: int = 1, per_page: int = 60,
                                name: Optional[str] = None) -> SpaceGroupList:
        m, p, kw = _list_space_groups(page, per_page, name)
        return SpaceGroupList.model_validate(await self._t.request(m, p, **kw))

    async def create_space_group(self, *, name: str, slug: str, **kwargs: Any) -> SpaceGroup:
        m, p, kw = _create_space_group(name, slug, kwargs)
        return SpaceGroup.model_validate(await self._t.request(m, p, **kw))

    async def show_space_group(self, space_group_id: int) -> SpaceGroup:
        m, p, kw = _show_space_group(space_group_id)
        return SpaceGroup.model_validate(await self._t.request(m, p, **kw))

    async def update_space_group(self, space_group_id: int, **kwargs: Any) -> SpaceGroup:
        m, p, kw = _update_space_group(space_group_id, kwargs)
        return SpaceGroup.model_validate(await self._t.request(m, p, **kw))

    async def delete_space_group(self, space_group_id: int) -> Dict[str, Any]:
        m, p, kw = _delete_space_group(space_group_id)
        return await self._t.request(m, p, **kw)

    # -- Space Members --
    async def list_space_members(self, *, space_id: int, page: int = 1, per_page: int = 60,
                                 status: Optional[str] = None) -> SpaceMemberList:
        m, p, kw = _list_space_members(space_id, page, per_page, status)
        return SpaceMemberList.model_validate(await self._t.request(m, p, **kw))

    async def show_space_member(self, *, email: str, space_id: int) -> SpaceMember:
        m, p, kw = _show_space_member(email, space_id)
        return SpaceMember.model_validate(await self._t.request(m, p, **kw))

    async def add_space_member(self, *, email: str, space_id: int) -> Dict[str, Any]:
        m, p, kw = _add_space_member(email, space_id)
        return await self._t.request(m, p, **kw)

    async def remove_space_member(self, *, email: str, space_id: int) -> Dict[str, Any]:
        m, p, kw = _remove_space_member(email, space_id)
        return await self._t.request(m, p, **kw)

    # -- Space Group Members --
    async def list_space_group_members(self, *, space_group_id: int, page: int = 1, per_page: int = 60,
                                       status: Optional[str] = None) -> SpaceGroupMemberList:
        m, p, kw = _list_space_group_members(space_group_id, page, per_page, status)
        return SpaceGroupMemberList.model_validate(await self._t.request(m, p, **kw))

    async def show_space_group_member(self, *, email: str, space_group_id: int) -> SpaceGroupMember:
        m, p, kw = _show_space_group_member(email, space_group_id)
        return SpaceGroupMember.model_validate(await self._t.request(m, p, **kw))

    async def create_space_group_member(self, *, email: str, space_group_id: int) -> Dict[str, Any]:
        m, p, kw = _create_space_group_member(email, space_group_id)
        return await self._t.request(m, p, **kw)

    async def destroy_space_group_member(self, *, email: str, space_group_id: int) -> Dict[str, Any]:
        m, p, kw = _destroy_space_group_member(email, space_group_id)
        return await self._t.request(m, p, **kw)
