"""
ATTOM Data API Adapter
https://api.gateway.attomdata.com/propertyapi/v1.0.0/

ATTOM provides data on 158M+ US properties including:
- Property characteristics, tax/assessment data
- Sales history and transaction data
- Foreclosure and pre-foreclosure data
- Hazard risk data

To use:
1. Sign up at https://api.gateway.attomdata.com/
2. Get your API key
3. Set ATTOM_API_KEY in your .env file

Pricing: Tiered/scalable, self-service plans available.
"""

from app.config import settings
from app.sources.base import DataSource


class AttomSource(DataSource):
    name = "attom"
    display_name = "ATTOM Data"
    requires_api_key = True

    @property
    def api_key(self):
        return settings.attom_api_key

    async def fetch_listings(self) -> list[dict]:
        if not self.is_configured:
            raise RuntimeError(
                "ATTOM API key not configured. Set ATTOM_API_KEY in .env. "
                "Sign up at https://api.gateway.attomdata.com/"
            )

        # TODO: Implement ATTOM API integration
        # Key endpoints:
        #   GET /property/snapshot - property details by address/ID
        #   GET /sale/snapshot - recent sales data
        #   GET /property/expandedprofile - detailed property profiles
        #
        # Filter for property_type containing "multifamily" or "apartment"
        # Use geographic bounding box or postal code searches
        #
        # Example request:
        #   headers = {"apikey": self.api_key, "Accept": "application/json"}
        #   response = await httpx.AsyncClient().get(
        #       "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/snapshot",
        #       headers=headers,
        #       params={"postalcode": "10001", "propertytype": "APARTMENT"}
        #   )

        raise NotImplementedError("ATTOM adapter not yet implemented - add API key and complete integration")
