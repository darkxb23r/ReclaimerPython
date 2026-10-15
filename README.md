# ReclaimerForge Python

Python 3.10+ synchronous and asynchronous clients for the ReclaimerForge API.
All **105 current HTTP operations** and **75 wire schemas** are included, with
explicit method signatures, TypedDict request/response types, and IDE autocomplete.

Start with the [API exploration and endpoint matrix](docs/API_SURFACE.md).
It lists every path, verb, Python method, return type, authentication rules,
documentation gaps, and superseded `/api/v1` proposals. The
[contract snapshot](docs/openapi.json), [original partner guide](docs/partner-api.md),
and [source hashes](docs/source-inventory.json) make coverage auditable.

## Installation

From this checkout:

```sh
python -m pip install .
# Development tools:
python -m pip install -e '.[dev]'
```

The import name and distribution name are `reclaimerforge`. Runtime dependencies
are HTTPX and typing-extensions. Sync and async work with the same installation.
No server packages, database, Pydantic, or application checkout are needed at runtime.

## API keys and catalog access

Create a key through the Forge Developer console with the scopes your integration
needs. Keys act as their creator and do not bypass verification, roles, bans,
private membership, or resource ownership. Keys are not OAuth tokens; the API
documents no OAuth flow. Use HTTPS in production.

```python
import os
from reclaimerforge import ReclaimerForgeClient, models

with ReclaimerForgeClient(
    base_url=os.environ['FORGE_URL'],  # origin, e.g. https://forge.example.com
    api_key=os.environ['FORGE_API_KEY'],
) as client:
    page: models.ListingPageResponse = client.listings.public_listings(
        tags=['slayer', 'competitive'],  # repeated tags=; every tag must match
        page_size=100,
        sort='latest',
        include_private=False,
    )
    for listing in page['items']:
        print(listing['id'], listing['title'])
```

Catalog, manifests, favorites and image reads use `catalog:read`; file/ZIP
downloads use `assets:download`. Draft editing, uploads, publishing and deletion
use `listings:write`, `files:upload`, `listings:publish` and `listings:delete`.
Legacy immediate-publication uploads require both upload and publish scopes.
Each endpoint's docstring identifies its scopes and original route source.

## Async and manual sessions

```python
import asyncio
import os
from reclaimerforge import AsyncReclaimerForgeClient

async def main() -> None:
    async with AsyncReclaimerForgeClient(
        os.environ['FORGE_URL'], api_key=os.environ['FORGE_API_KEY']
    ) as client:
        favorites = await client.favourites.active_favourites()
        print(len(favorites))

asyncio.run(main())
```

Every resource and operation has identical sync/async names and arguments.
Without a context manager, call `client.close()` or `await client.aclose()` in
a `finally` block. Sync clients can share their HTTPX pool across threads;
use an async client within one event loop. Concurrent requests share observed
quota state; the server remains authoritative across clients and processes.

## Cookie sessions and anonymous website routes

Accounts, key management, votes, invitations and staff operations require cookie
sessions. Use a client without a bearer key; login/register automatically retain
the `reclaimerforge_session` cookie. Existing session cookies can be supplied
through `cookies={'reclaimerforge_session': session_token}`.

```python
with ReclaimerForgeClient(os.environ['FORGE_URL']) as session:
    user = session.auth.login(body={
        'identifier': os.environ['FORGE_USERNAME'],
        'password': os.environ['FORGE_PASSWORD'],
    })
    me = session.user.current_user()
    access = session.developer.developer_access()
    session.auth.logout()

with ReclaimerForgeClient(os.environ['FORGE_URL']) as anonymous:
    announcement = anonymous.website.active_announcement()  # dict or None
```

Bearer credentials are sent on all requests by default. The server rejects keys
on session-only/website routes, including staff keys. To explicitly omit a
client's configured key for one call, use `options=RequestOptions(api_key=None)`.
The library never silently substitutes cookie authentication for a failed key.
Do not submit website visit/view events as integration traffic.

## Typed bodies and unchanged responses

