# Partner API contract

This guide covers the current supported API, including shared authorship,
Reclaimer Favorites, thumbs votes, traffic metrics, editable release details,
and Markdown content. Manifest `schema_version` remains `1`; the additions
preserve existing resource IDs and response fields.

ReclaimerForge's supported catalog API requires a scoped API key. Use
`Authorization: Bearer <key>` over HTTPS. Browser session cookies do not
substitute for a key on catalog or manifest reads. The generated request and
response schemas are available at `GET /api/openapi.json`, which requires
Developer browser access or a valid `catalog:read` key. Raw Swagger UI at
`/api/docs` (also `/docs`) requires a signed-in account with Developer access;
API keys do not grant access to the UI. Sign in on the same hostname first,
then use Swagger's Authorize button with a scoped key to try supported API
operations. Authorization is not persisted by Swagger. Both the UI and schema
are served with `private, no-store`; ReDoc and the default unprotected docs/schema
routes are disabled. The Swagger page alone permits its CDN scripts/styles and
uses a nonce for its initialization script; the rest of the site's script policy
remains unchanged. The developer documentation page is `/developer/docs`.
Both `/developer` and `/developer/docs`
require a signed-in account with Developer access (Developers, Administrators,
and Owners). The full guide at `GET /api/developer/guide` requires the same
browser access or a valid API key with `catalog:read`.

Website browsing remains public through `/api/public/listings` and
`/api/public/listings/{id}`. Those routes serve the website, including anonymous
visitors; public metadata is not confidential. Integrations should use the
supported keyed catalog contract. Images and public file links remain
accessible for website downloads.

## Private listings and Authorized users

Listing creation accepts `visibility: "public" | "private"` (default `public`).
The original owner can change it through `PATCH /api/listings/{id}` alongside
the required title. Omit visibility to preserve it; other editors cannot change
visibility. Publishing a release preserves the listing's visibility.
Private listings, manifests, downloads, thumbnails, and gallery images require
the original owner's or an accepted member's browser session or scoped API key.
Staff roles do not bypass this membership check. Unrelated users and pending
invitees receive 404 for protected resources. Removed listings and unpublished
assets remain unavailable for download.

Catalog and change feeds show public listings by default. Add
`include_private=true` to `GET /api/listings` or `GET /api/listings/changes` to
include private releases accessible to the key's owner. `catalog:read` suffices
for listing details, manifests, and image reads; `assets:download` is still
required for file/ZIP downloads. A key grants neither membership nor additional
roles. `GET /api/listings/mine` and `/mine/{id}` continue to require
`listings:write` and include editable drafts for accepted editors. Those
responses expose `can_edit: true`; ordinary catalog responses are read views.

Owner browser invitations at `POST /api/listings/{id}/collaborators` now accept
`role: "author" | "authorized"` (default `author`). Both roles require acceptance
through the existing `/api/user/me/collaborations/{id}/accept` route. Authorized
users can edit metadata/images, upload, create and publish versions, and remove
old versions like accepted authors. They are excluded from `authors`, attribution,
author search, and public author profiles. Only the owner manages invitations,
listing visibility, and whole-listing deletion. Membership responses and pending
invitations include `role`; changing a membership's role requires removal and a
fresh invitation so credit is never changed without acceptance. Membership
management remains session-only. Removal/decline immediately removes private
access and editing rights from browser sessions, keys, and staged uploads.

Private listings are omitted from public profiles, share-preview metadata,
Reclaimer Favorites, and anonymous browsing. They do not collect public views
or community votes. Private images and files use `private, no-store`, and file
redirects stay on the API hostname rather than the public download CDN host.
Use the relative download URL on the same host with the same credentials.

When an owner switches a public listing to private, origin permissions change
immediately and ReclaimerForge requests a purge of known listing, thumbnail,
gallery, manifest, ZIP, and file URLs on configured application/download hosts.
The update response includes `visibility_warning`: previously downloaded or
cached copies may remain, and purge failures/disabled purging are explicitly
reported. This is access control, not recall of previously distributed files.
The public change feed emits a `withdrawn` record with the listing ID and privacy
transition timestamp, but empty version arrays. Later private edits do not update
that public tombstone. Listings created private never appear in the public feed.
Making a listing public again resumes normal catalog/change-feed visibility.
Hosts must revalidate access when reading pinned private content and stop serving
it after 404/401/403; membership revocation is not a public catalog event.

Deploy migration `0020_private_listings` before the new backend, then retire all
older backend workers before enabling private listings: older versions do not
enforce privacy. Existing listings migrate as public and existing collaborators
remain authors. Downgrade refuses while any private listing or Authorized user
exists, preventing the old application from exposing content or adding unwanted
author credit. Resolve those records explicitly before rollback.

## Optional thumbnail and gallery retrieval

Listing responses already provide `thumbnail_url` (nullable) and `images[]`
with stable image IDs, ordering, media types, filenames, sizes, and image URLs.
Image bytes are fetched separately; an in-game UI can skip them entirely or
request them only as needed. Fetch `GET /api/listings/{id}/thumbnail` and
`GET /api/listings/{id}/images/{image_id}` with a `catalog:read` key. Follow
the returned URLs (including thumbnail version query strings), resolved against
the API base URL. Send the key in the Authorization header, never in a URL.
The same membership checks protect private image bytes. Image requests neither
increment listing views nor downloads and do consume the key's request quota.
Do not embed a reusable server key in a publicly distributed game client;
use a user's own key or a server integration that enforces each user's access.

The Admin panel's **API activity** subsection is private to staff with
`audit.view` (Owners and Administrators by default). Browser-session endpoints
are `GET /api/admin/api-activity/keys`, `GET /api/admin/api-activity/keys/{key_id}`,
and `GET /api/admin/api-activity/requests`. API keys cannot access these endpoints.
The key directory includes all owners and active, expired, and revoked keys;
`q` searches key name, prefix, or username. Key and request lists support
`page` (default 1) and `page_size` (default 25, maximum 100), with `items`,
`total`, `page`, `page_size`, and `pages`. Filter requests with `key_id`.
Responses are `private, no-store` and include safe key identity and owner
username, never token hashes or secret tokens.

Request history starts after migration `0019_api_key_requests` is deployed.
Each request reaching key authorization with a recognized token records its
UTC timestamp, method, URL path (up to 512 characters, without query strings),
HTTP status, and response time in milliseconds. Response time excludes the
transfer of streamed downloads. Scope, quota, expired-key, and revoked-key
denials are included; anonymous requests, unknown/malformed tokens, and
requests blocked before key authorization are excluded. Bodies and headers
are not stored. Existing `request_count`/`last_used_at` continue to describe
requests accepted by key authorization, including accepted requests whose
endpoint later returns an error. Revocation preserves history; physical
deletion of a key/account removes its history. History writes are best effort:
a database failure is logged server-side and does not change the API response.

