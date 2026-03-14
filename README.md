# circle-so-python-sdk

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

## License

MIT
