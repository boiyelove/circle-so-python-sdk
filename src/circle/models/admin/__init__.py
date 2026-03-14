"""Admin API V2 models."""

from circle.models.admin.community import *  # noqa: F401,F403
from circle.models.admin.members import *  # noqa: F401,F403
from circle.models.admin.spaces import *  # noqa: F401,F403
from circle.models.admin.posts import *  # noqa: F401,F403
from circle.models.admin.events import *  # noqa: F401,F403
from circle.models.admin.courses import *  # noqa: F401,F403
from circle.models.admin.tags import *  # noqa: F401,F403
from circle.models.admin.misc import *  # noqa: F401,F403

__all__ = [
    # community
    "BrandColor", "CommunityPrefs", "CommunitySetting", "Community", "ChatPreferences",
    # members
    "MemberTagRef", "ProfileFieldChoice", "CommunityMemberProfileField", "ProfileFieldPage",
    "MemberProfileField", "GamificationStats", "ActivityScore",
    "CommunityMember", "CommunityMemberList", "CommunityMemberCreated",
    # spaces
    "SpaceGroupRef", "CourseSetting", "MetaTagAttributes", "Space", "SpaceList", "SpaceCreateResponse",
    "SpaceGroup", "SpaceGroupList", "SpaceMemberCommunityMember", "SpaceMember", "SpaceMemberList",
    "SpaceGroupMember", "SpaceGroupMemberList", "SpaceAISummaryTopic", "SpaceAISummary",
    # posts
    "TiptapBody", "PostBody", "BasicPost", "PostList", "ImageGalleryImage", "ImageGallery", "ImagePost",
    "BasicPostCreatedResponse", "BasicPostUpdatedResponse", "BasicPostDeletedResponse",
    "ImagePostCreatedResponse", "AISummary",
    "CommentUser", "CommentPost", "CommentSpace", "Comment", "CommentList",
    "TopicAuthor", "Topic", "TopicList",
    # events
    "EventSpace", "Event", "EventList", "EventAttendee", "EventAttendeeList",
    # courses
    "CourseSection", "CourseSectionList", "CourseLesson", "CourseLessonList",
    # tags
    "MemberTagDisplayLocations", "MemberTag", "MemberTagList",
    "TaggedMember", "TaggedMemberList",
    "ProfileFieldNumberOptions", "ProfileFieldChoice", "ProfileFieldPage",
    "ProfileField", "ProfileFieldList",
    # misc
    "AccessGroup", "AccessGroupList", "AccessGroupCommunityMember", "AccessGroupCommunityMemberList",
    "FormEmbedStyles", "Form", "FormList", "FormSubmissionField", "FormSubmission", "FormSubmissionList",
    "SegmentCreatedBy", "CommunitySegment", "CommunitySegmentList",
    "InvitationLink", "InvitationLinkList",
    "Embed", "DirectUploadInfo", "DirectUpload",
    "LiveRoom", "LiveRoomList",
    "FlaggedContent", "FlaggedContentList",
    "LeaderboardMember", "AdvancedSearchedPost", "AdvancedSearchResults",
]
