"""Generated wire schemas. Strings retain their JSON date/URL representation."""
from __future__ import annotations
from typing import Any, Literal
from typing_extensions import TypedDict, Required, NotRequired

class AdminApiKeyPage(TypedDict):
    """Wire contract: #/components/schemas/AdminApiKeyPage."""
    items: Required[list[AdminApiKeySummary]]
    page: Required[int]
    page_size: Required[int]
    pages: Required[int]
    total: Required[int]

class AdminApiKeySummary(TypedDict):
    """Wire contract: #/components/schemas/AdminApiKeySummary."""
    created_at: Required[str]
    expires_at: Required[str]
    id: Required[str]
    last_used_at: Required[str | None]
    name: Required[str]
    prefix: Required[str]
    request_count: Required[int]
    revoked_at: Required[str | None]
    scopes: Required[list[Literal['catalog:read', 'assets:download', 'listings:write', 'files:upload', 'listings:publish', 'listings:delete']]]
    status: Required[Literal['active', 'expired', 'revoked']]
    user_id: Required[int]
    username: Required[str]

class AdminApiRequestPage(TypedDict):
    """Wire contract: #/components/schemas/AdminApiRequestPage."""
    items: Required[list[AdminApiRequestSummary]]
    page: Required[int]
    page_size: Required[int]
    pages: Required[int]
    total: Required[int]

class AdminApiRequestSummary(TypedDict):
    """Wire contract: #/components/schemas/AdminApiRequestSummary."""
    duration_ms: Required[int]
    id: Required[int]
    key_id: Required[str]
    key_name: Required[str]
    key_prefix: Required[str]
    method: Required[str]
    occurred_at: Required[str]
    path: Required[str]
    status_code: Required[int]
    user_id: Required[int]
    username: Required[str]

class AdminListingSummary(TypedDict):
    """Wire contract: #/components/schemas/AdminListingSummary."""
    description: Required[str]
    id: Required[str]
    status: Required[str]
    title: Required[str]
    updated_at: Required[str]

class AdminMetricsResponse(TypedDict):
    """Wire contract: #/components/schemas/AdminMetricsResponse."""
    active_accounts: Required[int]
    active_users_last_7_days: Required[int]
    active_users_today: Required[int]
    login_events_last_7_days: Required[int]
    login_events_today: Required[int]
    new_users_last_7_days: Required[int]
    new_users_today: Required[int]
    permanently_banned_accounts: Required[int]
    published_listings: Required[int]
    published_versions: Required[int]
    site_visits_last_7_days: NotRequired[int]
    site_visits_today: NotRequired[int]
    site_visits_total: NotRequired[int]
    temporarily_banned_accounts: Required[int]
    total_users: Required[int]
    uploaded_assets: Required[int]
    verified_users: Required[int]

class AdminRatingSummary(TypedDict):
    """Wire contract: #/components/schemas/AdminRatingSummary."""
    id: Required[int]
    listing_id: Required[str]
    listing_title: Required[str]
    score: Required[int]
    updated_at: Required[str]
    vote: NotRequired[str | None]

class AdminUserDetail(TypedDict):
    """Wire contract: #/components/schemas/AdminUserDetail."""
    listings: Required[list[AdminListingSummary]]
    ratings: Required[list[AdminRatingSummary]]
    user: Required[AdminUserSummary]

class AdminUserPage(TypedDict):
    """Wire contract: #/components/schemas/AdminUserPage."""
    items: Required[list[AdminUserSummary]]
    page: Required[int]
    page_size: Required[int]
    pages: Required[int]
    total: Required[int]

class AdminUserSummary(TypedDict):
    """Wire contract: #/components/schemas/AdminUserSummary."""
    account_status: Required[str]
    asset_count: Required[int]
    banned_until: Required[str | None]
    created_at: Required[str]
    email: Required[str]
    email_verified: Required[bool]
    id: Required[int]
    last_login_at: Required[str | None]
    listing_count: Required[int]
    published_listing_count: Required[int]
    roles: Required[list[str]]
    username: Required[str]