Clients should tolerate additional response fields. Existing listing/download
paths remain supported. A breaking manifest change requires a new
`schema_version`; clients must check it before processing a manifest. IDs are
opaque strings: use listing, version, and asset IDs as keys, never titles,
filenames, version labels, or array positions. Published version IDs and asset
IDs are retained across later releases. Public availability can be withdrawn.

## Access and deployment

The operator must arrange a Cloudflare browser-challenge exception for approved
partner server egress IPs, scoped to GET requests for the public endpoints in
this document and `/files/assets/`. Include the configured download hostname
when it differs from the catalog hostname. This is an edge deployment setting;
the application cannot bypass a challenge returned before a request reaches it.
Include specifically approved upload paths when a partner needs upload access;
never exempt account or administration routes. Keep origin access
restricted and existing WAF protections in place. Before onboarding, verify the
catalog, OpenAPI, manifest, and manifest download URLs from the partner server
with its key and without browser cookies. Identify the integration with a
descriptive User-Agent and contact information; this does not grant additional
application privileges. An arbitrary Authorization header must never be used as
an unconditional edge allow rule: authentication occurs at the application.

Authenticated requests must bypass CDN caching, including downloads. Configure
an edge cache-bypass rule when the Authorization header is present, ahead of
public download cache rules. The application sends `private, no-store` and
`Cloudflare-CDN-Cache-Control: no-store` on keyed responses, but an existing CDN
cache hit can happen before origin authentication. Do not forward Forge keys to
author-provided dependency/script URLs.

## Developer access and self-service keys

Owners can assign the `developer` primary role through the existing admin
role-management UI. It grants only `developer.access`, not moderation or account
administration. Administrators and Owners also receive `developer.access`.
Active role assignments are authoritative, including their expiration dates.
Role management remains Owner-only.

Open `/developer`, verify your email, and create a named key with the selected
permissions. The key is shown once, can be copied, and is never returned by
later list requests. Only its SHA-256 digest and display prefix are stored.
Use separate keys for separate integrations. Expiry defaults to 90 days and
can be chosen from 1 to 365 days. Each account can have 20 active keys. Rotate
by creating a replacement, updating the integration, then revoking the old key.

Key management uses the existing browser session, never another API key:

| Endpoint | Behavior |
| --- | --- |
| `GET /api/developer/access` | Signed-in account's actual Developer access and verification state. |
| `GET /api/developer/scopes` | Available permission codes and descriptions; Developer access required. |
| `GET /api/developer/keys` | Your keys' IDs, names, prefixes, permissions, expiry/revocation dates, last use, and authorized request counts. |
| `POST /api/developer/keys` | `{name, scopes, expires_in_days}`; returns `{key, token}` once. Requires a verified account with Developer access. |
| `DELETE /api/developer/keys/{key_id}` | Idempotently revokes your own key. Other accounts' keys return `404`, including for Admins/Owners. |

Keys act as their creator and cannot bypass ownership, verification, ban, or
file-validation checks. Subsequent requests fail after revocation or expiry.
Expired/lost role assignments and unverified/banned accounts block existing
keys. Changing a primary role to Member or Moderator revokes that account's
keys; those keys do not reactivate when Developer access is later restored.
Keys cannot access account settings, ratings, admin routes, or key-management
routes, even when created by an Owner. Invalid or underscoped keys never fall
back to cookie or anonymous access.

| Permission | Allowed operations |
| --- | --- |
| `catalog:read` | Public listing/file metadata, searches, change polling, exact release manifests, active Reclaimer Favorites, OpenAPI, and the full developer guide. |
| `assets:download` | Public asset/file downloads and tracked download redirects; keyed requests do not increase popularity. |
| `listings:write` | Create listings; inspect drafts and create/edit versions, metadata, compatibility, thumbnails, and gallery on owned or accepted collaborative listings. |
| `files:upload` | Start uploads on authored drafts; send chunks, inspect progress, and complete your own upload sessions while author access remains active. |
| `listings:publish` | Publish validated drafts on owned or accepted collaborative listings. Legacy file completion and content replacement also require `files:upload`, because they publish immediately. |
| `listings:delete` | Remove your owned listing; delete draft versions/assets or withdraw old published versions on owned or accepted collaborative listings. |

New endpoints deny key access until explicitly added to the scope allowlist.

