# Changelog

## 0.1.0 (2026-03-14)

Initial release covering all three Circle.so APIs:

- Headless Auth API (4 endpoints)
- Admin API V2 (~118 endpoints)
- Headless Client API V1 (~101 endpoints)

Features:
- Sync and async clients via httpx
- Pydantic V2 models for all API responses
- Typed exceptions (AuthenticationError, NotFoundError, ValidationError, ForbiddenError, RateLimitError)
- Auto-retry with exponential backoff and Retry-After support
- Auto-pagination helpers (page-based and search_after cursor-based)
- Context manager support
- py.typed marker for PEP 561 compliance
