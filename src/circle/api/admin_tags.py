"""Admin API -- Member Tags, Tagged Members, Profile Fields."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.http import AsyncTransport, SyncTransport
from circle.models.admin.tags import (
    MemberTag, MemberTagList, TaggedMember, TaggedMemberList, ProfileField, ProfileFieldList,
)

_P = "/api/admin/v2"


class TagsClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    # -- Member Tags --
    def list_member_tags(self, *, page: int = 1, per_page: int = 10, name: Optional[str] = None,
                         is_public: Optional[bool] = None, sort: Optional[str] = None) -> MemberTagList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if name: p["name"] = name
        if is_public is not None: p["is_public"] = is_public
        if sort: p["sort"] = sort
        return MemberTagList.model_validate(self._t.request("GET", f"{_P}/member_tags", params=p))

    def create_member_tag(self, **kwargs: Any) -> MemberTag:
        return MemberTag.model_validate(self._t.request("POST", f"{_P}/member_tags", json=kwargs))

    def show_member_tag(self, tag_id: int) -> MemberTag:
        return MemberTag.model_validate(self._t.request("GET", f"{_P}/member_tags/{tag_id}"))

    def update_member_tag(self, tag_id: int, **kwargs: Any) -> MemberTag:
        return MemberTag.model_validate(self._t.request("PUT", f"{_P}/member_tags/{tag_id}", json=kwargs))

    def delete_member_tag(self, tag_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/member_tags/{tag_id}")

    # -- Tagged Members --
    def list_tagged_members(self, *, page: int = 1, per_page: int = 10) -> TaggedMemberList:
        return TaggedMemberList.model_validate(
            self._t.request("GET", f"{_P}/tagged_members", params={"page": page, "per_page": per_page}))

    def show_tagged_member(self, tagged_member_id: int) -> TaggedMember:
        return TaggedMember.model_validate(self._t.request("GET", f"{_P}/tagged_members/{tagged_member_id}"))

    def create_tagged_member(self, *, member_tag_id: int, user_email: str) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/tagged_members",
                               json={"member_tag_id": member_tag_id, "user_email": user_email})

    def delete_tagged_member(self, *, member_tag_id: int, user_email: str) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/tagged_members",
                               params={"member_tag_id": member_tag_id, "user_email": user_email})

    # -- Profile Fields --
    def list_profile_fields(self, *, page: int = 1, per_page: int = 10, label: Optional[str] = None,
                            archived: Optional[str] = None) -> ProfileFieldList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if label: p["label"] = label
        if archived: p["archived"] = archived
        return ProfileFieldList.model_validate(self._t.request("GET", f"{_P}/profile_fields", params=p))

    def archive_profile_field(self, field_id: int) -> Dict[str, Any]:
        return self._t.request("PUT", f"{_P}/profile_fields/{field_id}/archive")

    def unarchive_profile_field(self, field_id: int) -> Dict[str, Any]:
        return self._t.request("PUT", f"{_P}/profile_fields/{field_id}/unarchive")

    def get_page_profile_fields(self, *, page_name: str) -> List[Any]:
        return self._t.request("GET", f"{_P}/page_profile_fields", params={"page_name": page_name})


class AsyncTagsClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def list_member_tags(self, *, page: int = 1, per_page: int = 10, name: Optional[str] = None,
                               is_public: Optional[bool] = None, sort: Optional[str] = None) -> MemberTagList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if name: p["name"] = name
        if is_public is not None: p["is_public"] = is_public
        if sort: p["sort"] = sort
        return MemberTagList.model_validate(await self._t.request("GET", f"{_P}/member_tags", params=p))

    async def create_member_tag(self, **kwargs: Any) -> MemberTag:
        return MemberTag.model_validate(await self._t.request("POST", f"{_P}/member_tags", json=kwargs))

    async def show_member_tag(self, tag_id: int) -> MemberTag:
        return MemberTag.model_validate(await self._t.request("GET", f"{_P}/member_tags/{tag_id}"))

    async def update_member_tag(self, tag_id: int, **kwargs: Any) -> MemberTag:
        return MemberTag.model_validate(await self._t.request("PUT", f"{_P}/member_tags/{tag_id}", json=kwargs))

    async def delete_member_tag(self, tag_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/member_tags/{tag_id}")

    async def list_tagged_members(self, *, page: int = 1, per_page: int = 10) -> TaggedMemberList:
        return TaggedMemberList.model_validate(
            await self._t.request("GET", f"{_P}/tagged_members", params={"page": page, "per_page": per_page}))

    async def show_tagged_member(self, tagged_member_id: int) -> TaggedMember:
        return TaggedMember.model_validate(await self._t.request("GET", f"{_P}/tagged_members/{tagged_member_id}"))

    async def create_tagged_member(self, *, member_tag_id: int, user_email: str) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/tagged_members",
                                     json={"member_tag_id": member_tag_id, "user_email": user_email})

    async def delete_tagged_member(self, *, member_tag_id: int, user_email: str) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/tagged_members",
                                     params={"member_tag_id": member_tag_id, "user_email": user_email})

    async def list_profile_fields(self, *, page: int = 1, per_page: int = 10, label: Optional[str] = None,
                                  archived: Optional[str] = None) -> ProfileFieldList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if label: p["label"] = label
        if archived: p["archived"] = archived
        return ProfileFieldList.model_validate(await self._t.request("GET", f"{_P}/profile_fields", params=p))

    async def archive_profile_field(self, field_id: int) -> Dict[str, Any]:
        return await self._t.request("PUT", f"{_P}/profile_fields/{field_id}/archive")

    async def unarchive_profile_field(self, field_id: int) -> Dict[str, Any]:
        return await self._t.request("PUT", f"{_P}/profile_fields/{field_id}/unarchive")

    async def get_page_profile_fields(self, *, page_name: str) -> List[Any]:
        return await self._t.request("GET", f"{_P}/page_profile_fields", params={"page_name": page_name})