Request bodies use `body={...}` for JSON and `content=b'...'` for raw bytes.
Return values are ordinary dictionaries/lists/scalars, bytes for files/images,
strings for documentation, and `None` for 204 or JSON null. Timestamps/URLs remain
JSON strings; new server fields pass through unchanged. TypedDict types describe
the contract and do not validate or coerce at runtime. Server validation errors
retain their full field details. Bounds/defaults are recorded in the OpenAPI snapshot.

```python
from reclaimerforge import models

draft: models.ListingCreateRequest = {
    'title': 'Arena', 'version_label': '1.0', 'visibility': 'private',
    'description': 'A **small** arena.', 'tags': ['slayer'],
}
with ReclaimerForgeClient(os.environ['FORGE_URL'], api_key=os.environ['FORGE_API_KEY']) as client:
    listing = client.listings.new_listing(body=draft)
```

Optional query parameters default to `UNSET`, which means omit. JSON dictionaries
are sent exactly as supplied; omitted keys remain omitted and `None` becomes
JSON null. `UNSET` values in a JSON object are omitted. Keep `null` (unknown)
distinct from `[]` (explicitly none), especially in compatibility requirements.

Listing metadata PATCH requires `title`: omitted description/tags/mod fields use
server defaults and can clear existing values. Only omitted/null player bounds
preserve their values. Version metadata PATCH is partial; explicit nulls are
rejected despite the automatic schema's nullable representation. Compatibility
PUT replaces the whole draft contract; published claims cannot be edited.

## Uploads, pagination and pinned downloads

[upload_release.py](examples/upload_release.py) implements draft creation,
sequential chunks, resume via server progress, asset completion, compatibility,
and optional publication. Chunk size/expiry/expected size come from the server.
Raw chunks use application/octet-stream; images use their actual JPEG/PNG/WebP
Content-Type and gallery uploads also accept `x_filename`. No multipart encoding
is used. The server supports Reclaimer JSON, Halo `.mvar`/`.bin`, and Megalo `.rvt`;
archive uploads are rejected. The older Markdown guide omits `.rvt` support.

Catalog pages are live. Request pages 1 through `pages`, deduplicate IDs, retain
an overlapping `updated_since`, and advance a successful polling watermark only
after all pages succeed. For changes, use the first response's `as_of` as
`updated_before` on later pages. Reconcile the full catalog periodically and poll
favorites independently. Withdrawals/private access revocations require stopping
use of affected content. No SDK helper treats this feed as a durable event log.

[download_verified.py](examples/download_verified.py) pins the exact manifest,
checks schema_version, streams to a temporary file, verifies size and SHA-256,
and installs bytes only after successful verification. Caller-provided output
paths are used rather than trusting remote filenames. Compatibility is an author
claim, not proof that a map runs on a particular server build.

Resource methods buffer file responses for convenience. For ZIPs/large files:

```python
with client.stream('GET', '/files/assets/ASSET_ID/map.json') as response:
    for chunk in response.iter_bytes():
        consume(chunk)

# async with client.stream(...) as response:
#     async for chunk in response.aiter_bytes():
#         ...
```

Use manifest URLs for synchronization rather than browser tracking URLs. A
separate download hostname must be explicitly allowed using
`download_origins=('https://downloads.example.com',)`. Only GET/HEAD `/files/`
paths are allowed there, and **credentials and custom headers are stripped**.
Private downloads stay on the API origin and retain authentication. Dependency
and script URLs in manifests are not fetched. HTTPS downgrades, URL credentials,
unapproved origins and unbounded redirect chains are rejected.

## Retries, rate limits and errors

```python
from reclaimerforge import (
    ReclaimerForgeClient, RetryConfig, RequestOptions, APIError,
    AuthenticationError, RateLimitError, ValidationError,
)

client = ReclaimerForgeClient(
    os.environ['FORGE_URL'], api_key=os.environ['FORGE_API_KEY'],
    timeout=20.0,
    retries=RetryConfig(max_retries=4, backoff_factor=0.5, max_delay=30, jitter=0.25),
    headers={'User-Agent': 'my-forge-integration/1.0 (operator@example.com)'},
)
try:
    page = client.listings.public_listings(
        options=RequestOptions(timeout=10, headers={'X-Request-ID': 'job-42'})
    )
except APIError as error:
    print(error.status_code, error.request_id)
    # Inspect error.detail, error.body, error.headers, error.response as needed.
finally:
    client.close()
```

