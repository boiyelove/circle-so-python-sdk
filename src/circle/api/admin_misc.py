"""Admin API -- Forms, Segments, Invitations, and Misc endpoints."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from circle.constants import ADMIN_V2_PREFIX as _P
from circle.http import AsyncTransport, SyncTransport
from circle.models.admin.misc import (
    Form, FormList, FormSubmission, FormSubmissionList,
    CommunitySegment, CommunitySegmentList, InvitationLink, InvitationLinkList,
    Embed, DirectUpload, LiveRoom, LiveRoomList,
    FlaggedContent, FlaggedContentList, LeaderboardMember, AdvancedSearchResults,
)
from circle.models.admin.community import ChatPreferences

_Req = Tuple[str, str, Dict[str, Any]]


# -- Param helpers --

def _list_forms_req(page: int, per_page: int, name: Optional[str]) -> _Req:
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if name:
        p["name"] = name
    return "GET", f"{_P}/forms", {"params": p}


def _list_community_segments_req(page: int, per_page: int, title: Optional[str]) -> _Req:
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if title:
        p["title"] = title
    return "GET", f"{_P}/community_segments", {"params": p}


def _list_invitation_links_req(page: int, per_page: int, name: Optional[str],
                                status: Optional[str]) -> _Req:
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if name:
        p["name"] = name
    if status:
        p["status"] = status
    return "GET", f"{_P}/invitation_links", {"params": p}


def _list_flagged_contents_req(page: int, per_page: int, status: Optional[str]) -> _Req:
    p: Dict[str, Any] = {"page": page, "per_page": per_page}
    if status:
        p["status"] = status
    return "GET", f"{_P}/flagged_contents", {"params": p}


def _advanced_search_req(query: str, page: int, per_page: int,
                          type: Optional[str], kwargs: Dict[str, Any]) -> _Req:
    p: Dict[str, Any] = {"query": query, "page": page, "per_page": per_page, **kwargs}
    if type:
        p["type"] = type
    return "GET", f"{_P}/advanced_search", {"params": p}


# ---------------------------------------------------------------------------
# Sync client
# ---------------------------------------------------------------------------

class AdminMiscClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    # -- Forms --
    def list_forms(self, *, page: int = 1, per_page: int = 60, name: Optional[str] = None) -> FormList:
        m, p, kw = _list_forms_req(page, per_page, name)
        return FormList.model_validate(self._t.request(m, p, **kw))

    def show_form(self, form_id: int) -> Form:
        return Form.model_validate(self._t.request("GET", f"{_P}/forms/{form_id}"))

    def update_form(self, form_id: int, **kwargs: Any) -> Form:
        return Form.model_validate(self._t.request("PUT", f"{_P}/forms/{form_id}", json=kwargs))

    def delete_form(self, form_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/forms/{form_id}")

    def duplicate_form(self, form_id: int) -> Form:
        return Form.model_validate(self._t.request("POST", f"{_P}/forms/{form_id}/duplicate"))

    def list_form_submissions(self, form_id: int, *, page: int = 1, per_page: int = 10) -> FormSubmissionList:
        return FormSubmissionList.model_validate(
            self._t.request("GET", f"{_P}/forms/{form_id}/submissions",
                            params={"page": page, "per_page": per_page}))

    def create_form_submission(self, form_id: int, *, elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/forms/{form_id}/submissions", json={"elements": elements})

    # -- Community Segments --
    def list_community_segments(self, *, page: int = 1, per_page: int = 60,
                                title: Optional[str] = None) -> CommunitySegmentList:
        m, p, kw = _list_community_segments_req(page, per_page, title)
        return CommunitySegmentList.model_validate(self._t.request(m, p, **kw))

    def create_community_segment(self, **kwargs: Any) -> CommunitySegment:
        return CommunitySegment.model_validate(self._t.request("POST", f"{_P}/community_segments", json=kwargs))

    def update_community_segment(self, segment_id: int, **kwargs: Any) -> CommunitySegment:
        return CommunitySegment.model_validate(
            self._t.request("PUT", f"{_P}/community_segments/{segment_id}", json=kwargs))

    def delete_community_segment(self, segment_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/community_segments/{segment_id}")

    def duplicate_community_segment(self, segment_id: int, *, title: str) -> CommunitySegment:
        return CommunitySegment.model_validate(
            self._t.request("POST", f"{_P}/community_segments/{segment_id}/duplicate", params={"title": title}))

    # -- Invitation Links --
    def list_invitation_links(self, *, page: int = 1, per_page: int = 10, name: Optional[str] = None,
                              status: Optional[str] = None) -> InvitationLinkList:
        m, p, kw = _list_invitation_links_req(page, per_page, name, status)
        return InvitationLinkList.model_validate(self._t.request(m, p, **kw))

    def delete_invitation_link(self, link_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/invitation_links/{link_id}")

    def revoke_invitation_link(self, link_id: int) -> Dict[str, Any]:
        return self._t.request("PATCH", f"{_P}/invitation_links/{link_id}/revoke")

    # -- Chat Preferences --
    def update_chat_preferences(self, **kwargs: Any) -> ChatPreferences:
        return ChatPreferences.model_validate(self._t.request("PUT", f"{_P}/chat_preferences", json=kwargs))

    # -- Direct Uploads --
    def create_direct_upload(self, *, blob: Dict[str, Any]) -> DirectUpload:
        return DirectUpload.model_validate(self._t.request("POST", f"{_P}/direct_uploads", json={"blob": blob}))

    # -- Embeds --
    def create_embed(self, *, url: str) -> Embed:
        return Embed.model_validate(self._t.request("POST", f"{_P}/embeds", json={"url": url}))

    def get_embed(self, sgid: str) -> Embed:
        return Embed.model_validate(self._t.request("GET", f"{_P}/embeds/{sgid}"))

    # -- Messages --
    def create_message(self, *, rich_text_body: Dict[str, Any],
                       user_email: Optional[str] = None, user_emails: Optional[List[str]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"rich_text_body": rich_text_body}
        if user_email:
            body["user_email"] = user_email
        if user_emails:
            body["user_emails"] = user_emails
        return self._t.request("POST", f"{_P}/messages", json=body)

    # -- Advanced Search --
    def advanced_search(self, *, query: str, page: int = 1, per_page: int = 20,
                        type: Optional[str] = None, **kwargs: Any) -> AdvancedSearchResults:
        m, p, kw = _advanced_search_req(query, page, per_page, type, kwargs)
        return AdvancedSearchResults.model_validate(self._t.request(m, p, **kw))

    # -- Leaderboard --
    def get_leaderboard(self, *, period: Optional[str] = None) -> List[LeaderboardMember]:
        p: Dict[str, Any] = {}
        if period:
            p["period"] = period
        data = self._t.request("GET", f"{_P}/gamification/leaderboard", params=p)
        return [LeaderboardMember.model_validate(r) for r in data]

    # -- Flagged Contents --
    def list_flagged_contents(self, *, page: int = 1, per_page: int = 10,
                              status: Optional[str] = None) -> FlaggedContentList:
        m, p, kw = _list_flagged_contents_req(page, per_page, status)
        return FlaggedContentList.model_validate(self._t.request(m, p, **kw))

    def report_flagged_content(self, **kwargs: Any) -> FlaggedContent:
        return FlaggedContent.model_validate(
            self._t.request("POST", f"{_P}/flagged_contents", json={"flagged_content": kwargs}))

    # -- Live Rooms --
    def list_live_rooms(self, *, page: int = 1, per_page: int = 20) -> LiveRoomList:
        return LiveRoomList.model_validate(
            self._t.request("GET", f"{_P}/live/rooms", params={"page": page, "per_page": per_page}))

    def list_live_room_transcripts(self, room_id: int) -> Dict[str, Any]:
        return self._t.request("GET", f"{_P}/live/rooms/{room_id}/transcripts")


# ---------------------------------------------------------------------------
# Async client
# ---------------------------------------------------------------------------

class AsyncAdminMiscClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    # -- Forms --
    async def list_forms(self, *, page: int = 1, per_page: int = 60, name: Optional[str] = None) -> FormList:
        m, p, kw = _list_forms_req(page, per_page, name)
        return FormList.model_validate(await self._t.request(m, p, **kw))

    async def show_form(self, form_id: int) -> Form:
        return Form.model_validate(await self._t.request("GET", f"{_P}/forms/{form_id}"))

    async def update_form(self, form_id: int, **kwargs: Any) -> Form:
        return Form.model_validate(await self._t.request("PUT", f"{_P}/forms/{form_id}", json=kwargs))

    async def delete_form(self, form_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/forms/{form_id}")

    async def duplicate_form(self, form_id: int) -> Form:
        return Form.model_validate(await self._t.request("POST", f"{_P}/forms/{form_id}/duplicate"))

    async def list_form_submissions(self, form_id: int, *, page: int = 1, per_page: int = 10) -> FormSubmissionList:
        return FormSubmissionList.model_validate(
            await self._t.request("GET", f"{_P}/forms/{form_id}/submissions",
                                  params={"page": page, "per_page": per_page}))

    async def create_form_submission(self, form_id: int, *, elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/forms/{form_id}/submissions", json={"elements": elements})

    # -- Community Segments --
    async def list_community_segments(self, *, page: int = 1, per_page: int = 60,
                                      title: Optional[str] = None) -> CommunitySegmentList:
        m, p, kw = _list_community_segments_req(page, per_page, title)
        return CommunitySegmentList.model_validate(await self._t.request(m, p, **kw))

    async def create_community_segment(self, **kwargs: Any) -> CommunitySegment:
        return CommunitySegment.model_validate(
            await self._t.request("POST", f"{_P}/community_segments", json=kwargs))

    async def update_community_segment(self, segment_id: int, **kwargs: Any) -> CommunitySegment:
        return CommunitySegment.model_validate(
            await self._t.request("PUT", f"{_P}/community_segments/{segment_id}", json=kwargs))

    async def delete_community_segment(self, segment_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/community_segments/{segment_id}")

    async def duplicate_community_segment(self, segment_id: int, *, title: str) -> CommunitySegment:
        return CommunitySegment.model_validate(
            await self._t.request("POST", f"{_P}/community_segments/{segment_id}/duplicate",
                                  params={"title": title}))

    # -- Invitation Links --
    async def list_invitation_links(self, *, page: int = 1, per_page: int = 10, name: Optional[str] = None,
                                    status: Optional[str] = None) -> InvitationLinkList:
        m, p, kw = _list_invitation_links_req(page, per_page, name, status)
        return InvitationLinkList.model_validate(await self._t.request(m, p, **kw))

    async def delete_invitation_link(self, link_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/invitation_links/{link_id}")

    async def revoke_invitation_link(self, link_id: int) -> Dict[str, Any]:
        return await self._t.request("PATCH", f"{_P}/invitation_links/{link_id}/revoke")

    # -- Chat Preferences --
    async def update_chat_preferences(self, **kwargs: Any) -> ChatPreferences:
        return ChatPreferences.model_validate(await self._t.request("PUT", f"{_P}/chat_preferences", json=kwargs))

    # -- Direct Uploads --
    async def create_direct_upload(self, *, blob: Dict[str, Any]) -> DirectUpload:
        return DirectUpload.model_validate(
            await self._t.request("POST", f"{_P}/direct_uploads", json={"blob": blob}))

    # -- Embeds --
    async def create_embed(self, *, url: str) -> Embed:
        return Embed.model_validate(await self._t.request("POST", f"{_P}/embeds", json={"url": url}))

    async def get_embed(self, sgid: str) -> Embed:
        return Embed.model_validate(await self._t.request("GET", f"{_P}/embeds/{sgid}"))

    # -- Messages --
    async def create_message(self, *, rich_text_body: Dict[str, Any],
                             user_email: Optional[str] = None,
                             user_emails: Optional[List[str]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"rich_text_body": rich_text_body}
        if user_email:
            body["user_email"] = user_email
        if user_emails:
            body["user_emails"] = user_emails
        return await self._t.request("POST", f"{_P}/messages", json=body)

    # -- Advanced Search --
    async def advanced_search(self, *, query: str, page: int = 1, per_page: int = 20,
                              type: Optional[str] = None, **kwargs: Any) -> AdvancedSearchResults:
        m, p, kw = _advanced_search_req(query, page, per_page, type, kwargs)
        return AdvancedSearchResults.model_validate(await self._t.request(m, p, **kw))

    # -- Leaderboard --
    async def get_leaderboard(self, *, period: Optional[str] = None) -> List[LeaderboardMember]:
        p: Dict[str, Any] = {}
        if period:
            p["period"] = period
        data = await self._t.request("GET", f"{_P}/gamification/leaderboard", params=p)
        return [LeaderboardMember.model_validate(r) for r in data]

    # -- Flagged Contents --
    async def list_flagged_contents(self, *, page: int = 1, per_page: int = 10,
                                    status: Optional[str] = None) -> FlaggedContentList:
        m, p, kw = _list_flagged_contents_req(page, per_page, status)
        return FlaggedContentList.model_validate(await self._t.request(m, p, **kw))

    async def report_flagged_content(self, **kwargs: Any) -> FlaggedContent:
        return FlaggedContent.model_validate(
            await self._t.request("POST", f"{_P}/flagged_contents", json={"flagged_content": kwargs}))

    # -- Live Rooms --
    async def list_live_rooms(self, *, page: int = 1, per_page: int = 20) -> LiveRoomList:
        return LiveRoomList.model_validate(
            await self._t.request("GET", f"{_P}/live/rooms", params={"page": page, "per_page": per_page}))

    async def list_live_room_transcripts(self, room_id: int) -> Dict[str, Any]:
        return await self._t.request("GET", f"{_P}/live/rooms/{room_id}/transcripts")
