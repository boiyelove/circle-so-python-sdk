"""Token bucket rate limiter for proactive 429 prevention."""
from __future__ import annotations
import time
import asyncio


class TokenBucket:
    """Simple token bucket rate limiter."""

    def __init__(self, rate: float = 10.0) -> None:
        self._rate = rate
        self._max_tokens = rate
        self._tokens = rate
        self._last_refill = time.monotonic()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._max_tokens, self._tokens + elapsed * self._rate)
        self._last_refill = now

    def acquire(self) -> None:
        self._refill()
        if self._tokens < 1:
            wait = (1 - self._tokens) / self._rate
            time.sleep(wait)
            self._refill()
        self._tokens -= 1

    async def aacquire(self) -> None:
        self._refill()
        if self._tokens < 1:
            wait = (1 - self._tokens) / self._rate
            await asyncio.sleep(wait)
            self._refill()
        self._tokens -= 1
