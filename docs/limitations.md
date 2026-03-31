# Circle API Limitations

Known limitations of the Circle.so API that affect SDK operations. These are platform-level restrictions, not SDK bugs.

## Mentions

Circle uses Rails Signed Global IDs (SGIDs) to resolve @mentions. The SGID is a cryptographically signed token generated server-side that maps to a `CommunityMember` record.

**What works:**
- Reading mentions from existing posts via `tiptap_body.community_members` and `sgids_to_object_map`
- Reusing a known SGID to embed a mention in a new post or comment

**What does not work:**
- Creating mentions with just a `community_member_id` or email -- the mention node renders as blank text
- Generating SGIDs via the API -- no endpoint returns member SGIDs
- Sending `community_members` in the request body -- Circle ignores it and resolves from SGIDs only

**Workaround:** Manually mention a member once in the Circle UI, retrieve the post via API to capture their SGID from `tiptap_body.sgids_to_object_map`, store it, and reuse it in future API posts. SGIDs have no expiry.

```python
# Reading a mention SGID from an existing post
post = client.admin.posts.show_post(post_id)
tiptap = post.tiptap_body  # dict
for sgid, obj in tiptap["sgids_to_object_map"].items():
    if obj["type"] == "CommunityMember":
        print(f'{obj["name"]}: sgid={sgid}')

# Using a captured SGID in a new post
client.admin.posts.create_post(
    space_id=space_id,
    name="Post with mention",
    status="published",
    tiptap_body={
        "body": {
            "type": "doc",
            "content": [{
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Hey "},
                    {"type": "mention", "attrs": {"sgid": captured_sgid}},
                    {"type": "text", "text": " check this out"},
                ]
            }]
        },
        "community_members": [{
            "id": member_id, "name": "Member Name",
            "user_id": user_id, "sgid": captured_sgid,
            "type": "CommunityMember",
        }],
        "sgids_to_object_map": {
            captured_sgid: {
                "id": member_id, "name": "Member Name",
                "user_id": user_id, "sgid": captured_sgid,
                "type": "CommunityMember",
            }
        }
    },
)
```

## Polls

Polls use the same SGID mechanism as mentions. Each poll is a server-side object referenced by a signed token.

**What works:**
- Reading poll data from existing posts via `tiptap_body.polls` and `sgids_to_object_map`
- Reading poll titles, options, status, and closing dates
- Embedding an existing poll in a new post by reusing its SGID (same poll instance, shared votes)

**What does not work:**
- Creating new polls via any API endpoint -- no `/polls` endpoint exists
- Sending poll data in `tiptap_body.polls`, `polls_attributes`, or as inline node attrs -- all ignored
- Creating a poll node without an SGID -- the node is stripped from the post

**Workaround:** Create polls in the Circle UI. Use the API to read poll data for reporting and dashboards.

```python
# Reading polls from a post
post = client.admin.posts.show_post(post_id)
tiptap = post.tiptap_body  # dict
for poll in tiptap.get("polls", []):
    print(f'Poll: {poll["title"]} (id={poll["id"]})')
    print(f'  Status: {poll["status"]}, Closes: {poll["closes_at"]}')
    for opt in poll["poll_options"]:
        print(f'  - {opt["value"]} (id={opt["id"]})')
```

## Other Limitations

| Feature | Limitation |
|---|---|
| Moderator assignment | Per-space moderator roles can only be set in the Circle UI, not via API |
| Bulk member add | No bulk endpoint -- members must be added one at a time |
| Post move | Posts cannot be moved between spaces via API |
| Comment authorship | Comments are always authored as the API token owner; no `user_email` override (posts do support `user_email`) |
| Space slugs | Circle appends a hash to slugs even when explicitly set via API |
| Inherited access | `show_space_member` returns space group inherited access as if it were direct space membership |
| Resend invitation | No endpoint to resend a member invitation |
| Workflows | No API for Circle automations or workflows |
| Poll votes | Vote counts and individual votes are not returned in the API response |
