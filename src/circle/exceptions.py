"""Typed exceptions for Circle API errors."""

from __future__ import annotations

from typing import Any


class CircleAPIError(Exception):
    """Base exception for all Circle API errors."""

    def __init__(self, message: str, status_code: int | None = None, error_details: Any = None) -> None:
        self.status_code = status_code
        self.error_details = error_details
        super().__init__(message)


class AuthenticationError(CircleAPIError):
    """401 Unauthorized."""


class ForbiddenError(CircleAPIError):
    """403 Forbidden."""


class NotFoundError(CircleAPIError):
    """404 Not Found."""


class ValidationError(CircleAPIError):
    """422 Unprocessable Entity."""


class RateLimitError(CircleAPIError):
    """429 Too Many Requests."""
