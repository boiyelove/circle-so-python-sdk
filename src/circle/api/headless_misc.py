"""Headless Client API -- Courses, Search, Bookmarks, Misc."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.http import AsyncTransport, SyncTransport
from circle.models.headless.courses import Section, Lesson, LessonFileList, QuizAttempt, QuizAttemptList
from circle.models.headless.misc import (
    Bookmark, BookmarkList, SearchResults, HeadlessAdvancedSearchResults,
    CommunityLink, HeadlessDirectUpload, HeadlessPageProfileFieldList,
)
from circle.models.headless.notifications import MediumNotificationPreferences, SpaceMemberNotificationPreferences
from circle.models.headless.spaces import HeadlessSpaceTopicList

_P = "/api/headless/v1"


class HeadlessMiscClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    # -- Courses --
    def list_course_sections(self, course_id: int) -> List[Section]:
        data = self._t.request("GET", f"{_P}/courses/{course_id}/sections")
        return [Section.model_validate(s) for s in data]

    def get_lesson(self, course_id: int, lesson_id: int) -> Lesson:
        return Lesson.model_validate(self._t.request("GET", f"{_P}/courses/{course_id}/lessons/{lesson_id}"))

    def update_lesson_progress(self, course_id: int, lesson_id: int, *, status: str) -> Dict[str, Any]:
        return self._t.request("PATCH", f"{_P}/courses/{course_id}/lessons/{lesson_id}/progress",
                               json={"status": status})

    def list_lesson_files(self, course_id: int, lesson_id: int, *, page: int = 1,
                          per_page: int = 10) -> LessonFileList:
        return LessonFileList.model_validate(
            self._t.request("GET", f"{_P}/courses/{course_id}/lessons/{lesson_id}/files",
                            params={"page": page, "per_page": per_page}))

    def list_course_quiz_attempts(self, course_id: int, *, page: int = 1, per_page: int = 10) -> QuizAttemptList:
        return QuizAttemptList.model_validate(
            self._t.request("GET", f"{_P}/courses/{course_id}/quiz_attempts",
                            params={"page": page, "per_page": per_page}))

    def create_quiz_attempt(self, quiz_id: int, *, responses: List[Dict[str, Any]]) -> QuizAttempt:
        return QuizAttempt.model_validate(
            self._t.request("POST", f"{_P}/quizzes/{quiz_id}/attempts", json={"responses": responses}))

    def get_quiz_attempt(self, quiz_id: int, attempt_id: int, *,
                         for_admin_review: Optional[bool] = None) -> QuizAttempt:
        p: Dict[str, Any] = {}
        if for_admin_review is not None: p["for_admin_review"] = for_admin_review
        return QuizAttempt.model_validate(
            self._t.request("GET", f"{_P}/quizzes/{quiz_id}/attempts/{attempt_id}", params=p))

    def update_quiz_attempt(self, quiz_id: int, attempt_id: int, *, result: str) -> None:
        self._t.request("PUT", f"{_P}/quizzes/{quiz_id}/attempts/{attempt_id}", json={"result": result})

    def get_course_topics(self, *, page: int = 1, per_page: int = 10) -> HeadlessSpaceTopicList:
        return HeadlessSpaceTopicList.model_validate(
            self._t.request("GET", f"{_P}/course_topics", params={"page": page, "per_page": per_page}))

    # -- Search --
    def search(self, *, search_text: str, page: int = 1, per_page: int = 15) -> SearchResults:
        return SearchResults.model_validate(
            self._t.request("GET", f"{_P}/search",
                            params={"search_text": search_text, "page": page, "per_page": per_page}))

    def advanced_search(self, *, query: str, page: int = 1, per_page: int = 20,
                        type: Optional[str] = None, **kwargs: Any) -> HeadlessAdvancedSearchResults:
        p: Dict[str, Any] = {"query": query, "page": page, "per_page": per_page, **kwargs}
        if type: p["type"] = type
        return HeadlessAdvancedSearchResults.model_validate(
            self._t.request("GET", f"{_P}/advanced_search", params=p))

    # -- Bookmarks --
    def list_bookmarks(self, *, page: int = 1, per_page: int = 10,
                       bookmark_type: Optional[str] = None) -> BookmarkList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if bookmark_type: p["bookmark_type"] = bookmark_type
        return BookmarkList.model_validate(self._t.request("GET", f"{_P}/bookmarks", params=p))

    def create_bookmark(self, *, record_id: int, bookmark_type: str) -> Bookmark:
        return Bookmark.model_validate(
            self._t.request("POST", f"{_P}/bookmarks",
                            json={"record_id": record_id, "bookmark_type": bookmark_type}))

    def delete_bookmark(self, bookmark_id: int) -> None:
        self._t.request("DELETE", f"{_P}/bookmarks/{bookmark_id}")

    # -- Cookies --
    def create_cookies(self) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/cookies")

    def delete_cookies(self) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/cookies")

    # -- Direct Uploads --
    def create_direct_upload(self, *, blob: Dict[str, Any]) -> HeadlessDirectUpload:
        return HeadlessDirectUpload.model_validate(
            self._t.request("POST", f"{_P}/direct_uploads", json={"blob": blob}))

    # -- Live Streams --
    def create_live_room(self, **kwargs: Any) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/live_streams/rooms", json=kwargs)

    # -- Flagged Content --
    def flag_content(self, **kwargs: Any) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/flagged_contents", json={"flagged_content": kwargs})

    # -- Notification Preferences --
    def get_notification_preferences(self, medium: str) -> MediumNotificationPreferences:
        return MediumNotificationPreferences.model_validate(
            self._t.request("GET", f"{_P}/notification_preferences/{medium}"))

    def update_notification_preferences(self, medium: str, *, type: str, enabled: bool) -> Dict[str, Any]:
        return self._t.request("PUT", f"{_P}/notification_preferences/{medium}",
                               params={"type": type, "enabled": enabled})

    def update_space_notification_preference(self, medium: str, space_member_id: int, *,
                                             choice: str) -> Dict[str, Any]:
        return self._t.request("PUT", f"{_P}/notification_preferences/{medium}/spaces/{space_member_id}",
                               params={"choice": choice})

    def update_all_space_notification_preferences(self, medium: str, *, choice: str) -> Dict[str, Any]:
        return self._t.request("PUT", f"{_P}/notification_preferences/{medium}/spaces",
                               params={"choice": choice})

    def get_space_member_notification_preferences(self, space_member_id: int) -> SpaceMemberNotificationPreferences:
        return SpaceMemberNotificationPreferences.model_validate(
            self._t.request("GET", f"{_P}/notification_preferences/space_members/{space_member_id}"))

    # -- Space Members --
    def mark_space_member_as_read(self, space_member_id: int) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/space_members/{space_member_id}/mark_as_read")

    # -- Community Links --
    def get_community_links(self) -> List[CommunityLink]:
        data = self._t.request("GET", f"{_P}/community_links")
        return [CommunityLink.model_validate(l) for l in data]

    # -- Page Profile Fields --
    def get_page_profile_fields(self, *, page_name: str, page: int = 1,
                                per_page: int = 10) -> HeadlessPageProfileFieldList:
        return HeadlessPageProfileFieldList.model_validate(
            self._t.request("GET", f"{_P}/page_profile_fields",
                            params={"page_name": page_name, "page": page, "per_page": per_page}))

    # -- Invitation Links --
    def join_via_invitation_link(self, token: str) -> Dict[str, Any]:
        return self._t.request("POST", f"{_P}/invitation_links/{token}/join")


class AsyncHeadlessMiscClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def list_course_sections(self, course_id: int) -> List[Section]:
        data = await self._t.request("GET", f"{_P}/courses/{course_id}/sections")
        return [Section.model_validate(s) for s in data]

    async def get_lesson(self, course_id: int, lesson_id: int) -> Lesson:
        return Lesson.model_validate(await self._t.request("GET", f"{_P}/courses/{course_id}/lessons/{lesson_id}"))

    async def update_lesson_progress(self, course_id: int, lesson_id: int, *, status: str) -> Dict[str, Any]:
        return await self._t.request("PATCH", f"{_P}/courses/{course_id}/lessons/{lesson_id}/progress",
                                     json={"status": status})

    async def list_lesson_files(self, course_id: int, lesson_id: int, *, page: int = 1,
                                per_page: int = 10) -> LessonFileList:
        return LessonFileList.model_validate(
            await self._t.request("GET", f"{_P}/courses/{course_id}/lessons/{lesson_id}/files",
                                  params={"page": page, "per_page": per_page}))

    async def list_course_quiz_attempts(self, course_id: int, *, page: int = 1,
                                        per_page: int = 10) -> QuizAttemptList:
        return QuizAttemptList.model_validate(
            await self._t.request("GET", f"{_P}/courses/{course_id}/quiz_attempts",
                                  params={"page": page, "per_page": per_page}))

    async def create_quiz_attempt(self, quiz_id: int, *, responses: List[Dict[str, Any]]) -> QuizAttempt:
        return QuizAttempt.model_validate(
            await self._t.request("POST", f"{_P}/quizzes/{quiz_id}/attempts", json={"responses": responses}))

    async def get_quiz_attempt(self, quiz_id: int, attempt_id: int, *,
                               for_admin_review: Optional[bool] = None) -> QuizAttempt:
        p: Dict[str, Any] = {}
        if for_admin_review is not None: p["for_admin_review"] = for_admin_review
        return QuizAttempt.model_validate(
            await self._t.request("GET", f"{_P}/quizzes/{quiz_id}/attempts/{attempt_id}", params=p))

    async def update_quiz_attempt(self, quiz_id: int, attempt_id: int, *, result: str) -> None:
        await self._t.request("PUT", f"{_P}/quizzes/{quiz_id}/attempts/{attempt_id}", json={"result": result})

    async def get_course_topics(self, *, page: int = 1, per_page: int = 10) -> HeadlessSpaceTopicList:
        return HeadlessSpaceTopicList.model_validate(
            await self._t.request("GET", f"{_P}/course_topics", params={"page": page, "per_page": per_page}))

    async def search(self, *, search_text: str, page: int = 1, per_page: int = 15) -> SearchResults:
        return SearchResults.model_validate(
            await self._t.request("GET", f"{_P}/search",
                                  params={"search_text": search_text, "page": page, "per_page": per_page}))

    async def advanced_search(self, *, query: str, page: int = 1, per_page: int = 20,
                              type: Optional[str] = None, **kwargs: Any) -> HeadlessAdvancedSearchResults:
        p: Dict[str, Any] = {"query": query, "page": page, "per_page": per_page, **kwargs}
        if type: p["type"] = type
        return HeadlessAdvancedSearchResults.model_validate(
            await self._t.request("GET", f"{_P}/advanced_search", params=p))

    async def list_bookmarks(self, *, page: int = 1, per_page: int = 10,
                             bookmark_type: Optional[str] = None) -> BookmarkList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if bookmark_type: p["bookmark_type"] = bookmark_type
        return BookmarkList.model_validate(await self._t.request("GET", f"{_P}/bookmarks", params=p))

    async def create_bookmark(self, *, record_id: int, bookmark_type: str) -> Bookmark:
        return Bookmark.model_validate(
            await self._t.request("POST", f"{_P}/bookmarks",
                                  json={"record_id": record_id, "bookmark_type": bookmark_type}))

    async def delete_bookmark(self, bookmark_id: int) -> None:
        await self._t.request("DELETE", f"{_P}/bookmarks/{bookmark_id}")

    async def create_cookies(self) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/cookies")

    async def delete_cookies(self) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/cookies")

    async def create_direct_upload(self, *, blob: Dict[str, Any]) -> HeadlessDirectUpload:
        return HeadlessDirectUpload.model_validate(
            await self._t.request("POST", f"{_P}/direct_uploads", json={"blob": blob}))

    async def create_live_room(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/live_streams/rooms", json=kwargs)

    async def flag_content(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/flagged_contents", json={"flagged_content": kwargs})

    async def get_notification_preferences(self, medium: str) -> MediumNotificationPreferences:
        return MediumNotificationPreferences.model_validate(
            await self._t.request("GET", f"{_P}/notification_preferences/{medium}"))

    async def update_notification_preferences(self, medium: str, *, type: str, enabled: bool) -> Dict[str, Any]:
        return await self._t.request("PUT", f"{_P}/notification_preferences/{medium}",
                                     params={"type": type, "enabled": enabled})

    async def update_space_notification_preference(self, medium: str, space_member_id: int, *,
                                                   choice: str) -> Dict[str, Any]:
        return await self._t.request("PUT", f"{_P}/notification_preferences/{medium}/spaces/{space_member_id}",
                                     params={"choice": choice})

    async def update_all_space_notification_preferences(self, medium: str, *, choice: str) -> Dict[str, Any]:
        return await self._t.request("PUT", f"{_P}/notification_preferences/{medium}/spaces",
                                     params={"choice": choice})

    async def get_space_member_notification_preferences(self,
                                                        space_member_id: int) -> SpaceMemberNotificationPreferences:
        return SpaceMemberNotificationPreferences.model_validate(
            await self._t.request("GET", f"{_P}/notification_preferences/space_members/{space_member_id}"))

    async def mark_space_member_as_read(self, space_member_id: int) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/space_members/{space_member_id}/mark_as_read")

    async def get_community_links(self) -> List[CommunityLink]:
        data = await self._t.request("GET", f"{_P}/community_links")
        return [CommunityLink.model_validate(l) for l in data]

    async def get_page_profile_fields(self, *, page_name: str, page: int = 1,
                                      per_page: int = 10) -> HeadlessPageProfileFieldList:
        return HeadlessPageProfileFieldList.model_validate(
            await self._t.request("GET", f"{_P}/page_profile_fields",
                                  params={"page_name": page_name, "page": page, "per_page": per_page}))

    async def join_via_invitation_link(self, token: str) -> Dict[str, Any]:
        return await self._t.request("POST", f"{_P}/invitation_links/{token}/join")