Each key has a separate default quota of **120 requests per 60 seconds** shared
across its allowed reads, downloads, and writes. This uses a fixed window that
starts with the first authorized request and is stored under a database row
lock, so quotas persist across restarts and apply across PostgreSQL workers.
Successful authorization consumes a request even if subsequent file or input
validation fails. Authentication/scope failures do not consume this quota.
Headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset`
report the quota and reset timestamp in Unix seconds.

Anonymous website/catalog-image requests share the existing rolling limit of
**120 requests per 60 seconds per client IP**. Valid key requests use their own
bucket instead of sharing that IP quota. A rejection is JSON with status `429` and
`Retry-After` in seconds. Wait at least that long and add retry jitter. Database
unavailability is `503` with `Retry-After: 5`; retry that as well. Invalid input
is `422`. Missing/invalid/expired/revoked keys are `401`; insufficient scopes or
account access are `403`. Unknown, draft, and unavailable releases return `404`.

`API_KEY_RATE_LIMIT` and `API_KEY_RATE_WINDOW_SECONDS` configure key quotas;
`SEARCH_RATE_LIMIT` and `SEARCH_RATE_WINDOW_SECONDS` configure anonymous browsing.
`RATE_LIMIT_ENABLED` controls application enforcement. Agree on deployed limits
with the operator. The anonymous limiter remains process-local: production must
use one API worker or enforce a shared anonymous limit at the proxy. Only trust
Cloudflare client IP headers when direct access to the origin is blocked.
Anonymous direct file downloads have no application rate limit; edge bandwidth
policies can still limit downloads. API responses remain outside CDN cache rules.

## Discover and identify releases

| Endpoint | Contract |
| --- | --- |
| `GET /api/listings` | Paginated published catalog; published versions and assets only. |
| `GET /api/listings/{listing_id}` | Current listing metadata with published version history, newest sequence first. |
| `GET /api/listings/{listing_id}/workshop` | Best-effort required Steam Workshop mod title for a published modded listing; requires `catalog:read`. |
| `GET /api/listings/{listing_id}/versions/{version_id}/manifest` | One exact published release; never resolves to the latest release automatically. |
| `GET /api/favourites` | Active, nonempty Reclaimer Favorites collections, with ordered full published listings; requires `catalog:read`. |
| `GET /files/assets/{asset_id}/{filename}` | Validated bytes for one published asset; obtain the URL from its manifest. |

Listings expose `workshop_urls`, an ordered array of all required Steam Workshop
links (`[]` for unmodded listings). The legacy `workshop_url` remains the first
link, or `null`. Create/update requests accept up to 16 HTTPS Steam file-details
links in `workshop_urls`; links are canonicalized and duplicate mod IDs removed.
A modded listing needs at least one link. If both fields are sent, `workshop_url`
must match the first plural entry. Single-link clients remain supported; a legacy
edit resending the same primary link preserves additional requirements, while
changing that link replaces the requirements. Send `workshop_urls` to explicitly
replace the complete list. Turning off `is_modded_map` clears all links.

The Workshop title endpoint returns, for example:
```json
{
  "workshop_id": "12345",
  "title": "Hugegrass",
  "mods": [
    {"workshop_id": "12345", "title": "Hugegrass", "workshop_url": "https://steamcommunity.com/sharedfiles/filedetails/?id=12345"},
    {"workshop_id": "67890", "title": "Ultimate Forge 2.0", "workshop_url": "https://steamcommunity.com/sharedfiles/filedetails/?id=67890"}
  ]
}
```
The top-level ID/title retain the first mod for older integrations. `mods` follows
the saved link order and includes every required mod. Titles are fetched in a
single Steam batch for uncached IDs and cached
for one hour per API process. Unavailable/private items and failed lookups return
`200` with that mod's `title: null`; its link/ID remain available. Those failures are cached for five minutes. Missing,
unpublished, or non-modded listings, and listings without a valid Workshop URL,
return `404`. The website uses the anonymous
`GET /api/public/listings/{listing_id}/workshop` alias without API-key authorization.
Lookup does not increase views/downloads or change listing timestamps. A Steam
title is display metadata, not a verified compatibility or required-version claim;
pinned releases still use manifest `required_workshop_mods`.

The website shows an avatar for one author, smaller names without avatars for two,
and "Various Authors." for larger groups. API `authors` arrays retain every
accepted author's identity and avatar URL.

Catalog query parameters:

| Parameter | Default and meaning |
| --- | --- |
| `page` | 1; positive integer. Values beyond the last page are clamped to the last page. |
| `page_size` | 20; integer from 1 to 100. |
| `q` | Empty; up to 100 characters, searches title, description, and author username. |
| `file_type` | Empty, `forged_map`, `gamemode`, or `playlist`; matches an asset in a published version. |
| `tags` | Repeat for each required tag, e.g. `tags=slayer&tags=hugegrass`; all tags must match. |
| `updated_since` | Optional ISO 8601 timestamp with timezone; only `updated_at` strictly later than this instant. URL-encode `+` in timezone offsets, or use `Z`. |
| `sort` | `updated` by default; also `latest`, `downloads`, `rated`, `unrated`, `overlooked`, `trending`, or `rising`. |
| `window` | `7d` by default; `24h`, `7d`, or `30d` for trending/rising. These are rolling intervals, not calendar periods. |

The website's tag dropdown includes `capture-the-flag`, `assault`,
`territories`, `juggernaut`, `vip`, `oddball`, and `koth` alongside existing
tags. Listing creation and metadata updates accept up to eight tags, each
1–32 lowercase letters, numbers, or hyphens, starting with a letter or number.
Custom valid tags remain supported; these suggestions do not claim verified
layout compatibility. Repeat `tags` in discovery requests to require every
selected tag, for example `tags=capture-the-flag&tags=competitive`.

Results have `items`, `total`, `page`, `page_size`, and `pages` (at least 1 even
when empty). Default order is `updated_at` descending, then listing ID descending
to resolve ties. A listing includes `created_at`, `updated_at`, stable `owner_id`,
creator username, tags, `upvote_count`, `downvote_count`, `vote_count`, total tracked download
count, lifetime `view_count`, and versions. Discovery responses also include `recent_downloads` with
`last_24h`, `last_7d`, and `last_30d` counts. Other listing responses may leave
`recent_downloads` as `null`; read the discovery endpoint for current metrics.
Listing `min_players` and `max_players` are the author's overall recommendation
(defaults 2–16, each from 2 to 128). They do not establish compatibility or
playtested counts for a particular layout. Metadata edits may omit these fields
to preserve the current range; partial changes must still form a valid range.
Timestamps use UTC; treat a timezone-less timestamp from legacy storage as UTC.
`vote_count` is the sum of up and down votes. Public cards, listing pages,
profiles, and share previews display only thumbs-up totals. API consumers can
use both counts to assess feedback. Existing stars are archived, not converted
into votes. Deprecated `rating_average` and `rating_count` describe archived
stars only, with a `null` average when that count is zero; they are excluded
from discovery ranking. Creator usernames can
change and should not be used as permanent author IDs. Use `authors[].user_id`
to enforce author diversity across feeds, including accepted collaborators;
`owner_id` remains the original owner's ID for older clients. Admin account/login metrics
remain private and are not discovery signals.

| Sort | Ranking and eligibility |
| --- | --- |
| `latest` | Most recent published version per listing; drafts do not affect ranking. |
| `updated` | Most recently changed public listing. |
| `downloads` | Lifetime tracked downloads, descending. |
| `rated` | Most thumbs up, then fewest thumbs down; only listings with at least one thumbs-up vote. |
| `unrated` | Listings with no thumbs votes, newest published version first. Archived stars do not count. |
| `overlooked` | Fewest lifetime downloads, then fewest thumbs votes, then newest published version. |
| `trending` | Most recorded downloads in the selected window; only positive counts. |
| `rising` | Largest download-count increase over the preceding interval of equal length, then current-window count; only positive growth and current activity. |

Ties then use `updated_at` descending and listing ID descending. Each request
returns one feed; combine them client-side for 30% latest, 30% downloads, 20%
rated, 10% overlooked, and 10% rising. Deduplicate listing IDs and cap repeated
author `user_id` values across the combined rotation. Use unrated/overlooked results
when a feed has too few eligible entries.

`metrics.as_of` is the UTC measurement time. `metrics.download_history_started_at`
reports when timestamped download recording began. Lifetime totals are retained;
they cannot be converted into historical daily counts. Windows overlapping the
recording start have partial coverage; compare the start with both intervals
before interpreting rising as a fully observed trend. No history is backfilled.
Counts are tracked browser/session asset-download redirects and successful ZIP
response preparations, limited to one download per listing per viewer in a
rolling 24-hour window. All files, ZIPs, and versions of a listing share that
limit; downloading another listing can count separately. Repeat downloads do
not extend the window, and the next download counts at or after 24 hours from
the last counted download. Both lifetime totals and recent activity use this
rule. They do not represent unique players or confirmed transfers.

Signed-in viewers are identified by their validated account across sessions and
devices. Guests, including browsers without cookies, use a SHA-256 hash of the
trusted client IP and User-Agent. Raw addresses and User-Agents are not stored
in download receipts. Guests sharing both identifiers share a limit; changing
either identifier can count as a new guest. Proxy IP headers are used only when
the operator enables the existing trusted-proxy setting. API-key traffic is
excluded before viewer identification and does not create or update receipts.
Direct file URLs, CDN cache hits, and API-key downloads are not counted. Existing anonymous
automation cannot be identified retrospectively; integrations must send keys.

`updated_at` advances on publication, listing edits, gallery changes, published
release label/note corrections, version withdrawal, accepted-author changes,
and moderation. Draft compatibility edits are private and become public only upon
publication. Rating/download counters and thumbnail-only changes do not advance
this timestamp. The `updated_since` catalog filter includes only published
listings. Use the change-polling endpoint below to catch withdrawals as well.
Recheck previously selected listing IDs; a `404` means stop selecting that
listing. Periodically reconcile against the full catalog.

Pages are live queries, not a catalog snapshot. For polling, record the UTC
start of a successful scan, retain an overlap with the previous scan, deduplicate
by IDs, and only advance the watermark after all pages succeed. Rescan
periodically to catch entries moved between pages by concurrent publications.
Do not use the newest item's timestamp as the next watermark.

### Polling changes and withdrawals

`GET /api/listings/changes?updated_since=<UTC timestamp>` requires `catalog:read`.
It returns `items`, `total`, `page`, `page_size`, `pages`, and `as_of`. Each item
contains `listing_id`, `status` (`published` or `withdrawn`), `updated_at`, and
`published_version_ids`, and `withdrawn_version_ids`; draft releases and draft-only listings are excluded.
Withdrawing an old release leaves the listing published and removes its version
ID from `published_version_ids`, adding it to `withdrawn_version_ids`. Release
label/note corrections advance the listing timestamp; refresh the manifest
while keeping the same pinned file IDs and hashes.
Items sort by update time and listing ID ascending. `page_size` defaults to 100
and must be from 1 to 100. All timestamps supplied in queries need a timezone.

For subsequent pages, supply the first page's `as_of` as `updated_before`, along
with the same `updated_since`. Advance the watermark only after all pages
succeed; keep an overlap and periodically reconcile the full catalog. This
reports current states, not every transition: a rapid withdrawal and restoration
may produce only the latest state, and updates during pagination can move rows.
It is polling support for reconciliation, not a durable event queue.
Signed webhooks and broken-release status/event reporting remain follow-up work.

```sh
curl --get 'https://forge.example.com/api/listings' \
  -H "Authorization: Bearer $FORGE_API_KEY" \
  --data-urlencode 'updated_since=2026-10-01T00:00:00Z' \
  --data-urlencode 'page_size=100' --data-urlencode 'page=1'
