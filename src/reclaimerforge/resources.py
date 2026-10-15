"""Generated endpoint methods; regenerate with tools/generate.py."""
from __future__ import annotations
from typing import Any, Literal, TYPE_CHECKING, cast
import httpx
from . import models
from ._types import UNSET, Unset, RequestOptions
from ._encoding import endpoint_path
if TYPE_CHECKING:
    from .client import ReclaimerForgeClient, AsyncReclaimerForgeClient

class AdminAnnouncement:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def announcement_settings(self, *, options: RequestOptions | None = None) -> models.AnnouncementResponse:
        """Announcement Settings.

        HTTP: GET /api/admin/announcement.

        Source: backend/app/routes/api/announcements/router.py:29; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session with announcements.manage: saved settings, including disabled content and a protected image URL.
        """
        return cast('models.AnnouncementResponse', self._client._call('GET', endpoint_path('/api/admin/announcement', {}), params={}, headers={}, options=options, response_kind='json'))

    def update_announcement(self, *, content_type: str, body: models.AnnouncementUpdateRequest, options: RequestOptions | None = None) -> models.AnnouncementResponse:
        """Update Announcement.

        HTTP: PUT /api/admin/announcement.

        Source: backend/app/routes/api/announcements/router.py:38; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session: atomically save settings and issue a new browser-dismissal revision.

Requires JSON (415 otherwise), at most 8 MiB (413), with all text/type/enabled fields.
Markdown body limit: 20,000 characters. Optional raw base64 JPEG/PNG/WebP image:
at most 5 MiB decoded, with no data-URL prefix. Invalid fields/images return 422.
API keys cannot edit announcements. Missing migration initialization returns 503.

        content-type: {"type": "string"}
        """
        return cast('models.AnnouncementResponse', self._client._call('PUT', endpoint_path('/api/admin/announcement', {}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', json=body))

    def admin_image(self, image_id: str, *, options: RequestOptions | None = None) -> bytes:
        """Admin Image.

        HTTP: GET /api/admin/announcement/image/{image_id}.

        Source: backend/app/routes/api/announcements/router.py:91; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session with announcements.manage: current image preview, available even while publication is disabled.

        image_id: {"title": "Image Id", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/api/admin/announcement/image/{image_id}', {'image_id': image_id}), params={}, headers={}, options=options, response_kind='bytes'))

class AsyncAdminAnnouncement:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def announcement_settings(self, *, options: RequestOptions | None = None) -> models.AnnouncementResponse:
        """Announcement Settings.

        HTTP: GET /api/admin/announcement.

        Source: backend/app/routes/api/announcements/router.py:29; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session with announcements.manage: saved settings, including disabled content and a protected image URL.
        """
        return cast('models.AnnouncementResponse', await self._client._call('GET', endpoint_path('/api/admin/announcement', {}), params={}, headers={}, options=options, response_kind='json'))

    async def update_announcement(self, *, content_type: str, body: models.AnnouncementUpdateRequest, options: RequestOptions | None = None) -> models.AnnouncementResponse:
        """Update Announcement.

        HTTP: PUT /api/admin/announcement.

        Source: backend/app/routes/api/announcements/router.py:38; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session: atomically save settings and issue a new browser-dismissal revision.

Requires JSON (415 otherwise), at most 8 MiB (413), with all text/type/enabled fields.
Markdown body limit: 20,000 characters. Optional raw base64 JPEG/PNG/WebP image:
at most 5 MiB decoded, with no data-URL prefix. Invalid fields/images return 422.
API keys cannot edit announcements. Missing migration initialization returns 503.

        content-type: {"type": "string"}
        """
        return cast('models.AnnouncementResponse', await self._client._call('PUT', endpoint_path('/api/admin/announcement', {}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', json=body))

    async def admin_image(self, image_id: str, *, options: RequestOptions | None = None) -> bytes:
        """Admin Image.

        HTTP: GET /api/admin/announcement/image/{image_id}.

        Source: backend/app/routes/api/announcements/router.py:91; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session with announcements.manage: current image preview, available even while publication is disabled.

        image_id: {"title": "Image Id", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/api/admin/announcement/image/{image_id}', {'image_id': image_id}), params={}, headers={}, options=options, response_kind='bytes'))

class AdminApiActivity:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def keys(self, *, q: str | None | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, options: RequestOptions | None = None) -> models.AdminApiKeyPage:
        """Keys.

        HTTP: GET /api/admin/api-activity/keys.

        Source: backend/app/routes/api/admin/api_activity/router.py:18; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        q: {"anyOf": [{"maxLength": 80, "type": "string"}, {"type": "null"}], "title": "Q"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 25, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}
        """
        return cast('models.AdminApiKeyPage', self._client._call('GET', endpoint_path('/api/admin/api-activity/keys', {}), params={'q': q, 'page': page, 'page_size': page_size}, headers={}, options=options, response_kind='json'))

    def key_detail(self, key_id: str, *, options: RequestOptions | None = None) -> models.AdminApiKeySummary:
        """Key Detail.

        HTTP: GET /api/admin/api-activity/keys/{key_id}.

        Source: backend/app/routes/api/admin/api_activity/router.py:28; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        key_id: {"title": "Key Id", "type": "string"}
        """
        return cast('models.AdminApiKeySummary', self._client._call('GET', endpoint_path('/api/admin/api-activity/keys/{key_id}', {'key_id': key_id}), params={}, headers={}, options=options, response_kind='json'))

    def requests(self, *, key_id: str | None | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, options: RequestOptions | None = None) -> models.AdminApiRequestPage:
        """Requests.

        HTTP: GET /api/admin/api-activity/requests.

        Source: backend/app/routes/api/admin/api_activity/router.py:36; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        key_id: {"anyOf": [{"maxLength": 36, "type": "string"}, {"type": "null"}], "title": "Key Id"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 25, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}
        """
        return cast('models.AdminApiRequestPage', self._client._call('GET', endpoint_path('/api/admin/api-activity/requests', {}), params={'key_id': key_id, 'page': page, 'page_size': page_size}, headers={}, options=options, response_kind='json'))

class AsyncAdminApiActivity:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def keys(self, *, q: str | None | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, options: RequestOptions | None = None) -> models.AdminApiKeyPage:
        """Keys.

        HTTP: GET /api/admin/api-activity/keys.

        Source: backend/app/routes/api/admin/api_activity/router.py:18; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        q: {"anyOf": [{"maxLength": 80, "type": "string"}, {"type": "null"}], "title": "Q"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 25, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}
        """
        return cast('models.AdminApiKeyPage', await self._client._call('GET', endpoint_path('/api/admin/api-activity/keys', {}), params={'q': q, 'page': page, 'page_size': page_size}, headers={}, options=options, response_kind='json'))

    async def key_detail(self, key_id: str, *, options: RequestOptions | None = None) -> models.AdminApiKeySummary:
        """Key Detail.

        HTTP: GET /api/admin/api-activity/keys/{key_id}.

        Source: backend/app/routes/api/admin/api_activity/router.py:28; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        key_id: {"title": "Key Id", "type": "string"}
        """
        return cast('models.AdminApiKeySummary', await self._client._call('GET', endpoint_path('/api/admin/api-activity/keys/{key_id}', {'key_id': key_id}), params={}, headers={}, options=options, response_kind='json'))

    async def requests(self, *, key_id: str | None | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, options: RequestOptions | None = None) -> models.AdminApiRequestPage:
        """Requests.

        HTTP: GET /api/admin/api-activity/requests.

        Source: backend/app/routes/api/admin/api_activity/router.py:36; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        key_id: {"anyOf": [{"maxLength": 36, "type": "string"}, {"type": "null"}], "title": "Key Id"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 25, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}
        """
        return cast('models.AdminApiRequestPage', await self._client._call('GET', endpoint_path('/api/admin/api-activity/requests', {}), params={'key_id': key_id, 'page': page, 'page_size': page_size}, headers={}, options=options, response_kind='json'))

class AdminAudit:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def audit_history(self, *, limit: int | Unset = UNSET, options: RequestOptions | None = None) -> list[models.ModerationAuditResponse]:
        """Audit History.

        HTTP: GET /api/admin/audit.

        Source: backend/app/routes/api/admin/audit/router.py:14; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        limit: {"default": 100, "maximum": 500, "minimum": 1, "title": "Limit", "type": "integer"}
        """
        return cast('list[models.ModerationAuditResponse]', self._client._call('GET', endpoint_path('/api/admin/audit', {}), params={'limit': limit}, headers={}, options=options, response_kind='json'))

class AsyncAdminAudit:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def audit_history(self, *, limit: int | Unset = UNSET, options: RequestOptions | None = None) -> list[models.ModerationAuditResponse]:
        """Audit History.

        HTTP: GET /api/admin/audit.

        Source: backend/app/routes/api/admin/audit/router.py:14; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        limit: {"default": 100, "maximum": 500, "minimum": 1, "title": "Limit", "type": "integer"}
        """
        return cast('list[models.ModerationAuditResponse]', await self._client._call('GET', endpoint_path('/api/admin/audit', {}), params={'limit': limit}, headers={}, options=options, response_kind='json'))

class AdminFavourites:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def all_favourites(self, *, limit: int | Unset = UNSET, options: RequestOptions | None = None) -> list[models.FavouriteCollectionResponse]:
        """All Favourites.

        HTTP: GET /api/admin/favourites.

        Source: backend/app/routes/api/favourites/router.py:28; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session with favourites.manage: newest scheduled/history collections, retaining unavailable selected IDs.

        limit: {"default": 100, "maximum": 100, "minimum": 1, "title": "Limit", "type": "integer"}
        """
        return cast('list[models.FavouriteCollectionResponse]', self._client._call('GET', endpoint_path('/api/admin/favourites', {}), params={'limit': limit}, headers={}, options=options, response_kind='json'))

    def create_favourites(self, *, body: models.FavouriteCollectionRequest, options: RequestOptions | None = None) -> models.FavouriteCollectionResponse:
        """Create Favourites.

        HTTP: POST /api/admin/favourites.

        Source: backend/app/routes/api/favourites/router.py:46; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session with favourites.manage: create a scheduled 1–20-map selection; API keys cannot curate.
        """
        return cast('models.FavouriteCollectionResponse', self._client._call('POST', endpoint_path('/api/admin/favourites', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def delete_favourites(self, collection_id: str, *, options: RequestOptions | None = None) -> None:
        """Delete Favourites.

        HTTP: DELETE /api/admin/favourites/{collection_id}.

        Source: backend/app/routes/api/favourites/router.py:76; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session: remove this collection from the schedule; listings and their metrics are preserved.

        collection_id: {"title": "Collection Id", "type": "string"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/admin/favourites/{collection_id}', {'collection_id': collection_id}), params={}, headers={}, options=options, response_kind='json'))

    def favourite_detail(self, collection_id: str, *, options: RequestOptions | None = None) -> models.FavouriteCollectionResponse:
        """Favourite Detail.

        HTTP: GET /api/admin/favourites/{collection_id}.

        Source: backend/app/routes/api/favourites/router.py:37; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session: saved collection and ordered published listing expansion; unavailable IDs are retained.

        collection_id: {"title": "Collection Id", "type": "string"}
        """
        return cast('models.FavouriteCollectionResponse', self._client._call('GET', endpoint_path('/api/admin/favourites/{collection_id}', {'collection_id': collection_id}), params={}, headers={}, options=options, response_kind='json'))

    def update_favourites(self, collection_id: str, *, body: models.FavouriteCollectionRequest, options: RequestOptions | None = None) -> models.FavouriteCollectionResponse:
        """Update Favourites.

        HTTP: PUT /api/admin/favourites/{collection_id}.

        Source: backend/app/routes/api/favourites/router.py:59; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session: replace title, timezone-aware display period and ordered eligible map IDs; invalid selections return 422.

        collection_id: {"title": "Collection Id", "type": "string"}
        """
        return cast('models.FavouriteCollectionResponse', self._client._call('PUT', endpoint_path('/api/admin/favourites/{collection_id}', {'collection_id': collection_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class AsyncAdminFavourites:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def all_favourites(self, *, limit: int | Unset = UNSET, options: RequestOptions | None = None) -> list[models.FavouriteCollectionResponse]:
        """All Favourites.

        HTTP: GET /api/admin/favourites.

        Source: backend/app/routes/api/favourites/router.py:28; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session with favourites.manage: newest scheduled/history collections, retaining unavailable selected IDs.

        limit: {"default": 100, "maximum": 100, "minimum": 1, "title": "Limit", "type": "integer"}
        """
        return cast('list[models.FavouriteCollectionResponse]', await self._client._call('GET', endpoint_path('/api/admin/favourites', {}), params={'limit': limit}, headers={}, options=options, response_kind='json'))

    async def create_favourites(self, *, body: models.FavouriteCollectionRequest, options: RequestOptions | None = None) -> models.FavouriteCollectionResponse:
        """Create Favourites.

        HTTP: POST /api/admin/favourites.

        Source: backend/app/routes/api/favourites/router.py:46; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session with favourites.manage: create a scheduled 1–20-map selection; API keys cannot curate.
        """
        return cast('models.FavouriteCollectionResponse', await self._client._call('POST', endpoint_path('/api/admin/favourites', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def delete_favourites(self, collection_id: str, *, options: RequestOptions | None = None) -> None:
        """Delete Favourites.

        HTTP: DELETE /api/admin/favourites/{collection_id}.

        Source: backend/app/routes/api/favourites/router.py:76; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session: remove this collection from the schedule; listings and their metrics are preserved.

        collection_id: {"title": "Collection Id", "type": "string"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/admin/favourites/{collection_id}', {'collection_id': collection_id}), params={}, headers={}, options=options, response_kind='json'))

    async def favourite_detail(self, collection_id: str, *, options: RequestOptions | None = None) -> models.FavouriteCollectionResponse:
        """Favourite Detail.

        HTTP: GET /api/admin/favourites/{collection_id}.

        Source: backend/app/routes/api/favourites/router.py:37; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session: saved collection and ordered published listing expansion; unavailable IDs are retained.

        collection_id: {"title": "Collection Id", "type": "string"}
        """
        return cast('models.FavouriteCollectionResponse', await self._client._call('GET', endpoint_path('/api/admin/favourites/{collection_id}', {'collection_id': collection_id}), params={}, headers={}, options=options, response_kind='json'))

    async def update_favourites(self, collection_id: str, *, body: models.FavouriteCollectionRequest, options: RequestOptions | None = None) -> models.FavouriteCollectionResponse:
        """Update Favourites.

        HTTP: PUT /api/admin/favourites/{collection_id}.

        Source: backend/app/routes/api/favourites/router.py:59; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/Admin session: replace title, timezone-aware display period and ordered eligible map IDs; invalid selections return 422.

        collection_id: {"title": "Collection Id", "type": "string"}
        """
        return cast('models.FavouriteCollectionResponse', await self._client._call('PUT', endpoint_path('/api/admin/favourites/{collection_id}', {'collection_id': collection_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class AdminListings:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def clear_description(self, listing_id: str, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> models.AdminListingSummary:
        """Clear Description.

        HTTP: POST /api/admin/listings/{listing_id}/clear-description.

        Source: backend/app/routes/api/admin/listings/router.py:66; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.AdminListingSummary', self._client._call('POST', endpoint_path('/api/admin/listings/{listing_id}/clear-description', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def remove_listing(self, listing_id: str, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> models.AdminListingSummary:
        """Remove Listing.

        HTTP: POST /api/admin/listings/{listing_id}/remove.

        Source: backend/app/routes/api/admin/listings/router.py:44; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.AdminListingSummary', self._client._call('POST', endpoint_path('/api/admin/listings/{listing_id}/remove', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def restore_listing(self, listing_id: str, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> models.AdminListingSummary:
        """Restore Listing.

        HTTP: POST /api/admin/listings/{listing_id}/restore.

        Source: backend/app/routes/api/admin/listings/router.py:55; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.AdminListingSummary', self._client._call('POST', endpoint_path('/api/admin/listings/{listing_id}/restore', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class AsyncAdminListings:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def clear_description(self, listing_id: str, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> models.AdminListingSummary:
        """Clear Description.

        HTTP: POST /api/admin/listings/{listing_id}/clear-description.

        Source: backend/app/routes/api/admin/listings/router.py:66; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.AdminListingSummary', await self._client._call('POST', endpoint_path('/api/admin/listings/{listing_id}/clear-description', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def remove_listing(self, listing_id: str, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> models.AdminListingSummary:
        """Remove Listing.

        HTTP: POST /api/admin/listings/{listing_id}/remove.

        Source: backend/app/routes/api/admin/listings/router.py:44; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.AdminListingSummary', await self._client._call('POST', endpoint_path('/api/admin/listings/{listing_id}/remove', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def restore_listing(self, listing_id: str, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> models.AdminListingSummary:
        """Restore Listing.

        HTTP: POST /api/admin/listings/{listing_id}/restore.

        Source: backend/app/routes/api/admin/listings/router.py:55; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.AdminListingSummary', await self._client._call('POST', endpoint_path('/api/admin/listings/{listing_id}/restore', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class AdminMetrics:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def metrics(self, *, options: RequestOptions | None = None) -> models.AdminMetricsResponse:
        """Metrics.

        HTTP: GET /api/admin/metrics.

        Source: backend/app/routes/api/admin/metrics/router.py:14; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.AdminMetricsResponse', self._client._call('GET', endpoint_path('/api/admin/metrics', {}), params={}, headers={}, options=options, response_kind='json'))

    def reset_cooldowns(self, *, options: RequestOptions | None = None) -> models.MetricCooldownResetResponse:
        """Reset Cooldowns.

        HTTP: POST /api/admin/metrics/reset-cooldowns.

        Source: backend/app/routes/api/admin/metrics/router.py:22; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.MetricCooldownResetResponse', self._client._call('POST', endpoint_path('/api/admin/metrics/reset-cooldowns', {}), params={}, headers={}, options=options, response_kind='json'))

class AsyncAdminMetrics:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def metrics(self, *, options: RequestOptions | None = None) -> models.AdminMetricsResponse:
        """Metrics.

        HTTP: GET /api/admin/metrics.

        Source: backend/app/routes/api/admin/metrics/router.py:14; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.AdminMetricsResponse', await self._client._call('GET', endpoint_path('/api/admin/metrics', {}), params={}, headers={}, options=options, response_kind='json'))

    async def reset_cooldowns(self, *, options: RequestOptions | None = None) -> models.MetricCooldownResetResponse:
        """Reset Cooldowns.

        HTTP: POST /api/admin/metrics/reset-cooldowns.

        Source: backend/app/routes/api/admin/metrics/router.py:22; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.MetricCooldownResetResponse', await self._client._call('POST', endpoint_path('/api/admin/metrics/reset-cooldowns', {}), params={}, headers={}, options=options, response_kind='json'))

class AdminRatings:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def remove_rating(self, rating_id: int, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> None:
        """Remove Rating.

        HTTP: DELETE /api/admin/ratings/{rating_id}.

        Source: backend/app/routes/api/admin/ratings/router.py:16; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        rating_id: {"title": "Rating Id", "type": "integer"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/admin/ratings/{rating_id}', {'rating_id': rating_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class AsyncAdminRatings:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def remove_rating(self, rating_id: int, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> None:
        """Remove Rating.

        HTTP: DELETE /api/admin/ratings/{rating_id}.

        Source: backend/app/routes/api/admin/ratings/router.py:16; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        rating_id: {"title": "Rating Id", "type": "integer"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/admin/ratings/{rating_id}', {'rating_id': rating_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class AdminUsers:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def users(self, *, q: str | None | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, options: RequestOptions | None = None) -> models.AdminUserPage:
        """Users.

        HTTP: GET /api/admin/users.

        Source: backend/app/routes/api/admin/users/router.py:28; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        q: {"anyOf": [{"maxLength": 320, "type": "string"}, {"type": "null"}], "title": "Q"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 25, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}
        """
        return cast('models.AdminUserPage', self._client._call('GET', endpoint_path('/api/admin/users', {}), params={'q': q, 'page': page, 'page_size': page_size}, headers={}, options=options, response_kind='json'))

    def user_detail(self, user_id: int, *, options: RequestOptions | None = None) -> models.AdminUserDetail:
        """User Detail.

        HTTP: GET /api/admin/users/{user_id}.

        Source: backend/app/routes/api/admin/users/router.py:47; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('models.AdminUserDetail', self._client._call('GET', endpoint_path('/api/admin/users/{user_id}', {'user_id': user_id}), params={}, headers={}, options=options, response_kind='json'))

    def ban(self, user_id: int, *, body: models.UserBanRequest, options: RequestOptions | None = None) -> models.AdminUserDetail:
        """Ban.

        HTTP: POST /api/admin/users/{user_id}/ban.

        Source: backend/app/routes/api/admin/users/router.py:59; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('models.AdminUserDetail', self._client._call('POST', endpoint_path('/api/admin/users/{user_id}/ban', {'user_id': user_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def update_role(self, user_id: int, *, body: models.UserRoleUpdateRequest, options: RequestOptions | None = None) -> models.AdminUserDetail:
        """Update Role.

        HTTP: PUT /api/admin/users/{user_id}/role.

        Source: backend/app/routes/api/admin/users/router.py:92; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('models.AdminUserDetail', self._client._call('PUT', endpoint_path('/api/admin/users/{user_id}/role', {'user_id': user_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def unban(self, user_id: int, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> models.AdminUserDetail:
        """Unban.

        HTTP: POST /api/admin/users/{user_id}/unban.

        Source: backend/app/routes/api/admin/users/router.py:77; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('models.AdminUserDetail', self._client._call('POST', endpoint_path('/api/admin/users/{user_id}/unban', {'user_id': user_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class AsyncAdminUsers:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def users(self, *, q: str | None | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, options: RequestOptions | None = None) -> models.AdminUserPage:
        """Users.

        HTTP: GET /api/admin/users.

        Source: backend/app/routes/api/admin/users/router.py:28; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        q: {"anyOf": [{"maxLength": 320, "type": "string"}, {"type": "null"}], "title": "Q"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 25, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}
        """
        return cast('models.AdminUserPage', await self._client._call('GET', endpoint_path('/api/admin/users', {}), params={'q': q, 'page': page, 'page_size': page_size}, headers={}, options=options, response_kind='json'))

    async def user_detail(self, user_id: int, *, options: RequestOptions | None = None) -> models.AdminUserDetail:
        """User Detail.

        HTTP: GET /api/admin/users/{user_id}.

        Source: backend/app/routes/api/admin/users/router.py:47; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('models.AdminUserDetail', await self._client._call('GET', endpoint_path('/api/admin/users/{user_id}', {'user_id': user_id}), params={}, headers={}, options=options, response_kind='json'))

    async def ban(self, user_id: int, *, body: models.UserBanRequest, options: RequestOptions | None = None) -> models.AdminUserDetail:
        """Ban.

        HTTP: POST /api/admin/users/{user_id}/ban.

        Source: backend/app/routes/api/admin/users/router.py:59; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('models.AdminUserDetail', await self._client._call('POST', endpoint_path('/api/admin/users/{user_id}/ban', {'user_id': user_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def update_role(self, user_id: int, *, body: models.UserRoleUpdateRequest, options: RequestOptions | None = None) -> models.AdminUserDetail:
        """Update Role.

        HTTP: PUT /api/admin/users/{user_id}/role.

        Source: backend/app/routes/api/admin/users/router.py:92; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('models.AdminUserDetail', await self._client._call('PUT', endpoint_path('/api/admin/users/{user_id}/role', {'user_id': user_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def unban(self, user_id: int, *, body: models.ModerationReasonRequest, options: RequestOptions | None = None) -> models.AdminUserDetail:
        """Unban.

        HTTP: POST /api/admin/users/{user_id}/unban.

        Source: backend/app/routes/api/admin/users/router.py:77; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('models.AdminUserDetail', await self._client._call('POST', endpoint_path('/api/admin/users/{user_id}/unban', {'user_id': user_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class Auth:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def forgot_password(self, *, body: models.ForgotPasswordRequest, options: RequestOptions | None = None) -> models.StatusResponse:
        """Forgot Password.

        HTTP: POST /api/auth/forgot-password.

        Source: backend/app/routes/api/auth/router.py:135; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', self._client._call('POST', endpoint_path('/api/auth/forgot-password', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def login(self, *, body: models.LoginRequest, options: RequestOptions | None = None) -> models.UserResponse:
        """Login.

        HTTP: POST /api/auth/login.

        Source: backend/app/routes/api/auth/router.py:68; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', self._client._call('POST', endpoint_path('/api/auth/login', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def logout(self, *, options: RequestOptions | None = None) -> models.StatusResponse:
        """Logout.

        HTTP: POST /api/auth/logout.

        Source: backend/app/routes/api/auth/router.py:164; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', self._client._call('POST', endpoint_path('/api/auth/logout', {}), params={}, headers={}, options=options, response_kind='json'))

    def register(self, *, body: models.RegisterRequest, options: RequestOptions | None = None) -> models.UserResponse:
        """Register.

        HTTP: POST /api/auth/register.

        Source: backend/app/routes/api/auth/router.py:40; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', self._client._call('POST', endpoint_path('/api/auth/register', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def resend_verification(self, *, body: models.ResendVerificationRequest, options: RequestOptions | None = None) -> models.StatusResponse:
        """Resend Verification.

        HTTP: POST /api/auth/resend-verification.

        Source: backend/app/routes/api/auth/router.py:121; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', self._client._call('POST', endpoint_path('/api/auth/resend-verification', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def reset_password(self, *, body: models.ResetPasswordRequest, options: RequestOptions | None = None) -> models.StatusResponse:
        """Reset Password.

        HTTP: POST /api/auth/reset-password.

        Source: backend/app/routes/api/auth/router.py:149; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', self._client._call('POST', endpoint_path('/api/auth/reset-password', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def verify_email(self, *, body: models.EmailTokenRequest, options: RequestOptions | None = None) -> models.UserResponse:
        """Verify Email.

        HTTP: POST /api/auth/verify-email.

        Source: backend/app/routes/api/auth/router.py:99; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', self._client._call('POST', endpoint_path('/api/auth/verify-email', {}), params={}, headers={}, options=options, response_kind='json', json=body))

class AsyncAuth:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def forgot_password(self, *, body: models.ForgotPasswordRequest, options: RequestOptions | None = None) -> models.StatusResponse:
        """Forgot Password.

        HTTP: POST /api/auth/forgot-password.

        Source: backend/app/routes/api/auth/router.py:135; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', await self._client._call('POST', endpoint_path('/api/auth/forgot-password', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def login(self, *, body: models.LoginRequest, options: RequestOptions | None = None) -> models.UserResponse:
        """Login.

        HTTP: POST /api/auth/login.

        Source: backend/app/routes/api/auth/router.py:68; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', await self._client._call('POST', endpoint_path('/api/auth/login', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def logout(self, *, options: RequestOptions | None = None) -> models.StatusResponse:
        """Logout.

        HTTP: POST /api/auth/logout.

        Source: backend/app/routes/api/auth/router.py:164; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', await self._client._call('POST', endpoint_path('/api/auth/logout', {}), params={}, headers={}, options=options, response_kind='json'))

    async def register(self, *, body: models.RegisterRequest, options: RequestOptions | None = None) -> models.UserResponse:
        """Register.

        HTTP: POST /api/auth/register.

        Source: backend/app/routes/api/auth/router.py:40; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', await self._client._call('POST', endpoint_path('/api/auth/register', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def resend_verification(self, *, body: models.ResendVerificationRequest, options: RequestOptions | None = None) -> models.StatusResponse:
        """Resend Verification.

        HTTP: POST /api/auth/resend-verification.

        Source: backend/app/routes/api/auth/router.py:121; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', await self._client._call('POST', endpoint_path('/api/auth/resend-verification', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def reset_password(self, *, body: models.ResetPasswordRequest, options: RequestOptions | None = None) -> models.StatusResponse:
        """Reset Password.

        HTTP: POST /api/auth/reset-password.

        Source: backend/app/routes/api/auth/router.py:149; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', await self._client._call('POST', endpoint_path('/api/auth/reset-password', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def verify_email(self, *, body: models.EmailTokenRequest, options: RequestOptions | None = None) -> models.UserResponse:
        """Verify Email.

        HTTP: POST /api/auth/verify-email.

        Source: backend/app/routes/api/auth/router.py:99; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', await self._client._call('POST', endpoint_path('/api/auth/verify-email', {}), params={}, headers={}, options=options, response_kind='json', json=body))

class Collaboration:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def list_collaborators(self, listing_id: str, *, options: RequestOptions | None = None) -> list[models.CollaboratorResponse]:
        """List Collaborators.

        HTTP: GET /api/listings/{listing_id}/collaborators.

        Source: backend/app/routes/api/listings/collaboration.py:21; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/accepted-editor session: pending and accepted membership details; unavailable to API keys.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('list[models.CollaboratorResponse]', self._client._call('GET', endpoint_path('/api/listings/{listing_id}/collaborators', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    def invite(self, listing_id: str, *, body: models.CollaboratorInviteRequest, options: RequestOptions | None = None) -> list[models.CollaboratorResponse]:
        """Invite.

        HTTP: POST /api/listings/{listing_id}/collaborators.

        Source: backend/app/routes/api/listings/collaboration.py:31; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Verified owner session: invite an author or uncredited Authorized user; pending invitations grant no access/credit.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('list[models.CollaboratorResponse]', self._client._call('POST', endpoint_path('/api/listings/{listing_id}/collaborators', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def remove(self, listing_id: str, user_id: int, *, options: RequestOptions | None = None) -> None:
        """Remove.

        HTTP: DELETE /api/listings/{listing_id}/collaborators/{user_id}.

        Source: backend/app/routes/api/listings/collaboration.py:44; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner session removes a collaborator; accepted authors may leave. Further writes and staged-upload operations lose access.

        listing_id: {"title": "Listing Id", "type": "string"}

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/collaborators/{user_id}', {'listing_id': listing_id, 'user_id': user_id}), params={}, headers={}, options=options, response_kind='json'))

    def pending_invitations(self, *, options: RequestOptions | None = None) -> list[models.CollaborationInvitationResponse]:
        """Pending Invitations.

        HTTP: GET /api/user/me/collaborations.

        Source: backend/app/routes/api/listings/collaboration.py:55; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Recipient session: pending invitation summaries without private draft contents; API keys are not accepted.
        """
        return cast('list[models.CollaborationInvitationResponse]', self._client._call('GET', endpoint_path('/api/user/me/collaborations', {}), params={}, headers={}, options=options, response_kind='json'))

    def decline(self, listing_id: str, *, options: RequestOptions | None = None) -> None:
        """Decline.

        HTTP: DELETE /api/user/me/collaborations/{listing_id}.

        Source: backend/app/routes/api/listings/collaboration.py:71; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Recipient session declines a pending invitation or leaves accepted collaboration; API keys cannot manage membership.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/user/me/collaborations/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    def accept(self, listing_id: str, *, options: RequestOptions | None = None) -> None:
        """Accept.

        HTTP: POST /api/user/me/collaborations/{listing_id}/accept.

        Source: backend/app/routes/api/listings/collaboration.py:61; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Verified recipient session: accept private/editing access and author credit only for author invitations; no Developer-role or key-scope grant.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('None', self._client._call('POST', endpoint_path('/api/user/me/collaborations/{listing_id}/accept', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

class AsyncCollaboration:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def list_collaborators(self, listing_id: str, *, options: RequestOptions | None = None) -> list[models.CollaboratorResponse]:
        """List Collaborators.

        HTTP: GET /api/listings/{listing_id}/collaborators.

        Source: backend/app/routes/api/listings/collaboration.py:21; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner/accepted-editor session: pending and accepted membership details; unavailable to API keys.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('list[models.CollaboratorResponse]', await self._client._call('GET', endpoint_path('/api/listings/{listing_id}/collaborators', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    async def invite(self, listing_id: str, *, body: models.CollaboratorInviteRequest, options: RequestOptions | None = None) -> list[models.CollaboratorResponse]:
        """Invite.

        HTTP: POST /api/listings/{listing_id}/collaborators.

        Source: backend/app/routes/api/listings/collaboration.py:31; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Verified owner session: invite an author or uncredited Authorized user; pending invitations grant no access/credit.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('list[models.CollaboratorResponse]', await self._client._call('POST', endpoint_path('/api/listings/{listing_id}/collaborators', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def remove(self, listing_id: str, user_id: int, *, options: RequestOptions | None = None) -> None:
        """Remove.

        HTTP: DELETE /api/listings/{listing_id}/collaborators/{user_id}.

        Source: backend/app/routes/api/listings/collaboration.py:44; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Owner session removes a collaborator; accepted authors may leave. Further writes and staged-upload operations lose access.

        listing_id: {"title": "Listing Id", "type": "string"}

        user_id: {"title": "User Id", "type": "integer"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/collaborators/{user_id}', {'listing_id': listing_id, 'user_id': user_id}), params={}, headers={}, options=options, response_kind='json'))

    async def pending_invitations(self, *, options: RequestOptions | None = None) -> list[models.CollaborationInvitationResponse]:
        """Pending Invitations.

        HTTP: GET /api/user/me/collaborations.

        Source: backend/app/routes/api/listings/collaboration.py:55; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Recipient session: pending invitation summaries without private draft contents; API keys are not accepted.
        """
        return cast('list[models.CollaborationInvitationResponse]', await self._client._call('GET', endpoint_path('/api/user/me/collaborations', {}), params={}, headers={}, options=options, response_kind='json'))

    async def decline(self, listing_id: str, *, options: RequestOptions | None = None) -> None:
        """Decline.

        HTTP: DELETE /api/user/me/collaborations/{listing_id}.

        Source: backend/app/routes/api/listings/collaboration.py:71; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Recipient session declines a pending invitation or leaves accepted collaboration; API keys cannot manage membership.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/user/me/collaborations/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    async def accept(self, listing_id: str, *, options: RequestOptions | None = None) -> None:
        """Accept.

        HTTP: POST /api/user/me/collaborations/{listing_id}/accept.

        Source: backend/app/routes/api/listings/collaboration.py:61; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Verified recipient session: accept private/editing access and author credit only for author invitations; no Developer-role or key-scope grant.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('None', await self._client._call('POST', endpoint_path('/api/user/me/collaborations/{listing_id}/accept', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

class Developer:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def developer_access(self, *, options: RequestOptions | None = None) -> models.DeveloperAccessResponse:
        """Developer Access.

        HTTP: GET /api/developer/access.

        Source: backend/app/routes/api/developer/router.py:36; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.DeveloperAccessResponse', self._client._call('GET', endpoint_path('/api/developer/access', {}), params={}, headers={}, options=options, response_kind='json'))

    def developer_guide(self, *, options: RequestOptions | None = None) -> str:
        """Developer Guide.

        HTTP: GET /api/developer/guide.

        Source: backend/app/routes/api/developer/router.py:23; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.
        """
        return cast('str', self._client._call('GET', endpoint_path('/api/developer/guide', {}), params={}, headers={}, options=options, response_kind='text'))

    def keys(self, *, options: RequestOptions | None = None) -> list[models.ApiKeyResponse]:
        """Keys.

        HTTP: GET /api/developer/keys.

        Source: backend/app/routes/api/developer/router.py:50; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('list[models.ApiKeyResponse]', self._client._call('GET', endpoint_path('/api/developer/keys', {}), params={}, headers={}, options=options, response_kind='json'))

    def new_key(self, *, body: models.ApiKeyCreateRequest, options: RequestOptions | None = None) -> models.ApiKeyCreatedResponse:
        """New Key.

        HTTP: POST /api/developer/keys.

        Source: backend/app/routes/api/developer/router.py:59; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.ApiKeyCreatedResponse', self._client._call('POST', endpoint_path('/api/developer/keys', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def revoke_key(self, key_id: str, *, options: RequestOptions | None = None) -> None:
        """Revoke Key.

        HTTP: DELETE /api/developer/keys/{key_id}.

        Source: backend/app/routes/api/developer/router.py:67; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        key_id: {"title": "Key Id", "type": "string"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/developer/keys/{key_id}', {'key_id': key_id}), params={}, headers={}, options=options, response_kind='json'))

    def scopes(self, *, options: RequestOptions | None = None) -> list[models.ApiScopeResponse]:
        """Scopes.

        HTTP: GET /api/developer/scopes.

        Source: backend/app/routes/api/developer/router.py:45; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('list[models.ApiScopeResponse]', self._client._call('GET', endpoint_path('/api/developer/scopes', {}), params={}, headers={}, options=options, response_kind='json'))

class AsyncDeveloper:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def developer_access(self, *, options: RequestOptions | None = None) -> models.DeveloperAccessResponse:
        """Developer Access.

        HTTP: GET /api/developer/access.

        Source: backend/app/routes/api/developer/router.py:36; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.DeveloperAccessResponse', await self._client._call('GET', endpoint_path('/api/developer/access', {}), params={}, headers={}, options=options, response_kind='json'))

    async def developer_guide(self, *, options: RequestOptions | None = None) -> str:
        """Developer Guide.

        HTTP: GET /api/developer/guide.

        Source: backend/app/routes/api/developer/router.py:23; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.
        """
        return cast('str', await self._client._call('GET', endpoint_path('/api/developer/guide', {}), params={}, headers={}, options=options, response_kind='text'))

    async def keys(self, *, options: RequestOptions | None = None) -> list[models.ApiKeyResponse]:
        """Keys.

        HTTP: GET /api/developer/keys.

        Source: backend/app/routes/api/developer/router.py:50; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('list[models.ApiKeyResponse]', await self._client._call('GET', endpoint_path('/api/developer/keys', {}), params={}, headers={}, options=options, response_kind='json'))

    async def new_key(self, *, body: models.ApiKeyCreateRequest, options: RequestOptions | None = None) -> models.ApiKeyCreatedResponse:
        """New Key.

        HTTP: POST /api/developer/keys.

        Source: backend/app/routes/api/developer/router.py:59; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.ApiKeyCreatedResponse', await self._client._call('POST', endpoint_path('/api/developer/keys', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def revoke_key(self, key_id: str, *, options: RequestOptions | None = None) -> None:
        """Revoke Key.

        HTTP: DELETE /api/developer/keys/{key_id}.

        Source: backend/app/routes/api/developer/router.py:67; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        key_id: {"title": "Key Id", "type": "string"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/developer/keys/{key_id}', {'key_id': key_id}), params={}, headers={}, options=options, response_kind='json'))

    async def scopes(self, *, options: RequestOptions | None = None) -> list[models.ApiScopeResponse]:
        """Scopes.

        HTTP: GET /api/developer/scopes.

        Source: backend/app/routes/api/developer/router.py:45; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('list[models.ApiScopeResponse]', await self._client._call('GET', endpoint_path('/api/developer/scopes', {}), params={}, headers={}, options=options, response_kind='json'))

class Documentation:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def swagger_ui(self, *, options: RequestOptions | None = None) -> str:
        """Swagger Ui.

        HTTP: GET /api/docs.

        Source: backend/app/routes/api/documentation/router.py:17; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('str', self._client._call('GET', endpoint_path('/api/docs', {}), params={}, headers={}, options=options, response_kind='text'))

    def openapi_schema(self, *, options: RequestOptions | None = None) -> dict[str, Any]:
        """Openapi Schema.

        HTTP: GET /api/openapi.json.

        Source: backend/app/routes/api/documentation/router.py:40; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.
        """
        return cast('dict[str, Any]', self._client._call('GET', endpoint_path('/api/openapi.json', {}), params={}, headers={}, options=options, response_kind='json'))

    def swagger_ui_alias(self, *, options: RequestOptions | None = None) -> str:
        """Swagger Ui.

        HTTP: GET /docs.

        Source: backend/app/routes/api/documentation/router.py:17; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('str', self._client._call('GET', endpoint_path('/docs', {}), params={}, headers={}, options=options, response_kind='text'))

class AsyncDocumentation:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def swagger_ui(self, *, options: RequestOptions | None = None) -> str:
        """Swagger Ui.

        HTTP: GET /api/docs.

        Source: backend/app/routes/api/documentation/router.py:17; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('str', await self._client._call('GET', endpoint_path('/api/docs', {}), params={}, headers={}, options=options, response_kind='text'))

    async def openapi_schema(self, *, options: RequestOptions | None = None) -> dict[str, Any]:
        """Openapi Schema.

        HTTP: GET /api/openapi.json.

        Source: backend/app/routes/api/documentation/router.py:40; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.
        """
        return cast('dict[str, Any]', await self._client._call('GET', endpoint_path('/api/openapi.json', {}), params={}, headers={}, options=options, response_kind='json'))

    async def swagger_ui_alias(self, *, options: RequestOptions | None = None) -> str:
        """Swagger Ui.

        HTTP: GET /docs.

        Source: backend/app/routes/api/documentation/router.py:17; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('str', await self._client._call('GET', endpoint_path('/docs', {}), params={}, headers={}, options=options, response_kind='text'))

class Downloads:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def download_listing_asset(self, asset_id: str, filename: str, *, options: RequestOptions | None = None) -> bytes:
        """Download Listing Asset.

        HTTP: GET /files/assets/{asset_id}/{filename}.

        Source: backend/app/routes/public/files/router.py:19; docs/partner-api.md; docs/openapi.json.

        API key scopes: assets:download.

        asset_id: {"title": "Asset Id", "type": "string"}

        filename: {"title": "Filename", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/files/assets/{asset_id}/{filename}', {'asset_id': asset_id, 'filename': filename}), params={}, headers={}, options=options, response_kind='bytes'))

    def download_file(self, file_id: str, filename: str, *, options: RequestOptions | None = None) -> bytes:
        """Download File.

        HTTP: GET /files/{file_id}/{filename}.

        Source: backend/app/routes/public/files/router.py:59; docs/partner-api.md; docs/openapi.json.

        API key scopes: assets:download.

        file_id: {"title": "File Id", "type": "string"}

        filename: {"title": "Filename", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/files/{file_id}/{filename}', {'file_id': file_id, 'filename': filename}), params={}, headers={}, options=options, response_kind='bytes'))

class AsyncDownloads:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def download_listing_asset(self, asset_id: str, filename: str, *, options: RequestOptions | None = None) -> bytes:
        """Download Listing Asset.

        HTTP: GET /files/assets/{asset_id}/{filename}.

        Source: backend/app/routes/public/files/router.py:19; docs/partner-api.md; docs/openapi.json.

        API key scopes: assets:download.

        asset_id: {"title": "Asset Id", "type": "string"}

        filename: {"title": "Filename", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/files/assets/{asset_id}/{filename}', {'asset_id': asset_id, 'filename': filename}), params={}, headers={}, options=options, response_kind='bytes'))

    async def download_file(self, file_id: str, filename: str, *, options: RequestOptions | None = None) -> bytes:
        """Download File.

        HTTP: GET /files/{file_id}/{filename}.

        Source: backend/app/routes/public/files/router.py:59; docs/partner-api.md; docs/openapi.json.

        API key scopes: assets:download.

        file_id: {"title": "File Id", "type": "string"}

        filename: {"title": "Filename", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/files/{file_id}/{filename}', {'file_id': file_id, 'filename': filename}), params={}, headers={}, options=options, response_kind='bytes'))

class Favourites:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def active_favourites(self, *, options: RequestOptions | None = None) -> list[models.FavouriteCollectionResponse]:
        """Active Favourites.

        HTTP: GET /api/favourites.

        Source: backend/app/routes/api/favourites/router.py:17; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        Read active ordered Reclaimer Favourites; /api/favourites requires catalog:read, /api/public/favourites is anonymous.

Returns an unpaginated array, excluding unavailable maps and empty collections.
Full listing descriptions remain in the API even though the homepage card omits them.
Reads do not create views/downloads; poll separately from listing-change events.
        """
        return cast('list[models.FavouriteCollectionResponse]', self._client._call('GET', endpoint_path('/api/favourites', {}), params={}, headers={}, options=options, response_kind='json'))

class AsyncFavourites:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def active_favourites(self, *, options: RequestOptions | None = None) -> list[models.FavouriteCollectionResponse]:
        """Active Favourites.

        HTTP: GET /api/favourites.

        Source: backend/app/routes/api/favourites/router.py:17; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        Read active ordered Reclaimer Favourites; /api/favourites requires catalog:read, /api/public/favourites is anonymous.

Returns an unpaginated array, excluding unavailable maps and empty collections.
Full listing descriptions remain in the API even though the homepage card omits them.
Reads do not create views/downloads; poll separately from listing-change events.
        """
        return cast('list[models.FavouriteCollectionResponse]', await self._client._call('GET', endpoint_path('/api/favourites', {}), params={}, headers={}, options=options, response_kind='json'))

class Files:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def current_listings(self, *, q: str | Unset = UNSET, file_type: str | Unset = UNSET, tags: list[str] | Unset = UNSET, options: RequestOptions | None = None) -> list[models.UploadedFileResponse]:
        """Current Listings.

        HTTP: GET /api/files.

        Source: backend/app/routes/api/files/router.py:99; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        q: {"default": "", "maxLength": 100, "title": "Q", "type": "string"}

        file_type: {"default": "", "title": "File Type", "type": "string"}

        tags: {"default": [], "items": {"type": "string"}, "title": "Tags", "type": "array"}
        """
        return cast('list[models.UploadedFileResponse]', self._client._call('GET', endpoint_path('/api/files', {}), params={'q': q, 'file_type': file_type, 'tags': tags}, headers={}, options=options, response_kind='json'))

    def my_files(self, *, options: RequestOptions | None = None) -> list[models.UploadedFileResponse]:
        """My Files.

        HTTP: GET /api/files/mine.

        Source: backend/app/routes/api/files/router.py:315; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.
        """
        return cast('list[models.UploadedFileResponse]', self._client._call('GET', endpoint_path('/api/files/mine', {}), params={}, headers={}, options=options, response_kind='json'))

    def start_upload(self, *, body: models.UploadCreateRequest, options: RequestOptions | None = None) -> models.UploadSessionResponse:
        """Start Upload.

        HTTP: POST /api/files/uploads.

        Source: backend/app/routes/api/files/router.py:141; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.
        """
        return cast('models.UploadSessionResponse', self._client._call('POST', endpoint_path('/api/files/uploads', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def upload_status(self, upload_id: str, *, options: RequestOptions | None = None) -> models.UploadSessionResponse:
        """Upload Status.

        HTTP: GET /api/files/uploads/{upload_id}.

        Source: backend/app/routes/api/files/router.py:172; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.

        upload_id: {"title": "Upload Id", "type": "string"}
        """
        return cast('models.UploadSessionResponse', self._client._call('GET', endpoint_path('/api/files/uploads/{upload_id}', {'upload_id': upload_id}), params={}, headers={}, options=options, response_kind='json'))

    def upload_chunk(self, upload_id: str, chunk_index: int, *, content: bytes, content_type: str = 'application/octet-stream', options: RequestOptions | None = None) -> models.UploadSessionResponse:
        """Upload Chunk.

        HTTP: PUT /api/files/uploads/{upload_id}/chunks/{chunk_index}.

        Source: backend/app/routes/api/files/router.py:186; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.

        upload_id: {"title": "Upload Id", "type": "string"}

        chunk_index: {"title": "Chunk Index", "type": "integer"}
        """
        return cast('models.UploadSessionResponse', self._client._call('PUT', endpoint_path('/api/files/uploads/{upload_id}/chunks/{chunk_index}', {'upload_id': upload_id, 'chunk_index': chunk_index}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

    def finish_upload(self, upload_id: str, *, options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """Finish Upload.

        HTTP: POST /api/files/uploads/{upload_id}/complete.

        Source: backend/app/routes/api/files/router.py:263; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload, listings:publish.

        upload_id: {"title": "Upload Id", "type": "string"}
        """
        return cast('models.UploadedFileResponse', self._client._call('POST', endpoint_path('/api/files/uploads/{upload_id}/complete', {'upload_id': upload_id}), params={}, headers={}, options=options, response_kind='json'))

    def delete_file(self, file_id: str, *, options: RequestOptions | None = None) -> None:
        """Delete File.

        HTTP: DELETE /api/files/{file_id}.

        Source: backend/app/routes/api/files/router.py:534; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:delete.

        file_id: {"title": "File Id", "type": "string"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/files/{file_id}', {'file_id': file_id}), params={}, headers={}, options=options, response_kind='json'))

    def file_metadata(self, file_id: str, *, options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """File Metadata.

        HTTP: GET /api/files/{file_id}.

        Source: backend/app/routes/api/files/router.py:547; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        file_id: {"title": "File Id", "type": "string"}
        """
        return cast('models.UploadedFileResponse', self._client._call('GET', endpoint_path('/api/files/{file_id}', {'file_id': file_id}), params={}, headers={}, options=options, response_kind='json'))

    def edit_file(self, file_id: str, *, body: models.LegacyFileUpdateRequest, options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """Edit File.

        HTTP: PATCH /api/files/{file_id}.

        Source: backend/app/routes/api/files/router.py:330; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        file_id: {"title": "File Id", "type": "string"}
        """
        return cast('models.UploadedFileResponse', self._client._call('PATCH', endpoint_path('/api/files/{file_id}', {'file_id': file_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def replace_file_content(self, file_id: str, *, original_filename: str, file_type: str, content: bytes, content_type: str = 'application/octet-stream', options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """Replace File Content.

        HTTP: PUT /api/files/{file_id}/content.

        Source: backend/app/routes/api/files/router.py:359; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload, listings:publish.

        file_id: {"title": "File Id", "type": "string"}

        original_filename: {"maxLength": 255, "minLength": 1, "title": "Original Filename", "type": "string"}

        file_type: {"title": "File Type", "type": "string"}
        """
        return cast('models.UploadedFileResponse', self._client._call('PUT', endpoint_path('/api/files/{file_id}/content', {'file_id': file_id}), params={'original_filename': original_filename, 'file_type': file_type}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

    def get_thumbnail(self, file_id: str, *, resolution: Literal['720p', '1080p', 'native'] | Unset = UNSET, options: RequestOptions | None = None) -> bytes:
        """Get Thumbnail.

        HTTP: GET /api/files/{file_id}/thumbnail.

        Source: backend/app/routes/api/files/router.py:443; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        file_id: {"title": "File Id", "type": "string"}

        resolution: {"default": "native", "enum": ["720p", "1080p", "native"], "title": "Resolution", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/api/files/{file_id}/thumbnail', {'file_id': file_id}), params={'resolution': resolution}, headers={}, options=options, response_kind='bytes'))

    def set_thumbnail(self, file_id: str, *, content_type: str, content: bytes, options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """Set Thumbnail.

        HTTP: PUT /api/files/{file_id}/thumbnail.

        Source: backend/app/routes/api/files/router.py:478; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        file_id: {"title": "File Id", "type": "string"}

        content-type: {"type": "string"}
        """
        return cast('models.UploadedFileResponse', self._client._call('PUT', endpoint_path('/api/files/{file_id}/thumbnail', {'file_id': file_id}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

class AsyncFiles:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def current_listings(self, *, q: str | Unset = UNSET, file_type: str | Unset = UNSET, tags: list[str] | Unset = UNSET, options: RequestOptions | None = None) -> list[models.UploadedFileResponse]:
        """Current Listings.

        HTTP: GET /api/files.

        Source: backend/app/routes/api/files/router.py:99; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        q: {"default": "", "maxLength": 100, "title": "Q", "type": "string"}

        file_type: {"default": "", "title": "File Type", "type": "string"}

        tags: {"default": [], "items": {"type": "string"}, "title": "Tags", "type": "array"}
        """
        return cast('list[models.UploadedFileResponse]', await self._client._call('GET', endpoint_path('/api/files', {}), params={'q': q, 'file_type': file_type, 'tags': tags}, headers={}, options=options, response_kind='json'))

    async def my_files(self, *, options: RequestOptions | None = None) -> list[models.UploadedFileResponse]:
        """My Files.

        HTTP: GET /api/files/mine.

        Source: backend/app/routes/api/files/router.py:315; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.
        """
        return cast('list[models.UploadedFileResponse]', await self._client._call('GET', endpoint_path('/api/files/mine', {}), params={}, headers={}, options=options, response_kind='json'))

    async def start_upload(self, *, body: models.UploadCreateRequest, options: RequestOptions | None = None) -> models.UploadSessionResponse:
        """Start Upload.

        HTTP: POST /api/files/uploads.

        Source: backend/app/routes/api/files/router.py:141; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.
        """
        return cast('models.UploadSessionResponse', await self._client._call('POST', endpoint_path('/api/files/uploads', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def upload_status(self, upload_id: str, *, options: RequestOptions | None = None) -> models.UploadSessionResponse:
        """Upload Status.

        HTTP: GET /api/files/uploads/{upload_id}.

        Source: backend/app/routes/api/files/router.py:172; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.

        upload_id: {"title": "Upload Id", "type": "string"}
        """
        return cast('models.UploadSessionResponse', await self._client._call('GET', endpoint_path('/api/files/uploads/{upload_id}', {'upload_id': upload_id}), params={}, headers={}, options=options, response_kind='json'))

    async def upload_chunk(self, upload_id: str, chunk_index: int, *, content: bytes, content_type: str = 'application/octet-stream', options: RequestOptions | None = None) -> models.UploadSessionResponse:
        """Upload Chunk.

        HTTP: PUT /api/files/uploads/{upload_id}/chunks/{chunk_index}.

        Source: backend/app/routes/api/files/router.py:186; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.

        upload_id: {"title": "Upload Id", "type": "string"}

        chunk_index: {"title": "Chunk Index", "type": "integer"}
        """
        return cast('models.UploadSessionResponse', await self._client._call('PUT', endpoint_path('/api/files/uploads/{upload_id}/chunks/{chunk_index}', {'upload_id': upload_id, 'chunk_index': chunk_index}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

    async def finish_upload(self, upload_id: str, *, options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """Finish Upload.

        HTTP: POST /api/files/uploads/{upload_id}/complete.

        Source: backend/app/routes/api/files/router.py:263; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload, listings:publish.

        upload_id: {"title": "Upload Id", "type": "string"}
        """
        return cast('models.UploadedFileResponse', await self._client._call('POST', endpoint_path('/api/files/uploads/{upload_id}/complete', {'upload_id': upload_id}), params={}, headers={}, options=options, response_kind='json'))

    async def delete_file(self, file_id: str, *, options: RequestOptions | None = None) -> None:
        """Delete File.

        HTTP: DELETE /api/files/{file_id}.

        Source: backend/app/routes/api/files/router.py:534; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:delete.

        file_id: {"title": "File Id", "type": "string"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/files/{file_id}', {'file_id': file_id}), params={}, headers={}, options=options, response_kind='json'))

    async def file_metadata(self, file_id: str, *, options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """File Metadata.

        HTTP: GET /api/files/{file_id}.

        Source: backend/app/routes/api/files/router.py:547; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        file_id: {"title": "File Id", "type": "string"}
        """
        return cast('models.UploadedFileResponse', await self._client._call('GET', endpoint_path('/api/files/{file_id}', {'file_id': file_id}), params={}, headers={}, options=options, response_kind='json'))

    async def edit_file(self, file_id: str, *, body: models.LegacyFileUpdateRequest, options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """Edit File.

        HTTP: PATCH /api/files/{file_id}.

        Source: backend/app/routes/api/files/router.py:330; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        file_id: {"title": "File Id", "type": "string"}
        """
        return cast('models.UploadedFileResponse', await self._client._call('PATCH', endpoint_path('/api/files/{file_id}', {'file_id': file_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def replace_file_content(self, file_id: str, *, original_filename: str, file_type: str, content: bytes, content_type: str = 'application/octet-stream', options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """Replace File Content.

        HTTP: PUT /api/files/{file_id}/content.

        Source: backend/app/routes/api/files/router.py:359; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload, listings:publish.

        file_id: {"title": "File Id", "type": "string"}

        original_filename: {"maxLength": 255, "minLength": 1, "title": "Original Filename", "type": "string"}

        file_type: {"title": "File Type", "type": "string"}
        """
        return cast('models.UploadedFileResponse', await self._client._call('PUT', endpoint_path('/api/files/{file_id}/content', {'file_id': file_id}), params={'original_filename': original_filename, 'file_type': file_type}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

    async def get_thumbnail(self, file_id: str, *, resolution: Literal['720p', '1080p', 'native'] | Unset = UNSET, options: RequestOptions | None = None) -> bytes:
        """Get Thumbnail.

        HTTP: GET /api/files/{file_id}/thumbnail.

        Source: backend/app/routes/api/files/router.py:443; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        file_id: {"title": "File Id", "type": "string"}

        resolution: {"default": "native", "enum": ["720p", "1080p", "native"], "title": "Resolution", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/api/files/{file_id}/thumbnail', {'file_id': file_id}), params={'resolution': resolution}, headers={}, options=options, response_kind='bytes'))

    async def set_thumbnail(self, file_id: str, *, content_type: str, content: bytes, options: RequestOptions | None = None) -> models.UploadedFileResponse:
        """Set Thumbnail.

        HTTP: PUT /api/files/{file_id}/thumbnail.

        Source: backend/app/routes/api/files/router.py:478; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        file_id: {"title": "File Id", "type": "string"}

        content-type: {"type": "string"}
        """
        return cast('models.UploadedFileResponse', await self._client._call('PUT', endpoint_path('/api/files/{file_id}/thumbnail', {'file_id': file_id}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

class Health:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def health(self, *, options: RequestOptions | None = None) -> models.StatusResponse:
        """Health.

        HTTP: GET /api/health.

        Source: backend/app/routes/api/health/router.py:13; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', self._client._call('GET', endpoint_path('/api/health', {}), params={}, headers={}, options=options, response_kind='json'))

    def readiness(self, *, options: RequestOptions | None = None) -> models.StatusResponse:
        """Readiness.

        HTTP: GET /api/ready.

        Source: backend/app/routes/api/health/router.py:18; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', self._client._call('GET', endpoint_path('/api/ready', {}), params={}, headers={}, options=options, response_kind='json'))

class AsyncHealth:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def health(self, *, options: RequestOptions | None = None) -> models.StatusResponse:
        """Health.

        HTTP: GET /api/health.

        Source: backend/app/routes/api/health/router.py:13; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', await self._client._call('GET', endpoint_path('/api/health', {}), params={}, headers={}, options=options, response_kind='json'))

    async def readiness(self, *, options: RequestOptions | None = None) -> models.StatusResponse:
        """Readiness.

        HTTP: GET /api/ready.

        Source: backend/app/routes/api/health/router.py:18; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', await self._client._call('GET', endpoint_path('/api/ready', {}), params={}, headers={}, options=options, response_kind='json'))

class Listings:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def public_listings(self, *, q: str | Unset = UNSET, file_type: str | Unset = UNSET, tags: list[str] | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, updated_since: str | None | Unset = UNSET, sort: Literal['updated', 'latest', 'downloads', 'rated', 'unrated', 'overlooked', 'trending', 'rising', 'relevance', 'most_downloads', 'least_downloads', 'most_liked', 'least_liked', 'newest', 'oldest'] | Unset = UNSET, window: Literal['24h', '7d', '30d'] | Unset = UNSET, include_private: bool | Unset = UNSET, options: RequestOptions | None = None) -> models.ListingPageResponse:
        """Public Listings.

        HTTP: GET /api/listings.

        Source: backend/app/routes/api/listings/router.py:150; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        q: {"default": "", "maxLength": 100, "title": "Q", "type": "string"}

        file_type: {"default": "", "title": "File Type", "type": "string"}

        tags: {"default": [], "items": {"type": "string"}, "title": "Tags", "type": "array"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 20, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}

        updated_since: {"anyOf": [{"format": "date-time", "type": "string"}, {"type": "null"}], "title": "Updated Since"}

        sort: {"default": "updated", "enum": ["updated", "latest", "downloads", "rated", "unrated", "overlooked", "trending", "rising", "relevance", "most_downloads", "least_downloads", "most_liked", "least_liked", "newest", "oldest"], "title": "Sort", "type": "string"}

        window: {"default": "7d", "enum": ["24h", "7d", "30d"], "title": "Window", "type": "string"}

        include_private: {"default": false, "title": "Include Private", "type": "boolean"}
        """
        return cast('models.ListingPageResponse', self._client._call('GET', endpoint_path('/api/listings', {}), params={'q': q, 'file_type': file_type, 'tags': tags, 'page': page, 'page_size': page_size, 'updated_since': updated_since, 'sort': sort, 'window': window, 'include_private': include_private}, headers={}, options=options, response_kind='json'))

    def new_listing(self, *, body: models.ListingCreateRequest, options: RequestOptions | None = None) -> models.ListingResponse:
        """New Listing.

        HTTP: POST /api/listings.

        Source: backend/app/routes/api/listings/router.py:288; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.
        """
        return cast('models.ListingResponse', self._client._call('POST', endpoint_path('/api/listings', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def track_asset_download(self, asset_id: str, *, options: RequestOptions | None = None) -> bytes:
        """Track Asset Download.

        HTTP: GET /api/listings/assets/{asset_id}/download.

        Source: backend/app/routes/api/listings/router.py:219; docs/partner-api.md; docs/openapi.json.

        API key scopes: assets:download.

        asset_id: {"title": "Asset Id", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/api/listings/assets/{asset_id}/download', {'asset_id': asset_id}), params={}, headers={}, options=options, response_kind='redirect'))

    def catalog_changes(self, *, updated_since: str, updated_before: str | None | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, include_private: bool | Unset = UNSET, options: RequestOptions | None = None) -> models.ListingChangePageResponse:
        """Catalog Changes.

        HTTP: GET /api/listings/changes.

        Source: backend/app/routes/api/listings/router.py:199; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        updated_since: {"format": "date-time", "title": "Updated Since", "type": "string"}

        updated_before: {"anyOf": [{"format": "date-time", "type": "string"}, {"type": "null"}], "title": "Updated Before"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 100, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}

        include_private: {"default": false, "title": "Include Private", "type": "boolean"}
        """
        return cast('models.ListingChangePageResponse', self._client._call('GET', endpoint_path('/api/listings/changes', {}), params={'updated_since': updated_since, 'updated_before': updated_before, 'page': page, 'page_size': page_size, 'include_private': include_private}, headers={}, options=options, response_kind='json'))

    def my_listings(self, *, options: RequestOptions | None = None) -> list[models.ListingResponse]:
        """My Listings.

        HTTP: GET /api/listings/mine.

        Source: backend/app/routes/api/listings/router.py:407; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.
        """
        return cast('list[models.ListingResponse]', self._client._call('GET', endpoint_path('/api/listings/mine', {}), params={}, headers={}, options=options, response_kind='json'))

    def my_listing_detail(self, listing_id: str, *, options: RequestOptions | None = None) -> models.ListingResponse:
        """My Listing Detail.

        HTTP: GET /api/listings/mine/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:426; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', self._client._call('GET', endpoint_path('/api/listings/mine/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    def finish_asset_upload(self, upload_id: str, *, options: RequestOptions | None = None) -> models.ListingAssetResponse:
        """Finish Asset Upload.

        HTTP: POST /api/listings/uploads/{upload_id}/complete.

        Source: backend/app/routes/api/listings/router.py:626; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.

        upload_id: {"title": "Upload Id", "type": "string"}
        """
        return cast('models.ListingAssetResponse', self._client._call('POST', endpoint_path('/api/listings/uploads/{upload_id}/complete', {'upload_id': upload_id}), params={}, headers={}, options=options, response_kind='json'))

    def download_version_archive(self, version_id: str, *, options: RequestOptions | None = None) -> bytes:
        """Download Version Archive.

        HTTP: GET /api/listings/versions/{version_id}/download.

        Source: backend/app/routes/api/listings/router.py:248; docs/partner-api.md; docs/openapi.json.

        API key scopes: assets:download.

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/api/listings/versions/{version_id}/download', {'version_id': version_id}), params={}, headers={}, options=options, response_kind='bytes'))

    def remove_listing(self, listing_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Listing.

        HTTP: DELETE /api/listings/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:537; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:delete.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    def listing_detail(self, listing_id: str, *, options: RequestOptions | None = None) -> models.ListingResponse:
        """Listing Detail.

        HTTP: GET /api/listings/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:440; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', self._client._call('GET', endpoint_path('/api/listings/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    def edit_listing(self, listing_id: str, *, body: models.ListingUpdateRequest, options: RequestOptions | None = None) -> models.ListingResponse:
        """Edit Listing.

        HTTP: PATCH /api/listings/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:508; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', self._client._call('PATCH', endpoint_path('/api/listings/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def upload_gallery_image(self, listing_id: str, *, content_type: str, x_filename: str | Unset = UNSET, content: bytes, options: RequestOptions | None = None) -> models.ListingResponse:
        """Upload Gallery Image.

        HTTP: POST /api/listings/{listing_id}/images.

        Source: backend/app/routes/api/listings/router.py:300; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        content-type: {"type": "string"}

        x-filename: {"type": "string"}
        """
        return cast('models.ListingResponse', self._client._call('POST', endpoint_path('/api/listings/{listing_id}/images', {'listing_id': listing_id}), params={}, headers={'content-type': content_type, 'x-filename': x_filename}, options=options, response_kind='json', content=content))

    def remove_gallery_image(self, listing_id: str, image_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Gallery Image.

        HTTP: DELETE /api/listings/{listing_id}/images/{image_id}.

        Source: backend/app/routes/api/listings/router.py:388; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        image_id: {"title": "Image Id", "type": "string"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/images/{image_id}', {'listing_id': listing_id, 'image_id': image_id}), params={}, headers={}, options=options, response_kind='json'))

    def get_gallery_image(self, listing_id: str, image_id: str, *, resolution: Literal['720p', '1080p', 'native'] | Unset = UNSET, options: RequestOptions | None = None) -> bytes:
        """Get Gallery Image.

        HTTP: GET /api/listings/{listing_id}/images/{image_id}.

        Source: backend/app/routes/api/listings/router.py:354; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        listing_id: {"title": "Listing Id", "type": "string"}

        image_id: {"title": "Image Id", "type": "string"}

        resolution: {"default": "native", "enum": ["720p", "1080p", "native"], "title": "Resolution", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/api/listings/{listing_id}/images/{image_id}', {'listing_id': listing_id, 'image_id': image_id}), params={'resolution': resolution}, headers={}, options=options, response_kind='bytes'))

    def get_listing_thumbnail(self, listing_id: str, *, resolution: Literal['720p', '1080p', 'native'] | Unset = UNSET, options: RequestOptions | None = None) -> bytes:
        """Get Listing Thumbnail.

        HTTP: GET /api/listings/{listing_id}/thumbnail.

        Source: backend/app/routes/api/listings/router.py:789; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        listing_id: {"title": "Listing Id", "type": "string"}

        resolution: {"default": "native", "enum": ["720p", "1080p", "native"], "title": "Resolution", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/api/listings/{listing_id}/thumbnail', {'listing_id': listing_id}), params={'resolution': resolution}, headers={}, options=options, response_kind='bytes'))

    def set_listing_thumbnail(self, listing_id: str, *, content_type: str, content: bytes, options: RequestOptions | None = None) -> models.ListingResponse:
        """Set Listing Thumbnail.

        HTTP: PUT /api/listings/{listing_id}/thumbnail.

        Source: backend/app/routes/api/listings/router.py:838; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        content-type: {"type": "string"}
        """
        return cast('models.ListingResponse', self._client._call('PUT', endpoint_path('/api/listings/{listing_id}/thumbnail', {'listing_id': listing_id}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

    def new_version(self, listing_id: str, *, body: models.ListingVersionCreateRequest, options: RequestOptions | None = None) -> models.ListingResponse:
        """New Version.

        HTTP: POST /api/listings/{listing_id}/versions.

        Source: backend/app/routes/api/listings/router.py:552; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', self._client._call('POST', endpoint_path('/api/listings/{listing_id}/versions', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def remove_version(self, listing_id: str, version_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Version.

        HTTP: DELETE /api/listings/{listing_id}/versions/{version_id}.

        Source: backend/app/routes/api/listings/router.py:731; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:delete.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/versions/{version_id}', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json'))

    def edit_version_metadata(self, listing_id: str, version_id: str, *, body: models.ListingVersionUpdateRequest, options: RequestOptions | None = None) -> models.ListingResponse:
        """Edit Version Metadata.

        HTTP: PATCH /api/listings/{listing_id}/versions/{version_id}.

        Source: backend/app/routes/api/listings/router.py:714; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.ListingResponse', self._client._call('PATCH', endpoint_path('/api/listings/{listing_id}/versions/{version_id}', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def remove_draft_asset(self, listing_id: str, version_id: str, asset_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Draft Asset.

        HTTP: DELETE /api/listings/{listing_id}/versions/{version_id}/assets/{asset_id}.

        Source: backend/app/routes/api/listings/router.py:758; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:delete.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}

        asset_id: {"title": "Asset Id", "type": "string"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/assets/{asset_id}', {'listing_id': listing_id, 'version_id': version_id, 'asset_id': asset_id}), params={}, headers={}, options=options, response_kind='json'))

    def edit_version_compatibility(self, listing_id: str, version_id: str, *, body: models.ReleaseCompatibility, options: RequestOptions | None = None) -> models.ListingVersionResponse:
        """Edit Version Compatibility.

        HTTP: PUT /api/listings/{listing_id}/versions/{version_id}/compatibility.

        Source: backend/app/routes/api/listings/router.py:482; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.ListingVersionResponse', self._client._call('PUT', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/compatibility', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def release_manifest(self, listing_id: str, version_id: str, *, options: RequestOptions | None = None) -> models.ReleaseManifestResponse:
        """Release Manifest.

        HTTP: GET /api/listings/{listing_id}/versions/{version_id}/manifest.

        Source: backend/app/routes/api/listings/router.py:457; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.ReleaseManifestResponse', self._client._call('GET', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/manifest', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json'))

    def publish_listing_version(self, listing_id: str, version_id: str, *, options: RequestOptions | None = None) -> models.ListingResponse:
        """Publish Listing Version.

        HTTP: POST /api/listings/{listing_id}/versions/{version_id}/publish.

        Source: backend/app/routes/api/listings/router.py:686; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:publish.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.ListingResponse', self._client._call('POST', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/publish', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json'))

    def new_asset_upload(self, listing_id: str, version_id: str, *, body: models.ListingAssetUploadCreateRequest, options: RequestOptions | None = None) -> models.UploadSessionResponse:
        """New Asset Upload.

        HTTP: POST /api/listings/{listing_id}/versions/{version_id}/uploads.

        Source: backend/app/routes/api/listings/router.py:578; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.UploadSessionResponse', self._client._call('POST', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/uploads', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    def listing_workshop(self, listing_id: str, *, options: RequestOptions | None = None) -> models.WorkshopModsResponse:
        """Listing Workshop.

        HTTP: GET /api/listings/{listing_id}/workshop.

        Source: backend/app/routes/api/listings/router.py:175; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        Read all current required Workshop mods; legacy fields describe the first mod.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.WorkshopModsResponse', self._client._call('GET', endpoint_path('/api/listings/{listing_id}/workshop', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

class AsyncListings:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def public_listings(self, *, q: str | Unset = UNSET, file_type: str | Unset = UNSET, tags: list[str] | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, updated_since: str | None | Unset = UNSET, sort: Literal['updated', 'latest', 'downloads', 'rated', 'unrated', 'overlooked', 'trending', 'rising', 'relevance', 'most_downloads', 'least_downloads', 'most_liked', 'least_liked', 'newest', 'oldest'] | Unset = UNSET, window: Literal['24h', '7d', '30d'] | Unset = UNSET, include_private: bool | Unset = UNSET, options: RequestOptions | None = None) -> models.ListingPageResponse:
        """Public Listings.

        HTTP: GET /api/listings.

        Source: backend/app/routes/api/listings/router.py:150; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        q: {"default": "", "maxLength": 100, "title": "Q", "type": "string"}

        file_type: {"default": "", "title": "File Type", "type": "string"}

        tags: {"default": [], "items": {"type": "string"}, "title": "Tags", "type": "array"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 20, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}

        updated_since: {"anyOf": [{"format": "date-time", "type": "string"}, {"type": "null"}], "title": "Updated Since"}

        sort: {"default": "updated", "enum": ["updated", "latest", "downloads", "rated", "unrated", "overlooked", "trending", "rising", "relevance", "most_downloads", "least_downloads", "most_liked", "least_liked", "newest", "oldest"], "title": "Sort", "type": "string"}

        window: {"default": "7d", "enum": ["24h", "7d", "30d"], "title": "Window", "type": "string"}

        include_private: {"default": false, "title": "Include Private", "type": "boolean"}
        """
        return cast('models.ListingPageResponse', await self._client._call('GET', endpoint_path('/api/listings', {}), params={'q': q, 'file_type': file_type, 'tags': tags, 'page': page, 'page_size': page_size, 'updated_since': updated_since, 'sort': sort, 'window': window, 'include_private': include_private}, headers={}, options=options, response_kind='json'))

    async def new_listing(self, *, body: models.ListingCreateRequest, options: RequestOptions | None = None) -> models.ListingResponse:
        """New Listing.

        HTTP: POST /api/listings.

        Source: backend/app/routes/api/listings/router.py:288; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.
        """
        return cast('models.ListingResponse', await self._client._call('POST', endpoint_path('/api/listings', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def track_asset_download(self, asset_id: str, *, options: RequestOptions | None = None) -> bytes:
        """Track Asset Download.

        HTTP: GET /api/listings/assets/{asset_id}/download.

        Source: backend/app/routes/api/listings/router.py:219; docs/partner-api.md; docs/openapi.json.

        API key scopes: assets:download.

        asset_id: {"title": "Asset Id", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/api/listings/assets/{asset_id}/download', {'asset_id': asset_id}), params={}, headers={}, options=options, response_kind='redirect'))

    async def catalog_changes(self, *, updated_since: str, updated_before: str | None | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, include_private: bool | Unset = UNSET, options: RequestOptions | None = None) -> models.ListingChangePageResponse:
        """Catalog Changes.

        HTTP: GET /api/listings/changes.

        Source: backend/app/routes/api/listings/router.py:199; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        updated_since: {"format": "date-time", "title": "Updated Since", "type": "string"}

        updated_before: {"anyOf": [{"format": "date-time", "type": "string"}, {"type": "null"}], "title": "Updated Before"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 100, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}

        include_private: {"default": false, "title": "Include Private", "type": "boolean"}
        """
        return cast('models.ListingChangePageResponse', await self._client._call('GET', endpoint_path('/api/listings/changes', {}), params={'updated_since': updated_since, 'updated_before': updated_before, 'page': page, 'page_size': page_size, 'include_private': include_private}, headers={}, options=options, response_kind='json'))

    async def my_listings(self, *, options: RequestOptions | None = None) -> list[models.ListingResponse]:
        """My Listings.

        HTTP: GET /api/listings/mine.

        Source: backend/app/routes/api/listings/router.py:407; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.
        """
        return cast('list[models.ListingResponse]', await self._client._call('GET', endpoint_path('/api/listings/mine', {}), params={}, headers={}, options=options, response_kind='json'))

    async def my_listing_detail(self, listing_id: str, *, options: RequestOptions | None = None) -> models.ListingResponse:
        """My Listing Detail.

        HTTP: GET /api/listings/mine/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:426; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', await self._client._call('GET', endpoint_path('/api/listings/mine/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    async def finish_asset_upload(self, upload_id: str, *, options: RequestOptions | None = None) -> models.ListingAssetResponse:
        """Finish Asset Upload.

        HTTP: POST /api/listings/uploads/{upload_id}/complete.

        Source: backend/app/routes/api/listings/router.py:626; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.

        upload_id: {"title": "Upload Id", "type": "string"}
        """
        return cast('models.ListingAssetResponse', await self._client._call('POST', endpoint_path('/api/listings/uploads/{upload_id}/complete', {'upload_id': upload_id}), params={}, headers={}, options=options, response_kind='json'))

    async def download_version_archive(self, version_id: str, *, options: RequestOptions | None = None) -> bytes:
        """Download Version Archive.

        HTTP: GET /api/listings/versions/{version_id}/download.

        Source: backend/app/routes/api/listings/router.py:248; docs/partner-api.md; docs/openapi.json.

        API key scopes: assets:download.

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/api/listings/versions/{version_id}/download', {'version_id': version_id}), params={}, headers={}, options=options, response_kind='bytes'))

    async def remove_listing(self, listing_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Listing.

        HTTP: DELETE /api/listings/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:537; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:delete.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    async def listing_detail(self, listing_id: str, *, options: RequestOptions | None = None) -> models.ListingResponse:
        """Listing Detail.

        HTTP: GET /api/listings/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:440; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', await self._client._call('GET', endpoint_path('/api/listings/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    async def edit_listing(self, listing_id: str, *, body: models.ListingUpdateRequest, options: RequestOptions | None = None) -> models.ListingResponse:
        """Edit Listing.

        HTTP: PATCH /api/listings/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:508; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', await self._client._call('PATCH', endpoint_path('/api/listings/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def upload_gallery_image(self, listing_id: str, *, content_type: str, x_filename: str | Unset = UNSET, content: bytes, options: RequestOptions | None = None) -> models.ListingResponse:
        """Upload Gallery Image.

        HTTP: POST /api/listings/{listing_id}/images.

        Source: backend/app/routes/api/listings/router.py:300; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        content-type: {"type": "string"}

        x-filename: {"type": "string"}
        """
        return cast('models.ListingResponse', await self._client._call('POST', endpoint_path('/api/listings/{listing_id}/images', {'listing_id': listing_id}), params={}, headers={'content-type': content_type, 'x-filename': x_filename}, options=options, response_kind='json', content=content))

    async def remove_gallery_image(self, listing_id: str, image_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Gallery Image.

        HTTP: DELETE /api/listings/{listing_id}/images/{image_id}.

        Source: backend/app/routes/api/listings/router.py:388; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        image_id: {"title": "Image Id", "type": "string"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/images/{image_id}', {'listing_id': listing_id, 'image_id': image_id}), params={}, headers={}, options=options, response_kind='json'))

    async def get_gallery_image(self, listing_id: str, image_id: str, *, resolution: Literal['720p', '1080p', 'native'] | Unset = UNSET, options: RequestOptions | None = None) -> bytes:
        """Get Gallery Image.

        HTTP: GET /api/listings/{listing_id}/images/{image_id}.

        Source: backend/app/routes/api/listings/router.py:354; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        listing_id: {"title": "Listing Id", "type": "string"}

        image_id: {"title": "Image Id", "type": "string"}

        resolution: {"default": "native", "enum": ["720p", "1080p", "native"], "title": "Resolution", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/api/listings/{listing_id}/images/{image_id}', {'listing_id': listing_id, 'image_id': image_id}), params={'resolution': resolution}, headers={}, options=options, response_kind='bytes'))

    async def get_listing_thumbnail(self, listing_id: str, *, resolution: Literal['720p', '1080p', 'native'] | Unset = UNSET, options: RequestOptions | None = None) -> bytes:
        """Get Listing Thumbnail.

        HTTP: GET /api/listings/{listing_id}/thumbnail.

        Source: backend/app/routes/api/listings/router.py:789; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        listing_id: {"title": "Listing Id", "type": "string"}

        resolution: {"default": "native", "enum": ["720p", "1080p", "native"], "title": "Resolution", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/api/listings/{listing_id}/thumbnail', {'listing_id': listing_id}), params={'resolution': resolution}, headers={}, options=options, response_kind='bytes'))

    async def set_listing_thumbnail(self, listing_id: str, *, content_type: str, content: bytes, options: RequestOptions | None = None) -> models.ListingResponse:
        """Set Listing Thumbnail.

        HTTP: PUT /api/listings/{listing_id}/thumbnail.

        Source: backend/app/routes/api/listings/router.py:838; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        content-type: {"type": "string"}
        """
        return cast('models.ListingResponse', await self._client._call('PUT', endpoint_path('/api/listings/{listing_id}/thumbnail', {'listing_id': listing_id}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

    async def new_version(self, listing_id: str, *, body: models.ListingVersionCreateRequest, options: RequestOptions | None = None) -> models.ListingResponse:
        """New Version.

        HTTP: POST /api/listings/{listing_id}/versions.

        Source: backend/app/routes/api/listings/router.py:552; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', await self._client._call('POST', endpoint_path('/api/listings/{listing_id}/versions', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def remove_version(self, listing_id: str, version_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Version.

        HTTP: DELETE /api/listings/{listing_id}/versions/{version_id}.

        Source: backend/app/routes/api/listings/router.py:731; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:delete.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/versions/{version_id}', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json'))

    async def edit_version_metadata(self, listing_id: str, version_id: str, *, body: models.ListingVersionUpdateRequest, options: RequestOptions | None = None) -> models.ListingResponse:
        """Edit Version Metadata.

        HTTP: PATCH /api/listings/{listing_id}/versions/{version_id}.

        Source: backend/app/routes/api/listings/router.py:714; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.ListingResponse', await self._client._call('PATCH', endpoint_path('/api/listings/{listing_id}/versions/{version_id}', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def remove_draft_asset(self, listing_id: str, version_id: str, asset_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Draft Asset.

        HTTP: DELETE /api/listings/{listing_id}/versions/{version_id}/assets/{asset_id}.

        Source: backend/app/routes/api/listings/router.py:758; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:delete.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}

        asset_id: {"title": "Asset Id", "type": "string"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/assets/{asset_id}', {'listing_id': listing_id, 'version_id': version_id, 'asset_id': asset_id}), params={}, headers={}, options=options, response_kind='json'))

    async def edit_version_compatibility(self, listing_id: str, version_id: str, *, body: models.ReleaseCompatibility, options: RequestOptions | None = None) -> models.ListingVersionResponse:
        """Edit Version Compatibility.

        HTTP: PUT /api/listings/{listing_id}/versions/{version_id}/compatibility.

        Source: backend/app/routes/api/listings/router.py:482; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:write.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.ListingVersionResponse', await self._client._call('PUT', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/compatibility', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def release_manifest(self, listing_id: str, version_id: str, *, options: RequestOptions | None = None) -> models.ReleaseManifestResponse:
        """Release Manifest.

        HTTP: GET /api/listings/{listing_id}/versions/{version_id}/manifest.

        Source: backend/app/routes/api/listings/router.py:457; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.ReleaseManifestResponse', await self._client._call('GET', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/manifest', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json'))

    async def publish_listing_version(self, listing_id: str, version_id: str, *, options: RequestOptions | None = None) -> models.ListingResponse:
        """Publish Listing Version.

        HTTP: POST /api/listings/{listing_id}/versions/{version_id}/publish.

        Source: backend/app/routes/api/listings/router.py:686; docs/partner-api.md; docs/openapi.json.

        API key scopes: listings:publish.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.ListingResponse', await self._client._call('POST', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/publish', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json'))

    async def new_asset_upload(self, listing_id: str, version_id: str, *, body: models.ListingAssetUploadCreateRequest, options: RequestOptions | None = None) -> models.UploadSessionResponse:
        """New Asset Upload.

        HTTP: POST /api/listings/{listing_id}/versions/{version_id}/uploads.

        Source: backend/app/routes/api/listings/router.py:578; docs/partner-api.md; docs/openapi.json.

        API key scopes: files:upload.

        listing_id: {"title": "Listing Id", "type": "string"}

        version_id: {"title": "Version Id", "type": "string"}
        """
        return cast('models.UploadSessionResponse', await self._client._call('POST', endpoint_path('/api/listings/{listing_id}/versions/{version_id}/uploads', {'listing_id': listing_id, 'version_id': version_id}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def listing_workshop(self, listing_id: str, *, options: RequestOptions | None = None) -> models.WorkshopModsResponse:
        """Listing Workshop.

        HTTP: GET /api/listings/{listing_id}/workshop.

        Source: backend/app/routes/api/listings/router.py:175; docs/partner-api.md; docs/openapi.json.

        API key scopes: catalog:read.

        Read all current required Workshop mods; legacy fields describe the first mod.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.WorkshopModsResponse', await self._client._call('GET', endpoint_path('/api/listings/{listing_id}/workshop', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

class Ratings:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def remove_rating(self, listing_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Rating.

        HTTP: DELETE /api/listings/{listing_id}/rating.

        Source: backend/app/routes/api/ratings/router.py:50; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('None', self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/rating', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    def my_rating(self, listing_id: str, *, options: RequestOptions | None = None) -> models.RatingResponse | None:
        """My Rating.

        HTTP: GET /api/listings/{listing_id}/rating.

        Source: backend/app/routes/api/ratings/router.py:20; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.RatingResponse | None', self._client._call('GET', endpoint_path('/api/listings/{listing_id}/rating', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    def update_rating(self, listing_id: str, *, body: models.RatingUpdateRequest, options: RequestOptions | None = None) -> models.RatingResponse:
        """Update Rating.

        HTTP: PUT /api/listings/{listing_id}/rating.

        Source: backend/app/routes/api/ratings/router.py:31; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.RatingResponse', self._client._call('PUT', endpoint_path('/api/listings/{listing_id}/rating', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class AsyncRatings:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def remove_rating(self, listing_id: str, *, options: RequestOptions | None = None) -> None:
        """Remove Rating.

        HTTP: DELETE /api/listings/{listing_id}/rating.

        Source: backend/app/routes/api/ratings/router.py:50; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('None', await self._client._call('DELETE', endpoint_path('/api/listings/{listing_id}/rating', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    async def my_rating(self, listing_id: str, *, options: RequestOptions | None = None) -> models.RatingResponse | None:
        """My Rating.

        HTTP: GET /api/listings/{listing_id}/rating.

        Source: backend/app/routes/api/ratings/router.py:20; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.RatingResponse | None', await self._client._call('GET', endpoint_path('/api/listings/{listing_id}/rating', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    async def update_rating(self, listing_id: str, *, body: models.RatingUpdateRequest, options: RequestOptions | None = None) -> models.RatingResponse:
        """Update Rating.

        HTTP: PUT /api/listings/{listing_id}/rating.

        Source: backend/app/routes/api/ratings/router.py:31; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.RatingResponse', await self._client._call('PUT', endpoint_path('/api/listings/{listing_id}/rating', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json', json=body))

class User:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def current_user(self, *, options: RequestOptions | None = None) -> models.UserResponse:
        """Current User.

        HTTP: GET /api/user/me.

        Source: backend/app/routes/api/user/router.py:34; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', self._client._call('GET', endpoint_path('/api/user/me', {}), params={}, headers={}, options=options, response_kind='json'))

    def update_current_user(self, *, body: models.UserProfileUpdateRequest, options: RequestOptions | None = None) -> models.UserProfileUpdateResponse:
        """Update Current User.

        HTTP: PATCH /api/user/me.

        Source: backend/app/routes/api/user/router.py:42; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserProfileUpdateResponse', self._client._call('PATCH', endpoint_path('/api/user/me', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    def delete_current_avatar(self, *, options: RequestOptions | None = None) -> models.UserResponse:
        """Delete Current Avatar.

        HTTP: DELETE /api/user/me/avatar.

        Source: backend/app/routes/api/user/router.py:117; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', self._client._call('DELETE', endpoint_path('/api/user/me/avatar', {}), params={}, headers={}, options=options, response_kind='json'))

    def set_current_avatar(self, *, content_type: str, content: bytes, options: RequestOptions | None = None) -> models.UserResponse:
        """Set Current Avatar.

        HTTP: PUT /api/user/me/avatar.

        Source: backend/app/routes/api/user/router.py:83; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        content-type: {"type": "string"}
        """
        return cast('models.UserResponse', self._client._call('PUT', endpoint_path('/api/user/me/avatar', {}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

    def update_current_password(self, *, body: models.PasswordChangeRequest, options: RequestOptions | None = None) -> models.StatusResponse:
        """Update Current Password.

        HTTP: PUT /api/user/me/password.

        Source: backend/app/routes/api/user/router.py:63; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', self._client._call('PUT', endpoint_path('/api/user/me/password', {}), params={}, headers={}, options=options, response_kind='json', json=body))

class AsyncUser:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def current_user(self, *, options: RequestOptions | None = None) -> models.UserResponse:
        """Current User.

        HTTP: GET /api/user/me.

        Source: backend/app/routes/api/user/router.py:34; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', await self._client._call('GET', endpoint_path('/api/user/me', {}), params={}, headers={}, options=options, response_kind='json'))

    async def update_current_user(self, *, body: models.UserProfileUpdateRequest, options: RequestOptions | None = None) -> models.UserProfileUpdateResponse:
        """Update Current User.

        HTTP: PATCH /api/user/me.

        Source: backend/app/routes/api/user/router.py:42; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserProfileUpdateResponse', await self._client._call('PATCH', endpoint_path('/api/user/me', {}), params={}, headers={}, options=options, response_kind='json', json=body))

    async def delete_current_avatar(self, *, options: RequestOptions | None = None) -> models.UserResponse:
        """Delete Current Avatar.

        HTTP: DELETE /api/user/me/avatar.

        Source: backend/app/routes/api/user/router.py:117; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.UserResponse', await self._client._call('DELETE', endpoint_path('/api/user/me/avatar', {}), params={}, headers={}, options=options, response_kind='json'))

    async def set_current_avatar(self, *, content_type: str, content: bytes, options: RequestOptions | None = None) -> models.UserResponse:
        """Set Current Avatar.

        HTTP: PUT /api/user/me/avatar.

        Source: backend/app/routes/api/user/router.py:83; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        content-type: {"type": "string"}
        """
        return cast('models.UserResponse', await self._client._call('PUT', endpoint_path('/api/user/me/avatar', {}), params={}, headers={'content-type': content_type}, options=options, response_kind='json', content=content))

    async def update_current_password(self, *, body: models.PasswordChangeRequest, options: RequestOptions | None = None) -> models.StatusResponse:
        """Update Current Password.

        HTTP: PUT /api/user/me/password.

        Source: backend/app/routes/api/user/router.py:63; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.
        """
        return cast('models.StatusResponse', await self._client._call('PUT', endpoint_path('/api/user/me/password', {}), params={}, headers={}, options=options, response_kind='json', json=body))

class Users:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def public_profile(self, username: str, *, options: RequestOptions | None = None) -> models.PublicProfileResponse:
        """Public Profile.

        HTTP: GET /api/users/{username}.

        Source: backend/app/routes/api/users/router.py:48; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        username: {"title": "Username", "type": "string"}
        """
        return cast('models.PublicProfileResponse', self._client._call('GET', endpoint_path('/api/users/{username}', {'username': username}), params={}, headers={}, options=options, response_kind='json'))

    def public_avatar(self, username: str, *, options: RequestOptions | None = None) -> bytes:
        """Public Avatar.

        HTTP: GET /api/users/{username}/avatar.

        Source: backend/app/routes/api/users/router.py:24; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        username: {"title": "Username", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/api/users/{username}/avatar', {'username': username}), params={}, headers={}, options=options, response_kind='bytes'))

class AsyncUsers:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def public_profile(self, username: str, *, options: RequestOptions | None = None) -> models.PublicProfileResponse:
        """Public Profile.

        HTTP: GET /api/users/{username}.

        Source: backend/app/routes/api/users/router.py:48; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        username: {"title": "Username", "type": "string"}
        """
        return cast('models.PublicProfileResponse', await self._client._call('GET', endpoint_path('/api/users/{username}', {'username': username}), params={}, headers={}, options=options, response_kind='json'))

    async def public_avatar(self, username: str, *, options: RequestOptions | None = None) -> bytes:
        """Public Avatar.

        HTTP: GET /api/users/{username}/avatar.

        Source: backend/app/routes/api/users/router.py:24; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        username: {"title": "Username", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/api/users/{username}/avatar', {'username': username}), params={}, headers={}, options=options, response_kind='bytes'))

class Website:
    def __init__(self, client: ReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    def active_announcement(self, *, options: RequestOptions | None = None) -> models.AnnouncementResponse | None:
        """Active Announcement.

        HTTP: GET /api/public/announcement.

        Source: backend/app/routes/api/announcements/router.py:22; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Anonymous website read: enabled Markdown announcement or JSON null while disabled; API-key requests are denied.
        """
        return cast('models.AnnouncementResponse | None', self._client._call('GET', endpoint_path('/api/public/announcement', {}), params={}, headers={}, options=options, response_kind='json'))

    def public_image(self, image_id: str, *, options: RequestOptions | None = None) -> bytes:
        """Public Image.

        HTTP: GET /api/public/announcement/image/{image_id}.

        Source: backend/app/routes/api/announcements/router.py:85; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Anonymous current enabled image, obtained through image_url; disabled, replaced, removed or missing images return 404.

        image_id: {"title": "Image Id", "type": "string"}
        """
        return cast('bytes', self._client._call('GET', endpoint_path('/api/public/announcement/image/{image_id}', {'image_id': image_id}), params={}, headers={}, options=options, response_kind='bytes'))

    def active_favourites(self, *, options: RequestOptions | None = None) -> list[models.FavouriteCollectionResponse]:
        """Active Favourites.

        HTTP: GET /api/public/favourites.

        Source: backend/app/routes/api/favourites/router.py:17; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Read active ordered Reclaimer Favourites; /api/favourites requires catalog:read, /api/public/favourites is anonymous.

Returns an unpaginated array, excluding unavailable maps and empty collections.
Full listing descriptions remain in the API even though the homepage card omits them.
Reads do not create views/downloads; poll separately from listing-change events.
        """
        return cast('list[models.FavouriteCollectionResponse]', self._client._call('GET', endpoint_path('/api/public/favourites', {}), params={}, headers={}, options=options, response_kind='json'))

    def public_listings(self, *, q: str | Unset = UNSET, file_type: str | Unset = UNSET, tags: list[str] | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, updated_since: str | None | Unset = UNSET, sort: Literal['updated', 'latest', 'downloads', 'rated', 'unrated', 'overlooked', 'trending', 'rising', 'relevance', 'most_downloads', 'least_downloads', 'most_liked', 'least_liked', 'newest', 'oldest'] | Unset = UNSET, window: Literal['24h', '7d', '30d'] | Unset = UNSET, include_private: bool | Unset = UNSET, options: RequestOptions | None = None) -> models.ListingPageResponse:
        """Public Listings.

        HTTP: GET /api/public/listings.

        Source: backend/app/routes/api/listings/router.py:150; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        q: {"default": "", "maxLength": 100, "title": "Q", "type": "string"}

        file_type: {"default": "", "title": "File Type", "type": "string"}

        tags: {"default": [], "items": {"type": "string"}, "title": "Tags", "type": "array"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 20, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}

        updated_since: {"anyOf": [{"format": "date-time", "type": "string"}, {"type": "null"}], "title": "Updated Since"}

        sort: {"default": "updated", "enum": ["updated", "latest", "downloads", "rated", "unrated", "overlooked", "trending", "rising", "relevance", "most_downloads", "least_downloads", "most_liked", "least_liked", "newest", "oldest"], "title": "Sort", "type": "string"}

        window: {"default": "7d", "enum": ["24h", "7d", "30d"], "title": "Window", "type": "string"}

        include_private: {"default": false, "title": "Include Private", "type": "boolean"}
        """
        return cast('models.ListingPageResponse', self._client._call('GET', endpoint_path('/api/public/listings', {}), params={'q': q, 'file_type': file_type, 'tags': tags, 'page': page, 'page_size': page_size, 'updated_since': updated_since, 'sort': sort, 'window': window, 'include_private': include_private}, headers={}, options=options, response_kind='json'))

    def listing_detail(self, listing_id: str, *, options: RequestOptions | None = None) -> models.ListingResponse:
        """Listing Detail.

        HTTP: GET /api/public/listings/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:440; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', self._client._call('GET', endpoint_path('/api/public/listings/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    def view_listing(self, listing_id: str, *, origin: str | Unset = UNSET, sec_fetch_site: str | Unset = UNSET, options: RequestOptions | None = None) -> models.ListingViewResponse:
        """View Listing.

        HTTP: POST /api/public/listings/{listing_id}/view.

        Source: backend/app/routes/api/browser/router.py:61; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Visible listing navigation: once per listing/browser or IP fallback every 24 hours; also records a site visit.

Returns the current lifetime view_count. Ordinary catalog/share-preview reads
do not count, and API keys cannot submit these browser events.

        listing_id: {"title": "Listing Id", "type": "string"}

        origin: {"type": "string"}

        sec-fetch-site: {"type": "string"}
        """
        return cast('models.ListingViewResponse', self._client._call('POST', endpoint_path('/api/public/listings/{listing_id}/view', {'listing_id': listing_id}), params={}, headers={'origin': origin, 'sec-fetch-site': sec_fetch_site}, options=options, response_kind='json'))

    def listing_workshop(self, listing_id: str, *, options: RequestOptions | None = None) -> models.WorkshopModsResponse:
        """Listing Workshop.

        HTTP: GET /api/public/listings/{listing_id}/workshop.

        Source: backend/app/routes/api/listings/router.py:175; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Read all current required Workshop mods; legacy fields describe the first mod.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.WorkshopModsResponse', self._client._call('GET', endpoint_path('/api/public/listings/{listing_id}/workshop', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    def visit_site(self, *, origin: str | Unset = UNSET, sec_fetch_site: str | Unset = UNSET, options: RequestOptions | None = None) -> None:
        """Visit Site.

        HTTP: POST /api/public/site-visit.

        Source: backend/app/routes/api/browser/router.py:52; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Website navigation event: once per anonymous browser or IP fallback every 24 hours.

        origin: {"type": "string"}

        sec-fetch-site: {"type": "string"}
        """
        return cast('None', self._client._call('POST', endpoint_path('/api/public/site-visit', {}), params={}, headers={'origin': origin, 'sec-fetch-site': sec_fetch_site}, options=options, response_kind='json'))

class AsyncWebsite:
    def __init__(self, client: AsyncReclaimerForgeClient) -> None:
        """Bind this resource to its owning client."""
        self._client = client

    async def active_announcement(self, *, options: RequestOptions | None = None) -> models.AnnouncementResponse | None:
        """Active Announcement.

        HTTP: GET /api/public/announcement.

        Source: backend/app/routes/api/announcements/router.py:22; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Anonymous website read: enabled Markdown announcement or JSON null while disabled; API-key requests are denied.
        """
        return cast('models.AnnouncementResponse | None', await self._client._call('GET', endpoint_path('/api/public/announcement', {}), params={}, headers={}, options=options, response_kind='json'))

    async def public_image(self, image_id: str, *, options: RequestOptions | None = None) -> bytes:
        """Public Image.

        HTTP: GET /api/public/announcement/image/{image_id}.

        Source: backend/app/routes/api/announcements/router.py:85; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Anonymous current enabled image, obtained through image_url; disabled, replaced, removed or missing images return 404.

        image_id: {"title": "Image Id", "type": "string"}
        """
        return cast('bytes', await self._client._call('GET', endpoint_path('/api/public/announcement/image/{image_id}', {'image_id': image_id}), params={}, headers={}, options=options, response_kind='bytes'))

    async def active_favourites(self, *, options: RequestOptions | None = None) -> list[models.FavouriteCollectionResponse]:
        """Active Favourites.

        HTTP: GET /api/public/favourites.

        Source: backend/app/routes/api/favourites/router.py:17; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Read active ordered Reclaimer Favourites; /api/favourites requires catalog:read, /api/public/favourites is anonymous.

Returns an unpaginated array, excluding unavailable maps and empty collections.
Full listing descriptions remain in the API even though the homepage card omits them.
Reads do not create views/downloads; poll separately from listing-change events.
        """
        return cast('list[models.FavouriteCollectionResponse]', await self._client._call('GET', endpoint_path('/api/public/favourites', {}), params={}, headers={}, options=options, response_kind='json'))

    async def public_listings(self, *, q: str | Unset = UNSET, file_type: str | Unset = UNSET, tags: list[str] | Unset = UNSET, page: int | Unset = UNSET, page_size: int | Unset = UNSET, updated_since: str | None | Unset = UNSET, sort: Literal['updated', 'latest', 'downloads', 'rated', 'unrated', 'overlooked', 'trending', 'rising', 'relevance', 'most_downloads', 'least_downloads', 'most_liked', 'least_liked', 'newest', 'oldest'] | Unset = UNSET, window: Literal['24h', '7d', '30d'] | Unset = UNSET, include_private: bool | Unset = UNSET, options: RequestOptions | None = None) -> models.ListingPageResponse:
        """Public Listings.

        HTTP: GET /api/public/listings.

        Source: backend/app/routes/api/listings/router.py:150; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        q: {"default": "", "maxLength": 100, "title": "Q", "type": "string"}

        file_type: {"default": "", "title": "File Type", "type": "string"}

        tags: {"default": [], "items": {"type": "string"}, "title": "Tags", "type": "array"}

        page: {"default": 1, "minimum": 1, "title": "Page", "type": "integer"}

        page_size: {"default": 20, "maximum": 100, "minimum": 1, "title": "Page Size", "type": "integer"}

        updated_since: {"anyOf": [{"format": "date-time", "type": "string"}, {"type": "null"}], "title": "Updated Since"}

        sort: {"default": "updated", "enum": ["updated", "latest", "downloads", "rated", "unrated", "overlooked", "trending", "rising", "relevance", "most_downloads", "least_downloads", "most_liked", "least_liked", "newest", "oldest"], "title": "Sort", "type": "string"}

        window: {"default": "7d", "enum": ["24h", "7d", "30d"], "title": "Window", "type": "string"}

        include_private: {"default": false, "title": "Include Private", "type": "boolean"}
        """
        return cast('models.ListingPageResponse', await self._client._call('GET', endpoint_path('/api/public/listings', {}), params={'q': q, 'file_type': file_type, 'tags': tags, 'page': page, 'page_size': page_size, 'updated_since': updated_since, 'sort': sort, 'window': window, 'include_private': include_private}, headers={}, options=options, response_kind='json'))

    async def listing_detail(self, listing_id: str, *, options: RequestOptions | None = None) -> models.ListingResponse:
        """Listing Detail.

        HTTP: GET /api/public/listings/{listing_id}.

        Source: backend/app/routes/api/listings/router.py:440; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.ListingResponse', await self._client._call('GET', endpoint_path('/api/public/listings/{listing_id}', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    async def view_listing(self, listing_id: str, *, origin: str | Unset = UNSET, sec_fetch_site: str | Unset = UNSET, options: RequestOptions | None = None) -> models.ListingViewResponse:
        """View Listing.

        HTTP: POST /api/public/listings/{listing_id}/view.

        Source: backend/app/routes/api/browser/router.py:61; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Visible listing navigation: once per listing/browser or IP fallback every 24 hours; also records a site visit.

Returns the current lifetime view_count. Ordinary catalog/share-preview reads
do not count, and API keys cannot submit these browser events.

        listing_id: {"title": "Listing Id", "type": "string"}

        origin: {"type": "string"}

        sec-fetch-site: {"type": "string"}
        """
        return cast('models.ListingViewResponse', await self._client._call('POST', endpoint_path('/api/public/listings/{listing_id}/view', {'listing_id': listing_id}), params={}, headers={'origin': origin, 'sec-fetch-site': sec_fetch_site}, options=options, response_kind='json'))

    async def listing_workshop(self, listing_id: str, *, options: RequestOptions | None = None) -> models.WorkshopModsResponse:
        """Listing Workshop.

        HTTP: GET /api/public/listings/{listing_id}/workshop.

        Source: backend/app/routes/api/listings/router.py:175; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Read all current required Workshop mods; legacy fields describe the first mod.

        listing_id: {"title": "Listing Id", "type": "string"}
        """
        return cast('models.WorkshopModsResponse', await self._client._call('GET', endpoint_path('/api/public/listings/{listing_id}/workshop', {'listing_id': listing_id}), params={}, headers={}, options=options, response_kind='json'))

    async def visit_site(self, *, origin: str | Unset = UNSET, sec_fetch_site: str | Unset = UNSET, options: RequestOptions | None = None) -> None:
        """Visit Site.

        HTTP: POST /api/public/site-visit.

        Source: backend/app/routes/api/browser/router.py:52; docs/partner-api.md; docs/openapi.json.

        API key scopes: unavailable; use cookie session or anonymous access as documented.

        Website navigation event: once per anonymous browser or IP fallback every 24 hours.

        origin: {"type": "string"}

        sec-fetch-site: {"type": "string"}
        """
        return cast('None', await self._client._call('POST', endpoint_path('/api/public/site-visit', {}), params={}, headers={'origin': origin, 'sec-fetch-site': sec_fetch_site}, options=options, response_kind='json'))

