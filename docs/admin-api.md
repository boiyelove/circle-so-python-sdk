# Admin API V2

Server-side community management. All methods available under `client.admin.*`.

## Sub-clients

| Namespace | Description |
|---|---|
| `client.admin.community` | Community settings, member CRUD |
| `client.admin.access_groups` | Access groups and their members |
| `client.admin.spaces` | Spaces, space groups, space members |
| `client.admin.posts` | Posts, comments, topics |
| `client.admin.events` | Events and attendees |
| `client.admin.courses` | Course sections, lessons, progress |
| `client.admin.tags` | Member tags, tagged members, profile fields |
| `client.admin.misc` | Forms, segments, invitations, embeds, uploads, search, leaderboard, flagged content, live rooms |

## Community

```python
community = client.admin.get_community()
updated = client.admin.community.update_community(name="New Name")
```

## Community Members

```python
members = client.admin.community.list_community_members(page=1, per_page=20)
member = client.admin.community.show_community_member(123)
created = client.admin.community.create_community_member(email="new@example.com", name="New User")
client.admin.community.update_community_member(123, headline="Updated")
client.admin.community.deactivate_community_member(123)
found = client.admin.community.search_community_member(email="user@example.com")
client.admin.community.ban_community_member(123)
```

## Spaces

```python
spaces = client.admin.spaces.list_spaces(per_page=30)
space = client.admin.spaces.show_space(1)
new_space = client.admin.spaces.create_space(name="My Space", slug="my-space", space_group_id=1, space_type="basic")
client.admin.spaces.update_space(1, name="Renamed")
client.admin.spaces.delete_space(1)
summary = client.admin.spaces.get_space_ai_summary(1)
```

## Space Groups

```python
groups = client.admin.spaces.list_space_groups()
group = client.admin.spaces.create_space_group(name="VIP", slug="vip")
```

## Posts

```python
posts = client.admin.posts.list_posts(space_id=1)
created = client.admin.posts.create_post(space_id=1, name="Hello", body="World")
post = client.admin.posts.show_post(42)
client.admin.posts.update_post(42, name="Updated Title")
client.admin.posts.delete_post(42)
summary = client.admin.posts.get_post_summary(42)
```

## Events

```python
events = client.admin.events.list_events(space_id=2)
event = client.admin.events.create_event(space_id=2, name="Meetup", status="published",
    event_setting_attributes={"starts_at": "2024-06-15T09:00:00Z", "location_type": "virtual"})
attendees = client.admin.events.list_event_attendees(event_id=1)
```

## Courses

```python
sections = client.admin.courses.list_course_sections(space_id=3)
lesson = client.admin.courses.create_course_lesson(name="Intro", section_id=1)
client.admin.courses.update_course_lesson_progress(lesson_id=1, member_email="user@example.com", status="completed")
```

## Tags

```python
tags = client.admin.tags.list_member_tags()
tag = client.admin.tags.create_member_tag(name="VIP", color="#FF0000")
client.admin.tags.create_tagged_member(member_tag_id=1, user_email="user@example.com")
```

## Forms, Segments, and More

```python
forms = client.admin.misc.list_forms()
segments = client.admin.misc.list_community_segments()
results = client.admin.misc.advanced_search(query="python")
leaderboard = client.admin.misc.get_leaderboard()
```