curl -H "Authorization: Bearer $FORGE_API_KEY" \
  'https://forge.example.com/api/listings/LISTING_ID/versions/VERSION_ID/manifest'
```

## Shared authorship and staff favorites

Listing responses and exact-release manifests include `authors`: an array of
`{user_id, username, avatar_url, is_owner}`. The original owner appears first;
accepted collaborators follow in stable user-ID order. Pending invitations never
appear in public attribution. Existing `owner_id`, `owner_username`, and
`owner_avatar_url` retain their meaning and remain available for older clients.
Use each author's `user_id` for attribution and author diversity. Author credit
describes the current listing team; a release's recorded `created_by` remains
unchanged. Accepting or removing an author updates the listing timestamp and
appears in incremental change polling. Ordinary invitation creation does not.

The listing owner invites an existing username. The recipient must sign in and
verify their email before accepting. Acceptance grants listing editing, gallery
and thumbnail changes, draft access, new releases, compatibility edits, publishing,
and draft/old-version removal, subject to existing validation and release rules.
Only the original owner can delete the whole listing or invite/remove other
collaborators. A collaborator may leave. Removing a collaborator immediately
blocks subsequent writes and their existing staged upload progress, chunks, and
completion requests. Upload sessions still belong to the user who started them;
one author cannot take over another author's upload. Accounts remain subject to
verification and ban checks, and authors cannot cast new votes on their listing.

The website's My uploads includes accepted collaborations. Public creator
profiles and author-name catalog searches also include collaborative listings.
These listing routes work with an accepted author's API key and the existing
operation scopes; accepting an invitation does not grant Developer access or
additional key scopes. Legacy `/api/files` editing remains uploader-only.
Membership management is browser-session-only and is unavailable to API keys:

| Endpoint | Behavior |
| --- | --- |
| `GET /api/listings/{id}/collaborators` | Owner/accepted editor reads pending and accepted members with their roles. |
| `POST /api/listings/{id}/collaborators` | Owner sends `{username, role?}`; role defaults to `author`. Same-role retries are idempotent. |
| `DELETE /api/listings/{id}/collaborators/{user_id}` | Owner cancels/removes a member; any member may remove themselves. |
| `GET /api/user/me/collaborations` | Your pending invitations, with listing title and inviter; no draft contents. |
| `POST /api/user/me/collaborations/{id}/accept` | Verified recipient accepts; retrying acceptance is idempotent. |
| `DELETE /api/user/me/collaborations/{id}` | Recipient declines or leaves. |

Reclaimer Favorites are editorial selections, separate from thumbs votes and
popularity rankings. Owners and Administrators receive `favourites.manage`;
active permission assignments are authoritative. Staff create named collections
of 1–20 distinct published map listings in carousel order, with timezone-aware
`starts_at` and `ends_at`. The display window includes its start and excludes its
end. Collections may overlap. They follow current listing metadata and published
releases rather than pinning a particular version. Maps may be selected regardless
of upload date. Gametype-only, playlist-only, draft, and unavailable listings
cannot be newly selected.

`GET /api/favourites` requires `catalog:read` and returns active, nonempty
collections, newest start first. The anonymous website equivalent is
`GET /api/public/favourites`. Each collection contains `id`, `title`, `starts_at`,
`ends_at`, `updated_at`, ordered `listing_ids`, and matching full `listings`.
Withdrawn/unavailable maps are removed from the public response dynamically;
collections with no available maps disappear. Reading or rotating the carousel
does not count a view or download. Opening the map uses the normal view flow.

Staff browser endpoints at `/api/admin/favourites` support `GET` (the newest
100 collections by default; `limit=1..100`), `POST` to create, and `GET`, `PUT`,
and `DELETE` at `/{collection_id}`. Create/update bodies are
`{title, starts_at, ends_at, listing_ids}`; PUT replaces the selection and order.
Admin responses retain all selected IDs so staff can remove unavailable entries,
while expanded listing contents remain published-only. API keys cannot curate,
including keys issued to Owners. The carousel provides previous/next and pause
controls and pauses automatic changes for focus, hover, hidden tabs, and reduced
motion preferences.

Poll `/api/favourites` independently of `/api/listings/changes`: collection
creation, reordering, and scheduling are not listing-change events. Collection
`updated_at` records curation saves; the currently visible entries can change
with time or listing withdrawal without that timestamp advancing.

The homepage carousel uses full-width thumbnail cards, bottom image fades,
the existing File Share typography for map titles, and compact author attribution
(one avatar for a single author, smaller names for two, or "Various Authors." for more). The
description is omitted from that card's presentation; the API still returns
the full `ListingResponse`, including Markdown `description`, versions,
compatibility, images, votes, views, and downloads. Collection `title` is the
curator's label, not a map title. The Reclaimer Favorites branding changes no
endpoint, identifier, response shape, or manifest version. The feed is an
unpaginated JSON array; with no active eligible selections it returns `[]`.

```sh
curl -H "Authorization: Bearer $FORGE_API_KEY" \
  "$FORGE_URL/api/favourites"
