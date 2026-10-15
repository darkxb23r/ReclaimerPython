"""The verified download example must never install unverified bytes."""
import hashlib
import importlib.util
from pathlib import Path

import httpx
import pytest

from reclaimerforge import ReclaimerForgeClient

MODULE_PATH = Path(__file__).resolve().parents[1] / "examples/download_verified.py"
SPEC = importlib.util.spec_from_file_location("download_verified", MODULE_PATH)
DOWNLOAD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOWNLOAD)


@pytest.mark.parametrize("mode", ["valid", "hash", "short", "long", "version", "existing"])
def test_verified_download_is_atomic_and_checks_both_size_and_hash(tmp_path, mode):
    payload = b"immutable asset bytes"
    manifest = {
        "schema_version": 2 if mode == "version" else 1,
        "assets": [{"id": "asset", "download_url": "/files/assets/asset/map.json", "size_bytes": len(payload) + (1 if mode == "short" else -1 if mode == "long" else 0), "sha256": "0" * 64 if mode == "hash" else hashlib.sha256(payload).hexdigest()}],
    }
    def handler(request):
        return httpx.Response(200, json=manifest) if request.url.path.endswith("manifest") else httpx.Response(200, content=payload)
    destination = tmp_path / "map.json"
    if mode == "existing":
        destination.write_bytes(b"user data")
    with ReclaimerForgeClient("https://forge.test", transport=httpx.MockTransport(handler)) as client:
        if mode == "valid":
            DOWNLOAD.download(client, "listing", "version", "asset", destination)
            assert destination.read_bytes() == payload
        elif mode == "existing":
            with pytest.raises(FileExistsError):
                DOWNLOAD.download(client, "listing", "version", "asset", destination)
            assert destination.read_bytes() == b"user data"
        else:
            with pytest.raises(ValueError):
                DOWNLOAD.download(client, "listing", "version", "asset", destination)
            assert not destination.exists()
    assert not list(tmp_path.glob(".forge-*"))
