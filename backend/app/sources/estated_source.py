"""
Estated API Adapter
https://estated.com/developers/docs

Estated provides property data including:
- Property attributes (bedrooms, bathrooms, square footage, etc.)
- Ownership information
- Valuations and assessments
- Deed/mortgage history

To use:
1. Sign up at https://estated.com/developers
2. Get your API token
3. Set ESTATED_API_TOKEN in your .env file

Pricing: Usage-based, self-service plans available.
"""

from app.config import settings
from app.sources.base import DataSource


class EstatedSource(DataSource):
    name = "estated"
    display_name = "Estated"
    requires_api_key = True

    @property
    def api_key(self):
        return settings.estated_api_token

    async def fetch_listings(self) -> list[dict]:
        if not self.is_configured:
            raise RuntimeError(
                "Estated API token not configured. Set ESTATED_API_TOKEN in .env. "
                "Sign up at https://estated.com/developers"
            )

        # TODO: Implement Estated API integration
        # Key endpoints:
        #   GET /v4/properties - property lookup by address
        #   GET /v4/properties/fips - lookup by FIPS code
        #
        # Estated is primarily a property-data enrichment API (lookup by address),
        # not a search/listing API. Best used to enrich listings from other sources.
        #
        # Example request:
        #   response = await httpx.AsyncClient().get(
        #       "https://apis.estated.com/v4/properties",
        #       params={
        #           "token": self.api_key,
        #           "combined_address": "123 Main St, New York, NY 10001"
        #       }
        #   )

        raise NotImplementedError("Estated adapter not yet implemented - add API key and complete integration")
