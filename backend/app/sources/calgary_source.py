"""
Calgary Open Data - Property Assessments (SODA API)

Provides property assessment data for ~617K properties in Calgary including
multi-residential zones (M-C1, M-C2) with 60K+ units.

API: Socrata SODA API, free, no API key required (throttled without app token).
https://data.calgary.ca/Government/Current-Year-Property-Assessments-Parcel-/4bsw-nn7w
"""

import httpx

from app.sources.base import DataSource

CALGARY_DATASET_URL = "https://data.calgary.ca/resource/4bsw-nn7w.json"


class CalgarySource(DataSource):
    name = "calgary_opendata"
    display_name = "Calgary Open Data (Assessments)"

    async def fetch_listings(self) -> list[dict]:
        listings = []
        offset = 0
        limit = 1000

        async with httpx.AsyncClient(timeout=60) as client:
            while True:
                resp = await client.get(
                    CALGARY_DATASET_URL,
                    params={
                        "$where": "assess_class = 'RA'",  # Residential Apartment
                        "$limit": limit,
                        "$offset": offset,
                        "$order": "assessed_value DESC",
                    },
                )
                resp.raise_for_status()
                batch = resp.json()
                if not batch:
                    break

                for rec in batch:
                    addr = rec.get("address") or rec.get("location_address") or ""
                    if not addr:
                        continue

                    assessed_value = rec.get("assessed_value")
                    try:
                        price = float(assessed_value) if assessed_value else None
                    except (ValueError, TypeError):
                        price = None

                    community = rec.get("comm_name") or rec.get("community_name") or ""

                    listings.append({
                        "external_id": f"calgary-{rec.get('roll_number', offset + len(listings))}",
                        "source_name": "calgary_opendata",
                        "title": f"Multi-Residential Property at {addr}",
                        "description": (
                            f"Multi-residential property in Calgary"
                            f"{f', {community} community' if community else ''}. "
                            f"{f'Assessed value: ${price:,.0f}. ' if price else ''}"
                            f"Data from City of Calgary Open Data."
                        ),
                        "property_type": "multifamily",
                        "address": addr,
                        "city": "Calgary",
                        "province_state": "AB",
                        "country": "CA",
                        "price": price,
                        "listing_url": "https://data.calgary.ca/Government/Current-Year-Property-Assessments-Parcel-/4bsw-nn7w",
                        "raw_data": rec,
                    })

                offset += limit
                if len(listings) >= 2000 or len(batch) < limit:
                    break

        return listings
