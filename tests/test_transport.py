from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from unittest.mock import patch

import httpx
import pytest

import reclaimerforge as forge
from reclaimerforge._policy import retry_after

ZERO = forge.RetryConfig(max_retries=2, backoff_factor=0, jitter=0)


def execute(asynchronous, handler, action, **kwargs):
    transport = httpx.MockTransport(handler)
    if asynchronous:
        async def run():
            async with forge.AsyncReclaimerForgeClient("https://forge.test", transport=transport, **kwargs) as client:
                return await action(client)
        return asyncio.run(run())
    with forge.ReclaimerForgeClient("https://forge.test", transport=transport, **kwargs) as client:
        return action(client)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("status,error", [
    (400, forge.BadRequestError), (401, forge.AuthenticationError),
    (403, forge.PermissionDeniedError), (404, forge.NotFoundError),
    (409, forge.ConflictError), (410, forge.GoneError),
    (413, forge.PayloadTooLargeError), (415, forge.UnsupportedMediaTypeError),
    (422, forge.ValidationError), (429, forge.RateLimitError),
    (503, forge.ServiceUnavailableError), (500, forge.ServerError),
    (418, forge.APIError),
])
def test_status_mapping_preserves_data_without_exposing_secrets(asynchronous, status, error):
    def handler(request):
        return httpx.Response(status, json={"detail": "private-response", "new_field": True})
    with pytest.raises(error) as raised:
        execute(asynchronous, handler, lambda c: c.health.health(), retries=forge.RetryConfig(max_retries=0))
    assert raised.value.status_code == status
    assert raised.value.detail == "private-response"
    assert raised.value.body["new_field"] is True
    assert "private-response" not in str(raised.value)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("failure", [408, 429, 500, 502, 503, 504, "transport"])
def test_safe_transient_requests_retry(asynchronous, failure):
    calls = []
    def handler(request):
        calls.append(request)
        if len(calls) < 3:
            if failure == "transport":
                raise httpx.ConnectError("network", request=request)
            return httpx.Response(failure, json={"detail": "temporary"})
        return httpx.Response(200, json={"status": "ok"})
    assert execute(asynchronous, handler, lambda c: c.health.health(), retries=ZERO) == {"status": "ok"}
    assert len(calls) == 3


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
def test_mutations_do_not_replay_without_opt_in(asynchronous, method):
    calls = []
    def handler(request):
        calls.append(request)
        return httpx.Response(503, json={"detail": "unknown commit state"})
    with pytest.raises(forge.ServiceUnavailableError):
        execute(asynchronous, handler, lambda c: c.request(method, "/api/listings", json={"title": "Arena"}), retries=ZERO)
    assert len(calls) == 1


@pytest.mark.parametrize("asynchronous", [False, True])
def test_explicit_mutation_retry_and_idempotent_chunks(asynchronous):
    for chunk in (False, True):
        calls = []
        def handler(request):
            calls.append(request)
            return httpx.Response(503 if len(calls) == 1 else 200, json={"ok": True})
        action = (lambda c: c.files.upload_chunk("upload", 0, content=b"data")) if chunk else (lambda c: c.request("POST", "/api/listings", json={"title": "Arena"}, options=forge.RequestOptions(retry=True)))
        execute(asynchronous, handler, action, retries=ZERO)
        assert len(calls) == 2
        assert calls[0].content == calls[1].content


@pytest.mark.parametrize("asynchronous", [False, True])
def test_exhausted_transport_error_retains_cause(asynchronous):
    calls = []
    def handler(request):
        calls.append(request)
        raise httpx.ReadTimeout("private URL", request=request)
    with pytest.raises(forge.TransportError) as raised:
        execute(asynchronous, handler, lambda c: c.health.health(), retries=ZERO)
    assert len(calls) == 3
    assert isinstance(raised.value.__cause__, httpx.ReadTimeout)
    assert "private URL" not in str(raised.value)


@pytest.mark.parametrize("asynchronous", [False, True])
def test_retry_after_and_exhausted_quota_wait(asynchronous):
    now = [1000.0]
    sleeps = []
    calls = []
    def sleep(delay):
        sleeps.append(delay)
        now[0] += delay
    async def async_sleep(delay):
        sleep(delay)
    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(429, headers={"Retry-After": "5"}, json={"detail": "wait"})
        return httpx.Response(200, json={"status": "ok"}, headers={"X-RateLimit-Limit": "120", "X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1012"})
    async def async_action(client):
        await client.health.health()
        assert client.rate_limit == forge.RateLimit(120, 0, 1012.0)
        return await client.health.health()
    def sync_action(client):
        client.health.health()
        assert client.rate_limit == forge.RateLimit(120, 0, 1012.0)
        return client.health.health()
    with patch("reclaimerforge._policy.time.time", lambda: now[0]), patch("reclaimerforge.client.time.sleep", sleep), patch("reclaimerforge.client.asyncio.sleep", async_sleep):
        execute(asynchronous, handler, async_action if asynchronous else sync_action, retries=ZERO)
    assert sleeps == [5.0, 7.0]


