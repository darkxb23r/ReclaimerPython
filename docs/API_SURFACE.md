# API surface and coverage

The current supported contract is `partner-api.md`, the source README, and the
FastAPI route/Pydantic schema definitions. `openapi.json` captures that contract
plus raw streams, headers, documentation routes and response types omitted by
FastAPI's automatic schema. All operations have concrete sync and async methods.

## Authentication and invariants

- Bearer API keys: catalog:read, assets:download, listings:write, files:upload, listings:publish, listings:delete. Keys never grant membership or staff privileges.
- Cookie sessions (`reclaimerforge_session`): account, keys, votes, collaborations and staff APIs. Website aliases support anonymous reads. No OAuth contract exists.
- Key default quota: 120 requests / 60 seconds. Respect Retry-After and X-RateLimit-*; database failures use 503 with Retry-After: 5.
- IDs are opaque; private content requires accepted membership. Keep null distinct from empty lists. Manifest schema_version is 1; compatibility and published bytes are pinned.
- PATCH listing metadata requires title and defaults can clear fields; version PATCH is partial. Raw images and chunks are not multipart forms.
- Server errors carry detail (string or validation array). Errors include 400/401/403/404/409/410/413/415/422/429/503.

## Historical proposals and documentation gaps

`docs/architecture-plan.md` proposes `/api/v1` releases, reports, and uploads.
Those routes are not implemented and have no complete request/response contracts.
The current README and partner guide supersede them. They are recorded below
and remain accessible through request() if a future server implements them;
the SDK does not claim server support or invent schemas. Webhooks, hosting
permissions, script uploads and host feedback are explicitly future work.

The automatic schema omits stream bodies, x-filename, Content-Type, and hidden
documentation routes; this snapshot supplements them from route definitions.
Source hashes are in source-inventory.json. No .env, uploads, or secrets were read.

## Operations

| Resource | Operations |
| --- | ---: |
| admin_announcement | 3 |
| admin_api_activity | 3 |
| admin_audit | 1 |
| admin_favourites | 5 |
| admin_listings | 3 |
| admin_metrics | 2 |
| admin_ratings | 1 |
| admin_users | 5 |
| auth | 7 |
| collaboration | 6 |
| developer | 6 |
| documentation | 3 |
| downloads | 2 |
| favourites | 1 |
| files | 12 |
| health | 2 |
| listings | 25 |
| ratings | 3 |
| user | 5 |
| users | 2 |
| website | 8 |
| **Total** | **105** |

