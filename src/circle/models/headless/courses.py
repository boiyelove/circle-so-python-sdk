"""Headless course models."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse
from circle.models.admin.posts import TiptapBody


class LessonProgress(CircleModel):
    status: Optional[str] = None


class SectionLesson(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    is_featured_media_enabled: Optional[bool] = None
    featured_media_duration: Optional[int] = None
    dripped_at: Optional[str] = None
    needs_to_complete_previous_lesson: Optional[bool] = None
    progress: Optional[LessonProgress] = None


class Section(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    drip_delay: Optional[int] = None
    notify_students_enabled: Optional[bool] = None
    is_dripped: Optional[bool] = None
    dripped_at: Optional[str] = None
    lessons: Optional[List[SectionLesson]] = None


class FeaturedMedia(CircleModel):
    filename: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    byte_size: Optional[int] = None
    type: Optional[str] = None
    url: Optional[str] = None
    webvtt_file_url: Optional[str] = None
    chapters_url: Optional[str] = None
    preview_thumbnails_url: Optional[str] = None
    image_variants: Optional[Dict[str, Any]] = None
    signed_id: Optional[str] = None


class LessonSpace(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class Lesson(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    enforce_featured_media_completion: Optional[bool] = None
    autocomplete_on_featured_media_completion: Optional[bool] = None
    is_comments_enabled: Optional[bool] = None
    is_featured_media_enabled: Optional[bool] = None
    featured_media: Optional[FeaturedMedia] = None
    is_featured_media_download_enabled: Optional[bool] = None
    space: Optional[LessonSpace] = None
    bookmark_id: Optional[int] = None
    chat_room_uuid: Optional[str] = None
    rich_text_body: Optional[TiptapBody] = None
    featured_media_duration: Optional[int] = None
    section_id: Optional[int] = None
    dripped_at: Optional[str] = None
    progress: Optional[LessonProgress] = None
    needs_to_complete_previous_lesson: Optional[bool] = None


class LessonFile(CircleModel):
    id: Optional[int] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None
    byte_size: Optional[int] = None
    created_at: Optional[str] = None
    signed_id: Optional[str] = None
    url: Optional[str] = None
    type: Optional[str] = None

LessonFileList = PaginatedResponse[LessonFile]


class QuizAttemptQuestion(CircleModel):
    id: Optional[int] = None
    question_type: Optional[str] = None
    statement: Optional[str] = None
    correct: Optional[bool] = None
    options: Optional[List[Any]] = None


class QuizAttempt(CircleModel):
    id: Optional[int] = None
    quiz_id: Optional[int] = None
    created_at: Optional[str] = None
    grade: Optional[int] = None
    result: Optional[str] = None
    passing_grade: Optional[int] = None
    enforce_passing_grade: Optional[bool] = None
    hide_answers: Optional[bool] = None
    correct_responses: Optional[int] = None
    description: Optional[str] = None
    questions: Optional[List[QuizAttemptQuestion]] = None
    quiz_attempts_count: Optional[int] = None
    lesson_name: Optional[str] = None
    section_name: Optional[str] = None

QuizAttemptList = PaginatedResponse[QuizAttempt]
