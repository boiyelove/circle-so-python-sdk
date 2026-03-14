"""Admin API -- Courses (Sections, Lessons, Progress)."""
from __future__ import annotations
from typing import Any, Dict, Optional
from circle.http import AsyncTransport, SyncTransport
from circle.models.admin.courses import CourseSection, CourseSectionList, CourseLesson, CourseLessonList

_P = "/api/admin/v2"


class CoursesClient:
    def __init__(self, transport: SyncTransport) -> None:
        self._t = transport

    # -- Sections --
    def list_course_sections(self, *, page: int = 1, per_page: int = 10, space_id: Optional[int] = None,
                             sort: Optional[str] = None) -> CourseSectionList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if space_id: p["space_id"] = space_id
        if sort: p["sort"] = sort
        return CourseSectionList.model_validate(self._t.request("GET", f"{_P}/course_sections", params=p))

    def create_course_section(self, *, name: str, space_id: int) -> CourseSection:
        return CourseSection.model_validate(
            self._t.request("POST", f"{_P}/course_sections", json={"name": name, "space_id": space_id}))

    def show_course_section(self, section_id: int) -> CourseSection:
        return CourseSection.model_validate(self._t.request("GET", f"{_P}/course_sections/{section_id}"))

    def update_course_section(self, section_id: int, *, name: str) -> CourseSection:
        return CourseSection.model_validate(
            self._t.request("PUT", f"{_P}/course_sections/{section_id}", json={"name": name}))

    def delete_course_section(self, section_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/course_sections/{section_id}")

    # -- Lessons --
    def list_course_lessons(self, *, page: int = 1, per_page: int = 10, section_id: Optional[int] = None,
                            space_id: Optional[int] = None, status: Optional[str] = None,
                            sort: Optional[str] = None) -> CourseLessonList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if section_id: p["section_id"] = section_id
        if space_id: p["space_id"] = space_id
        if status: p["status"] = status
        if sort: p["sort"] = sort
        return CourseLessonList.model_validate(self._t.request("GET", f"{_P}/course_lessons", params=p))

    def create_course_lesson(self, *, name: str, section_id: int, **kwargs: Any) -> CourseLesson:
        return CourseLesson.model_validate(
            self._t.request("POST", f"{_P}/course_lessons", json={"name": name, "section_id": section_id, **kwargs}))

    def show_course_lesson(self, lesson_id: int) -> CourseLesson:
        return CourseLesson.model_validate(self._t.request("GET", f"{_P}/course_lessons/{lesson_id}"))

    def update_course_lesson(self, lesson_id: int, **kwargs: Any) -> CourseLesson:
        return CourseLesson.model_validate(
            self._t.request("PATCH", f"{_P}/course_lessons/{lesson_id}", json=kwargs))

    def delete_course_lesson(self, lesson_id: int) -> Dict[str, Any]:
        return self._t.request("DELETE", f"{_P}/course_lessons/{lesson_id}")

    # -- Progress --
    def update_course_lesson_progress(self, *, lesson_id: int, member_email: str, status: str) -> Dict[str, Any]:
        return self._t.request("PUT", f"{_P}/course_lesson_progress",
                               json={"lesson_id": lesson_id, "member_email": member_email, "status": status})


class AsyncCoursesClient:
    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def list_course_sections(self, *, page: int = 1, per_page: int = 10, space_id: Optional[int] = None,
                                   sort: Optional[str] = None) -> CourseSectionList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if space_id: p["space_id"] = space_id
        if sort: p["sort"] = sort
        return CourseSectionList.model_validate(await self._t.request("GET", f"{_P}/course_sections", params=p))

    async def create_course_section(self, *, name: str, space_id: int) -> CourseSection:
        return CourseSection.model_validate(
            await self._t.request("POST", f"{_P}/course_sections", json={"name": name, "space_id": space_id}))

    async def show_course_section(self, section_id: int) -> CourseSection:
        return CourseSection.model_validate(await self._t.request("GET", f"{_P}/course_sections/{section_id}"))

    async def update_course_section(self, section_id: int, *, name: str) -> CourseSection:
        return CourseSection.model_validate(
            await self._t.request("PUT", f"{_P}/course_sections/{section_id}", json={"name": name}))

    async def delete_course_section(self, section_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/course_sections/{section_id}")

    async def list_course_lessons(self, *, page: int = 1, per_page: int = 10, section_id: Optional[int] = None,
                                  space_id: Optional[int] = None, status: Optional[str] = None,
                                  sort: Optional[str] = None) -> CourseLessonList:
        p: Dict[str, Any] = {"page": page, "per_page": per_page}
        if section_id: p["section_id"] = section_id
        if space_id: p["space_id"] = space_id
        if status: p["status"] = status
        if sort: p["sort"] = sort
        return CourseLessonList.model_validate(await self._t.request("GET", f"{_P}/course_lessons", params=p))

    async def create_course_lesson(self, *, name: str, section_id: int, **kwargs: Any) -> CourseLesson:
        return CourseLesson.model_validate(
            await self._t.request("POST", f"{_P}/course_lessons",
                                  json={"name": name, "section_id": section_id, **kwargs}))

    async def show_course_lesson(self, lesson_id: int) -> CourseLesson:
        return CourseLesson.model_validate(await self._t.request("GET", f"{_P}/course_lessons/{lesson_id}"))

    async def update_course_lesson(self, lesson_id: int, **kwargs: Any) -> CourseLesson:
        return CourseLesson.model_validate(
            await self._t.request("PATCH", f"{_P}/course_lessons/{lesson_id}", json=kwargs))

    async def delete_course_lesson(self, lesson_id: int) -> Dict[str, Any]:
        return await self._t.request("DELETE", f"{_P}/course_lessons/{lesson_id}")

    async def update_course_lesson_progress(self, *, lesson_id: int, member_email: str,
                                            status: str) -> Dict[str, Any]:
        return await self._t.request("PUT", f"{_P}/course_lesson_progress",
                                     json={"lesson_id": lesson_id, "member_email": member_email, "status": status})
