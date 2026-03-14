"""Course section and lesson models."""
from __future__ import annotations
from typing import Optional
from circle.models.base import CircleModel, PaginatedResponse


class CourseSection(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    space_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

CourseSectionList = PaginatedResponse[CourseSection]


class CourseLesson(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    section_id: Optional[int] = None
    is_comments_enabled: Optional[bool] = None
    is_featured_media_enabled: Optional[bool] = None
    is_featured_media_download_enabled: Optional[bool] = None
    body_html: Optional[str] = None
    space_id: Optional[int] = None

CourseLessonList = PaginatedResponse[CourseLesson]
