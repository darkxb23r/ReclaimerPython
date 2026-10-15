"""Shared URL, credential, retry and rate-limit policy; no I/O."""
from __future__ import annotations

import logging
import math
import random
import re
import threading
import time
from datetime import timezone
from email.utils import parsedate_to_datetime
from typing import Any, Mapping

import httpx

from ._encoding import json_value, query_pairs
from ._types import UNSET, RateLimit, RequestOptions, RetryConfig, Unset
from .exceptions import ResponseDecodeError, UnsafeURLError, raise_for_response

logger = logging.getLogger("reclaimerforge")
logger.addHandler(logging.NullHandler())


def origin(url: httpx.URL) -> tuple[str, str, int | None]:
    return url.scheme, url.host, url.port


def retry_after(value: str | None, now: float | None = None) -> float:
    if not value:
        return 0.0
    now = time.time() if now is None else now
    try:
        seconds = float(value)
    except ValueError:
        try:
            stamp = parsedate_to_datetime(value)
            if stamp.tzinfo is None:
                stamp = stamp.replace(tzinfo=timezone.utc)
            seconds = stamp.timestamp() - now
        except (ValueError, OverflowError, TypeError):
            return 0.0
    return max(0.0, seconds) if math.isfinite(seconds) else 0.0


class Policy:
    def __init__(self, base_url: str, api_key: str | None, retries: RetryConfig, respect_rate_limits: bool, download_origins: tuple[str, ...]) -> None:
        self.base_url = httpx.URL(base_url.rstrip("/") + "/")
        if self.base_url.scheme not in {"http", "https"} or not self.base_url.host or self.base_url.userinfo or self.base_url.query or self.base_url.fragment:
            raise ValueError("base_url must be an HTTP(S) URL without credentials, query or fragment")
        self.api_key = api_key
        self.retries = retries
        self.respect_rate_limits = respect_rate_limits
        self.rate_limit = RateLimit()
        self._lock = threading.Lock()
        self._blocked_until = 0.0
        self.download_origins: set[tuple[str, str, int | None]] = set()
        for text in download_origins:
            url = httpx.URL(text)
            if url.scheme not in {"http", "https"} or not url.host or url.userinfo or url.path != "/" or url.query or url.fragment:
                raise ValueError("download_origins must contain HTTP(S) origins without paths or credentials")
            self.download_origins.add(origin(url))

    def resolve(self, path: str | httpx.URL, method: str) -> httpx.URL:
        candidate = httpx.URL(path)
        if candidate.is_relative_url:
            if candidate.host or str(path).startswith("//"):
                raise UnsafeURLError("Protocol-relative URLs are not accepted")
            candidate = self.base_url.join(str(path).lstrip("/"))
        if candidate.userinfo or candidate.scheme not in {"http", "https"}:
            raise UnsafeURLError("Only credential-free HTTP(S) URLs are accepted")
        if self.base_url.scheme == "https" and candidate.scheme != "https":
            raise UnsafeURLError("HTTPS requests cannot be downgraded")
        if origin(candidate) != origin(self.base_url):
            if origin(candidate) not in self.download_origins or method not in {"GET", "HEAD"} or not candidate.path.startswith("/files/"):
                raise UnsafeURLError("External downloads require an approved download origin and /files/ path")
        elif not candidate.path.startswith(self.base_url.path):
            raise UnsafeURLError("Request escaped the configured base URL path")
        return candidate

    def prepare(self, client: httpx.Client | httpx.AsyncClient, method: str, path: str | httpx.URL, *, params: Mapping[str, Any] | None, headers: Mapping[str, Any] | None, json: Any, content: bytes | Unset, options: RequestOptions) -> httpx.Request:
        url = self.resolve(path, method)
        merged = httpx.Headers({k: str(v) for k, v in (headers or {}).items() if not isinstance(v, Unset)})
        merged.update(options.headers)
        key = self.api_key if isinstance(options.api_key, Unset) else options.api_key
        if key is not None and "authorization" not in merged:
            merged["Authorization"] = "Bearer " + key
        kwargs: dict[str, Any] = {"headers": merged}
        if params is not None:
            # Preserve query strings already present in server-provided URLs.
            pairs = list(url.params.multi_items()) + query_pairs(params)
            kwargs["params"] = pairs
        if not isinstance(options.timeout, Unset):
            kwargs["timeout"] = options.timeout
        if not isinstance(json, Unset):
            kwargs["json"] = json_value(json)
        if not isinstance(content, Unset):
            if not isinstance(content, bytes):
                raise TypeError("content must be buffered bytes for safe transport replay")
            kwargs["content"] = content
        request = client.build_request(method, url, **kwargs)
        if options.api_key is None and "authorization" not in merged:
            request.headers.pop("authorization", None)
        if origin(url) != origin(self.base_url):
            # Never send Forge credentials or arbitrary caller headers to a CDN.
            allowed = {"host", "accept", "accept-encoding", "user-agent", "range", "if-range", "if-none-match", "if-modified-since", "connection"}
            for name in list(request.headers):
                if name not in allowed:
                    del request.headers[name]
        return request

    def can_retry(self, request: httpx.Request, options: RequestOptions) -> bool:
        if options.retry is not None:
            return options.retry
        return request.method in {"GET", "HEAD", "OPTIONS"} or (request.method == "PUT" and re.search(r"/api/files/uploads/[^/]+/chunks/[0-9]+$", request.url.path) is not None)

    def delay(self, attempt: int, response: httpx.Response | None = None) -> float:
        backoff = min(self.retries.max_delay, self.retries.backoff_factor * (2 ** min(attempt, 30)))
        server = retry_after(response.headers.get("retry-after")) if response is not None else 0.0
        return max(backoff, server) + random.uniform(0.0, self.retries.jitter)

    def wait_seconds(self, request: httpx.Request) -> float:
        if not self.respect_rate_limits or origin(request.url) != origin(self.base_url):
            return 0.0
        with self._lock:
            return max(0.0, self._blocked_until - time.time())

    def observe(self, response: httpx.Response) -> None:
        if origin(response.request.url) != origin(self.base_url):
            return
        def number(header: str) -> float | None:
            try:
                value = float(response.headers[header])
                return value if math.isfinite(value) and value >= 0 else None
            except (KeyError, ValueError):
                return None
        limit, remaining, reset = (number(h) for h in ("x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset"))
        with self._lock:
            if any(v is not None for v in (limit, remaining, reset)):
                old = self.rate_limit
                # Concurrent responses may arrive out of order in one window.
                if reset == old.reset_at and remaining is not None and old.remaining is not None:
                    remaining = min(remaining, old.remaining)
                if reset is None or old.reset_at is None or reset >= old.reset_at:
                    self.rate_limit = RateLimit(int(limit) if limit is not None else None, int(remaining) if remaining is not None else None, reset)
                if remaining == 0 and reset is not None:
                    self._blocked_until = max(self._blocked_until, reset)
            if response.status_code in {429, 503}:
                self._blocked_until = max(self._blocked_until, time.time() + retry_after(response.headers.get("retry-after")))


def decode(response: httpx.Response, kind: str) -> Any:
    raise_for_response(response)
    if response.status_code == 204:
        return None
    if kind in {"bytes", "redirect"}:
        return response.content
    if kind == "text":
        return response.text
    try:
        return response.json()
    except ValueError as error:
        raise ResponseDecodeError(response) from error

