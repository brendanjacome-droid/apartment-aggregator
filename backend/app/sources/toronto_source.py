"""
Toronto Open Data - Apartment Building Registration & Evaluation

Two key datasets:
1. Apartment Building Registration - registered apartment buildings in Toronto
2. Apartment Building Evaluation - building condition scores

API: CKAN-based, free, no API key required.
https://open.toronto.ca/dataset/apartment-building-evaluation/
"""

import httpx

from app.sources.base import DataSource

# Toronto Open Data CKAN API
CKAN_BASE = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
# Apartment Building Evaluation dataset
ABE_PACKAGE_ID = "apartment-building-evaluation"


class TorontoSource(DataSource):
    name = "toronto_opendata"
    display_name = "Toronto Open Data (Apartments)"

    async def fetch_listings(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as client:
            # Step 1: Get the dataset package to find resource IDs
            pkg_resp = await client.get(
                f"{CKAN_BASE}/api/3/action/package_show",
                params={"id": ABE_PACKAGE_ID},
            )
            pkg_resp.raise_for_status()
            pkg = pkg_resp.json()

            # Find the CSV or JSON datastore resource
            resources = pkg["result"]["resources"]
            datastore_resource = None
            for r in resources:
                if r.get("datastore_active"):
                    datastore_resource = r
                    break

            if not datastore_resource:
                raise RuntimeError("No active datastore resource found for Toronto apartment data")

            # Step 2: Fetch records from the datastore
            records = []
            offset = 0
            limit = 100
            while True:
                data_resp = await client.get(
                    f"{CKAN_BASE}/api/3/action/datastore_search",
                    params={
                        "id": datastore_resource["id"],
                        "limit": limit,
                        "offset": offset,
                    },
                )
                data_resp.raise_for_status()
                result = data_resp.json()["result"]
                batch = result.get("records", [])
                if not batch:
                    break
                records.extend(batch)
                offset += limit
                if len(records) >= 2000:
                    break

        # Step 3: Normalize into our listing format
        listings = []
        for i, rec in enumerate(records):
            addr = rec.get("SITE_ADDRESS") or rec.get("ADDRESS") or ""
            ward = rec.get("WARD") or ""
            score = rec.get("SCORE") or rec.get("CURRENT_BUILDING_EVAL_SCORE")
            year = rec.get("YEAR_BUILT")
            units = rec.get("CONFIRMED_UNITS") or rec.get("NO_OF_UNITS")
            storeys = rec.get("CONFIRMED_STOREYS") or rec.get("NO_OF_STOREYS")

            if not addr:
                continue

            try:
                num_units = int(units) if units else None
            except (ValueError, TypeError):
                num_units = None

            try:
                num_floors = int(storeys) if storeys else None
            except (ValueError, TypeError):
                num_floors = None

            try:
                year_built = int(year) if year else None
            except (ValueError, TypeError):
                year_built = None

            listings.append({
                "external_id": f"toronto-{rec.get('_id', i)}",
                "source_name": "toronto_opendata",
                "title": f"Apartment Building at {addr}",
                "description": (
                    f"Registered apartment building in Toronto, Ward {ward}. "
                    f"{f'Building evaluation score: {score}/100. ' if score else ''}"
                    f"{f'{num_units} units. ' if num_units else ''}"
                    f"{f'Built {year_built}. ' if year_built else ''}"
                    f"Data from City of Toronto Open Data."
                ),
                "property_type": "multifamily",
                "address": addr,
                "city": "Toronto",
                "province_state": "ON",
                "country": "CA",
                "postal_code": rec.get("POSTAL_CODE"),
                "latitude": rec.get("LATITUDE"),
                "longitude": rec.get("LONGITUDE"),
                "num_units": num_units,
                "num_floors": num_floors,
                "year_built": year_built,
                "listing_url": "https://open.toronto.ca/dataset/apartment-building-evaluation/",
                "raw_data": rec,
            })

        return listings
