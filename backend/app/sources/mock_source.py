import random
from datetime import datetime, timedelta
from faker import Faker

from app.sources.base import DataSource

fake = Faker()

US_STATES_WITH_COORDS = {
    "AL": (32.36, -86.30), "AK": (63.59, -154.49), "AZ": (34.05, -111.09),
    "AR": (35.20, -91.83), "CA": (36.78, -119.42), "CO": (39.55, -105.78),
    "CT": (41.60, -72.76), "DE": (38.91, -75.53), "FL": (27.66, -81.52),
    "GA": (32.16, -82.90), "HI": (19.90, -155.58), "ID": (44.07, -114.74),
    "IL": (40.63, -89.40), "IN": (40.27, -86.13), "IA": (41.88, -93.10),
    "KS": (39.01, -98.48), "KY": (37.67, -84.67), "LA": (31.17, -91.87),
    "ME": (45.37, -69.45), "MD": (39.05, -76.64), "MA": (42.41, -71.38),
    "MI": (44.31, -85.60), "MN": (46.73, -94.69), "MS": (32.35, -89.40),
    "MO": (37.96, -91.83), "MT": (46.88, -110.36), "NE": (41.49, -99.90),
    "NV": (38.80, -116.42), "NH": (43.19, -71.57), "NJ": (40.06, -74.41),
    "NM": (34.52, -105.87), "NY": (43.30, -74.22), "NC": (35.76, -79.02),
    "ND": (47.55, -101.00), "OH": (40.42, -82.91), "OK": (35.47, -97.52),
    "OR": (43.80, -120.55), "PA": (41.20, -77.19), "RI": (41.58, -71.48),
    "SC": (33.84, -81.16), "SD": (43.97, -99.90), "TN": (35.52, -86.58),
    "TX": (31.97, -99.90), "UT": (39.32, -111.09), "VT": (44.56, -72.58),
    "VA": (37.43, -78.66), "WA": (47.75, -120.74), "WV": (38.60, -80.45),
    "WI": (43.78, -88.79), "WY": (43.08, -107.29), "DC": (38.91, -77.04),
}

CA_PROVINCES_WITH_COORDS = {
    "ON": (43.65, -79.38), "QC": (45.50, -73.57), "BC": (49.28, -123.12),
    "AB": (51.05, -114.07), "MB": (49.90, -97.14), "SK": (50.45, -104.62),
    "NS": (44.65, -63.57), "NB": (45.96, -66.64), "NL": (47.57, -52.71),
    "PE": (46.24, -63.13),
}

MAJOR_CITIES = {
    "NY": ["New York", "Brooklyn", "Queens", "Bronx", "Buffalo"],
    "CA": ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "Oakland"],
    "TX": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth"],
    "FL": ["Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale"],
    "IL": ["Chicago", "Aurora", "Naperville", "Evanston", "Schaumburg"],
    "PA": ["Philadelphia", "Pittsburgh", "Allentown", "Reading", "Bethlehem"],
    "OH": ["Columbus", "Cleveland", "Cincinnati", "Dayton", "Akron"],
    "GA": ["Atlanta", "Savannah", "Augusta", "Macon", "Athens"],
    "NC": ["Charlotte", "Raleigh", "Durham", "Greensboro", "Winston-Salem"],
    "MI": ["Detroit", "Grand Rapids", "Ann Arbor", "Lansing", "Kalamazoo"],
    "NJ": ["Newark", "Jersey City", "Hoboken", "Trenton", "Camden"],
    "VA": ["Richmond", "Virginia Beach", "Arlington", "Norfolk", "Alexandria"],
    "WA": ["Seattle", "Tacoma", "Spokane", "Bellevue", "Redmond"],
    "MA": ["Boston", "Cambridge", "Worcester", "Springfield", "Lowell"],
    "AZ": ["Phoenix", "Tucson", "Scottsdale", "Mesa", "Tempe"],
    "CO": ["Denver", "Colorado Springs", "Boulder", "Aurora", "Lakewood"],
    "TN": ["Nashville", "Memphis", "Knoxville", "Chattanooga", "Clarksville"],
    "MD": ["Baltimore", "Bethesda", "Silver Spring", "Rockville", "Columbia"],
    "MN": ["Minneapolis", "St. Paul", "Rochester", "Duluth", "Bloomington"],
    "MO": ["St. Louis", "Kansas City", "Springfield", "Columbia", "Independence"],
}

CA_MAJOR_CITIES = {
    "ON": ["Toronto", "Ottawa", "Mississauga", "Hamilton", "London", "Brampton", "Kitchener"],
    "QC": ["Montreal", "Quebec City", "Laval", "Gatineau", "Longueuil", "Sherbrooke"],
    "BC": ["Vancouver", "Surrey", "Burnaby", "Richmond", "Victoria", "Kelowna"],
    "AB": ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "St. Albert"],
    "MB": ["Winnipeg", "Brandon", "Steinbach"],
    "SK": ["Saskatoon", "Regina", "Prince Albert"],
    "NS": ["Halifax", "Dartmouth", "Sydney"],
    "NB": ["Moncton", "Saint John", "Fredericton"],
    "NL": ["St. John's", "Mount Pearl", "Corner Brook"],
    "PE": ["Charlottetown", "Summerside"],
}

