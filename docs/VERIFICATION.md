# Verification record

Checked locally on Python 3.10.12 with HTTPX 0.28.1:

- 518 tests passed: all 105 operations in sync and async mode with successful
  responses and 422 errors, plus status mapping, retry exhaustion, safe mutation
  handling, chunk replay, quota/reset waits, Retry-After dates, cookie login,
  credential suppression, redirect boundaries, streaming cleanup, cancellation,
  request encoding, future response fields, and verified-download installation.
- All package, test, generator and example modules compile on Python 3.10.
- Every component schema's properties match its TypedDict annotations; endpoint
  parameter signatures and documentation references are checked mechanically.
- Every explicit current endpoint in the partner guide is in the operation
  inventory. Historical /api/v1 proposals are listed separately because the
  current server does not implement them or provide complete schemas.
- Generated outputs reproduce from the committed contract snapshot; source
  inventory hashes verify the files inspected without modifying Forge.
- Package metadata and source layout are checked locally. The distribution has
  not been published.

Not verified here:

- Wheel/sdist build, mypy and Ruff: this environment has setuptools 59.6.0 and
  lacks build/mypy/Ruff. Installing the newer build and development tools failed
  because outbound package-index DNS/network access is unavailable. The package
  declares setuptools >=61 for pyproject metadata. CI defines the build, lint,
  typing and Python 3.10–3.13 checks for an environment with dependency access;
  those CI checks have not been run here.
- Live API, Cloudflare, database transactions, server permissions, upload format
  validation, SMTP and deployment quotas: tests use HTTPX MockTransport and
  make no external requests. A deployment smoke test still needs its actual
  base URL and scoped credentials.

The library is implemented against the inspected contract. These checks are
evidence of client behavior and coverage, not a live-service certification.