class AnnouncementResponse(TypedDict):
    """Wire contract: #/components/schemas/AnnouncementResponse."""
    body: Required[str]
    enabled: Required[bool]
    image_url: Required[str | None]
    kind: Required[Literal['motd', 'patch_notes']]
    revision: Required[str]
    title: Required[str]
    updated_at: Required[str]

class AnnouncementUpdateRequest(TypedDict):
    """Wire contract: #/components/schemas/AnnouncementUpdateRequest."""
    body: Required[str]
    enabled: Required[bool]
    image_base64: NotRequired[str | None]
    kind: Required[Literal['motd', 'patch_notes']]
    remove_image: NotRequired[bool]
    title: Required[str]

class ApiKeyCreateRequest(TypedDict):
    """Wire contract: #/components/schemas/ApiKeyCreateRequest."""
    expires_in_days: NotRequired[int]
    name: Required[str]
    scopes: Required[list[Literal['catalog:read', 'assets:download', 'listings:write', 'files:upload', 'listings:publish', 'listings:delete']]]

class ApiKeyCreatedResponse(TypedDict):
    """Wire contract: #/components/schemas/ApiKeyCreatedResponse."""
    key: Required[ApiKeyResponse]
    token: Required[str]

class ApiKeyResponse(TypedDict):
    """Wire contract: #/components/schemas/ApiKeyResponse."""
    created_at: Required[str]
    expires_at: Required[str]
    id: Required[str]
    last_used_at: Required[str | None]
    name: Required[str]
    prefix: Required[str]
    request_count: Required[int]
    revoked_at: Required[str | None]
    scopes: Required[list[Literal['catalog:read', 'assets:download', 'listings:write', 'files:upload', 'listings:publish', 'listings:delete']]]

class ApiScopeResponse(TypedDict):
    """Wire contract: #/components/schemas/ApiScopeResponse."""
    code: Required[Literal['catalog:read', 'assets:download', 'listings:write', 'files:upload', 'listings:publish', 'listings:delete']]
    description: Required[str]
    label: Required[str]

class AssetBundle(TypedDict):
    """Wire contract: #/components/schemas/AssetBundle."""
    asset_ids: Required[list[str]]
    name: Required[str]

class CatalogMetricsResponse(TypedDict):
    """Wire contract: #/components/schemas/CatalogMetricsResponse."""
    as_of: Required[str]
    download_history_started_at: Required[str | None]

class CollaborationInvitationResponse(TypedDict):
    """Wire contract: #/components/schemas/CollaborationInvitationResponse."""
    invited_at: Required[str]
    listing_id: Required[str]
    listing_title: Required[str]
    owner_username: Required[str]
    role: NotRequired[Literal['author', 'authorized']]

class CollaboratorInviteRequest(TypedDict):
    """Wire contract: #/components/schemas/CollaboratorInviteRequest."""
    role: NotRequired[Literal['author', 'authorized']]
    username: Required[str]

class CollaboratorResponse(TypedDict):
    """Wire contract: #/components/schemas/CollaboratorResponse."""
    accepted_at: Required[str | None]
    invited_at: Required[str]
    role: NotRequired[Literal['author', 'authorized']]
    user_id: Required[int]
    username: Required[str]

class DeveloperAccessResponse(TypedDict):
    """Wire contract: #/components/schemas/DeveloperAccessResponse."""
    allowed: Required[bool]
    email_verified: Required[bool]

class EmailTokenRequest(TypedDict):
    """Wire contract: #/components/schemas/EmailTokenRequest."""
    token: Required[str]

class ExternalDependency(TypedDict):
    """Wire contract: #/components/schemas/ExternalDependency."""
    name: Required[str]
    required_version: NotRequired[str | None]
    sha256: NotRequired[str | None]
    url: NotRequired[str | None]

