import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Listing, DataSourceStatus
from app.schemas import (
    ListingResponse,
    PaginatedListings,
    DataSourceResponse,
    StatsResponse,
)
from app.sources.registry import registry

router = APIRouter(prefix="/api")


@router.get("/listings", response_model=PaginatedListings)
def search_listings(
    q: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_units: Optional[int] = None,
    max_units: Optional[int] = None,
    min_cap_rate: Optional[float] = None,
    max_cap_rate: Optional[float] = None,
    source: Optional[str] = None,
    sort_by: str = Query("fetched_at", pattern="^(price|num_units|cap_rate|fetched_at|listed_date|city|state)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Listing)

    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                Listing.title.ilike(search),
                Listing.city.ilike(search),
                Listing.state.ilike(search),
                Listing.address.ilike(search),
                Listing.description.ilike(search),
            )
        )

    if state:
        query = query.filter(Listing.state == state.upper())
    if city:
        query = query.filter(Listing.city.ilike(f"%{city}%"))
    if min_price is not None:
        query = query.filter(Listing.price >= min_price)
    if max_price is not None:
        query = query.filter(Listing.price <= max_price)
    if min_units is not None:
        query = query.filter(Listing.num_units >= min_units)
    if max_units is not None:
        query = query.filter(Listing.num_units <= max_units)
    if min_cap_rate is not None:
        query = query.filter(Listing.cap_rate >= min_cap_rate)
    if max_cap_rate is not None:
        query = query.filter(Listing.cap_rate <= max_cap_rate)
    if source:
        query = query.filter(Listing.source_name == source)

    total = query.count()

    sort_col = getattr(Listing, sort_by, Listing.fetched_at)
    if sort_order == "desc":
        query = query.order_by(sort_col.desc())
    else:
        query = query.order_by(sort_col.asc())

    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedListings(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=math.ceil(total / per_page) if total > 0 else 0,
    )


@router.get("/listings/{listing_id}", response_model=ListingResponse)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.get("/sources", response_model=list[DataSourceResponse])
def list_sources(db: Session = Depends(get_db)):
    sources = []
    for source in registry.list_sources():
        status = db.query(DataSourceStatus).filter_by(name=source.name).first()
        if status:
            sources.append(status)
        else:
            sources.append(
                DataSourceResponse(
                    name=source.name,
                    enabled=source.is_configured,
                    total_listings=0,
                )
            )
    return sources


@router.post("/sources/{source_name}/fetch")
async def fetch_source(source_name: str, db: Session = Depends(get_db)):
    source = registry.get(source_name)
    if not source:
        raise HTTPException(status_code=404, detail=f"Source '{source_name}' not found")
    if not source.is_configured:
        raise HTTPException(status_code=400, detail=f"Source '{source_name}' is not configured (missing API key)")
    result = await registry.fetch_from_source(source_name, db)
    return result


@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Listing).count()

    avg_price = db.query(func.avg(Listing.price)).filter(Listing.price.isnot(None)).scalar()
    avg_cap = db.query(func.avg(Listing.cap_rate)).filter(Listing.cap_rate.isnot(None)).scalar()
    avg_units = db.query(func.avg(Listing.num_units)).filter(Listing.num_units.isnot(None)).scalar()

    by_state_rows = (
        db.query(Listing.state, func.count(Listing.id))
        .filter(Listing.state.isnot(None))
        .group_by(Listing.state)
        .all()
    )
    by_state = {row[0]: row[1] for row in by_state_rows}

    by_source_rows = (
        db.query(Listing.source_name, func.count(Listing.id))
        .group_by(Listing.source_name)
        .all()
    )
    by_source = {row[0]: row[1] for row in by_source_rows}

    source_count = db.query(DataSourceStatus).count()

    return StatsResponse(
        total_listings=total,
        total_sources=source_count,
        avg_price=round(avg_price, 2) if avg_price else None,
        avg_cap_rate=round(avg_cap, 2) if avg_cap else None,
        avg_units=round(avg_units, 1) if avg_units else None,
        by_state=by_state,
        by_source=by_source,
    )
