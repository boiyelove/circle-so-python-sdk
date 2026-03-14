"""Admin API -- Access Groups & Access Group Members."""
from __future__ import annotations
from typing import Any, Dict, Optional
from circle.http import AsyncTransport, SyncTransport
from circle.models.admin.misc import (
    AccessGroup, AccessGroupList, AccessGroupCommunityMember, AccessGroupCommunityMemberList,
)

_P = "/api/admin/v2"


class AccessGroupsClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    def list_access_groups(self, *, page: int = 1, per_page: int = 60, status: Optional[str] = None,
                           ids: Optional[list[int]] = None, name: Optional[str] = None) -> AccessGroupList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if status: p["status"] = status
        if ids: p["ids"] = ids
        if name: p["name"] = name
        return AccessGroupList.model_validate(self._t.request("GET", f"{_P}/access_groups", params=p))

    def create_access_group(self, *, name: str, description: Optional[str] = None) -> AccessGroup:
        body: Dict[str, Any] = {"access_group": {"name": name}}
        if description is not None: body["access_group"]["description"] = description
        return AccessGroup.model_validate(self._t.request("POST", f"{_P}/access_groups", json=body))

    def update_access_group(self, access_group_id: int, **kwargs: Any) -> AccessGroup:
        return AccessGroup.model_validate(
            self._t.request("PUT", f"{_P}/access_groups/{access_group_id}", json={"access_group": kwargs}))

    def archive_access_group(self, access_group_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/access_groups/{access_group_id}")

    def unarchive_access_group(self, access_group_id: int) -> AccessGroup:
        return AccessGroup.model_validate(
            self._t.request("PATCH", f"{_P}/access_groups/{access_group_id}/unarchive"))

    def list_access_group_members(self, access_group_id: int, *, page: int = 1,
                                  per_page: int = 60) -> AccessGroupCommunityMemberList:
        return AccessGroupCommunityMemberList.model_validate(
            self._t.request("GET", f"{_P}/access_groups/{access_group_id}/community_members",
                            params={"page": page, "per_page": per_page}))

    def show_access_group_member(self, access_group_id: int, *, email: str) -> AccessGroupCommunityMember:
        return AccessGroupCommunityMember.model_validate(
            self._t.request("GET", f"{_P}/access_groups/{access_group_id}/community_member",
                            params={"email": email}))

    def add_access_group_member(self, access_group_id: int, *, email: str) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/access_groups/{access_group_id}/community_members",
                               json={"email": email})

    def remove_access_group_member(self, access_group_id: int, *, email: str) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/access_groups/{access_group_id}/community_members",
                               params={"email": email})

    def list_community_member_access_groups(self, community_member_id: int, *, page: int = 1,
                                            per_page: int = 60) -> AccessGroupList:
        return AccessGroupList.model_validate(
            self._t.request("GET", f"{_P}/community_members/{community_member_id}/access_groups",
                            params={"page": page, "per_page": per_page}))


class AsyncAccessGroupsClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def list_access_groups(self, *, page: int = 1, per_page: int = 60, status: Optional[str] = None,
                                 ids: Optional[list[int]] = None, name: Optional[str] = None) -> AccessGroupList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if status: p["status"] = status
        if ids: p["ids"] = ids
        if name: p["name"] = name
        return AccessGroupList.model_validate(await self._t.request("GET", f"{_P}/access_groups", params=p))

    async def create_access_group(self, *, name: str, description: Optional[str] = None) -> AccessGroup:
        body: Dict[str, Any] = {"access_group": {"name": name}}
        if description is not None: body["access_group"]["description"] = description
        return AccessGroup.model_validate(await self._t.request("POST", f"{_P}/access_groups", json=body))

    async def update_access_group(self, access_group_id: int, **kwargs: Any) -> AccessGroup:
        return AccessGroup.model_validate(
            await self._t.request("PUT", f"{_P}/access_groups/{access_group_id}", json={"access_group": kwargs}))

    async def archive_access_group(self, access_group_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/access_groups/{access_group_id}")

    async def unarchive_access_group(self, access_group_id: int) -> AccessGroup:
        return AccessGroup.model_validate(
            await self._t.request("PATCH", f"{_P}/access_groups/{access_group_id}/unarchive"))

    async def list_access_group_members(self, access_group_id: int, *, page: int = 1,
                                        per_page: int = 60) -> AccessGroupCommunityMemberList:
        return AccessGroupCommunityMemberList.model_validate(
            await self._t.request("GET", f"{_P}/access_groups/{access_group_id}/community_members",
                                  params={"page": page, "per_page": per_page}))

    async def show_access_group_member(self, access_group_id: int, *, email: str) -> AccessGroupCommunityMember:
        return AccessGroupCommunityMember.model_validate(
            await self._t.request("GET", f"{_P}/access_groups/{access_group_id}/community_member",
                                  params={"email": email}))

    async def add_access_group_member(self, access_group_id: int, *, email: str) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/access_groups/{access_group_id}/community_members",
                                     json={"email": email})

    async def remove_access_group_member(self, access_group_id: int, *, email: str) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/access_groups/{access_group_id}/community_members",
                                     params={"email": email})

    async def list_community_member_access_groups(self, community_member_id: int, *, page: int = 1,
                                                  per_page: int = 60) -> AccessGroupList:
        return AccessGroupList.model_validate(
            await self._t.request("GET", f"{_P}/community_members/{community_member_id}/access_groups",
                                  params={"page": page, "per_page": per_page}))
