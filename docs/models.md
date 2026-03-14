# Models Reference

All response models use Pydantic V2 with `extra="allow"` so new API fields won't break the SDK.

## Base

- `CircleModel` -- base for all models, allows extra fields
- `PaginatedResponse[T]` -- generic paginated list with `page`, `per_page`, `has_next_page`, `count`, `records`
- `ErrorResponse` -- `success`, `message`, `error_details`

## Auth Models (`circle.models.auth`)

- `HeadlessAuthToken` -- `access_token`, `refresh_token`, expiry timestamps, `community_member_id`, `community_id`
- `RefreshedAccessToken` -- `access_token`, `access_token_expires_at`

## Admin Models (`circle.models.admin`)

| Module | Key Models |
|---|---|
| `community` | `Community`, `CommunitySetting`, `CommunityPrefs`, `ChatPreferences` |
| `members` | `CommunityMember`, `CommunityMemberList`, `CommunityMemberCreated` |
| `spaces` | `Space`, `SpaceGroup`, `SpaceMember`, `SpaceGroupMember`, `SpaceAISummary` |
| `posts` | `BasicPost`, `ImagePost`, `Comment`, `Topic` + created/updated/deleted responses |
| `events` | `Event`, `EventAttendee` |
| `courses` | `CourseSection`, `CourseLesson` |
| `tags` | `MemberTag`, `TaggedMember`, `ProfileField` |
| `misc` | `AccessGroup`, `Form`, `FormSubmission`, `CommunitySegment`, `InvitationLink`, `Embed`, `DirectUpload`, `LiveRoom`, `FlaggedContent`, `LeaderboardMember`, `AdvancedSearchResults` |

## Headless Models (`circle.models.headless`)

| Module | Key Models |
|---|---|
| `spaces` | `HeadlessSpace`, `SpaceNotificationDetail`, `SpaceBookmark` |
| `posts` | `HeadlessPost`, `HeadlessImagePost`, `HeadlessEventPost`, `SharedCommunityMember` |
| `comments` | `HeadlessComment`, `UserLike` |
| `chat` | `ChatRoom`, `ChatRoomMessage`, `ChatRoomMessages`, `ChatThread`, `ChatRoomParticipant` |
| `notifications` | `Notification`, `NewNotificationsCount`, `MediumNotificationPreferences` |
| `members` | `CurrentCommunityMember`, `PublicProfile`, `BasicCommunityMember`, `SearchedMember` |
| `courses` | `Section`, `Lesson`, `LessonFile`, `QuizAttempt` |
| `misc` | `Bookmark`, `HeadlessEventAttendee`, `RecurringEvent`, `SearchResults`, `CommunityLink`, `HeadlessDirectUpload` |