| Method | Path | Sync/async resource method | Return |
| --- | --- | --- | --- |
| GET | `/api/admin/announcement` | `admin_announcement.announcement_settings` | `models.AnnouncementResponse` |
| PUT | `/api/admin/announcement` | `admin_announcement.update_announcement` | `models.AnnouncementResponse` |
| GET | `/api/admin/announcement/image/{image_id}` | `admin_announcement.admin_image` | `bytes` |
| GET | `/api/admin/api-activity/keys` | `admin_api_activity.keys` | `models.AdminApiKeyPage` |
| GET | `/api/admin/api-activity/keys/{key_id}` | `admin_api_activity.key_detail` | `models.AdminApiKeySummary` |
| GET | `/api/admin/api-activity/requests` | `admin_api_activity.requests` | `models.AdminApiRequestPage` |
| GET | `/api/admin/audit` | `admin_audit.audit_history` | `list[models.ModerationAuditResponse]` |
| GET | `/api/admin/favourites` | `admin_favourites.all_favourites` | `list[models.FavouriteCollectionResponse]` |
| POST | `/api/admin/favourites` | `admin_favourites.create_favourites` | `models.FavouriteCollectionResponse` |
| DELETE | `/api/admin/favourites/{collection_id}` | `admin_favourites.delete_favourites` | `None` |
| GET | `/api/admin/favourites/{collection_id}` | `admin_favourites.favourite_detail` | `models.FavouriteCollectionResponse` |
| PUT | `/api/admin/favourites/{collection_id}` | `admin_favourites.update_favourites` | `models.FavouriteCollectionResponse` |
| POST | `/api/admin/listings/{listing_id}/clear-description` | `admin_listings.clear_description` | `models.AdminListingSummary` |
| POST | `/api/admin/listings/{listing_id}/remove` | `admin_listings.remove_listing` | `models.AdminListingSummary` |
| POST | `/api/admin/listings/{listing_id}/restore` | `admin_listings.restore_listing` | `models.AdminListingSummary` |
| GET | `/api/admin/metrics` | `admin_metrics.metrics` | `models.AdminMetricsResponse` |
| POST | `/api/admin/metrics/reset-cooldowns` | `admin_metrics.reset_cooldowns` | `models.MetricCooldownResetResponse` |
| DELETE | `/api/admin/ratings/{rating_id}` | `admin_ratings.remove_rating` | `None` |
| GET | `/api/admin/users` | `admin_users.users` | `models.AdminUserPage` |
| GET | `/api/admin/users/{user_id}` | `admin_users.user_detail` | `models.AdminUserDetail` |
| POST | `/api/admin/users/{user_id}/ban` | `admin_users.ban` | `models.AdminUserDetail` |
| PUT | `/api/admin/users/{user_id}/role` | `admin_users.update_role` | `models.AdminUserDetail` |
| POST | `/api/admin/users/{user_id}/unban` | `admin_users.unban` | `models.AdminUserDetail` |
| POST | `/api/auth/forgot-password` | `auth.forgot_password` | `models.StatusResponse` |
| POST | `/api/auth/login` | `auth.login` | `models.UserResponse` |
| POST | `/api/auth/logout` | `auth.logout` | `models.StatusResponse` |
| POST | `/api/auth/register` | `auth.register` | `models.UserResponse` |
| POST | `/api/auth/resend-verification` | `auth.resend_verification` | `models.StatusResponse` |
| POST | `/api/auth/reset-password` | `auth.reset_password` | `models.StatusResponse` |
| POST | `/api/auth/verify-email` | `auth.verify_email` | `models.UserResponse` |
| GET | `/api/listings/{listing_id}/collaborators` | `collaboration.list_collaborators` | `list[models.CollaboratorResponse]` |
| POST | `/api/listings/{listing_id}/collaborators` | `collaboration.invite` | `list[models.CollaboratorResponse]` |
| DELETE | `/api/listings/{listing_id}/collaborators/{user_id}` | `collaboration.remove` | `None` |
| GET | `/api/user/me/collaborations` | `collaboration.pending_invitations` | `list[models.CollaborationInvitationResponse]` |
| DELETE | `/api/user/me/collaborations/{listing_id}` | `collaboration.decline` | `None` |
| POST | `/api/user/me/collaborations/{listing_id}/accept` | `collaboration.accept` | `None` |
| GET | `/api/developer/access` | `developer.developer_access` | `models.DeveloperAccessResponse` |
| GET | `/api/developer/guide` | `developer.developer_guide` | `str` |
| GET | `/api/developer/keys` | `developer.keys` | `list[models.ApiKeyResponse]` |
| POST | `/api/developer/keys` | `developer.new_key` | `models.ApiKeyCreatedResponse` |
| DELETE | `/api/developer/keys/{key_id}` | `developer.revoke_key` | `None` |
| GET | `/api/developer/scopes` | `developer.scopes` | `list[models.ApiScopeResponse]` |
| GET | `/api/docs` | `documentation.swagger_ui` | `str` |
| GET | `/api/openapi.json` | `documentation.openapi_schema` | `dict[str, Any]` |
| GET | `/docs` | `documentation.swagger_ui_alias` | `str` |
| GET | `/files/assets/{asset_id}/{filename}` | `downloads.download_listing_asset` | `bytes` |
| GET | `/files/{file_id}/{filename}` | `downloads.download_file` | `bytes` |
| GET | `/api/favourites` | `favourites.active_favourites` | `list[models.FavouriteCollectionResponse]` |
| GET | `/api/files` | `files.current_listings` | `list[models.UploadedFileResponse]` |
| GET | `/api/files/mine` | `files.my_files` | `list[models.UploadedFileResponse]` |
| POST | `/api/files/uploads` | `files.start_upload` | `models.UploadSessionResponse` |
| GET | `/api/files/uploads/{upload_id}` | `files.upload_status` | `models.UploadSessionResponse` |
| PUT | `/api/files/uploads/{upload_id}/chunks/{chunk_index}` | `files.upload_chunk` | `models.UploadSessionResponse` |
| POST | `/api/files/uploads/{upload_id}/complete` | `files.finish_upload` | `models.UploadedFileResponse` |
| DELETE | `/api/files/{file_id}` | `files.delete_file` | `None` |
| GET | `/api/files/{file_id}` | `files.file_metadata` | `models.UploadedFileResponse` |
| PATCH | `/api/files/{file_id}` | `files.edit_file` | `models.UploadedFileResponse` |
| PUT | `/api/files/{file_id}/content` | `files.replace_file_content` | `models.UploadedFileResponse` |
| GET | `/api/files/{file_id}/thumbnail` | `files.get_thumbnail` | `bytes` |
| PUT | `/api/files/{file_id}/thumbnail` | `files.set_thumbnail` | `models.UploadedFileResponse` |
| GET | `/api/health` | `health.health` | `models.StatusResponse` |
| GET | `/api/ready` | `health.readiness` | `models.StatusResponse` |
| GET | `/api/listings` | `listings.public_listings` | `models.ListingPageResponse` |
| POST | `/api/listings` | `listings.new_listing` | `models.ListingResponse` |
| GET | `/api/listings/assets/{asset_id}/download` | `listings.track_asset_download` | `bytes` |
| GET | `/api/listings/changes` | `listings.catalog_changes` | `models.ListingChangePageResponse` |
| GET | `/api/listings/mine` | `listings.my_listings` | `list[models.ListingResponse]` |
| GET | `/api/listings/mine/{listing_id}` | `listings.my_listing_detail` | `models.ListingResponse` |
| POST | `/api/listings/uploads/{upload_id}/complete` | `listings.finish_asset_upload` | `models.ListingAssetResponse` |
| GET | `/api/listings/versions/{version_id}/download` | `listings.download_version_archive` | `bytes` |
| DELETE | `/api/listings/{listing_id}` | `listings.remove_listing` | `None` |
| GET | `/api/listings/{listing_id}` | `listings.listing_detail` | `models.ListingResponse` |
| PATCH | `/api/listings/{listing_id}` | `listings.edit_listing` | `models.ListingResponse` |
| POST | `/api/listings/{listing_id}/images` | `listings.upload_gallery_image` | `models.ListingResponse` |
| DELETE | `/api/listings/{listing_id}/images/{image_id}` | `listings.remove_gallery_image` | `None` |
| GET | `/api/listings/{listing_id}/images/{image_id}` | `listings.get_gallery_image` | `bytes` |
| GET | `/api/listings/{listing_id}/thumbnail` | `listings.get_listing_thumbnail` | `bytes` |
| PUT | `/api/listings/{listing_id}/thumbnail` | `listings.set_listing_thumbnail` | `models.ListingResponse` |
| POST | `/api/listings/{listing_id}/versions` | `listings.new_version` | `models.ListingResponse` |
| DELETE | `/api/listings/{listing_id}/versions/{version_id}` | `listings.remove_version` | `None` |
| PATCH | `/api/listings/{listing_id}/versions/{version_id}` | `listings.edit_version_metadata` | `models.ListingResponse` |
| DELETE | `/api/listings/{listing_id}/versions/{version_id}/assets/{asset_id}` | `listings.remove_draft_asset` | `None` |
| PUT | `/api/listings/{listing_id}/versions/{version_id}/compatibility` | `listings.edit_version_compatibility` | `models.ListingVersionResponse` |
| GET | `/api/listings/{listing_id}/versions/{version_id}/manifest` | `listings.release_manifest` | `models.ReleaseManifestResponse` |
| POST | `/api/listings/{listing_id}/versions/{version_id}/publish` | `listings.publish_listing_version` | `models.ListingResponse` |
| POST | `/api/listings/{listing_id}/versions/{version_id}/uploads` | `listings.new_asset_upload` | `models.UploadSessionResponse` |
| GET | `/api/listings/{listing_id}/workshop` | `listings.listing_workshop` | `models.WorkshopModsResponse` |
| DELETE | `/api/listings/{listing_id}/rating` | `ratings.remove_rating` | `None` |
| GET | `/api/listings/{listing_id}/rating` | `ratings.my_rating` | `models.RatingResponse | None` |
| PUT | `/api/listings/{listing_id}/rating` | `ratings.update_rating` | `models.RatingResponse` |
| GET | `/api/user/me` | `user.current_user` | `models.UserResponse` |
| PATCH | `/api/user/me` | `user.update_current_user` | `models.UserProfileUpdateResponse` |
| DELETE | `/api/user/me/avatar` | `user.delete_current_avatar` | `models.UserResponse` |
| PUT | `/api/user/me/avatar` | `user.set_current_avatar` | `models.UserResponse` |
| PUT | `/api/user/me/password` | `user.update_current_password` | `models.StatusResponse` |
| GET | `/api/users/{username}` | `users.public_profile` | `models.PublicProfileResponse` |
| GET | `/api/users/{username}/avatar` | `users.public_avatar` | `bytes` |
| GET | `/api/public/announcement` | `website.active_announcement` | `models.AnnouncementResponse | None` |
| GET | `/api/public/announcement/image/{image_id}` | `website.public_image` | `bytes` |
| GET | `/api/public/favourites` | `website.active_favourites` | `list[models.FavouriteCollectionResponse]` |
| GET | `/api/public/listings` | `website.public_listings` | `models.ListingPageResponse` |
| GET | `/api/public/listings/{listing_id}` | `website.listing_detail` | `models.ListingResponse` |
| POST | `/api/public/listings/{listing_id}/view` | `website.view_listing` | `models.ListingViewResponse` |
| GET | `/api/public/listings/{listing_id}/workshop` | `website.listing_workshop` | `models.WorkshopModsResponse` |
| POST | `/api/public/site-visit` | `website.visit_site` | `None` |

