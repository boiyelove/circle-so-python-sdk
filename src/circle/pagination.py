"""Auto-pagination helpers for page-based and search_after-based APIs."""
from __future__ import annotations
from typing import Any, AsyncIterator, Callable, Iterator, List, TypeVar

T = TypeVar("T")


def paginate(
    method: Callable[..., Any],
    *args: Any,
    per_page: int = 60,
    max_pages: int = 0,
    **kwargs: Any,
) -> Iterator[T]:
    """Yield all records across pages from a paginated sync method.

    Works with any method returning an object with `records`, `has_next_page`, and `page` attrs.

    Args:
        method: A sync SDK method that returns a PaginatedResponse.
        per_page: Records per page.
        max_pages: Stop after N pages (0 = unlimited).
        *args, **kwargs: Forwarded to method.

    Yields:
        Individual records from each page.
    """
    page = kwargs.pop("page", 1)
    pages_fetched = 0
    while True:
        result = method(*args, page=page, per_page=per_page, **kwargs)
        for record in result.records:
            yield record
        pages_fetched += 1
        if not result.has_next_page or (max_pages and pages_fetched >= max_pages):
            break
        page += 1


async def apaginate(
    method: Callable[..., Any],
    *args: Any,
    per_page: int = 60,
    max_pages: int = 0,
    **kwargs: Any,
) -> AsyncIterator[T]:
    """Yield all records across pages from a paginated async method.

    Args:
        method: An async SDK method that returns a PaginatedResponse.
        per_page: Records per page.
        max_pages: Stop after N pages (0 = unlimited).
        *args, **kwargs: Forwarded to method.

    Yields:
        Individual records from each page.
    """
    page = kwargs.pop("page", 1)
    pages_fetched = 0
    while True:
        result = await method(*args, page=page, per_page=per_page, **kwargs)
        for record in result.records:
            yield record
        pages_fetched += 1
        if not result.has_next_page or (max_pages and pages_fetched >= max_pages):
            break
        page += 1


def paginate_search_after(
    method: Callable[..., Any],
    *args: Any,
    per_page: int = 60,
    max_pages: int = 0,
    **kwargs: Any,
) -> Iterator[T]:
    """Yield all records using search_after cursor pagination (headless members).

    The response must have `records`, `has_next_page`, and `next_search_after` attrs.
    """
    pages_fetched = 0
    search_after = kwargs.pop("search_after", None)
    while True:
        if search_after:
            kwargs["search_after"] = search_after
        result = method(*args, per_page=per_page, **kwargs)
        for record in result.records:
            yield record
        pages_fetched += 1
        next_sa = getattr(result, "next_search_after", None)
        if not result.has_next_page or not next_sa or (max_pages and pages_fetched >= max_pages):
            break
        search_after = next_sa


async def apaginate_search_after(
    method: Callable[..., Any],
    *args: Any,
    per_page: int = 60,
    max_pages: int = 0,
    **kwargs: Any,
) -> AsyncIterator[T]:
    """Async version of paginate_search_after."""
    pages_fetched = 0
    search_after = kwargs.pop("search_after", None)
    while True:
        if search_after:
            kwargs["search_after"] = search_after
        result = await method(*args, per_page=per_page, **kwargs)
        for record in result.records:
            yield record
        pages_fetched += 1
        next_sa = getattr(result, "next_search_after", None)
        if not result.has_next_page or not next_sa or (max_pages and pages_fetched >= max_pages):
            break
        search_after = next_sa