class FavouriteCollectionRequest(TypedDict):
    """Wire contract: #/components/schemas/FavouriteCollectionRequest."""
    ends_at: Required[str]
    listing_ids: Required[list[str]]
    starts_at: Required[str]
    title: Required[str]

class FavouriteCollectionResponse(TypedDict):
    """Wire contract: #/components/schemas/FavouriteCollectionResponse."""
    ends_at: Required[str]
    id: Required[str]
    listing_ids: Required[list[str]]
    listings: Required[list[ListingResponse]]
    starts_at: Required[str]
    title: Required[str]
    updated_at: Required[str]

class ForgotPasswordRequest(TypedDict):
    """Wire contract: #/components/schemas/ForgotPasswordRequest."""
    email: Required[str]

class GametypeCompatibility(TypedDict):
    """Wire contract: #/components/schemas/GametypeCompatibility."""
    gametype: Required[str]
    gametype_asset_id: NotRequired[str | None]
    team_counts: NotRequired[list[int] | None]

class HTTPValidationError(TypedDict):
    """Wire contract: #/components/schemas/HTTPValidationError."""
    detail: NotRequired[list[ValidationError]]

class LayoutCompatibility(TypedDict):
    """Wire contract: #/components/schemas/LayoutCompatibility."""
    base_map_family: NotRequired[str | None]
    map_asset_id: Required[str]
    playtested_player_counts: NotRequired[list[int] | None]
    recommended_players: NotRequired[PlayerRange | None]
    supported_gametypes: NotRequired[list[GametypeCompatibility] | None]

class ListingAssetResponse(TypedDict):
    """Wire contract: #/components/schemas/ListingAssetResponse."""
    asset_type: Required[str]
    created_at: Required[str]
    download_url: Required[str]
    id: Required[str]
    label: Required[str]
    original_filename: Required[str]
    sha256: Required[str]
    size_bytes: Required[int]

class ListingAssetUploadCreateRequest(TypedDict):
    """Wire contract: #/components/schemas/ListingAssetUploadCreateRequest."""
    file_size: Required[int]
    file_type: NotRequired[Literal['auto', 'gamemode', 'forged_map', 'playlist', 'megalo_source']]
    label: NotRequired[str]
    original_filename: Required[str]

class ListingAuthorResponse(TypedDict):
    """Wire contract: #/components/schemas/ListingAuthorResponse."""
    avatar_url: Required[str | None]
    is_owner: Required[bool]
    user_id: Required[int]
    username: Required[str]

class ListingChangePageResponse(TypedDict):
    """Wire contract: #/components/schemas/ListingChangePageResponse."""
    as_of: Required[str]
    items: Required[list[ListingChangeResponse]]
    page: Required[int]
    page_size: Required[int]
    pages: Required[int]
    total: Required[int]

class ListingChangeResponse(TypedDict):
    """Wire contract: #/components/schemas/ListingChangeResponse."""
    listing_id: Required[str]
    published_version_ids: Required[list[str]]
    status: Required[Literal['published', 'withdrawn']]
    updated_at: Required[str]
    withdrawn_version_ids: NotRequired[list[str]]

class ListingCreateRequest(TypedDict):
    """Wire contract: #/components/schemas/ListingCreateRequest."""
    description: NotRequired[str]
    is_modded_map: NotRequired[bool]
    max_players: NotRequired[int]
    min_players: NotRequired[int]
    release_notes: NotRequired[str]
    tags: NotRequired[list[str]]
    title: Required[str]
    version_label: NotRequired[str]
    visibility: NotRequired[Literal['public', 'private']]
    workshop_url: NotRequired[str | None]
    workshop_urls: NotRequired[list[str] | None]

class ListingImageResponse(TypedDict):
    """Wire contract: #/components/schemas/ListingImageResponse."""
    id: Required[str]
    media_type: Required[str]
    original_filename: Required[str]
    position: Required[int]
    size_bytes: Required[int]
    url: Required[str]

