# Headless Client API V1

Member-facing operations. Requires a member access token from the Headless Auth API.

## Setup

```python
from circle import CircleClient

# Get member token first
admin = CircleClient(api_token="ADMIN_TOKEN")
token = admin.auth.create_auth_token(email="member@example.com")

# Create headless client with member token
client = CircleClient(api_token=token.access_token, community_url="https://your.circle.so")
```

## Sub-clients

| Namespace | Description |
|---|---|
| `client.headless.spaces_posts` | Spaces, posts, comments, replies, likes |
| `client.headless.chat_notif_members` | Chat, notifications, members, events |
| `client.headless.misc` | Courses, search, bookmarks, uploads, notification prefs |

## Spaces

```python
spaces = client.headless.list_spaces()
space = client.headless.spaces_posts.get_space(1)
client.headless.spaces_posts.join_space(1)
client.headless.spaces_posts.leave_space(1)
```

## Posts

```python
posts = client.headless.list_posts(1, per_page=20)
post = client.headless.spaces_posts.get_post(1, 42)
new_post = client.headless.spaces_posts.create_post(1, name="My Post", body="Content")
client.headless.spaces_posts.like_post(42)
client.headless.spaces_posts.follow_post(42)
home = client.headless.spaces_posts.get_home_posts()
```

## Comments and Replies

```python
comments = client.headless.spaces_posts.list_comments(42)
comment = client.headless.spaces_posts.create_comment(42, body="Nice post!")
replies = client.headless.spaces_posts.list_replies(comment.id)
client.headless.spaces_posts.create_reply(comment.id, body="Thanks!")
```

## Chat

```python
rooms = client.headless.chat_notif_members.list_chat_rooms()
room = client.headless.chat_notif_members.create_chat_room(kind="direct", community_member_ids=["2"])
messages = client.headless.chat_notif_members.list_chat_messages("room-uuid")
client.headless.chat_notif_members.create_chat_message("room-uuid", rich_text_body={...})
```

## Notifications

```python
notifs = client.headless.chat_notif_members.list_notifications()
client.headless.chat_notif_members.mark_notification_read(1)
client.headless.chat_notif_members.mark_all_notifications_read()
count = client.headless.chat_notif_members.get_new_notifications_count()
```

## Members

```python
members = client.headless.chat_notif_members.list_community_members()
me = client.headless.chat_notif_members.get_current_member()
profile = client.headless.chat_notif_members.get_public_profile(2)
client.headless.chat_notif_members.update_profile(headline="New headline")
```

## Courses

```python
sections = client.headless.misc.list_course_sections(course_id=1)
lesson = client.headless.misc.get_lesson(course_id=1, lesson_id=2)
client.headless.misc.update_lesson_progress(1, 2, status="completed")
```

## Search

```python
results = client.headless.misc.search(search_text="python")
advanced = client.headless.misc.advanced_search(query="python", type="posts")
```

## Bookmarks

```python
bookmarks = client.headless.misc.list_bookmarks()
bm = client.headless.misc.create_bookmark(record_id=42, bookmark_type="post")
client.headless.misc.delete_bookmark(bm.id)
```
