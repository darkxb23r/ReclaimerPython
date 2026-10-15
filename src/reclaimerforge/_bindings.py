"""Generated resource bindings for IDE autocomplete."""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .client import ReclaimerForgeClient, AsyncReclaimerForgeClient
from typing import cast
from . import resources

class ResourceBindings:
    def _bind_resources(self) -> None:
        self.admin_announcement: resources.AdminAnnouncement = resources.AdminAnnouncement(cast("ReclaimerForgeClient", self))
        self.admin_api_activity: resources.AdminApiActivity = resources.AdminApiActivity(cast("ReclaimerForgeClient", self))
        self.admin_audit: resources.AdminAudit = resources.AdminAudit(cast("ReclaimerForgeClient", self))
        self.admin_favourites: resources.AdminFavourites = resources.AdminFavourites(cast("ReclaimerForgeClient", self))
        self.admin_listings: resources.AdminListings = resources.AdminListings(cast("ReclaimerForgeClient", self))
        self.admin_metrics: resources.AdminMetrics = resources.AdminMetrics(cast("ReclaimerForgeClient", self))
        self.admin_ratings: resources.AdminRatings = resources.AdminRatings(cast("ReclaimerForgeClient", self))
        self.admin_users: resources.AdminUsers = resources.AdminUsers(cast("ReclaimerForgeClient", self))
        self.auth: resources.Auth = resources.Auth(cast("ReclaimerForgeClient", self))
        self.collaboration: resources.Collaboration = resources.Collaboration(cast("ReclaimerForgeClient", self))
        self.developer: resources.Developer = resources.Developer(cast("ReclaimerForgeClient", self))
        self.documentation: resources.Documentation = resources.Documentation(cast("ReclaimerForgeClient", self))
        self.downloads: resources.Downloads = resources.Downloads(cast("ReclaimerForgeClient", self))
        self.favourites: resources.Favourites = resources.Favourites(cast("ReclaimerForgeClient", self))
        self.files: resources.Files = resources.Files(cast("ReclaimerForgeClient", self))
        self.health: resources.Health = resources.Health(cast("ReclaimerForgeClient", self))
        self.listings: resources.Listings = resources.Listings(cast("ReclaimerForgeClient", self))
        self.ratings: resources.Ratings = resources.Ratings(cast("ReclaimerForgeClient", self))
        self.user: resources.User = resources.User(cast("ReclaimerForgeClient", self))
        self.users: resources.Users = resources.Users(cast("ReclaimerForgeClient", self))
        self.website: resources.Website = resources.Website(cast("ReclaimerForgeClient", self))

class AsyncResourceBindings:
    def _bind_resources(self) -> None:
        self.admin_announcement: resources.AsyncAdminAnnouncement = resources.AsyncAdminAnnouncement(cast("AsyncReclaimerForgeClient", self))
        self.admin_api_activity: resources.AsyncAdminApiActivity = resources.AsyncAdminApiActivity(cast("AsyncReclaimerForgeClient", self))
        self.admin_audit: resources.AsyncAdminAudit = resources.AsyncAdminAudit(cast("AsyncReclaimerForgeClient", self))
        self.admin_favourites: resources.AsyncAdminFavourites = resources.AsyncAdminFavourites(cast("AsyncReclaimerForgeClient", self))
        self.admin_listings: resources.AsyncAdminListings = resources.AsyncAdminListings(cast("AsyncReclaimerForgeClient", self))
        self.admin_metrics: resources.AsyncAdminMetrics = resources.AsyncAdminMetrics(cast("AsyncReclaimerForgeClient", self))
        self.admin_ratings: resources.AsyncAdminRatings = resources.AsyncAdminRatings(cast("AsyncReclaimerForgeClient", self))
        self.admin_users: resources.AsyncAdminUsers = resources.AsyncAdminUsers(cast("AsyncReclaimerForgeClient", self))
        self.auth: resources.AsyncAuth = resources.AsyncAuth(cast("AsyncReclaimerForgeClient", self))
        self.collaboration: resources.AsyncCollaboration = resources.AsyncCollaboration(cast("AsyncReclaimerForgeClient", self))
        self.developer: resources.AsyncDeveloper = resources.AsyncDeveloper(cast("AsyncReclaimerForgeClient", self))
        self.documentation: resources.AsyncDocumentation = resources.AsyncDocumentation(cast("AsyncReclaimerForgeClient", self))
        self.downloads: resources.AsyncDownloads = resources.AsyncDownloads(cast("AsyncReclaimerForgeClient", self))
        self.favourites: resources.AsyncFavourites = resources.AsyncFavourites(cast("AsyncReclaimerForgeClient", self))
        self.files: resources.AsyncFiles = resources.AsyncFiles(cast("AsyncReclaimerForgeClient", self))
        self.health: resources.AsyncHealth = resources.AsyncHealth(cast("AsyncReclaimerForgeClient", self))
        self.listings: resources.AsyncListings = resources.AsyncListings(cast("AsyncReclaimerForgeClient", self))
        self.ratings: resources.AsyncRatings = resources.AsyncRatings(cast("AsyncReclaimerForgeClient", self))
        self.user: resources.AsyncUser = resources.AsyncUser(cast("AsyncReclaimerForgeClient", self))
        self.users: resources.AsyncUsers = resources.AsyncUsers(cast("AsyncReclaimerForgeClient", self))
        self.website: resources.AsyncWebsite = resources.AsyncWebsite(cast("AsyncReclaimerForgeClient", self))

