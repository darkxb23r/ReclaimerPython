"""Sync and async clients for the complete contract in docs/API_SURFACE.md."""
from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncIterator, Iterator, Mapping

import httpx

from ._bindings import AsyncResourceBindings, ResourceBindings
from ._policy import Policy, decode, logger
from ._types import UNSET, RateLimit, RequestOptions, RetryConfig, Unset
from .exceptions import TransportError, UnsafeURLError, raise_for_response


class ReclaimerForgeClient(ResourceBindings):
    """Synchronous Forge client; docs/partner-api.md and docs/API_SURFACE.md.

    Use a separate cookie client for session-only endpoints. All sessions are
    owned by the client; close() or a context manager releases connections.
    TLS verification is enabled; environment proxies are disabled by default.
    """

    def __init__(self, base_url: str = "http://localhost:8000", *, api_key: str | None = None, timeout: float | httpx.Timeout | None = 30.0, retries: RetryConfig | None = None, cookies: Mapping[str, str] | None = None, headers: Mapping[str, str] | None = None, transport: httpx.BaseTransport | None = None, respect_rate_limits: bool = True, download_origins: tuple[str, ...] = (), trust_env: bool = False) -> None:
        """Configure an owned HTTPX session; partner-api.md, access and deployment."""
        self._policy = Policy(base_url, api_key, retries or RetryConfig(), respect_rate_limits, download_origins)
        self._http = httpx.Client(timeout=timeout, cookies=cookies, headers={"User-Agent": "reclaimerforge-python/0.1.0", **(headers or {})}, transport=transport, trust_env=trust_env)
        self._bind_resources()

    @property
    def rate_limit(self) -> RateLimit:
        """Last observed X-RateLimit-* headers; partner-api.md, access limits."""
        return self._policy.rate_limit

    @property
    def cookies(self) -> httpx.Cookies:
        """Session cookie jar; auth.login/register populate it automatically."""
        return self._http.cookies

    @property
    def is_closed(self) -> bool:
        """Whether close() has released this client's connection pool."""
        return self._http.is_closed

    def close(self) -> None:
        """Release all owned connections; docs/partner-api.md, integration flow."""
        self._http.close()

    def __enter__(self) -> ReclaimerForgeClient:
        """Enter an owned session; see README context-manager example."""
        self._http.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        """Close the session, including when a request raises."""
        self.close()

    def _send(self, request: httpx.Request, options: RequestOptions, *, stream: bool = False) -> httpx.Response:
        safe = self._policy.can_retry(request, options)
        for attempt in range(self._policy.retries.max_retries + 1):
            delay = self._policy.wait_seconds(request)
            if delay:
                time.sleep(delay)
            try:
                response = self._http.send(request, follow_redirects=False, stream=stream)
            except httpx.TransportError as error:
                if not safe or attempt == self._policy.retries.max_retries:
                    raise TransportError("HTTP transport failed") from error
                logger.debug("Retrying transport failure; attempt %d", attempt + 1)
                time.sleep(self._policy.delay(attempt))
                continue
            self._policy.observe(response)
            if not safe or response.status_code not in self._policy.retries.statuses or attempt == self._policy.retries.max_retries:
                return response
            delay = self._policy.delay(attempt, response)
            response.close()
            logger.debug("Retrying HTTP %d; attempt %d", response.status_code, attempt + 1)
            time.sleep(delay)
        raise AssertionError("unreachable")

    def request(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, headers: Mapping[str, str] | None = None, json: Any = UNSET, content: bytes | Unset = UNSET, options: RequestOptions | None = None, stream: bool = False) -> httpx.Response:
        """Send a raw request and return HTTPX response, retaining all headers.

        Supports documented Range, conditional-download, image version and
        future query parameters; see partner-api.md, downloads. External URLs
        require download_origins and receive no credentials. Non-2xx redirects
        may be inspected with RequestOptions(follow_redirects=False).
        """
        options = options or RequestOptions()
        method = method.upper()
        request = self._policy.prepare(self._http, method, path, params=params, headers=headers, json=json, content=content, options=options)
        for hop in range(11):
            response = self._send(request, options, stream=stream)
            if not options.follow_redirects or not response.has_redirect_location:
                if stream and response.is_error:
                    try:
                        response.read()
                    finally:
                        response.close()
                raise_for_response(response)
                return response
            if hop == 10:
                response.close()
                raise UnsafeURLError("Redirect limit exceeded")
            target = response.url.join(response.headers["location"])
            if response.status_code == 303 or (response.status_code in {301, 302} and request.method == "POST"):
                method, json, content = "GET", UNSET, UNSET
            response.close()
            request = self._policy.prepare(self._http, method, target, params=None, headers=headers, json=json, content=content, options=options)
        raise AssertionError("unreachable")

    @contextmanager
    def stream(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, headers: Mapping[str, str] | None = None, options: RequestOptions | None = None) -> Iterator[httpx.Response]:
        """Stream a download with bounded memory; partner-api.md, downloads.

        Iterate response.iter_bytes(); the context closes it on all exit paths.
        Retries apply before yielding headers; partial transfers are not replayed.
        """
        response = self.request(method, path, params=params, headers=headers, options=options, stream=True)
        try:
            yield response
        finally:
            response.close()

    def _call(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, headers: Mapping[str, Any] | None = None, json: Any = UNSET, content: bytes | Unset = UNSET, options: RequestOptions | None = None, response_kind: str = "json") -> Any:
        response = self.request(method, path, params=params, headers={k: str(v) for k, v in (headers or {}).items() if not isinstance(v, Unset)}, json=json, content=content, options=options)
        return decode(response, response_kind)


