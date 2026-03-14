"""Admin API -- Spaces, Space Groups, Space Members."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.http import AsyncTransport, SyncTransport
from circle.models.admin.spaces import (
    Space, SpaceList, SpaceCreateResponse, SpaceGroup, SpaceGroupList,
    SpaceMember, SpaceMemberList, SpaceGroupMember, SpaceGroupMemberList, SpaceAISummary,
)

_P = "/api/admin/v2"


class SpacesClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    # -- Spaces --
    def list_spaces(self, *, page: int = 1, per_page: int = 60, sort: Optional[str] = None) -> SpaceList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if sort: p["sort"] = sort
        return SpaceList.model_validate(self._t.request("GET", f"{_P}/spaces", params=p))

    def create_space(self, **kwargs: Any) -> SpaceCreateResponse:
        return SpaceCreateResponse.model_validate(self._t.request("POST", f"{_P}/spaces", json=kwargs))

    def show_space(self, space_id: int) -> Space:
        return Space.model_validate(self._t.request("GET", f"{_P}/spaces/{space_id}"))

    def update_space(self, space_id: int, **kwargs: Any) -> Space:
        return Space.model_validate(self._t.request("PUT", f"{_P}/spaces/{space_id}", json=kwargs))

    def delete_space(self, space_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/spaces/{space_id}")

    def get_space_ai_summary(self, space_id: int, *, date_from: Optional[str] = None,
                             first_unread_message_id: Optional[int] = None) -> SpaceAISummary:
        p: Dict[str, Any] = {}
        if date_from: p["date_from"] = date_from
        if first_unread_message_id: p["first_unread_message_id"] = first_unread_message_id
        return SpaceAISummary.model_validate(
            self._t.request("GET", f"{_P}/spaces/{space_id}/ai_summaries", params=p))

    # -- Space Groups --
    def list_space_groups(self, *, page: int = 1, per_page: int = 60, name: Optional[str] = None) -> SpaceGroupList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if name: p["name"] = name
        return SpaceGroupList.model_validate(self._t.request("GET", f"{_P}/space_groups", params=p))

    def create_space_group(self, *, name: str, slug: str, **kwargs: Any) -> SpaceGroup:
        return SpaceGroup.model_validate(
            self._t.request("POST", f"{_P}/space_groups", json={"name": name, "slug": slug, **kwargs}))

    def show_space_group(self, space_group_id: int) -> SpaceGroup:
        return SpaceGroup.model_validate(self._t.request("GET", f"{_P}/space_groups/{space_group_id}"))

    def update_space_group(self, space_group_id: int, **kwargs: Any) -> SpaceGroup:
        return SpaceGroup.model_validate(self._t.request("PUT", f"{_P}/space_groups/{space_group_id}", json=kwargs))

    def delete_space_group(self, space_group_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/space_groups/{space_group_id}")

    # -- Space Members --
    def list_space_members(self, *, space_id: int, page: int = 1, per_page: int = 60,
                           status: Optional[str] = None) -> SpaceMemberList:
        p: Dict[str, Any] = {"space_id": space_id, "page": page, "per_page": per_page}
        if status: p["status"] = status
        return SpaceMemberList.model_validate(self._t.request("GET", f"{_P}/space_members", params=p))

    def show_space_member(self, *, email: str, space_id: int) -> SpaceMember:
        return SpaceMember.model_validate(
            self._t.request("GET", f"{_P}/space_member", params={"email": email, "space_id": space_id}))

    def add_space_member(self, *, email: str, space_id: int) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/space_members", json={"email": email, "space_id": space_id})

    def remove_space_member(self, *, email: str, space_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/space_members", params={"email": email, "space_id": space_id})

    # -- Space Group Members --
    def list_space_group_members(self, *, space_group_id: int, page: int = 1, per_page: int = 60,
                                 status: Optional[str] = None) -> SpaceGroupMemberList:
        p: Dict[str, Any] = {"space_group_id": space_group_id, "page": page, "per_page": per_page}
        if status: p["status"] = status
        return SpaceGroupMemberList.model_validate(self._t.request("GET", f"{_P}/space_group_members", params=p))

    def show_space_group_member(self, *, email: str, space_group_id: int) -> SpaceGroupMember:
        return SpaceGroupMember.model_validate(
            self._t.request("GET", f"{_P}/space_group_member",
                            params={"email": email, "space_group_id": space_group_id}))

    def create_space_group_member(self, *, email: str, space_group_id: int) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/space_group_members",
                               json={"email": email, "space_group_id": space_group_id})

    def destroy_space_group_member(self, *, email: str, space_group_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/space_group_members",
                               params={"email": email, "space_group_id": space_group_id})


class AsyncSpacesClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def list_spaces(self, *, page: int = 1, per_page: int = 60, sort: Optional[str] = None) -> SpaceList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if sort: p["sort"] = sort
        return SpaceList.model_validate(await self._t.request("GET", f"{_P}/spaces", params=p))

    async def create_space(self, **kwargs: Any) -> SpaceCreateResponse:
        return SpaceCreateResponse.model_validate(await self._t.request("POST", f"{_P}/spaces", json=kwargs))

    async def show_space(self, space_id: int) -> Space:
        return Space.model_validate(await self._t.request("GET", f"{_P}/spaces/{space_id}"))

    async def update_space(self, space_id: int, **kwargs: Any) -> Space:
        return Space.model_validate(await self._t.request("PUT", f"{_P}/spaces/{space_id}", json=kwargs))

    async def delete_space(self, space_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/spaces/{space_id}")

    async def get_space_ai_summary(self, space_id: int, *, date_from: Optional[str] = None,
                                   first_unread_message_id: Optional[int] = None) -> SpaceAISummary:
        p: Dict[str, Any] = {}
        if date_from: p["date_from"] = date_from
        if first_unread_message_id: p["first_unread_message_id"] = first_unread_message_id
        return SpaceAISummary.model_validate(
            await self._t.request("GET", f"{_P}/spaces/{space_id}/ai_summaries", params=p))

    async def list_space_groups(self, *, page: int = 1, per_page: int = 60,
                                name: Optional[str] = None) -> SpaceGroupList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if name: p["name"] = name
        return SpaceGroupList.model_validate(await self._t.request("GET", f"{_P}/space_groups", params=p))

    async def create_space_group(self, *, name: str, slug: str, **kwargs: Any) -> SpaceGroup:
        return SpaceGroup.model_validate(
            await self._t.request("POST", f"{_P}/space_groups", json={"name": name, "slug": slug, **kwargs}))

    async def show_space_group(self, space_group_id: int) -> SpaceGroup:
        return SpaceGroup.model_validate(await self._t.request("GET", f"{_P}/space_groups/{space_group_id}"))

    async def update_space_group(self, space_group_id: int, **kwargs: Any) -> SpaceGroup:
        return SpaceGroup.model_validate(
            await self._t.request("PUT", f"{_P}/space_groups/{space_group_id}", json=kwargs))

    async def delete_space_group(self, space_group_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/space_groups/{space_group_id}")

    async def list_space_members(self, *, space_id: int, page: int = 1, per_page: int = 60,
                                 status: Optional[str] = None) -> SpaceMemberList:
        p: Dict[str, Any] = {"space_id": space_id, "page": page, "per_page": per_page}
        if status: p["status"] = status
        return SpaceMemberList.model_validate(await self._t.request("GET", f"{_P}/space_members", params=p))

    async def show_space_member(self, *, email: str, space_id: int) -> SpaceMember:
        return SpaceMember.model_validate(
            await self._t.request("GET", f"{_P}/space_member", params={"email": email, "space_id": space_id}))

    async def add_space_member(self, *, email: str, space_id: int) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/space_members", json={"email": email, "space_id": space_id})

    async def remove_space_member(self, *, email: str, space_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/space_members", params={"email": email, "space_id": space_id})

    async def list_space_group_members(self, *, space_group_id: int, page: int = 1, per_page: int = 60,
                                       status: Optional[str] = None) -> SpaceGroupMemberList:
        p: Dict[str, Any] = {"space_group_id": space_group_id, "page": page, "per_page": per_page}
        if status: p["status"] = status
        return SpaceGroupMemberList.model_validate(await self._t.request("GET", f"{_P}/space_group_members", params=p))

    async def show_space_group_member(self, *, email: str, space_group_id: int) -> SpaceGroupMember:
        return SpaceGroupMember.model_validate(
            await self._t.request("GET", f"{_P}/space_group_member",
                                  params={"email": email, "space_group_id": space_group_id}))

    async def create_space_group_member(self, *, email: str, space_group_id: int) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/space_group_members",
                                     json={"email": email, "space_group_id": space_group_id})

    async def destroy_space_group_member(self, *, email: str, space_group_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/space_group_members",
                                     params={"email": email, "space_group_id": space_group_id})
