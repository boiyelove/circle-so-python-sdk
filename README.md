# circle-so-python-sdk

[![CI](https://github.com/boiyelove/circle-so-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/boiyelove/circle-so-python-sdk/actions/workflows/ci.yml)

Python SDK for [Circle.so](https://circle.so) covering three APIs:

- Headless Auth API -- token management for headless integrations
- Admin API V2 -- server-side community management (~120 endpoints)
- Headless Client API V1 -- member-facing operations (~100 endpoints)

## Installation

```bash
pip install circle-so-python-sdk
```

## Quick Start

```python
from circle import CircleClient

# Admin API usage
client = CircleClient(api_token="YOUR_ADMIN_TOKEN")
community = client.admin.get_community()

# Headless Auth -- get member tokens
token = client.auth.create_auth_token(email="member@example.com")

# Headless Client -- use member access token
headless = CircleClient(api_token=token.access_token, community_url="https://your-community.circle.so")
spaces = headless.headless.list_spaces()
```

## Async Support

```python
from circle import AsyncCircleClient

async with AsyncCircleClient(api_token="YOUR_TOKEN") as client:
    members = await client.admin.list_community_members()
```

## API Coverage

| API | Endpoints | Sync | Async |
|---|---|---|---|
| Headless Auth | 4 | Yes | Yes |
| Admin V2 | ~118 | Yes | Yes |
| Headless Client V1 | ~101 | Yes | Yes |

## Documentation

- [Quickstart](docs/quickstart.md) -- install, auth, basic usage
- [Admin API](docs/admin-api.md) -- all admin endpoints with examples
- [Headless API](docs/headless-api.md) -- all headless endpoints with examples
- [Auth API](docs/auth-api.md) -- headless auth token management
- [Models](docs/models.md) -- complete models reference
- [Webhooks](docs/webhooks.md) -- signature verification and payload parsing
- [Limitations](docs/limitations.md) -- known Circle API limitations (mentions, polls, moderators)

## Project Structure

```
src/circle/
  __init__.py           # Public API exports
  client.py             # CircleClient / AsyncCircleClient facade
  http.py               # Sync/Async HTTP transport with retry
  exceptions.py         # Typed exceptions (401/403/404/422/429)
  pagination.py         # Auto-pagination helpers
  rate_limit.py         # Token bucket rate limiter
  validation.py         # Request body validation models
  webhooks.py           # Webhook signature verification
  models/
    auth.py             # HeadlessAuthToken, RefreshedAccessToken
    admin/              # ~35 Pydantic models for Admin API
    headless/           # ~40 Pydantic models for Headless API
  api/
    auth.py             # Headless Auth client (4 endpoints)
    admin_*.py          # 8 Admin API client modules
    headless_*.py       # 3 Headless API client modules
```

## Contributing

1. Clone the repo and install in dev mode: `pip install -e .[dev]`
2. Run tests: `pytest tests/ -v --ignore=tests/integration`
3. Follow conventional commit format for commit messages

## License

MIT