class ListingPageResponse(TypedDict):
    """Wire contract: #/components/schemas/ListingPageResponse."""
    items: Required[list[ListingResponse]]
    metrics: NotRequired[CatalogMetricsResponse | None]
    page: Required[int]
    page_size: Required[int]
    pages: Required[int]
    total: Required[int]

class ListingResponse(TypedDict):
    """Wire contract: #/components/schemas/ListingResponse."""
    authors: NotRequired[list[ListingAuthorResponse]]
    can_edit: NotRequired[bool]
    created_at: Required[str]
    description: Required[str]
    download_count: Required[int]
    downvote_count: NotRequired[int]
    id: Required[str]
    images: Required[list[ListingImageResponse]]
    is_modded_map: Required[bool]
    max_players: Required[int]
    min_players: Required[int]
    owner_avatar_url: Required[str | None]
    owner_id: Required[int]
    owner_username: Required[str]
    rating_average: Required[float | None]
    rating_count: Required[int]
    recent_downloads: NotRequired[RecentDownloadCounts | None]
    status: Required[str]
    tags: Required[list[str]]
    thumbnail_url: Required[str | None]
    title: Required[str]
    updated_at: Required[str]
    upvote_count: NotRequired[int]
    versions: Required[list[ListingVersionResponse]]
    view_count: NotRequired[int]
    visibility: NotRequired[Literal['public', 'private']]
    visibility_warning: NotRequired[str | None]
    vote_count: NotRequired[int]
    workshop_url: Required[str | None]
    workshop_urls: Required[list[str]]

class ListingVersionCreateRequest(TypedDict):
    """Wire contract: #/components/schemas/ListingVersionCreateRequest."""
    release_notes: NotRequired[str]
    version_label: Required[str]

class ListingVersionResponse(TypedDict):
    """Wire contract: #/components/schemas/ListingVersionResponse."""
    assets: Required[list[ListingAssetResponse]]
    compatibility: Required[ReleaseCompatibilityResponse]
    created_at: Required[str]
    id: Required[str]
    published_at: Required[str | None]
    release_notes: Required[str]
    sequence: Required[int]
    status: Required[str]
    version_label: Required[str]

class ListingVersionUpdateRequest(TypedDict):
    """Wire contract: #/components/schemas/ListingVersionUpdateRequest."""
    release_notes: NotRequired[str | None]
    version_label: NotRequired[str | None]

class ListingViewResponse(TypedDict):
    """Wire contract: #/components/schemas/ListingViewResponse."""
    view_count: Required[int]

class LoginRequest(TypedDict):
    """Wire contract: #/components/schemas/LoginRequest."""
    identifier: Required[str]
    password: Required[str]

class ManifestAssetResponse(TypedDict):
    """Wire contract: #/components/schemas/ManifestAssetResponse."""
    asset_type: Required[str]
    base_map_id: Required[int | None]
    base_map_stem: Required[str | None]
    created_at: Required[str]
    download_url: Required[str]
    format: Required[Literal['reclaimer_json', 'halo3_mvar', 'halo3_gametype_bin', 'megalo_rvt']]
    id: Required[str]
    label: Required[str]
    original_filename: Required[str]
    sha256: Required[str]
    size_bytes: Required[int]

class MetricCooldownResetResponse(TypedDict):
    """Wire contract: #/components/schemas/MetricCooldownResetResponse."""
    download_receipts: Required[int]
    view_receipts: Required[int]
    visit_receipts: Required[int]

class ModerationAuditResponse(TypedDict):
    """Wire contract: #/components/schemas/ModerationAuditResponse."""
    action: Required[str]
    actor_username: Required[str | None]
    created_at: Required[str]
    id: Required[int]
    listing_id: Required[str | None]
    listing_title: Required[str | None]
    reason: Required[str]
    target_username: Required[str | None]

class ModerationReasonRequest(TypedDict):
    """Wire contract: #/components/schemas/ModerationReasonRequest."""
    reason: Required[str]

