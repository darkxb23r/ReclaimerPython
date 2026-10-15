"""Upload/resume one draft asset; partner-api.md, Uploading with a key.

python examples/upload_release.py map.json --title Arena
python examples/upload_release.py map.json --resume UPLOAD_ID --listing LISTING_ID --version VERSION_ID
Add --publish to explicitly publish the completed draft.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from reclaimerforge import ReclaimerForgeClient


def main() -> None:
    """Use server progress to avoid appending accepted chunks twice."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--title", default="New listing")
    parser.add_argument("--listing")
    parser.add_argument("--version")
    parser.add_argument("--resume", help="Your own existing upload session ID")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--compatibility", type=Path, help="Full draft compatibility JSON; asset IDs must match this release")
    args = parser.parse_args()
    if bool(args.listing) != bool(args.version) or (args.resume and not args.listing):
        parser.error("--listing and --version must be paired; --resume requires both")
    with args.file.open("rb") as source, ReclaimerForgeClient(os.environ["FORGE_URL"], api_key=os.environ["FORGE_API_KEY"]) as client:
        if args.listing:
            listing_id, version_id = args.listing, args.version
        else:
            listing = client.listings.new_listing(body={"title": args.title, "version_label": "1.0"})
            listing_id = listing["id"]
            version_id = listing["versions"][0]["id"]
        if args.resume:
            upload = client.files.upload_status(args.resume)
        else:
            upload = client.listings.new_asset_upload(listing_id, version_id, body={"original_filename": args.file.name, "file_size": os.fstat(source.fileno()).st_size, "file_type": "auto"})
        print("listing:", listing_id, "version:", version_id, "upload:", upload["id"], flush=True)
        print("Resume only with the identical source bytes; the API does not check prior chunks against a local file.", flush=True)
        if os.fstat(source.fileno()).st_size != upload["expected_size"]:
            raise ValueError("Local file size differs from the upload session")
        source.seek(upload["received_size"])
        while upload["received_size"] < upload["expected_size"]:
            expected = min(upload["chunk_size"], upload["expected_size"] - upload["received_size"])
            chunk = source.read(expected)
            if len(chunk) != expected:
                raise ValueError("Source file changed or ended before expected size")
            upload = client.files.upload_chunk(upload["id"], upload["next_chunk_index"], content=chunk)
            # Duplicate accepted chunks can report a later offset during recovery.
            source.seek(upload["received_size"])
        asset = client.listings.finish_asset_upload(upload["id"])
        print("validated asset:", asset["id"])
        if args.compatibility:
            client.listings.edit_version_compatibility(listing_id, version_id, body=json.loads(args.compatibility.read_text()))
        # Leave compatibility unknown unless the author supplies actual claims.
        if args.publish:
            result = client.listings.publish_listing_version(listing_id, version_id)
            print("published:", result["id"])
        else:
            print("Draft retained. Set compatibility and bundles before publishing if applicable.")


if __name__ == "__main__":
    main()