class AsyncReclaimerForgeClient(AsyncResourceBindings):
    """Asynchronous equivalent of ReclaimerForgeClient; partner-api.md.

    Use within one event loop. Await aclose() or use async with. Async sleeps
    yield to the event loop and request cancellation is propagated unchanged.
    """

    def __init__(self, base_url: str = "http://localhost:8000", *, api_key: str | None = None, timeout: float | httpx.Timeout | None = 30.0, retries: RetryConfig | None = None, cookies: Mapping[str, str] | None = None, headers: Mapping[str, str] | None = None, transport: httpx.AsyncBaseTransport | None = None, respect_rate_limits: bool = True, download_origins: tuple[str, ...] = (), trust_env: bool = False) -> None:
        """Configure an owned async session; partner-api.md, access and deployment."""
        self._policy = Policy(base_url, api_key, retries or RetryConfig(), respect_rate_limits, download_origins)
        self._http = httpx.AsyncClient(timeout=timeout, cookies=cookies, headers={"User-Agent": "reclaimerforge-python/0.1.0", **(headers or {})}, transport=transport, trust_env=trust_env)
        self._bind_resources()

    @property
    def rate_limit(self) -> RateLimit:
        """Last observed X-RateLimit-* headers; partner-api.md, access limits."""
        return self._policy.rate_limit

    @property
    def cookies(self) -> httpx.Cookies:
        """Session cookie jar populated by auth.login/register."""
        return self._http.cookies

    @property
    def is_closed(self) -> bool:
        """Whether aclose() has released the connection pool."""
        return self._http.is_closed

    async def aclose(self) -> None:
        """Release all owned connections; partner-api.md, integration flow."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncReclaimerForgeClient:
        """Enter an owned async session; see README async example."""
        await self._http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Close the async session even when a request raises."""
        await self.aclose()

    async def _send(self, request: httpx.Request, options: RequestOptions, *, stream: bool = False) -> httpx.Response:
        safe = self._policy.can_retry(request, options)
        for attempt in range(self._policy.retries.max_retries + 1):
            delay = self._policy.wait_seconds(request)
            if delay:
                await asyncio.sleep(delay)
            try:
                response = await self._http.send(request, follow_redirects=False, stream=stream)
            except httpx.TransportError as error:
                if not safe or attempt == self._policy.retries.max_retries:
                    raise TransportError("HTTP transport failed") from error
                logger.debug("Retrying transport failure; attempt %d", attempt + 1)
                await asyncio.sleep(self._policy.delay(attempt))
                continue
            self._policy.observe(response)
            if not safe or response.status_code not in self._policy.retries.statuses or attempt == self._policy.retries.max_retries:
                return response
            delay = self._policy.delay(attempt, response)
            await response.aclose()
            logger.debug("Retrying HTTP %d; attempt %d", response.status_code, attempt + 1)
            await asyncio.sleep(delay)
        raise AssertionError("unreachable")

    async def request(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, headers: Mapping[str, str] | None = None, json: Any = UNSET, content: bytes | Unset = UNSET, options: RequestOptions | None = None, stream: bool = False) -> httpx.Response:
        """Send a raw async request; headers, quotas, errors match sync request().

        See partner-api.md, downloads. Approved external download origins receive
        no credentials; redirects are bounded and cannot downgrade HTTPS.
        """
        options = options or RequestOptions()
        method = method.upper()
        request = self._policy.prepare(self._http, method, path, params=params, headers=headers, json=json, content=content, options=options)
        for hop in range(11):
            response = await self._send(request, options, stream=stream)
            if not options.follow_redirects or not response.has_redirect_location:
                if stream and response.is_error:
                    try:
                        await response.aread()
                    finally:
                        await response.aclose()
                raise_for_response(response)
                return response
            if hop == 10:
                await response.aclose()
                raise UnsafeURLError("Redirect limit exceeded")
            target = response.url.join(response.headers["location"])
            if response.status_code == 303 or (response.status_code in {301, 302} and request.method == "POST"):
                method, json, content = "GET", UNSET, UNSET
            await response.aclose()
            request = self._policy.prepare(self._http, method, target, params=None, headers=headers, json=json, content=content, options=options)
        raise AssertionError("unreachable")

    @asynccontextmanager
    async def stream(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, headers: Mapping[str, str] | None = None, options: RequestOptions | None = None) -> AsyncIterator[httpx.Response]:
        """Stream downloads via response.aiter_bytes(); partner-api.md, downloads.

        Closes on errors/cancellation; partial transfers are not retried.
        """
        response = await self.request(method, path, params=params, headers=headers, options=options, stream=True)
        try:
            yield response
        finally:
            await response.aclose()

    async def _call(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, headers: Mapping[str, Any] | None = None, json: Any = UNSET, content: bytes | Unset = UNSET, options: RequestOptions | None = None, response_kind: str = "json") -> Any:
        response = await self.request(method, path, params=params, headers={k: str(v) for k, v in (headers or {}).items() if not isinstance(v, Unset)}, json=json, content=content, options=options)
        return decode(response, response_kind)

