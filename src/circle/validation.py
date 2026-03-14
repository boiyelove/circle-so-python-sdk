"""Client-side request body validation for common write endpoints."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, field_validator
from circle.exceptions import ValidationError as CircleValidationError


class _ValidatedRequest(BaseModel):
    """Base for request validation. Raises CircleValidationError on failure."""

    @classmethod
    def validate_kwargs(cls, **kwargs: Any) -> Dict[str, Any]:
        try:
            obj = cls.model_validate(kwargs)
            return obj.model_dump(exclude_none=True)
        except Exception as e:
            raise CircleValidationError(str(e), status_code=None, error_details=str(e)) from e


class CreatePostRequest(_ValidatedRequest):
    space_id: int
    name: str
    body: Optional[str] = None
    status: Optional[str] = None
    tiptap_body: Optional[Dict[str, Any]] = None
    slug: Optional[str] = None
    topics: Optional[List[int]] = None
    user_email: Optional[str] = None
    user_id: Optional[int] = None
    skip_notifications: Optional[bool] = None
    is_pinned: Optional[bool] = None
    cover_image: Optional[str] = None


class CreateCommunityMemberRequest(_ValidatedRequest):
    email: str
    name: Optional[str] = None
    headline: Optional[str] = None
    password: Optional[str] = None
    skip_invitation: Optional[bool] = None
    space_ids: Optional[List[int]] = None
    space_group_ids: Optional[List[int]] = None
    member_tag_ids: Optional[List[int]] = None


class CreateSpaceRequest(_ValidatedRequest):
    name: str
    slug: str
    space_group_id: int
    space_type: Optional[str] = None
    is_private: Optional[bool] = None
    is_hidden: Optional[bool] = None
    display_view: Optional[str] = None


class CreateEventRequest(_ValidatedRequest):
    name: str
    space_id: int
    status: str
    event_setting_attributes: Optional[Dict[str, Any]] = None


class CreateCommentRequest(_ValidatedRequest):
    body: str
    post_id: int
    parent_comment_id: Optional[int] = None
    skip_notifications: Optional[bool] = None
