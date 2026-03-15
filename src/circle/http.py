"""Sync and async HTTP transport for Circle APIs."""
from __future__ import annotations

import logging
import platform
import time
from typing import Any, Optional, Type

import httpx

from circle.exceptions import (
    AuthenticationError,
    CircleAPIError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from circle.rate_limit import TokenBucket

logger = logging.getLogger("circle")
logger.addHandler(logging.NullHandler())

_STATUS_MAP: dict[int, type[CircleAPIError]] = {
    401: AuthenticationError,
    403: ForbiddenError,
    404: NotFoundError,
    422: ValidationError,
    429: RateLimitError,
}

DEFAULT_BASE_URL = "https://app.circle.so"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_STATUSES = (429, 500, 502, 503, 504)
SDK_VERSION = "0.1.0"
USER_AGENT = f"circle-python-sdk/{SDK_VERSION} (python/{platform.python_version()})"


def _parse_error(resp: httpx.Response) -> CircleAPIError:
    try:
        data = resp.json()
    except Exception:
        data = {}
    message = data.get("message") or data.get("errors") or resp.text
    if isinstance(message, list):
        message = "; ".join(str(m) for m in message)
    elif not isinstance(message, str):
        message = str(message)
    exc_cls = _STATUS_MAP.get(resp.status_code, CircleAPIError)
    return exc_cls(message, status_code=resp.status_code, error_details=data.get("error_details"))


def _retry_delay(attempt: int, resp: httpx.Response | None) -> float:
    if resp is not None and resp.status_code == 429:
        retry_after = resp.headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass
    return min(2**attempt, 30)


class _BaseTransport:
    def __init__(
        self,
        api_token: str,
        base_url: str = DEFAULT_BASE_URL,
        auth_scheme: str = "Token",
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        headers: dict[str, str] | None = None,
        rate_limit: float | None = None,
    ) -> None:
        self._api_token = api_token
        self._base_url = base_url.rstrip("/")
        self._auth_scheme = auth_scheme
        self._timeout = timeout
        self._max_retries = max_retries
        self._extra_headers = headers or {}
        self._rate_limiter = TokenBucket(rate_limit) if rate_limit else None

    def _build_headers(self) -> dict[str, str]:
        h: dict[str, str] = {
            "Authorization": f"{self._auth_scheme} {self._api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        h.update(self._extra_headers)
        return h

    def _full_url(self, path: str) -> str:
        return f"{self._base_url}{path}"


class SyncTransport(_BaseTransport):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = httpx.Client(timeout=self._timeout, headers=self._build_headers())

    def request(self, method: str, path: str, retry: bool = True, **kwargs: Any) -> Any:
        """Execute a sync HTTP request.

        Args:
            method: HTTP method.
            path: API path.
            retry: If False, skip retry loop and fail immediately on error.
            **kwargs: Passed to httpx.Client.request.

        Returns:
            Parsed JSON response or None for 204.

        Raises:
            CircleAPIError: On HTTP error responses.
        """
        url = self._full_url(path)
        if self._rate_limiter:
            self._rate_limiter.acquire()
        max_attempts = (self._max_retries + 1) if retry else 1
        logger.debug("request %s %s", method, path)
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                resp = self._client.request(method, url, **kwargs)
            except httpx.TransportError as e:
                last_exc = e
                logger.error("transport error %s %s: %s", method, path, e)
                if attempt < max_attempts - 1:
                    delay = _retry_delay(attempt, None)
                    logger.warning("retry %d/%d after %.1fs", attempt + 1, max_attempts - 1, delay)
                    time.sleep(delay)
                    continue
                raise CircleAPIError(str(e)) from e

            logger.debug("response %s %s -> %d", method, path, resp.status_code)

            if resp.status_code in DEFAULT_RETRY_STATUSES and attempt < max_attempts - 1:
                delay = _retry_delay(attempt, resp)
                logger.warning("retry %d/%d on %d after %.1fs", attempt + 1, max_attempts - 1, resp.status_code, delay)
                time.sleep(delay)
                continue

            if resp.status_code >= 400:
                raise _parse_error(resp)

            if resp.status_code == 204:
                return None
            try:
                return resp.json()
            except Exception:
                return None

        if last_exc:
            raise CircleAPIError(str(last_exc)) from last_exc
        raise CircleAPIError("Max retries exceeded")

    def close(self) -> None:
        self._client.close()


class AsyncTransport(_BaseTransport):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = httpx.AsyncClient(timeout=self._timeout, headers=self._build_headers())

    async def request(self, method: str, path: str, retry: bool = True, **kwargs: Any) -> Any:
        """Execute an async HTTP request.

        Args:
            method: HTTP method.
            path: API path.
            retry: If False, skip retry loop and fail immediately on error.
            **kwargs: Passed to httpx.AsyncClient.request.

        Returns:
            Parsed JSON response or None for 204.

        Raises:
            CircleAPIError: On HTTP error responses.
        """
        import asyncio

        url = self._full_url(path)
        if self._rate_limiter:
            await self._rate_limiter.aacquire()
        max_attempts = (self._max_retries + 1) if retry else 1
        logger.debug("request %s %s", method, path)
        last_exc: Exception | None = None
        for attempt in range(max_attempts):
            try:
                resp = await self._client.request(method, url, **kwargs)
            except httpx.TransportError as e:
                last_exc = e
                logger.error("transport error %s %s: %s", method, path, e)
                if attempt < max_attempts - 1:
                    delay = _retry_delay(attempt, None)
                    logger.warning("retry %d/%d after %.1fs", attempt + 1, max_attempts - 1, delay)
                    await asyncio.sleep(delay)
                    continue
                raise CircleAPIError(str(e)) from e

            logger.debug("response %s %s -> %d", method, path, resp.status_code)

            if resp.status_code in DEFAULT_RETRY_STATUSES and attempt < max_attempts - 1:
                delay = _retry_delay(attempt, resp)
                logger.warning("retry %d/%d on %d after %.1fs", attempt + 1, max_attempts - 1, resp.status_code, delay)
                await asyncio.sleep(delay)
                continue

            if resp.status_code >= 400:
                raise _parse_error(resp)

            if resp.status_code == 204:
                return None
            try:
                return resp.json()
            except Exception:
                return None

        if last_exc:
            raise CircleAPIError(str(last_exc)) from last_exc
        raise CircleAPIError("Max retries exceeded")

    async def close(self) -> None:
        await self._client.aclose()