class PasswordChangeRequest(TypedDict):
    """Wire contract: #/components/schemas/PasswordChangeRequest."""
    current_password: Required[str]
    new_password: Required[str]

class PlayerRange(TypedDict):
    """Wire contract: #/components/schemas/PlayerRange."""
    maximum: Required[int]
    minimum: Required[int]

class PublicProfileResponse(TypedDict):
    """Wire contract: #/components/schemas/PublicProfileResponse."""
    avatar_url: Required[str | None]
    created_at: Required[str]
    listings: Required[list[ListingResponse]]
    username: Required[str]

class RatingResponse(TypedDict):
    """Wire contract: #/components/schemas/RatingResponse."""
    created_at: Required[str]
    id: Required[int]
    listing_id: Required[str]
    score: Required[int]
    updated_at: Required[str]
    vote: NotRequired[Literal['up', 'down'] | None]

class RatingUpdateRequest(TypedDict):
    """Wire contract: #/components/schemas/RatingUpdateRequest."""
    score: NotRequired[int | None]
    vote: NotRequired[Literal['up', 'down'] | None]

class RecentDownloadCounts(TypedDict):
    """Wire contract: #/components/schemas/RecentDownloadCounts."""
    last_24h: Required[int]
    last_30d: Required[int]
    last_7d: Required[int]

class RegisterRequest(TypedDict):
    """Wire contract: #/components/schemas/RegisterRequest."""
    email: Required[str]
    password: Required[str]
    username: Required[str]

class ReleaseCompatibility(TypedDict):
    """Wire contract: #/components/schemas/ReleaseCompatibility."""
    bundles: NotRequired[list[AssetBundle] | None]
    dependencies: NotRequired[list[ExternalDependency] | None]
    game_engine: NotRequired[str | None]
    layouts: NotRequired[list[LayoutCompatibility]]
    required_reclaimer_version: NotRequired[str | None]
    required_scripts: NotRequired[list[ExternalDependency] | None]
    required_workshop_mods: NotRequired[list[WorkshopDependency] | None]
    special_settings: NotRequired[list[str] | None]

class ReleaseCompatibilityResponse(TypedDict):
    """Wire contract: #/components/schemas/ReleaseCompatibilityResponse."""
    bundles: NotRequired[list[AssetBundle] | None]
    dependencies: NotRequired[list[ExternalDependency] | None]
    evidence: Required[Literal['unknown', 'author_reported']]
    game_engine: NotRequired[str | None]
    layouts: NotRequired[list[LayoutCompatibility]]
    required_reclaimer_version: NotRequired[str | None]
    required_scripts: NotRequired[list[ExternalDependency] | None]
    required_workshop_mods: NotRequired[list[WorkshopDependency] | None]
    special_settings: NotRequired[list[str] | None]

class ReleaseManifestResponse(TypedDict):
    """Wire contract: #/components/schemas/ReleaseManifestResponse."""
    assets: Required[list[ManifestAssetResponse]]
    authors: NotRequired[list[ListingAuthorResponse]]
    compatibility: Required[ReleaseCompatibilityResponse]
    listing_id: Required[str]
    published_at: Required[str]
    release_notes: Required[str]
    schema_version: NotRequired[Literal[1]]
    sequence: Required[int]
    version_id: Required[str]
    version_label: Required[str]

class RequiredWorkshopModResponse(TypedDict):
    """Wire contract: #/components/schemas/RequiredWorkshopModResponse."""
    title: NotRequired[str | None]
    workshop_id: Required[str]
    workshop_url: Required[str]

class ResendVerificationRequest(TypedDict):
    """Wire contract: #/components/schemas/ResendVerificationRequest."""
    email: Required[str]

class ResetPasswordRequest(TypedDict):
    """Wire contract: #/components/schemas/ResetPasswordRequest."""
    new_password: Required[str]
    token: Required[str]

