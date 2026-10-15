"""Prove the interactive live script without sending network requests."""
import importlib.util
from pathlib import Path

import httpx
import pytest

from reclaimerforge import AsyncReclaimerForgeClient, ReclaimerForgeClient

SCRIPT = Path(__file__).resolve().parents[1] / "test_api.py"
if not SCRIPT.is_file():
    pytest.skip("test_api.py is an optional local-only smoke script", allow_module_level=True)

SPEC = importlib.util.spec_from_file_location("live_smoke", SCRIPT)
SMOKE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SMOKE)


def mock_clients(monkeypatch, handler):
    transport = httpx.MockTransport(handler)
    monkeypatch.setattr(SMOKE, "ReclaimerForgeClient", lambda *args, **kwargs: ReclaimerForgeClient(*args, transport=transport, **kwargs))
    monkeypatch.setattr(SMOKE, "AsyncReclaimerForgeClient", lambda *args, **kwargs: AsyncReclaimerForgeClient(*args, transport=transport, **kwargs))


def catalog(items):
    return {"items": items, "total": len(items), "page": 1, "page_size": 5, "pages": 1}


def test_prompted_key_runs_all_checks_without_mutations_or_secret_output(monkeypatch, capsys):
    monkeypatch.delenv("FORGE_URL", raising=False)
    monkeypatch.delenv("FORGE_API_KEY", raising=False)
    monkeypatch.setattr("builtins.input", lambda prompt: "forge.test")
    monkeypatch.setattr(SMOKE, "getpass", lambda prompt: "test-secret")
    requests = []
    def handler(request):
        requests.append(request)
        assert request.method == "GET"
        assert request.headers["authorization"] == "Bearer test-secret"
        assert "test-secret" not in str(request.url)
        path = request.url.path
        if path == "/api/listings":
            return httpx.Response(200, json=catalog([{"id": "listing", "title": "Arena"}]))
        if path == "/api/listings/listing":
            return httpx.Response(200, json={"id": "listing", "versions": [{"id": "version", "status": "published"}]})
        if path.endswith("/manifest"):
            return httpx.Response(200, json={"schema_version": 1, "listing_id": "listing", "version_id": "version", "assets": [{"id": "asset"}]})
        assert path == "/api/favourites"
        return httpx.Response(200, json=[], headers={"X-RateLimit-Limit": "120", "X-RateLimit-Remaining": "116"})
    mock_clients(monkeypatch, handler)
    assert SMOKE.main() == 0
    output = capsys.readouterr()
    assert "test-secret" not in output.out + output.err
    assert "Arena" in output.out
    assert "Async catalog" in output.out
    assert "Smoke test passed" in output.out
    assert len(requests) == 5


def test_empty_catalog_skips_only_checks_that_need_a_listing(monkeypatch, capsys):
    monkeypatch.setenv("FORGE_URL", "https://forge.test")
    monkeypatch.setenv("FORGE_API_KEY", "test-secret")
    mock_clients(monkeypatch, lambda request: httpx.Response(200, json=[] if request.url.path == "/api/favourites" else catalog([])))
    assert SMOKE.main() == 0
    assert "[SKIP]" in capsys.readouterr().out


@pytest.mark.parametrize("status", [401, 403, 404])
def test_authentication_failures_are_actionable_and_do_not_echo_response(monkeypatch, capsys, status):
    monkeypatch.setenv("FORGE_URL", "https://forge.test")
    monkeypatch.setenv("FORGE_API_KEY", "test-secret")
    mock_clients(monkeypatch, lambda request: httpx.Response(status, json={"detail": "test-secret"}))
    assert SMOKE.main() == 1
    output = capsys.readouterr()
    assert str(status) in output.err
    assert "test-secret" not in output.out + output.err


@pytest.mark.parametrize("value", ["http://remote.test", "https://user:password@forge.test", "https://forge.test?api_key=secret", "https://forge.test/api", ""])
def test_unsafe_or_incorrect_base_urls_are_rejected(value):
    with pytest.raises(ValueError):
        SMOKE.website_url(value)


def test_malformed_catalog_is_reported_as_a_failure(monkeypatch, capsys):
    monkeypatch.setenv("FORGE_URL", "https://forge.test")
    monkeypatch.setenv("FORGE_API_KEY", "test-secret")
    mock_clients(monkeypatch, lambda request: httpx.Response(200, json={"unexpected": []}))
    assert SMOKE.main() == 1
    assert "Catalog response" in capsys.readouterr().err