BUILDING_NAMES = [
    "The {adj} at {street}",
    "{street} Apartments",
    "{adj} {noun} Residences",
    "The {noun}",
    "{street} Lofts",
    "{adj} Place Apartments",
    "The {adj} {noun}",
    "{noun} Tower",
    "{street} Commons",
]

ADJS = [
    "Grand", "Summit", "Park", "Metro", "Urban", "Vista", "Horizon", "Pinnacle",
    "Legacy", "Evergreen", "Sterling", "Crown", "Pacific", "Atlantic", "Harbor",
    "Riverview", "Lakeside", "Highland", "Midtown", "Downtown",
]

NOUNS = [
    "Terrace", "Gardens", "Heights", "Manor", "Pointe", "Square", "Court",
    "Village", "Landing", "Crossing", "Ridge", "Commons", "Place", "Park",
]

PLACEHOLDER_IMAGES = [
    "https://placehold.co/800x600/2563eb/white?text=Apartment+Building",
    "https://placehold.co/800x600/059669/white?text=Multifamily+Complex",
    "https://placehold.co/800x600/7c3aed/white?text=Residential+Tower",
    "https://placehold.co/800x600/dc2626/white?text=Garden+Apartments",
    "https://placehold.co/800x600/d97706/white?text=Luxury+Apartments",
]


def _generate_building_name() -> str:
    template = random.choice(BUILDING_NAMES)
    return template.format(
        adj=random.choice(ADJS),
        noun=random.choice(NOUNS),
        street=fake.street_name(),
    )


def _generate_listing(idx: int) -> dict:
    # 30% chance of Canadian listing
    is_canadian = random.random() < 0.3

    if is_canadian:
        country = "CA"
        region = random.choice(list(CA_PROVINCES_WITH_COORDS.keys()))
        base_lat, base_lon = CA_PROVINCES_WITH_COORDS[region]
        cities = CA_MAJOR_CITIES.get(region, [fake.city()])
        postal_code = fake.bothify("?#? #?#").upper()
        high_cost_regions = ("ON", "BC")
        low_cost_regions = ("NB", "NL", "PE", "SK")
    else:
        country = "US"
        region = random.choice(list(US_STATES_WITH_COORDS.keys()))
        base_lat, base_lon = US_STATES_WITH_COORDS[region]
        cities = MAJOR_CITIES.get(region, [fake.city()])
        postal_code = fake.zipcode()
        high_cost_regions = ("NY", "CA", "MA", "DC", "WA", "CO")
        low_cost_regions = ("MS", "AR", "WV", "AL")

    lat = base_lat + random.uniform(-1.5, 1.5)
    lon = base_lon + random.uniform(-1.5, 1.5)
    city = random.choice(cities)

    num_units = random.choice([4, 6, 8, 10, 12, 16, 20, 24, 30, 40, 50, 60, 80, 100, 150, 200, 300])
    num_floors = max(1, num_units // random.randint(4, 12))
    year_built = random.randint(1950, 2024)
    sqft_per_unit = random.randint(600, 1200)
    square_footage = num_units * sqft_per_unit

    base_price_per_unit = random.randint(50_000, 250_000)
    if region in high_cost_regions:
        base_price_per_unit = int(base_price_per_unit * random.uniform(1.3, 2.5))
    if region in low_cost_regions:
        base_price_per_unit = int(base_price_per_unit * random.uniform(0.5, 0.8))

    price = num_units * base_price_per_unit
    price_per_unit = price / num_units

    cap_rate = round(random.uniform(3.5, 10.0), 2)
    noi = round(price * (cap_rate / 100), 2)
    occupancy = round(random.uniform(82, 99), 1)

    listed_date = datetime.now() - timedelta(days=random.randint(1, 180))

    name = _generate_building_name()

    return {
        "external_id": f"mock-{idx:05d}",
        "source_name": "mock",
        "title": name,
        "description": (
            f"{num_units}-unit {['garden-style', 'mid-rise', 'high-rise', 'walk-up', 'townhome-style'][random.randint(0,4)]} "
            f"apartment complex built in {year_built}. Located in {city}, {region}. "
            f"Currently {occupancy}% occupied with strong rental demand. "
            f"{'Value-add opportunity with potential for rent increases.' if cap_rate > 6 else 'Stabilized asset with consistent cash flow.'} "
            f"{'Recently renovated.' if year_built > 2015 or random.random() > 0.7 else ''}"
        ),
        "property_type": "multifamily",
        "address": fake.street_address(),
        "city": city,
        "province_state": region,
        "country": country,
        "postal_code": postal_code,
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "price": round(price, 2),
        "price_per_unit": round(price_per_unit, 2),
        "num_units": num_units,
        "num_floors": num_floors,
        "year_built": year_built,
        "square_footage": square_footage,
        "cap_rate": cap_rate,
        "noi": noi,
        "occupancy_rate": occupancy,
        "listing_url": f"https://example.com/listing/mock-{idx:05d}",
        "image_urls": random.sample(PLACEHOLDER_IMAGES, k=random.randint(1, 3)),
        "broker_name": fake.name(),
        "broker_phone": fake.phone_number(),
        "broker_email": fake.email(),
        "listed_date": listed_date,
        "updated_date": listed_date + timedelta(days=random.randint(0, 14)),
    }


class MockSource(DataSource):
    name = "mock"
    display_name = "Mock Data (Demo)"

    def __init__(self, count: int = 250):
        self._count = count

    async def fetch_listings(self) -> list[dict]:
        return [_generate_listing(i) for i in range(self._count)]
