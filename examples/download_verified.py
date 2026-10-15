"""Stream and verify one pinned asset; partner-api.md, synchronization downloads.

python examples/download_verified.py LISTING_ID VERSION_ID ASSET_ID output.json
Optionally set FORGE_DOWNLOAD_ORIGIN for the operator's separate /files host.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import tempfile
from pathlib import Path

from reclaimerforge import ReclaimerForgeClient


def download(client: ReclaimerForgeClient, listing_id: str, version_id: str, asset_id: str, destination: Path) -> None:
    """Install verified bytes without overwriting an existing destination."""
    manifest = client.listings.release_manifest(listing_id, version_id)
    if manifest["schema_version"] != 1:
        raise ValueError("Unsupported manifest schema version")
    asset = next(a for a in manifest["assets"] if a["id"] == asset_id)
    digest, received = hashlib.sha256(), 0
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".forge-", delete=False) as target:
            temporary = Path(target.name)
            with client.stream("GET", asset["download_url"]) as response:
                if response.status_code != 200:
                    raise ValueError("Expected a complete asset response")
                for chunk in response.iter_bytes():
                    received += len(chunk)
                    if received > asset["size_bytes"]:
                        raise ValueError("Download exceeds pinned manifest size")
                    target.write(chunk)
                    digest.update(chunk)
            if received != asset["size_bytes"] or digest.hexdigest() != asset["sha256"]:
                raise ValueError("Pinned asset size or SHA-256 mismatch")
            target.flush()
            os.fsync(target.fileno())
        # Same-directory hard link atomically refuses to overwrite another file.
        os.link(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    """Download one exact asset to an explicit local path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("listing_id")
    parser.add_argument("version_id")
    parser.add_argument("asset_id")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    cdn = os.environ.get("FORGE_DOWNLOAD_ORIGIN")
    with ReclaimerForgeClient(os.environ["FORGE_URL"], api_key=os.environ["FORGE_API_KEY"], download_origins=(cdn,) if cdn else ()) as client:
        download(client, args.listing_id, args.version_id, args.asset_id, args.output)


if __name__ == "__main__":
    main()
