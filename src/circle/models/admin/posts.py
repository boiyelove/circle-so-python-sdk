"""Post, comment, and topic models."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from circle.models.base import CircleModel, PaginatedResponse


class TiptapBody(CircleModel):
    body: Optional[Dict[str, Any]] = None
    circle_ios_fallback_text: Optional[str] = None
    attachments: Optional[List[Any]] = None
    inline_attachments: Optional[List[Any]] = None
    sgids_to_object_map: Optional[Dict[str, Any]] = None
    format: Optional[str] = None
    community_members: Optional[List[Any]] = None
    entities: Optional[List[Any]] = None
    group_mentions: Optional[List[Any]] = None
    polls: Optional[List[Any]] = None


class PostBody(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    body: Optional[str] = None
    record_type: Optional[str] = None
    record_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class BasicPost(CircleModel):
    id: Optional[int] = None
    status: Optional[str] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    comments_count: Optional[int] = None
    hide_meta_info: Optional[bool] = None
    published_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_comments_enabled: Optional[bool] = None
    is_comments_closed: Optional[bool] = None
    is_liking_enabled: Optional[bool] = None
    flagged_for_approval_at: Optional[str] = None
    unresolved_flagged_reports_count: Optional[int] = None
    custom_html: Optional[str] = None
    likes_count: Optional[int] = None
    url: Optional[str] = None
    space_name: Optional[str] = None
    space_slug: Optional[str] = None
    space_id: Optional[int] = None
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    community_id: Optional[int] = None
    user_avatar_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    cover_image: Optional[str] = None
    cardview_thumbnail_url: Optional[str] = None
    cardview_thumbnail: Optional[str] = None
    member_posts_count: Optional[int] = None
    member_comments_count: Optional[int] = None
    member_likes_count: Optional[int] = None
    topics: Optional[List[int]] = None
    body: Optional[PostBody] = None
    tiptap_body: Optional[TiptapBody] = None

PostList = PaginatedResponse[BasicPost]


class ImageGalleryImage(CircleModel):
    id: Optional[int] = None
    signed_id: Optional[str] = None
    original_url: Optional[str] = None
    url: Optional[str] = None
    filename: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class ImageGallery(CircleModel):
    id: Optional[int] = None
    downloadable_images: Optional[bool] = None
    images: Optional[List[ImageGalleryImage]] = None


class ImagePost(BasicPost):
    gallery: Optional[ImageGallery] = None


class BasicPostCreatedResponse(CircleModel):
    message: Optional[str] = None
    post: Optional[BasicPost] = None


class BasicPostUpdatedResponse(CircleModel):
    message: Optional[str] = None
    post: Optional[BasicPost] = None


class BasicPostDeletedResponse(CircleModel):
    success: Optional[bool] = None
    message: Optional[str] = None


class ImagePostCreatedResponse(CircleModel):
    message: Optional[str] = None
    post: Optional[ImagePost] = None


class AISummary(CircleModel):
    overview: Optional[str] = None
    content: Optional[str] = None


class CommentUser(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None


class CommentPost(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class CommentSpace(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class Comment(CircleModel):
    id: Optional[int] = None
    parent_comment_id: Optional[int] = None
    flagged_for_approval_at: Optional[str] = None
    unresolved_flagged_reports_count: Optional[int] = None
    created_at: Optional[str] = None
    body: Optional[PostBody] = None
    user: Optional[CommentUser] = None
    post: Optional[CommentPost] = None
    space: Optional[CommentSpace] = None
    replies_count: Optional[int] = None
    replies: Optional[List[Comment]] = None
    url: Optional[str] = None
    community_id: Optional[int] = None
    likes_count: Optional[int] = None
    user_posts_count: Optional[int] = None
    user_comments_count: Optional[int] = None
    user_likes_count: Optional[int] = None
    author_type: Optional[str] = None

CommentList = PaginatedResponse[Comment]


class TopicAuthor(CircleModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None


class Topic(CircleModel):
    id: Optional[int] = None
    name: Optional[str] = None
    admin_only: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    author: Optional[TopicAuthor] = None
    space_ids: Optional[List[int]] = None

TopicList = PaginatedResponse[Topic]
