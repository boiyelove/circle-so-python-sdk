"""Community and community settings models."""
from __future__ import annotations
from typing import Any, List, Optional
from circle.models.base import CircleModel


class BrandColor(CircleModel):
    light: Optional[str] = None
    dark: Optional[str] = None


class CommunityPrefs(CircleModel):
    has_posts: Optional[bool] = None
    has_spaces: Optional[bool] = None
    has_invited_member: Optional[bool] = None
    brand_color: Optional[BrandColor] = None
    brand_text_color: Optional[BrandColor] = None


class CommunitySetting(CircleModel):
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    ios_app_enabled: Optional[bool] = None
    show_ios_app_banner: Optional[bool] = None
    deactivate_account_enabled: Optional[bool] = None
    allow_profile_search_indexing: Optional[bool] = None
    truncate_post_body_in_email_notifications: Optional[bool] = None
    hide_emails_on_member_profiles: Optional[bool] = None
    allow_members_to_go_live: Optional[bool] = None
    enforce_otp_for_signup: Optional[bool] = None
    community_activity_notifications_email_enabled: Optional[bool] = None
    community_activity_notifications_in_app_enabled: Optional[bool] = None
    desktop_app_community_visibility_enabled: Optional[bool] = None
    allow_moderator_csv_download: Optional[bool] = None
    default_space_ids: Optional[List[int]] = None
    default_logged_out_redirect_type: Optional[str] = None
    default_logged_out_redirect_id: Optional[int] = None


class Community(CircleModel):
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    name: Optional[str] = None
    locale: Optional[str] = None
    slug: Optional[str] = None
    allow_signups_to_public_community: Optional[bool] = None
    community_switcher_enabled: Optional[bool] = None
    custom_cta_for_share_links: Optional[bool] = None
    locked_post_cta_heading: Optional[str] = None
    locked_post_cta_body: Optional[str] = None
    locked_post_cta_button_text: Optional[str] = None
    locked_post_cta_button_url: Optional[str] = None
    custom_tos_enabled: Optional[bool] = None
    custom_tos: Optional[str] = None
    default_existing_member_space_id: Optional[int] = None
    default_logged_out_space_id: Optional[int] = None
    default_new_member_space_id: Optional[int] = None
    default_search_sorting: Optional[str] = None
    is_private: Optional[bool] = None
    private_signup_link_label: Optional[str] = None
    private_signup_link_url: Optional[str] = None
    reply_to_email: Optional[str] = None
    white_label: Optional[bool] = None
    weekly_digest_enabled: Optional[bool] = None
    digest_subject: Optional[str] = None
    digest_intro: Optional[str] = None
    digests_hide_posts: Optional[bool] = None
    digests_hide_comments: Optional[bool] = None
    digests_hide_stats: Optional[bool] = None
    digests_hide_members: Optional[bool] = None
    prefs: Optional[CommunityPrefs] = None
    community_setting: Optional[CommunitySetting] = None


class ChatPreferences(CircleModel):
    id: Optional[int] = None
    messaging_enabled: Optional[bool] = None
    group_messaging_enabled: Optional[bool] = None
    voice_messages_enabled: Optional[bool] = None
    member_to_member_messaging_enabled: Optional[bool] = None
