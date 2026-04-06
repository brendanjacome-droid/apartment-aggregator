"""
Edmonton Open Data - Property Assessment Data (SODA API)

Provides property assessment data for ~448K properties in Edmonton
with tax class and assessed values.

API: Socrata SODA API, free, no API key required.
https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg
"""

import httpx

from app.sources.base import DataSource

EDMONTON_DATASET_URL = "https://data.edmonton.ca/resource/q7d6-ambg.json"


class EdmontonSource(DataSource):
    name = "edmonton_opendata"
    display_name = "Edmonton Open Data (Assessments)"

    async def fetch_listings(self) -> list[dict]:
        listings = []
        offset = 0
        limit = 1000

        async with httpx.AsyncClient(timeout=60) as client:
            while True:
                resp = await client.get(
                    EDMONTON_DATASET_URL,
                    params={
                        "$where": "mill_class_description LIKE '%Multi%' OR mill_class_description LIKE '%Apartment%'",
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
                    addr = rec.get("house_number", "") + " " + rec.get("street_name", "")
                    addr = addr.strip()
                    if not addr:
                        addr = rec.get("legal_description", "Unknown")

                    assessed_value = rec.get("assessed_value")
                    try:
                        price = float(assessed_value) if assessed_value else None
                    except (ValueError, TypeError):
                        price = None

                    neighbourhood = rec.get("neighbourhood") or ""
                    year_built = rec.get("year_built")
                    try:
                        year_built = int(year_built) if year_built else None
                    except (ValueError, TypeError):
                        year_built = None

                    listings.append({
                        "external_id": f"edmonton-{rec.get('account_number', offset + len(listings))}",
                        "source_name": "edmonton_opendata",
                        "title": f"Multi-Residential Property at {addr}",
                        "description": (
                            f"Multi-residential property in Edmonton"
                            f"{f', {neighbourhood}' if neighbourhood else ''}. "
                            f"{f'Assessed value: ${price:,.0f}. ' if price else ''}"
                            f"{f'Built {year_built}. ' if year_built else ''}"
                            f"Data from City of Edmonton Open Data."
                        ),
                        "property_type": "multifamily",
                        "address": addr,
                        "city": "Edmonton",
                        "province_state": "AB",
                        "country": "CA",
                        "price": price,
                        "year_built": year_built,
                        "latitude": rec.get("latitude"),
                        "longitude": rec.get("longitude"),
                        "listing_url": "https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg",
                        "raw_data": rec,
                    })

                offset += limit
                if len(listings) >= 2000 or len(batch) < limit:
                    break

        return listings