def test_http_date_retry_and_backoff():
    stamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert retry_after(format_datetime(stamp + timedelta(seconds=12)), stamp.timestamp()) == 12
    assert retry_after("-1") == 0
    for malformed in ("nope", "nan", "inf", ""):
        assert retry_after(malformed) == 0
    with forge.ReclaimerForgeClient(retries=forge.RetryConfig(backoff_factor=1, max_delay=3, jitter=0)) as client:
        assert [client._policy.delay(i) for i in range(4)] == [1, 2, 3, 3]
        response = httpx.Response(503, headers={"Retry-After": "60"})
        assert client._policy.delay(0, response) == 60  # server minimum is not capped


@pytest.mark.parametrize("asynchronous", [False, True])
def test_cookie_login_and_per_call_credential_suppression(asynchronous):
    seen = []
    def handler(request):
        seen.append(request)
        if request.url.path == "/api/auth/login":
            assert "authorization" not in request.headers
            return httpx.Response(200, json={"id": 1}, headers={"set-cookie": "reclaimerforge_session=session-token; Path=/; Secure; HttpOnly"})
        assert "session-token" in request.headers["cookie"]
        assert "authorization" not in request.headers
        return httpx.Response(200, json={"id": 1})
    options = forge.RequestOptions(api_key=None)
    async def async_action(client):
        await client.auth.login(body={"identifier": "user", "password": "password"}, options=options)
        return await client.user.current_user(options=options)
    def sync_action(client):
        client.auth.login(body={"identifier": "user", "password": "password"}, options=options)
        return client.user.current_user(options=options)
    assert execute(asynchronous, handler, async_action if asynchronous else sync_action, api_key="secret") == {"id": 1}
    assert len(seen) == 2


@pytest.mark.parametrize("asynchronous", [False, True])
def test_approved_cdn_redirect_strips_credentials_and_custom_headers(asynchronous):
    seen = []
    def handler(request):
        seen.append(request)
        if len(seen) == 1:
            assert request.headers["authorization"] == "Bearer secret"
            return httpx.Response(307, headers={"location": "https://cdn.test/files/assets/asset/map.json"})
        assert request.url.host == "cdn.test"
        assert not any(name in request.headers for name in ("authorization", "cookie", "x-secret", "x-api-key", "proxy-authorization"))
        assert request.headers["range"] == "bytes=0-3"
        return httpx.Response(206, content=b"data")
    options = forge.RequestOptions(headers={"X-Secret": "private", "Cookie": "manual=secret", "Range": "bytes=0-3"})
    assert execute(asynchronous, handler, lambda c: c.listings.track_asset_download("asset", options=options), api_key="secret", cookies={"reclaimerforge_session": "cookie-secret"}, download_origins=("https://cdn.test",)) == b"data"
    assert len(seen) == 2


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("target", ["https://evil.test/files/a/b", "http://forge.test/files/a/b", "https://user:pass@forge.test/files/a/b", "https://cdn.test/anything-else"])
def test_unsafe_redirects_never_receive_request(asynchronous, target):
    seen = []
    def handler(request):
        seen.append(request)
        return httpx.Response(307, headers={"location": target})
    with pytest.raises(forge.UnsafeURLError):
        execute(asynchronous, handler, lambda c: c.request("GET", "/api/listings/assets/asset/download"), api_key="secret", download_origins=("https://cdn.test",))
    assert len(seen) == 1


@pytest.mark.parametrize("asynchronous", [False, True])
def test_redirect_loop_is_bounded_and_inspection_is_supported(asynchronous):
    calls = []
    def handler(request):
        calls.append(request)
        return httpx.Response(307, headers={"location": "/api/health"})
    with pytest.raises(forge.UnsafeURLError):
        execute(asynchronous, handler, lambda c: c.request("GET", "/api/health"))
    assert len(calls) == 11
    calls.clear()
    result = execute(asynchronous, handler, lambda c: c.request("GET", "/api/health", options=forge.RequestOptions(follow_redirects=False)))
    assert result.status_code == 307
    assert len(calls) == 1


@pytest.mark.parametrize("asynchronous", [False, True])
def test_omission_null_datetime_and_forward_compatible_json(asynchronous):
    def handler(request):
        assert request.url.params.get_list("tags") == ["slayer", "large"]
        assert request.url.params["updated_since"] == "2026-10-15T12:00:00+01:00"
        assert request.url.params["include_private"] == "false"
        return httpx.Response(200, json={"known": None, "extra": {"untouched": []}})
    stamp = datetime(2026, 10, 15, 12, tzinfo=timezone(timedelta(hours=1)))
    assert execute(asynchronous, handler, lambda c: c.listings.public_listings(tags=["slayer", "large"], updated_since=stamp.isoformat(), include_private=False)) == {"known": None, "extra": {"untouched": []}}
    def body_handler(request):
        assert request.content == b'{"title":"Arena","min_players":null}'
        return httpx.Response(200, json={})
    execute(asynchronous, body_handler, lambda c: c.listings.edit_listing("listing", body={"title": "Arena", "min_players": None, "tags": forge.UNSET}))


