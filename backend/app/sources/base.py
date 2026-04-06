from abc import ABC, abstractmethod
from typing import Optional


class DataSource(ABC):
    """Abstract base class for all apartment listing data sources."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this data source."""
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable name."""
        ...

    @property
    def requires_api_key(self) -> bool:
        return False

    @property
    def api_key(self) -> Optional[str]:
        return None

    @property
    def is_configured(self) -> bool:
        if self.requires_api_key:
            return self.api_key is not None and len(self.api_key) > 0
        return True

    @abstractmethod
    async def fetch_listings(self) -> list[dict]:
        """
        Fetch apartment building listings from this source.
        Returns a list of normalized listing dicts matching the Listing model fields.
        """
        ...
