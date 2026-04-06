"""
Montreal Open Data - Property Assessment Units

Provides property assessment data with CUBF use codes that can identify
apartment buildings. Includes dimensions, assessed values, registration numbers.

API: Available through Montreal's open data platform.
https://donnees.montreal.ca/
"""

import httpx

from app.sources.base import DataSource

# Montreal evaluation fonciere (property assessment) dataset
MONTREAL_API_URL = "https://donnees.montreal.ca/api/3/action/datastore_search"
# The resource ID for the evaluation fonciere dataset - may need updating
MONTREAL_RESOURCE_ID = "a0d4a830-ca63-4357-9a1e-4033025e6ee7"


class MontrealSource(DataSource):
    name = "montreal_opendata"
    display_name = "Montreal Open Data (Assessments)"

    async def fetch_listings(self) -> list[dict]:
        listings = []
        offset = 0
        limit = 100

        async with httpx.AsyncClient(timeout=60) as client:
            while True:
                resp = await client.get(
                    MONTREAL_API_URL,
                    params={
                        "id": MONTREAL_RESOURCE_ID,
                        "limit": limit,
                        "offset": offset,
                        # CUBF codes 1000-1999 are residential; 1300+ are apartments
                        "filters": '{"CUBF":"1300"}',
                    },
                )
                resp.raise_for_status()
                data = resp.json()

                if not data.get("success"):
                    # Resource ID may have changed; log and return what we have
                    if not listings:
                        raise RuntimeError(
                            "Montreal Open Data API returned unsuccessful response. "
                            "The resource ID may have changed. Check "
                            "https://donnees.montreal.ca/ for the current dataset."
                        )
                    break

                batch = data.get("result", {}).get("records", [])
                if not batch:
                    break

                for rec in batch:
                    addr_num = rec.get("NO_CIVIQUE", "")
                    street = rec.get("NOM_RUE", "")
                    full_addr = f"{addr_num} {street}".strip()
                    if not full_addr:
                        continue

                    val_terrain = rec.get("VALEUR_TERRAIN")
                    val_batiment = rec.get("VALEUR_BATIMENT")
                    try:
                        total_value = (float(val_terrain or 0)) + (float(val_batiment or 0))
                    except (ValueError, TypeError):
                        total_value = None

                    year_built = rec.get("ANNEE_CONSTRUCTION")
                    try:
                        year_built = int(year_built) if year_built else None
                    except (ValueError, TypeError):
                        year_built = None

                    num_units = rec.get("NB_LOGEMENTS") or rec.get("NOMBRE_LOGEMENTS")
                    try:
                        num_units = int(num_units) if num_units else None
                    except (ValueError, TypeError):
                        num_units = None

                    listings.append({
                        "external_id": f"montreal-{rec.get('ID_UEV', offset + len(listings))}",
                        "source_name": "montreal_opendata",
                        "title": f"Apartment Building at {full_addr}",
                        "description": (
                            f"Apartment building in Montreal. "
                            f"{f'Assessed value: ${total_value:,.0f}. ' if total_value else ''}"
                            f"{f'{num_units} units. ' if num_units else ''}"
                            f"{f'Built {year_built}. ' if year_built else ''}"
                            f"Data from Ville de Montreal Open Data."
                        ),
                        "property_type": "multifamily",
                        "address": full_addr,
                        "city": "Montreal",
                        "province_state": "QC",
                        "country": "CA",
                        "price": total_value if total_value and total_value > 0 else None,
                        "num_units": num_units,
                        "year_built": year_built,
                        "listing_url": "https://donnees.montreal.ca/",
                        "raw_data": rec,
                    })

                offset += limit
                if len(listings) >= 2000 or len(batch) < limit:
                    break

        return listings
