# Headless Auth API

Token management for headless integrations. Uses your admin API token to generate member access tokens.

## Endpoints

### Create Auth Token

```python
token = client.auth.create_auth_token(email="member@example.com")
# or by SSO user ID
token = client.auth.create_auth_token(sso_user_id="abc123")
# or by community member ID
token = client.auth.create_auth_token(community_member_id=42)

print(token.access_token)
print(token.refresh_token)
print(token.community_member_id)
```

### Refresh Access Token

```python
refreshed = client.auth.refresh_access_token(refresh_token="...")
print(refreshed.access_token)
```

### Revoke Access Token

```python
client.auth.revoke_access_token(access_token="...")
```

### Revoke Refresh Token

```python
client.auth.revoke_refresh_token(refresh_token="...")
```
