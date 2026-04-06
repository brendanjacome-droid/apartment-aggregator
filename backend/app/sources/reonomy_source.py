"""
Reonomy API Adapter (now part of Altus Group)
https://api.reonomy.com/v2/docs/

Reonomy provides data on 54M+ commercial parcels including:
- Ownership and entity resolution
- Debt/mortgage information
- Building violations
- Sales history

To use:
1. Sign up at https://www.reonomy.com/
2. Request API access (Starter ~$49/mo, Pro ~$249/mo)
3. Set REONOMY_API_KEY in your .env file
"""

from app.config import settings
from app.sources.base import DataSource


class ReonomySource(DataSource):
    name = "reonomy"
    display_name = "Reonomy (Altus Group)"
    requires_api_key = True

    @property
    def api_key(self):
        return settings.reonomy_api_key

    async def fetch_listings(self) -> list[dict]:
        if not self.is_configured:
            raise RuntimeError(
                "Reonomy API key not configured. Set REONOMY_API_KEY in .env. "
                "Sign up at https://www.reonomy.com/"
            )

        # TODO: Implement Reonomy API integration
        # Key endpoints:
        #   POST /v2/properties/search - search properties with filters
        #   GET /v2/properties/{id} - property details
        #   GET /v2/properties/{id}/ownership - ownership info
        #   GET /v2/properties/{id}/debt - mortgage/debt info
        #
        # Filter for asset_class: "Multifamily" or building_class containing apartment
        # Use geographic filters (state, city, zip)
        #
        # Example request:
        #   headers = {"Authorization": f"Bearer {self.api_key}"}
        #   response = await httpx.AsyncClient().post(
        #       "https://api.reonomy.com/v2/properties/search",
        #       headers=headers,
        #       json={
        #           "filters": {"asset_class": ["Multifamily"]},
        #           "location": {"state": "NY"},
        #           "page": 1, "per_page": 100
        #       }
        #   )

        raise NotImplementedError("Reonomy adapter not yet implemented - add API key and complete integration")
