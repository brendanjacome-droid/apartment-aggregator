"""
CMHC (Canada Mortgage and Housing Corporation) Data Source

Provides rental market data for purpose-built apartment buildings (3+ units)
across Canada: vacancy rates, average rents, construction starts.

Data is published on the Open Government Portal and accessible via CSV downloads.
https://open.canada.ca/data/organization/cmhc-schl

Free, no API key required.
"""

import httpx

from app.sources.base import DataSource

# CMHC publishes data tables as CSV; we use the rental market survey summary
CMHC_RENTAL_MARKET_URL = (
    "https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadTbl/en/"
    "TV=34100133&outputType=csv"
)


class CmhcSource(DataSource):
    name = "cmhc"
    display_name = "CMHC Rental Market (Canada)"

    async def fetch_listings(self) -> list[dict]:
        # CMHC provides market-level data (vacancy rates, rents), not individual
        # property listings. This adapter fetches aggregate rental market stats
        # that can be used to enrich Canadian apartment listings with market context.
        #
        # For now, this is a placeholder. To fully implement:
        # 1. Download CMHC Rental Market Survey data tables from open.canada.ca
        # 2. Parse the CSV for vacancy rates and average rents by city/province
        # 3. Store as market intelligence records (not individual listings)
        #
        # The cmhc R package (https://mountainmath.github.io/cmhc/) wraps the
        # HMIP portal and can be used via rpy2 if deeper integration is needed.
        #
        # Key data available:
        #   - Vacancy rates by bedroom type and building size
        #   - Average rents by bedroom type
        #   - Rental universe (total units tracked)
        #   - Construction starts/completions for apartments

        raise NotImplementedError(
            "CMHC adapter provides market intelligence data (vacancy rates, rents), "
            "not individual listings. Integration coming soon."
        )