@pytest.mark.parametrize("asynchronous", [False, True])
def test_raw_headers_timeouts_query_and_escaped_path(asynchronous):
    def handler(request):
        assert request.url.raw_path.startswith(b"/api/listings/a%2Fb%3Fc%23d%20e")
        assert request.headers["x-custom"] == "custom"
        assert request.extensions["timeout"]["read"] == 2.5
        return httpx.Response(200, json={})
    execute(asynchronous, handler, lambda c: c.listings.listing_detail("a/b?c#d e", options=forge.RequestOptions(headers={"X-Custom": "custom"}, timeout=2.5)))
    def raw_handler(request):
        assert request.url.params.get_list("v") == ["123"]
        assert request.url.params.get_list("resolution") == ["720p"]
        assert request.headers["if-none-match"] == '"sha256"'
        return httpx.Response(304)
    result = execute(asynchronous, raw_handler, lambda c: c.request("GET", "/api/listings/listing/thumbnail?v=123", params={"resolution": "720p"}, headers={"If-None-Match": '"sha256"'}))
    assert result.status_code == 304


@pytest.mark.parametrize("asynchronous", [False, True])
def test_non_json_edge_failure_and_malformed_success(asynchronous):
    with pytest.raises(forge.PermissionDeniedError) as raised:
        execute(asynchronous, lambda r: httpx.Response(403, text="<html>challenge</html>"), lambda c: c.health.health())
    assert raised.value.detail == "<html>challenge</html>"
    with pytest.raises(forge.ResponseDecodeError):
        execute(asynchronous, lambda r: httpx.Response(200, text="<html>challenge</html>"), lambda c: c.health.health())


class SyncBytes(httpx.SyncByteStream):
    def __init__(self):
        self.closed = False
    def __iter__(self):
        yield b"part-1"
        yield b"part-2"
    def close(self):
        self.closed = True


class AsyncBytes(httpx.AsyncByteStream):
    def __init__(self):
        self.closed = False
    async def __aiter__(self):
        yield b"part-1"
        yield b"part-2"
    async def aclose(self):
        self.closed = True


@pytest.mark.parametrize("asynchronous", [False, True])
def test_streaming_reads_incrementally_and_closes_on_exception(asynchronous):
    stream = AsyncBytes() if asynchronous else SyncBytes()
    def handler(request):
        return httpx.Response(200, stream=stream)
    async def async_action(client):
        async with client.stream("GET", "/files/assets/asset/map.json") as response:
            assert not response.is_stream_consumed
            assert [part async for part in response.aiter_bytes()] == [b"part-1", b"part-2"]
            raise RuntimeError("caller failed")
    def sync_action(client):
        with client.stream("GET", "/files/assets/asset/map.json") as response:
            assert not response.is_stream_consumed
            assert list(response.iter_bytes()) == [b"part-1", b"part-2"]
            raise RuntimeError("caller failed")
    with pytest.raises(RuntimeError, match="caller failed"):
        execute(asynchronous, handler, async_action if asynchronous else sync_action)
    assert stream.closed


@pytest.mark.parametrize("asynchronous", [False, True])
def test_streaming_errors_are_decoded_before_yield(asynchronous):
    async def async_action(client):
        async with client.stream("GET", "/api/health"):
            pytest.fail("must not yield rejected stream")
    def sync_action(client):
        with client.stream("GET", "/api/health"):
            pytest.fail("must not yield rejected stream")
    with pytest.raises(forge.AuthenticationError) as raised:
        execute(asynchronous, lambda r: httpx.Response(401, json={"detail": "expired"}), async_action if asynchronous else sync_action)
    assert raised.value.detail == "expired"
    assert raised.value.response.is_closed


def test_async_cancellation_is_propagated():
    async def handler(request):
        raise asyncio.CancelledError()
    with pytest.raises(asyncio.CancelledError):
        execute(True, handler, lambda c: c.health.health(), retries=ZERO)


@pytest.mark.parametrize("url", ["ftp://forge.test", "https://user:pass@forge.test", "https://forge.test?key=secret", "https://forge.test#fragment"])
def test_invalid_configuration_rejected(url):
    with pytest.raises(ValueError):
        forge.ReclaimerForgeClient(url)


@pytest.mark.parametrize("kwargs", [{"max_retries": -1}, {"max_retries": 1.5}, {"jitter": float("nan")}, {"backoff_factor": -1}])
def test_retry_configuration_validation(kwargs):
    with pytest.raises(ValueError):
        forge.RetryConfig(**kwargs)