Default retries: three after the first attempt, exponential backoff plus jitter,
for transport failures and HTTP 408/429/500/502/503/504. GET/HEAD/OPTIONS and the
documented idempotent chunk PUT can retry. Other mutations are not replayed:
an interrupted creation/publication may already have committed. Reconcile state
before resubmission; opt in only when safe with `RequestOptions(retry=True)`.
`retry=False` disables retries for a call. Stream retries stop once headers are
yielded; interruptions during iteration propagate to the caller.

`Retry-After` seconds and HTTP dates are respected as a minimum, even above
max_delay. Observed exhausted X-RateLimit quotas pause later calls until reset.
The default key limit is 120 requests / 60 seconds, shared across scopes.
`client.rate_limit` exposes the most recent quota. `respect_rate_limits=False`
disables proactive pauses; retry delays still honor Retry-After. Limits and
timeouts are configurable; HTTPX `Timeout` and explicit `None` are supported.

Exceptions map 400/401/403/404/409/410/413/415/422/429/503 to named subclasses;
other 5xx use ServerError and other failures APIError. TransportError retains its
HTTPX cause; ResponseDecodeError identifies malformed successful JSON. HTML edge
challenges remain inspectable in APIError.body. A key cannot bypass Cloudflare.
Exception messages and SDK debug logs omit URLs, credentials and response bodies.

Logging uses the `reclaimerforge` logger with a NullHandler; no root logging
configuration is changed. Enable it with Python logging configuration. HTTPX has
its own logger; configure that separately if request URLs contain sensitive data.
TLS verification stays enabled. Environment proxies are ignored unless you
explicitly pass `trust_env=True`.

## Raw responses and coverage

`client.request(method, path, ...)` returns an HTTPX Response with all headers,
status, ETag and content. It accepts arbitrary JSON, buffered byte bodies,
headers and query parameters, including Range, If-None-Match, thumbnail `v`, and
future additions. It shares the same credential, retry and exception policy.
`RequestOptions(follow_redirects=False)` preserves redirect responses for inspection.
Use request/stream for conditional requests returning 304 rather than typed
resource methods that expect a response body.

Resources: `listings`, `files`, `downloads`, `auth`, `user`, `users`, `developer`,
`collaboration`, `ratings`, `favourites`, `website`, `documentation`, `health`,
and `admin_announcement`, `admin_api_activity`, `admin_audit`, `admin_favourites`,
`admin_listings`, `admin_metrics`, `admin_ratings`, `admin_users`.
See [the complete method matrix](docs/API_SURFACE.md#operations).

## Development and verification

The optional local smoke script `test_api.py` is excluded from version control
and package distributions. Shared workflow examples are in `examples/`.

```sh
python -m pytest -q
python -m mypy
python -m ruff check src tests tools examples
python -m build
# Rebuild generated signatures/models from the committed schema (stdlib only):
python tools/generate.py
# Refresh against a local backend with its dependencies installed (Python 3.11+):
python tools/generate.py --source ../ReclaimerForge
```

The exporter imports routers only: it neither starts the app nor connects to
the database, reads `.env`, or reads stored uploads. Source files remain unchanged.
Generated files are committed so runtime use never needs generation. The schema
snapshot supplements FastAPI's omissions for raw bodies, headers, documentation
routes and response media; see the coverage report for conflicts and provenance.

The source Forge repository carries GPL version 2; its original license text is
retained in [UPSTREAM-LICENSE.txt](docs/UPSTREAM-LICENSE.txt) for the included
contract material. No new license for this SDK has been chosen by the generator.

Tests mock HTTPX in both modes for every operation's success and validation
failure, plus transport/security behavior. They do not claim live deployment,
Cloudflare, permissions/database, SMTP, or server upload-validation verification.
See [verification notes](docs/VERIFICATION.md) for checks run in this workspace.
