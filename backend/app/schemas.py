from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ListingResponse(BaseModel):
    id: int
    external_id: str
    source_name: str
    title: str
    description: Optional[str] = None
    property_type: str = "multifamily"
    address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    country: str = "US"
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price: Optional[float] = None
    price_per_unit: Optional[float] = None
    num_units: Optional[int] = None
    num_floors: Optional[int] = None
    year_built: Optional[int] = None
    square_footage: Optional[int] = None
    cap_rate: Optional[float] = None
    noi: Optional[float] = None
    occupancy_rate: Optional[float] = None
    listing_url: Optional[str] = None
    image_urls: list[str] = []
    broker_name: Optional[str] = None
    broker_phone: Optional[str] = None
    broker_email: Optional[str] = None
    listed_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    fetched_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ListingSearchParams(BaseModel):
    q: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_units: Optional[int] = None
    max_units: Optional[int] = None
    min_cap_rate: Optional[float] = None
    max_cap_rate: Optional[float] = None
    source: Optional[str] = None
    sort_by: str = "fetched_at"
    sort_order: str = "desc"
    page: int = 1
    per_page: int = 20


class PaginatedListings(BaseModel):
    items: list[ListingResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class DataSourceResponse(BaseModel):
    name: str
    enabled: bool
    last_fetch_at: Optional[datetime] = None
    last_fetch_count: int = 0
    last_error: Optional[str] = None
    total_listings: int = 0

    model_config = {"from_attributes": True}


class StatsResponse(BaseModel):
    total_listings: int
    total_sources: int
    avg_price: Optional[float] = None
    avg_cap_rate: Optional[float] = None
    avg_units: Optional[float] = None
    by_region: dict[str, int] = {}
    by_country: dict[str, int] = {}
    by_source: dict[str, int] = {}
