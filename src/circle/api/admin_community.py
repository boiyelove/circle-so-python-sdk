"""Admin API -- Community & Community Members."""
from __future__ import annotations
from typing import Any, Dict, Optional
from circle.constants import ADMIN_V2_PREFIX as _P
from circle.http import AsyncTransport, SyncTransport
from circle.models.admin.community import Community
from circle.models.admin.members import CommunityMember, CommunityMemberList, CommunityMemberCreated
from circle.models.admin.spaces import SpaceList


def _list_members_params(page: int, per_page: int, status: Optional[str]) -> Dict[str, Any]:
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if status:
        p["status"] = status
    return p


def _member_spaces_params(
    page: int, per_page: int,
    community_member_id: Optional[int], user_email: Optional[str],
) -> Dict[str, Any]:
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if community_member_id:
        p["community_member_id"] = community_member_id
    if user_email:
        p["user_email"] = user_email
    return p


class CommunityClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    def get_community(self) -> Community:
        return Community.model_validate(self._t.request("GET", f"{_P}/community"))

    def update_community(self, **kwargs: Any) -> Community:
        return Community.model_validate(self._t.request("PUT", f"{_P}/community", json={"community": kwargs}))

    def list_community_members(self, *, page: int = 1, per_page: int = 10,
                               status: Optional[str] = None) -> CommunityMemberList:
        return CommunityMemberList.model_validate(
            self._t.request("GET", f"{_P}/community_members", params=_list_members_params(page, per_page, status)))

    def create_community_member(self, *, email: str, **kwargs: Any) -> CommunityMemberCreated:
        return CommunityMemberCreated.model_validate(
            self._t.request("POST", f"{_P}/community_members", json={"email": email, **kwargs}))

    def show_community_member(self, member_id: int) -> CommunityMember:
        return CommunityMember.model_validate(self._t.request("GET", f"{_P}/community_members/{member_id}"))

    def update_community_member(self, member_id: int, **kwargs: Any) -> CommunityMember:
        return CommunityMember.model_validate(
            self._t.request("PUT", f"{_P}/community_members/{member_id}", json=kwargs))

    def deactivate_community_member(self, member_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/community_members/{member_id}")

    def search_community_member(self, *, email: str) -> CommunityMember:
        return CommunityMember.model_validate(
            self._t.request("GET", f"{_P}/community_members/search", params={"email": email}))

    def ban_community_member(self, member_id: int) -> Dict[str, Any]:
        return self._t.request("PUT", f"{_P}/community_members/{member_id}/ban_member")

    def delete_community_member(self, member_id: int) -> Dict[str, Any]:
        return self._t.request("PUT", f"{_P}/community_members/{member_id}/delete_member")

    def list_community_member_spaces(self, *, page: int = 1, per_page: int = 60,
                                     community_member_id: Optional[int] = None,
                                     user_email: Optional[str] = None) -> SpaceList:
        return SpaceList.model_validate(
            self._t.request("GET", f"{_P}/community_member_spaces",
                            params=_member_spaces_params(page, per_page, community_member_id, user_email)))


class AsyncCommunityClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def get_community(self) -> Community:
        return Community.model_validate(await self._t.request("GET", f"{_P}/community"))

    async def update_community(self, **kwargs: Any) -> Community:
        return Community.model_validate(await self._t.request("PUT", f"{_P}/community", json={"community": kwargs}))

    async def list_community_members(self, *, page: int = 1, per_page: int = 10,
                                     status: Optional[str] = None) -> CommunityMemberList:
        return CommunityMemberList.model_validate(
            await self._t.request("GET", f"{_P}/community_members",
                                  params=_list_members_params(page, per_page, status)))

    async def create_community_member(self, *, email: str, **kwargs: Any) -> CommunityMemberCreated:
        return CommunityMemberCreated.model_validate(
            await self._t.request("POST", f"{_P}/community_members", json={"email": email, **kwargs}))

    async def show_community_member(self, member_id: int) -> CommunityMember:
        return CommunityMember.model_validate(await self._t.request("GET", f"{_P}/community_members/{member_id}"))

    async def update_community_member(self, member_id: int, **kwargs: Any) -> CommunityMember:
        return CommunityMember.model_validate(
            await self._t.request("PUT", f"{_P}/community_members/{member_id}", json=kwargs))

    async def deactivate_community_member(self, member_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/community_members/{member_id}")

    async def search_community_member(self, *, email: str) -> CommunityMember:
        return CommunityMember.model_validate(
            await self._t.request("GET", f"{_P}/community_members/search", params={"email": email}))

    async def ban_community_member(self, member_id: int) -> Dict[str, Any]:
        return await self._t.request("PUT", f"{_P}/community_members/{member_id}/ban_member")

    async def delete_community_member(self, member_id: int) -> Dict[str, Any]:
        return await self._t.request("PUT", f"{_P}/community_members/{member_id}/delete_member")

    async def list_community_member_spaces(self, *, page: int = 1, per_page: int = 60,
                                           community_member_id: Optional[int] = None,
                                           user_email: Optional[str] = None) -> SpaceList:
        return SpaceList.model_validate(
            await self._t.request("GET", f"{_P}/community_member_spaces",
                                  params=_member_spaces_params(page, per_page, community_member_id, user_email)))
