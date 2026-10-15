"""Transport configuration shared by synchronous and asynchronous clients."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Mapping

import httpx


class Unset:
    """An omitted argument, distinct from an explicit JSON null."""

    def __repr__(self) -> str:
        return "UNSET"


UNSET = Unset()


@dataclass(frozen=True)
class RetryConfig:
    """Retries after the first attempt; partner-api.md, Access and deployment.

    Only reads and the documented idempotent chunk PUT retry by default.
    Server Retry-After is a minimum and is never truncated by max_delay.
    """

    max_retries: int = 3
    backoff_factor: float = 0.5
    max_delay: float = 30.0
    jitter: float = 0.25
    statuses: frozenset[int] = frozenset({408, 429, 500, 502, 503, 504})

    def __post_init__(self) -> None:
        if isinstance(self.max_retries, bool) or not isinstance(self.max_retries, int) or self.max_retries < 0:
            raise ValueError("max_retries must be a nonnegative integer")
        if any(not math.isfinite(v) or v < 0 for v in (self.backoff_factor, self.max_delay, self.jitter)):
            raise ValueError("Retry delays must be finite and nonnegative")


@dataclass(frozen=True)
class RequestOptions:
    """Per-call overrides; applies to every documented operation.

    headers override generated headers. api_key=None explicitly suppresses the
    client's bearer credential for session-only/website routes. retry=True is
    an explicit opt-in to replaying a mutation; use only when safe for the call.
    """

    headers: Mapping[str, str] = field(default_factory=dict)
    timeout: float | httpx.Timeout | None | Unset = UNSET
    api_key: str | None | Unset = UNSET
    retry: bool | None = None
    follow_redirects: bool = True


@dataclass(frozen=True)
class RateLimit:
    """Last observed quota headers; reset_at is Unix seconds, per partner-api.md."""

    limit: int | None = None
    remaining: int | None = None
    reset_at: float | None = None