```

The website uses **Reclaimer Favorites** branding and displays legacy default
collection titles with this spelling. Custom collection titles remain intact.
Existing `/api/favourites`, `/api/public/favourites`, and staff endpoint paths
and `favourites.manage` remain unchanged.

## Site announcements

Owners and Administrators manage one site-wide Message of the Day or Patch
Notes popup in **Admin → Site announcement**, using `announcements.manage`
from active role assignments. API keys cannot edit announcements. The browser
endpoints are `GET/PUT /api/admin/announcement`; the anonymous website reads
`GET /api/public/announcement`, which returns `null` while disabled. Reads do
not count listing views or downloads.

| Endpoint | Access and response |
| --- | --- |
| `GET /api/public/announcement` | Anonymous; the enabled `AnnouncementResponse`, or JSON `null` while disabled. |
| `GET /api/public/announcement/image/{image_id}` | Anonymous; only the current enabled image, otherwise `404`. Use the returned `image_url`. |
| `GET /api/admin/announcement` | Owner/Administrator session with active `announcements.manage`; returns saved settings even while disabled. |
| `PUT /api/admin/announcement` | Same permission; replaces settings atomically and returns saved settings with a new revision. |
| `GET /api/admin/announcement/image/{image_id}` | Same permission; current image preview, including while disabled. |

These are website/staff endpoints, not delegated key scopes. API-key requests
to them return `403`, including Owner-issued keys. Public readers should omit
the Authorization header. Public responses use public image URLs; staff
responses use permission-protected preview URLs. Disabled announcement text
is not included in the public response. Reads and image responses are
`Cache-Control: no-store`. Missing announcement initialization returns `503`
on staff settings reads/writes; apply the current migration before deployment.

PUT accepts JSON `{kind, title, body, enabled, image_base64?, remove_image?}`.
`kind` is `motd` or `patch_notes`; the title is 1–120 characters and body up to
20,000 characters. Enabled popups require a nonempty body. The website renders
the body as Markdown, with plain text line breaks preserved. Embedded HTML is
escaped, and unsafe link protocols are rejected. An omitted/null `image_base64`
preserves the image, `remove_image: true` clears it, and supplying both removal
and replacement is rejected. Images must have JPEG/PNG/WebP signatures, with
a decoded size of 1 byte–5 MiB; the entire request is limited to 8 MiB. Invalid
requests preserve the saved announcement and image. Replacement files become
visible only after a successful save; old files are removed.

The payload contains raw base64 image bytes, without a `data:` URL prefix.
Send `Content-Type: application/json`; another type returns `415`. Request
bodies over 8 MiB return `413`; invalid fields or images return `422`.
`title`, `body`, `kind`, and `enabled` are required even when only toggling
publication. Unknown fields are rejected. Image preservation/removal is
independent of the enable switch.

Responses contain `revision`, `kind`, `title`, `body`, `enabled`, `image_url`,
and UTC `updated_at`. Each save creates a revision. Visitors dismiss that
revision locally in their browser; a new revision is eligible to appear again.
Guests and signed-in visitors can reopen the current enabled revision using
the **MotD** or **Patch Notes** button beside the top-left logo. Manual reopening
preserves dismissal, so it does not cause another automatic popup on reload.
If browser storage is unavailable, dismissal lasts for the current page
session. Images on disabled announcements are available only to authorized
staff; public URLs serve only the current enabled announcement's image.
The image occupies the left side and fades horizontally into the text margin;
the desktop popup is wider, and small screens stack the image above the text
with a downward fade. The native modal provides
keyboard focus containment, Escape dismissal, and focus restoration.

Listing `description`, version `release_notes`, and announcement `body` remain
strings containing stored Markdown source in API responses, rather than
rendered HTML. The website shares one renderer across listings, cards, profiles,
release notes, and popup previews. Integrations should render these
strings with an HTML-disabled Markdown parser or display them as escaped text.
Existing IDs, fields, character limits, and stored content are preserved.
Existing leading/trailing whitespace normalization still applies when saving.

## Listing views and site visits

Listing responses expose `view_count`, independently of downloads and votes.
The website records a view when a visitor opens a published listing, including
through a shared listing URL. Hidden-tab navigation waits until the page becomes
visible. Catalog reads, metadata reads, manifests, downloads, and share-preview
HTML do not increment views. API integrations may read the counts with
`catalog:read`; API keys cannot submit browser traffic events.

| Browser endpoint | Response |
| --- | --- |
| `POST /api/public/listings/{listing_id}/view` | `{ "view_count": 1 }`, the current lifetime total; unavailable listings return `404`. Also records an eligible site visit. |
| `POST /api/public/site-visit` | `204`, records an eligible visit to any website page. |

These anonymous endpoints accept no required body and return `Cache-Control:
no-store`. They share the existing per-IP search request quota. Cross-site
browser submissions are rejected. Browser navigation sends the events; ordinary
GET requests do not count visits. Site visits therefore measure visible website
navigation, rather than all HTTP requests or confirmed human visitors.

Views count at most once **per listing per IP per rolling 24 hours**. Site visits
count at most once **site-wide per IP per rolling 24 hours**. Accounts, cookies,
and User-Agent changes do not reset either limit; guests are included. Repeated
events do not extend the window. A new event can count at or after 24 hours from
the previous accepted event. Different listings have independent view limits.
People sharing an IP share the applicable limit.

The server derives the IP from its trusted client-address handling, normalizes
it, and stores a SHA-256 digest in the deduplication receipts. Client-supplied
body IPs and untrusted forwarding headers cannot select another identity.
Configure `TRUST_CLOUDFLARE_PROXY` only when the origin is restricted to trusted
proxy traffic. Traffic tables contain no raw IP or account identity; existing
request logging is separate. Database claims and count updates are atomic
across workers and persist through restarts. Views do not change listing
`updated_at` or affect download-based discovery rankings.

Admin user directory, detail, and moderation responses return `email` with
the entire local part masked, for example `***@example.com`. Account email
storage and email search are unchanged. These routes require authorized
browser sessions; API keys cannot access them. Listing vote counts and vote
contracts are unchanged by the website's emoji-only vote presentation.

`GET /api/admin/metrics` adds `site_visits_total`, `site_visits_today`, and
`site_visits_last_7_days`, protected by the existing `metrics.view` permission.
Today starts at UTC midnight; seven days is rolling. These windows count accepted
visit events, not distinct IPs across the entire reporting period. The rolling
24-hour deduplication window does not reset at midnight. Counts begin when this
feature is deployed; there is no historical backfill.

## Pinned manifests and synchronization downloads

A manifest contains `schema_version: 1`, `listing_id`, `version_id`, `sequence`,
`version_label`, `release_notes`, `published_at`, `assets`, `compatibility`, and
current-listing `authors`. Published files/claims remain pinned; current
attribution and editable release labels/notes can change.
Each asset has its stable `id`, label, `asset_type`, original filename,
`size_bytes`, lowercase hex `sha256`, creation timestamp, download URL, format,
and detected `base_map_id`/`base_map_stem` (nullable). Supported formats are:

| `format` | `asset_type` | Typical extension |
| --- | --- | --- |
| `reclaimer_json` | `forged_map`, `gamemode`, or `playlist` | `.json` |
| `halo3_mvar` | `forged_map` | `.mvar` |
| `halo3_gametype_bin` | `gamemode` | `.bin` |

Binary formats follow the validated variant type, even when a file was uploaded
with a misleading filename. Original filenames are labels, not format evidence.

Manifest `download_url` values point directly to `/files/assets/`, possibly on
`PUBLIC_DOWNLOAD_BASE_URL`. Relative URLs resolve against the catalog origin.
These downloads **do not increment popularity counters**. Use them for fleet
synchronization, validation retries, and cache warming. The existing listing
response URLs at `/api/listings/assets/{asset_id}/download` are human download
tracking redirects and increment the counter for browser/session traffic.
Authenticated key requests are recognized as automation and do not increment
that counter either. Direct manifest download URLs remain preferred.

`GET /api/listings/versions/{version_id}/download` downloads a ZIP of a published
release, grouped into `maps/`, `gamemodes/`, and `playlists/`, with duplicate
filenames preserved through unique names. Keyed requests require
`assets:download` and do not increase popularity; browser requests do. Draft
or withdrawn releases return `404`. Validate each extracted file against its
manifest hash before use.

Always verify both size and SHA-256 before staging or promoting bytes. Direct
downloads send an ETag containing the SHA-256. A format name confirms server
upload validation, not successful execution on a particular host. The manifest
does not certify support for Merlin packed maps or any server build.

Pin `(listing_id, version_id, asset_id, sha256)` for rollback. Published asset
bytes, bundle relationships, and compatibility remain fixed. Authors must create
a new version to correct a compatibility claim. Release labels and release notes
can be corrected without changing IDs, sequence, publication date, or hashes.
Titles, listing
descriptions, tags, and deployment download hostnames can change independently.
Drafts and withdrawn listings have no public manifest or origin download.
Previously cached CDN bytes can outlive an origin withdrawal; catalog
availability remains the selection authority.

### Correcting release details and deleting versions

`PATCH /api/listings/{listing_id}/versions/{version_id}` accepts a non-empty
partial object containing `version_label` (1–32 nonblank characters) and/or
`release_notes` (up to 4,000 characters; `""` clears notes). It requires the
author's session or a key with `listings:write`, and returns the updated listing.
Labels must be unique within the listing, ignoring case; withdrawn labels remain
reserved. Explicit nulls and unrelated fields are rejected. Drafts and published
releases can be edited; withdrawn releases cannot. Published edits advance
`updated_at` so incremental polling observes the correction.

`DELETE /api/listings/{listing_id}/versions/{version_id}` requires the author or
their own key with `listings:delete`. Accepted collaborators have the same
version-level rights; whole-listing deletion remains owner-only. Drafts are discarded with their staged and
uploaded files. Published releases are withdrawn: IDs, hashes, and private stored
bytes are retained, while public history, manifests, individual downloads, ZIPs,
and legacy aliases stop serving that release at the origin. Configured
Cloudflare purges are attempted after commit; cached copies can persist if edge
purging is unavailable. Repeat withdrawal is idempotent. The final published
version cannot be deleted (`409`); remove the whole listing instead. Pinned
integrations must stop selecting withdrawn versions and reconcile availability.

### Voting

The session-authenticated `PUT /api/listings/{listing_id}/rating` accepts
`{"vote":"up"}` or `{"vote":"down"}`. One account has one editable vote per
listing; authors cannot vote on their own listings. GET returns that account's
feedback with nullable `vote`, and DELETE removes its feedback, including any
archived star rating. Aggregate thumbs-down counts are API metadata, not shown
on public listing cards or details. API keys cannot submit votes.

The same endpoint still accepts the deprecated `{"score":1..5}` shape for
older clients; this writes archived star feedback without creating or changing
a thumbs vote. Supplying both fields is rejected. `RatingResponse.score` remains
an integer for older readers: it projects a thumbs vote as 5/up or 1/down;
when there is no vote it represents the archived score. Use `vote` and the new
listing count fields for all new integrations.

## Compatibility and bundle relationships

Compatibility belongs to the exact release. Every forged-map asset receives a
layout entry; an omitted layout is returned with unknown fields. Detected base
map IDs/stems are file metadata and are never converted into family, objectives,
team support, or playtest claims. Clients must evaluate the selected layout,
not infer that all maps in a release support the same gametypes.

The map-objective inspection script and inventory reports are offline analysis
tools. The API does not currently expose detected flag/bomb/objective presence
fields. Continue treating omitted layout support as unknown; the reports do
not turn author compatibility claims into verified host testing.

| Field | Meaning |
| --- | --- |
| `evidence` | Output-only `unknown` for releases with no claims; `author_reported` when metadata was submitted or a known Workshop requirement snapshotted. Never host-verified. |
| `game_engine` | Engine identifier, e.g. `halo3`, or `null`. |
| `required_reclaimer_version` | Author's version requirement string, or `null`; no server-side requirement-string evaluation. |
| `layouts[].map_asset_id` | Exact forged-map asset defining this layout. |
| `layouts[].base_map_family` | Suggested identifiers: `hugegrass`, `thiccgrass`, `stock_halo3`, `halo3_forge_world_port`; other names allowed, `null` unknown. |
| `layouts[].supported_gametypes` | List of gametype claims for this layout; `null` unknown, `[]` explicitly none. |
| `supported_gametypes[].gametype` | Gametype name, e.g. `slayer` or `ctf`. |
| `supported_gametypes[].gametype_asset_id` | Optional exact bundled gamemode asset; `null` means no supplied asset link. |
| `supported_gametypes[].team_counts` | Claimed supported team counts for this layout/gametype; `null` unknown. For free-for-all, use the gametype name and leave team counts unknown unless applicable. |
| `layouts[].recommended_players` | `{minimum, maximum}` recommendation, separate from playtesting; `null` unknown. |
| `layouts[].playtested_player_counts` | Actual populations the author reports testing; `null` unknown, `[]` no reported tests. Still an author claim. |
| `bundles` | Named lists of exact asset IDs that belong together; `null` means relationships unknown. Assets in the same release are not automatically one runnable bundle. |
| `required_workshop_mods` | Workshop ID and nullable required version for each required mod. |
| `required_scripts`, `dependencies` | Names with optional HTTP(S) URL, required version, and SHA-256 for external prerequisites. These URLs are author-provided and are not fetched or validated by the server. |
| `special_settings` | Author's required settings, as a bounded list of strings. |

For all nullable requirement lists, `null` means unknown and `[]` explicitly
means no requirements claimed. Unknown must not be interpreted as compatible.
A modded listing's complete Workshop link list is snapshotted on publication when
the mod list is unknown, with each mod's version still unknown. An explicit mod list
must include every listing requirement; provided version requirements are retained.
Changing listing links does not change published manifest snapshots. Older releases remain unknown until an author
publishes a new revision. Scripts are external prerequisites in this deliverable;
script uploads and execution are not supported. Release-level requirements
apply to every bundle in the release.

A verified author can replace a draft's compatibility with:
`PUT /api/listings/{listing_id}/versions/{version_id}/compatibility` using the
existing owner session or a key with `listings:write`. It is a full replacement,
not a partial merge. Upload
assets first so their IDs are available. This returns the updated version.
Unknown input fields are rejected, including attempts to assert verified
evidence. Asset references must belong to this version and have the correct
map/gamemode type. Remove references from compatibility before deleting a draft
asset. Publishing freezes the claims; later edits return `409`.

Example draft payload (substitute actual asset IDs and dependency requirements):

```json
{
  "game_engine": "halo3",
  "required_reclaimer_version": ">=1.0",
  "layouts": [{
    "map_asset_id": "MAP_ASSET_ID",
    "base_map_family": "hugegrass",
    "supported_gametypes": [{
      "gametype": "slayer",
      "gametype_asset_id": "GAMETYPE_ASSET_ID",
      "team_counts": [2]
    }],
    "recommended_players": {"minimum": 8, "maximum": 16},
    "playtested_player_counts": [8]
  }],
  "bundles": [{"name": "Arena Slayer", "asset_ids": ["MAP_ASSET_ID", "GAMETYPE_ASSET_ID"]}],
  "required_workshop_mods": [{"workshop_id": "12345", "required_version": null}],
  "required_scripts": [],
  "dependencies": [],
  "special_settings": ["Disable friendly fire"]
}
```

## Integration flow and follow-up work

### Listing management with a key

The following supported routes apply to the key creator's owned listings and
accepted collaborations. Private reads include drafts and exclude withdrawn
versions; public detail and manifest reads remain published-only.

| Endpoint | Scope and behavior |
| --- | --- |
| `GET /api/listings/mine` | `listings:write`; unpaginated array of owned/accepted collaborative listings, including drafts. |
| `GET /api/listings/mine/{listing_id}` | `listings:write`; one editable listing, including drafts; returns `404` after membership removal. |
| `POST /api/listings` | `listings:write`; creates an owned listing and its first draft, returning the listing with draft IDs. |
| `PATCH /api/listings/{listing_id}` | `listings:write`; edits listing metadata and returns the listing. |
| `POST /api/listings/{listing_id}/versions` | `listings:write`; creates a draft using `{version_label, release_notes?}` and returns the listing with that draft on the first successful request. |
| `PATCH /api/listings/{listing_id}/versions/{version_id}` | `listings:write`; corrects draft/published labels and Markdown notes, returning the listing. |
| `DELETE /api/listings/{listing_id}/versions/{version_id}` | `listings:delete`; discards a draft or withdraws an old published release; `204`, or `409` for the last published version. |
| `DELETE /api/listings/{listing_id}/versions/{version_id}/assets/{asset_id}` | `listings:delete`; removes an editable draft asset; referenced bundle/layout assets must be removed from draft compatibility first. |
| `DELETE /api/listings/{listing_id}` | `listings:delete`; original owner only, even for accepted coauthors. |

Listing metadata PATCH requires `title`. Send the intended `description`,
`tags`, `is_modded_map`, and `workshop_urls` (or legacy `workshop_url`): omitted values use schema defaults
and can clear those fields. Only omitted/null `min_players` and `max_players`
preserve their current values. This differs from the genuinely partial
version-label/note PATCH. Listing descriptions allow 2,000 characters;
release notes allow 4,000. Both store Markdown source. Verified email is
required for new drafts, uploads, compatibility writes, and publication;
API-key authorization also requires a verified active account on every request.

Gallery operations use `listings:write`: `POST /api/listings/{id}/images`
accepts raw JPEG/PNG/WebP bytes (up to 8 MiB, at most 10 images); `DELETE`
at `/images/{image_id}` removes one. `PUT /api/listings/{id}/thumbnail` accepts
raw JPEG/PNG/WebP bytes up to 5 MiB. Send the matching image Content-Type.
Public image URLs from responses remain available to website visitors;
catalog keys can read them. Gallery POST and thumbnail PUT return the listing,
and gallery DELETE returns `204`. Images and thumbnails are shared listing
metadata, not immutable manifest assets.

### Uploading with a key

For staged uploads, grant `listings:write` and `files:upload`; add
`listings:publish` only if the integration should make releases public.
Send the bearer header on every operation:

1. `POST /api/listings` with `{title, version_label, description, tags}` creates
   a draft listing and its first version. Save both IDs.
2. `POST /api/listings/{listing_id}/versions/{version_id}/uploads` with
   `{original_filename, file_type, file_size, label}` creates each upload.
   `file_type` defaults to `auto` (detected from validated bytes), or can be
   `forged_map`, `gamemode`, or `playlist`. Save the upload ID and `chunk_size`.
3. Send raw binary bytes to `PUT /api/files/uploads/{upload_id}/chunks/{index}`,
   starting at index 0. Send exactly `chunk_size` bytes except for the final
   remaining bytes. For recovery, `GET /api/files/uploads/{upload_id}` reports
   `received_size` and `next_chunk_index`; retries of already accepted chunks
   return current progress without appending the bytes again.
4. `POST /api/listings/uploads/{upload_id}/complete` validates the assembled
   file and returns its asset ID. Invalid bytes are rejected with `422` and
   never become public. Repeat for each asset.
5. Replace draft compatibility and bundle relationships using the resulting
   asset IDs, then `POST /api/listings/{listing_id}/versions/{version_id}/publish`.

Defaults are 100 MiB per file, 8 MiB chunks, and 24-hour upload sessions. Listing
releases support more than 10 assets and staged listing uploads do not use the
legacy hourly upload-start limit. The legacy `/api/files/uploads` path allows
20 upload starts per account per hour. API key request quotas apply to both
paths. Configured
size/expiry values and the upload response are authoritative. Expired uploads
return `410` and need a new upload session. Existing validation and ownership
checks apply equally to session and key uploads. Scripts and archives remain
unsupported. `POST /api/files/uploads/{id}/complete` is the legacy immediate
publication path and requires both upload and publish permissions.

Discover → pin manifest → download on pve → verify hashes → validate on the
target server build → test → promote to a suitable rotation when empty →
monitor → roll back to a previously validated pinned release when needed.
Keep local host test evidence keyed by asset hash and server build; do not
overwrite author claims with it. API availability does not grant a creator's
hosting, redistribution, or cache license; explicit permission fields are
follow-up work.

The requested discovery mix is supported through the ranked catalog feeds and
stable author IDs. Use `authors[].user_id` for shared-team diversity, or
`owner_id` for original-owner compatibility. Playlist assets and curated map
favourites are supported;
followable authors/collections and featured playlists remain separate product features.
Hosting/cache permission records, signed webhook delivery, broken-release
reporting, and host feedback submission still need separate contracts. Scripts
can be declared as external dependencies with versions and optional hashes;
script upload and verification are not part of the supported file pipeline.

Deploy with `python -m alembic upgrade head` before starting the new backend.
Migration `0010_release_compatibility` adds one nullable JSON column to
`listing_versions`, preserving existing release/asset IDs and hashes. Roll back
to `0009_download_counts` only with the previous backend and after backing up
compatibility metadata: the downgrade removes that column and its claims.

Migration `0011_developer_api_keys` adds the key table, Developer role, and
`developer.access` grants to Developer/Administrator/Owner. It does not assign
the Developer role to ordinary accounts. Before downgrade to
`0010_release_compatibility`, back up the database and run the previous backend:
the downgrade deletes keys and Developer assignments and sets primary
Developer accounts back to Member. Key plaintext cannot be recovered from a
database backup; replacement keys must be issued after rollback/re-upgrade.

`0010_player_ranges` adds the listing-level player recommendations.
`0012_merge_feature_branches` joins that migration with
`0011_developer_api_keys` into a single head. Existing revision IDs are retained,
so databases on either original branch (or both heads) can run `upgrade head`
without resetting migrations or losing their existing data.

`0013_download_history` adds timestamped tracked-download events and a recording
start marker. It preserves existing lifetime totals, releases, keys, and claims.
Run `upgrade head` before starting this backend. To roll back, run the previous
backend and downgrade to `0012_merge_feature_branches`; lifetime totals survive,
but recorded event history is deleted. Back up that history before downgrade.

`0014_download_dedup` adds per-listing viewer receipts for the rolling 24-hour
limit. It preserves lifetime totals and existing timestamped history; older
downloads have no viewer identity and cannot be deduplicated retrospectively.
Run `upgrade head` before starting this backend. To roll back, run the previous
backend and downgrade to `0013_download_history`; totals and event history
survive, but receipts are deleted. Re-upgrading starts fresh viewer windows.

`0015_thumbs_votes` adds nullable vote and archived-score fields. Existing stars
are copied to the archive without creating thumbs votes; IDs and uniqueness
constraints are preserved. Run `upgrade head` before starting the new backend,
then deploy the matching frontend. Avoid concurrent writes by older backends
during the transition. Before downgrading to `0014_download_dedup`, back up vote
data and use the previous backend. Downgrade restores original archived star
scores; thumbs-only entries use the 5/up or 1/down projection, and thumbs vote
state is removed. Re-upgrading starts thumbs votes fresh.

`0016_listing_views` adds a zero-initialized listing view counter, persistent
per-IP view/visit receipts, and timestamped accepted site visits. Existing
downloads, votes, releases, keys, and claims are preserved. Run `upgrade head`
before starting the matching backend/frontend. Before downgrading to
`0015_thumbs_votes`, back up traffic data and use the previous application:
downgrade deletes view totals, receipts, and site-visit history only. Re-upgrading
starts those metrics and deduplication windows fresh.

`0017_collaboration_favourites` adds collaborator invitations/acceptances and
scheduled favourites collections/entries, plus `favourites.manage` grants for
Owners and Administrators. It changes no existing owners, files, release IDs,
hashes, votes, download counts, or views. Existing listings still have one author
until an invitation is accepted. Deploy with `upgrade head` before starting the
matching backend/frontend. Back up collaboration and favourites data before
downgrading to `0016_listing_views` with the previous application: that rollback
removes the new tables and permission only. Re-upgrading starts with no
collaborations or curated collections. Avoid writes from older applications
during rollout, since they do not enforce collaborator permissions.

`0018_site_announcements` adds a singleton announcement, initially disabled,
and `announcements.manage` for Owners and Administrators. It also renames
collection titles equal to `Forge Favourites` to `Reclaimer Favourites`;
custom titles and all selections are preserved. Existing listings, releases,
collaborations, and metrics are untouched. Run `upgrade head` before starting
the matching backend/frontend. Before downgrading to
`0017_collaboration_favourites`, back up the announcement table and its image
in storage and run the previous application. Downgrade removes announcement
metadata and its permission, leaves existing favourites/metrics intact, and
retains the renamed titles. Image files are not deleted by the migration.
Re-upgrading creates a blank, disabled announcement.

## Partner requirement coverage

| Requirement | Current contract |
| --- | --- |
| Documented access | Scoped self-service keys, stable IDs, pagination, timestamps, quotas, and OpenAPI. Cloudflare challenge exceptions are operator configuration and must be tested from the partner's server. |
| Discovery variety | Latest, updated, downloads, rated, unrated, overlooked, trending, and rising; explicit thumbs counts and recorded recent download counts. |
| Versioned files and bundles | Immutable files/claims, SHA-256, sizes, detected formats, playlist assets, bundle membership, Workshop versions, and external script/dependency declarations. Release labels/notes are editable; old releases can be withdrawn. |
| Compatibility | Engine/Reclaimer requirements, per-map layout families, gametypes/team counts, recommendations, author-reported playtests, dependencies/settings, and explicit unknown values. |
| Updates | Incremental catalog reads plus change polling including withdrawals. Signed webhooks and broken-release events are pending. |
| Popularity protection | API-key synchronization excluded from lifetime and recent download metrics. |
| Host feedback | Pending; author claims are never represented as verified host testing. |
| Collections and permissions | Shared author attribution and editing, scheduled staff favourites with ordered map selections, and downloadable playlist files. Followable collections/authors and hosting/cache permission fields are pending. |