class StatusResponse(TypedDict):
    """Wire contract: #/components/schemas/StatusResponse."""
    status: Required[str]

class UploadCreateRequest(TypedDict):
    """Wire contract: #/components/schemas/UploadCreateRequest."""
    description: NotRequired[str]
    file_size: Required[int]
    file_type: NotRequired[Literal['auto', 'gamemode', 'forged_map', 'playlist', 'megalo_source']]
    original_filename: Required[str]
    tags: NotRequired[list[str]]
    title: Required[str]

class UploadSessionResponse(TypedDict):
    """Wire contract: #/components/schemas/UploadSessionResponse."""
    chunk_size: Required[int]
    expected_size: Required[int]
    expires_at: Required[str]
    id: Required[str]
    next_chunk_index: Required[int]
    received_size: Required[int]

class UploadedFileResponse(TypedDict):
    """Wire contract: #/components/schemas/UploadedFileResponse."""
    created_at: Required[str]
    description: Required[str]
    download_url: Required[str]
    file_type: Required[str]
    id: Required[str]
    original_filename: Required[str]
    sha256: Required[str]
    size_bytes: Required[int]
    tags: Required[list[str]]
    thumbnail_url: Required[str | None]
    title: Required[str]
    uploader_username: Required[str]

class UserBanRequest(TypedDict):
    """Wire contract: #/components/schemas/UserBanRequest."""
    duration_hours: NotRequired[int | None]
    kind: Required[Literal['temporary', 'permanent']]
    reason: Required[str]

class UserProfileUpdateRequest(TypedDict):
    """Wire contract: #/components/schemas/UserProfileUpdateRequest."""
    email: Required[str]
    username: Required[str]

class UserProfileUpdateResponse(TypedDict):
    """Wire contract: #/components/schemas/UserProfileUpdateResponse."""
    email_change_pending: Required[bool]
    user: Required[UserResponse]

class UserResponse(TypedDict):
    """Wire contract: #/components/schemas/UserResponse."""
    avatar_url: Required[str | None]
    created_at: Required[str]
    email: Required[str]
    email_verified: Required[bool]
    id: Required[int]
    role: Required[Literal['member', 'developer', 'moderator', 'administrator', 'owner']]
    username: Required[str]

class UserRoleUpdateRequest(TypedDict):
    """Wire contract: #/components/schemas/UserRoleUpdateRequest."""
    reason: Required[str]
    role: Required[Literal['member', 'developer', 'moderator', 'administrator']]

class ValidationError(TypedDict):
    """Wire contract: #/components/schemas/ValidationError."""
    ctx: NotRequired[dict[str, Any]]
    input: NotRequired[Any]
    loc: Required[list[str | int]]
    msg: Required[str]
    type: Required[str]

class WorkshopDependency(TypedDict):
    """Wire contract: #/components/schemas/WorkshopDependency."""
    required_version: NotRequired[str | None]
    workshop_id: Required[str]

class WorkshopModsResponse(TypedDict):
    """Wire contract: #/components/schemas/WorkshopModsResponse."""
    mods: Required[list[RequiredWorkshopModResponse]]
    title: NotRequired[str | None]
    workshop_id: Required[str]

class LegacyFileUpdateRequest(TypedDict):
    """Wire contract: #/components/schemas/backend__app__schemas__files__ListingUpdateRequest."""
    description: NotRequired[str]
    tags: NotRequired[list[str]]
    title: Required[str]

class ListingUpdateRequest(TypedDict):
    """Wire contract: #/components/schemas/backend__app__schemas__listings__ListingUpdateRequest."""
    description: NotRequired[str]
    is_modded_map: NotRequired[bool]
    max_players: NotRequired[int | None]
    min_players: NotRequired[int | None]
    tags: NotRequired[list[str]]
    title: Required[str]
    visibility: NotRequired[Literal['public', 'private'] | None]
    workshop_url: NotRequired[str | None]
    workshop_urls: NotRequired[list[str] | None]

