"""
Vancouver Open Data - Property Tax Report (REST API)

Provides property tax data for all Vancouver parcels including zoning,
assessed land/improvement values, and property use.

API: Opendatasoft REST API, free, no API key required.
https://opendata.vancouver.ca/explore/dataset/property-tax-report/
"""

import httpx

from app.sources.base import DataSource

VANCOUVER_API_URL = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/property-tax-report/records"


class VancouverSource(DataSource):
    name = "vancouver_opendata"
    display_name = "Vancouver Open Data (Property Tax)"

    async def fetch_listings(self) -> list[dict]:
        listings = []
        offset = 0
        limit = 100

        async with httpx.AsyncClient(timeout=60) as client:
            while True:
                resp = await client.get(
                    VANCOUVER_API_URL,
                    params={
                        "where": "zoning_classification LIKE 'RM%' OR zoning_classification LIKE 'FM%' OR zoning_classification LIKE 'CD%'",
                        "limit": limit,
                        "offset": offset,
                        "order_by": "current_land_value DESC",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                batch = data.get("results", [])
                if not batch:
                    break

                for rec in batch:
                    addr = rec.get("to_civic_number", "")
                    street = rec.get("street_name", "")
                    full_addr = f"{addr} {street}".strip()
                    if not full_addr:
                        continue

                    land_val = rec.get("current_land_value")
                    impr_val = rec.get("current_improvement_value")
                    try:
                        total_value = (float(land_val or 0)) + (float(impr_val or 0))
                    except (ValueError, TypeError):
                        total_value = None

                    zoning = rec.get("zoning_classification", "")
                    year_built = rec.get("year_built")
                    try:
                        year_built = int(year_built) if year_built else None
                    except (ValueError, TypeError):
                        year_built = None

                    listings.append({
                        "external_id": f"vancouver-{rec.get('pid', offset + len(listings))}",
                        "source_name": "vancouver_opendata",
                        "title": f"Multi-Residential at {full_addr}",
                        "description": (
                            f"Multi-residential property in Vancouver, zoned {zoning}. "
                            f"{f'Total assessed value: ${total_value:,.0f}. ' if total_value else ''}"
                            f"{f'Built {year_built}. ' if year_built else ''}"
                            f"Data from City of Vancouver Open Data."
                        ),
                        "property_type": "multifamily",
                        "address": full_addr,
                        "city": "Vancouver",
                        "province_state": "BC",
                        "country": "CA",
                        "price": total_value if total_value and total_value > 0 else None,
                        "year_built": year_built,
                        "listing_url": "https://opendata.vancouver.ca/explore/dataset/property-tax-report/",
                        "raw_data": rec,
                    })

                offset += limit
                if len(listings) >= 2000 or len(batch) < limit:
                    break

        return listings
