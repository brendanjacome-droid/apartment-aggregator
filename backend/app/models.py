from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), nullable=False)
    source_name = Column(String(100), nullable=False)

    title = Column(String(500), nullable=False)
    description = Column(Text)
    property_type = Column(String(100), default="multifamily")

    address = Column(String(500))
    city = Column(String(200))
    state = Column(String(2))
    zip_code = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)

    price = Column(Float)
    price_per_unit = Column(Float)

    num_units = Column(Integer)
    num_floors = Column(Integer)
    year_built = Column(Integer)
    square_footage = Column(Integer)

    cap_rate = Column(Float)
    noi = Column(Float)
    occupancy_rate = Column(Float)

    listing_url = Column(String(1000))
    image_urls = Column(JSON, default=list)

    broker_name = Column(String(200))
    broker_phone = Column(String(50))
    broker_email = Column(String(200))

    listed_date = Column(DateTime)
    updated_date = Column(DateTime)
    fetched_at = Column(DateTime, server_default=func.now())

    raw_data = Column(JSON, default=dict)

    __table_args__ = (
        UniqueConstraint("external_id", "source_name", name="uq_listing_source"),
    )


class DataSourceStatus(Base):
    __tablename__ = "data_source_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    enabled = Column(Integer, default=1)
    last_fetch_at = Column(DateTime)
    last_fetch_count = Column(Integer, default=0)
    last_error = Column(Text)
    total_listings = Column(Integer, default=0)


class FetchLog(Base):
    __tablename__ = "fetch_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String(100), nullable=False)
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime)
    listings_fetched = Column(Integer, default=0)
    listings_new = Column(Integer, default=0)
    listings_updated = Column(Integer, default=0)
    error = Column(Text)
