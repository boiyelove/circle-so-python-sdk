# Quickstart

## Installation

```bash
pip install circle-so-python-sdk
```

## Authentication

Circle.so uses different auth schemes per API:

- Admin API V2: Uses `Token AUTH_TOKEN` header (server-side admin token)
- Headless Auth: Uses `Bearer AUTH_TOKEN` header (admin token to generate member tokens)
- Headless Client V1: Uses `Bearer ACCESS_TOKEN` header (member access token)

## Basic Usage

```python
from circle import CircleClient

# Create client with your admin API token
client = CircleClient(api_token="YOUR_ADMIN_TOKEN")

# Admin API -- manage your community
community = client.admin.get_community()
members = client.admin.list_community_members(per_page=20)

# Headless Auth -- get a member access token
token = client.auth.create_auth_token(email="member@example.com")

# Headless Client -- act as a member
member_client = CircleClient(
    api_token=token.access_token,
    community_url="https://your-community.circle.so"
)
spaces = member_client.headless.list_spaces()
```

## Async Usage

```python
from circle import AsyncCircleClient

async with AsyncCircleClient(api_token="YOUR_TOKEN") as client:
    community = await client.admin.get_community()
    members = await client.admin.list_community_members()
```

## Auto-Pagination

```python
from circle import CircleClient
from circle.pagination import paginate

client = CircleClient(api_token="YOUR_TOKEN")

# Iterate all members across all pages
for member in paginate(client.admin.community.list_community_members, per_page=100):
    print(member.name)
```

## Error Handling

```python
from circle import CircleClient, AuthenticationError, NotFoundError

client = CircleClient(api_token="YOUR_TOKEN")
try:
    member = client.admin.community.show_community_member(99999)
except NotFoundError as e:
    print(f"Not found: {e}")
except AuthenticationError as e:
    print(f"Auth failed: {e}")
```
