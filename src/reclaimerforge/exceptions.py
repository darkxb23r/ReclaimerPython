"""Structured errors matching partner-api.md and DeveloperDocs.vue error codes."""
from __future__ import annotations

from typing import Any

import httpx


class ReclaimerForgeError(Exception):
    """Base SDK failure."""


class TransportError(ReclaimerForgeError):
    """HTTP transport failed after the configured safe retry attempts."""


class UnsafeURLError(ReclaimerForgeError):
    """A URL would cross an unapproved origin or downgrade HTTPS."""


class ResponseDecodeError(ReclaimerForgeError):
    """A successful response does not contain the expected JSON."""

    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        super().__init__(f"Expected JSON in HTTP {response.status_code} response")


class APIError(ReclaimerForgeError):
    """API/edge rejection, retaining response, status, headers, and unmodified detail.

    The message deliberately omits bodies and URLs, which may contain secrets.
    Inspect detail/body explicitly; do not log authentication response bodies.
    """

    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        try:
            self.body: Any = response.json()
        except ValueError:
            self.body = response.text
        self.detail: Any = self.body.get("detail", self.body) if isinstance(self.body, dict) else self.body
        self.request_id = response.headers.get("x-request-id")
        super().__init__(f"ReclaimerForge returned HTTP {self.status_code}")


class BadRequestError(APIError):
    """400: malformed request or chunk size."""


class AuthenticationError(APIError):
    """401: missing, invalid, expired or revoked credential."""


class PermissionDeniedError(APIError):
    """403: insufficient scope, role or account access."""


class NotFoundError(APIError):
    """404: missing, private, draft or withdrawn resource."""


class ConflictError(APIError):
    """409: resource state conflict."""


class GoneError(APIError):
    """410: upload expired; start another upload."""


class PayloadTooLargeError(APIError):
    """413: request or asset exceeds configured limits."""


class UnsupportedMediaTypeError(APIError):
    """415: unsupported Content-Type."""


class ValidationError(APIError):
    """422: field, file or compatibility validation failed."""


class RateLimitError(APIError):
    """429: quota exceeded; inspect Retry-After in headers."""


class ServerError(APIError):
    """5xx: server or upstream service failure."""


class ServiceUnavailableError(ServerError):
    """503: database/service unavailable or initialization missing."""


ERROR_TYPES: dict[int, type[APIError]] = {
    400: BadRequestError, 401: AuthenticationError, 403: PermissionDeniedError,
    404: NotFoundError, 409: ConflictError, 410: GoneError,
    413: PayloadTooLargeError, 415: UnsupportedMediaTypeError,
    422: ValidationError, 429: RateLimitError, 503: ServiceUnavailableError,
}


def raise_for_response(response: httpx.Response) -> None:
    if response.status_code >= 400:
        raise ERROR_TYPES.get(response.status_code, ServerError if response.status_code >= 500 else APIError)(response)
