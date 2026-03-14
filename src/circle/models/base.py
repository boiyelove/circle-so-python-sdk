"""Shared base model and generic paginated response."""

from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class CircleModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class PaginatedResponse(CircleModel, Generic[T]):
    page: int
    per_page: int
    has_next_page: bool
    count: int
    page_count: int = 0
    records: List[T] = []


class ErrorResponse(CircleModel):
    success: bool = False
    message: str = ""
    error_details: Optional[object] = None