## Historical /api/v1 proposal (not available on current server)

See original docs/architecture-plan.md, section 13: account registration,
verification, login/logout/password resets/me; listing list/create/detail/edit;
listing release list/create; release detail/edit/download; upload start/chunk/
complete/status; listing rating and reports. These are superseded design sketches.

| Method | Proposed path |
| --- | --- |
| POST | `/api/v1/auth/register` |
| POST | `/api/v1/auth/verify-email` |
| POST | `/api/v1/auth/login` |
| POST | `/api/v1/auth/logout` |
| POST | `/api/v1/auth/request-password-reset` |
| POST | `/api/v1/auth/reset-password` |
| GET | `/api/v1/auth/me` |
| GET | `/api/v1/listings` |
| POST | `/api/v1/listings` |
| GET | `/api/v1/listings/{slug}` |
| PATCH | `/api/v1/listings/{id}` |
| GET | `/api/v1/listings/{id}/releases` |
| POST | `/api/v1/listings/{id}/releases` |
| GET | `/api/v1/releases/{id}` |
| PATCH | `/api/v1/releases/{id}` |
| POST | `/api/v1/uploads` |
| PUT | `/api/v1/uploads/{id}/chunks/{index}` |
| POST | `/api/v1/uploads/{id}/complete` |
| GET | `/api/v1/uploads/{id}/status` |
| GET | `/api/v1/releases/{id}/download` |
| PUT | `/api/v1/listings/{id}/rating` |
| POST | `/api/v1/listings/{id}/reports` |

## Conflicts resolved against current schemas and routes

The partner Markdown says script uploads are unsupported, but the current
developer page, schemas, and validator support `megalo_source` (.rvt) and
manifest format `megalo_rvt`. Both are included in the SDK. Discovery schemas
also allow relevance, most_downloads, least_downloads, most_liked, least_liked,
newest and oldest beyond the original eight sorts. Current code uses an
anonymous browser identifier with an IP fallback for traffic deduplication,
while parts of the prose still describe an IP-only rule. The SDK forwards
cookies and headers and delegates these rules to the server.
