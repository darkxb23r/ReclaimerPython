"""List current catalog pages asynchronously; partner-api.md, discovery."""
import asyncio
import os

from reclaimerforge import AsyncReclaimerForgeClient


async def main() -> None:
    """Read all pages and deduplicate the live catalog by stable IDs."""
    seen: set[str] = set()
    async with AsyncReclaimerForgeClient(os.environ["FORGE_URL"], api_key=os.environ["FORGE_API_KEY"]) as client:
        page = 1
        while True:
            result = await client.listings.public_listings(page=page, page_size=100, sort="latest")
            for listing in result["items"]:
                if listing["id"] not in seen:
                    seen.add(listing["id"])
                    print(listing["id"], listing["title"])
            if page >= result["pages"]:
                break
            page += 1


if __name__ == "__main__":
    asyncio.run(main())
