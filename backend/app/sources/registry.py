from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Listing, DataSourceStatus, FetchLog
from app.sources.base import DataSource


class SourceRegistry:
    def __init__(self):
        self._sources: dict[str, DataSource] = {}

    def register(self, source: DataSource):
        self._sources[source.name] = source

    def get(self, name: str) -> DataSource | None:
        return self._sources.get(name)

    def list_sources(self) -> list[DataSource]:
        return list(self._sources.values())

    async def fetch_from_source(self, source_name: str, db: Session) -> dict:
        source = self._sources.get(source_name)
        if not source:
            raise ValueError(f"Unknown source: {source_name}")

        log = FetchLog(source_name=source_name)
        db.add(log)
        db.flush()

        try:
            raw_listings = await source.fetch_listings()
            new_count = 0
            updated_count = 0

            for data in raw_listings:
                existing = (
                    db.query(Listing)
                    .filter_by(external_id=data["external_id"], source_name=data["source_name"])
                    .first()
                )
                if existing:
                    for key, value in data.items():
                        if key not in ("external_id", "source_name") and value is not None:
                            setattr(existing, key, value)
                    existing.fetched_at = datetime.utcnow()
                    updated_count += 1
                else:
                    listing = Listing(**data)
                    db.add(listing)
                    new_count += 1

            # Update source status
            status = db.query(DataSourceStatus).filter_by(name=source_name).first()
            if not status:
                status = DataSourceStatus(name=source_name)
                db.add(status)

            status.last_fetch_at = datetime.utcnow()
            status.last_fetch_count = len(raw_listings)
            status.last_error = None
            status.total_listings = db.query(Listing).filter_by(source_name=source_name).count()

            log.finished_at = datetime.utcnow()
            log.listings_fetched = len(raw_listings)
            log.listings_new = new_count
            log.listings_updated = updated_count

            db.commit()

            return {
                "source": source_name,
                "fetched": len(raw_listings),
                "new": new_count,
                "updated": updated_count,
            }

        except Exception as e:
            log.finished_at = datetime.utcnow()
            log.error = str(e)

            status = db.query(DataSourceStatus).filter_by(name=source_name).first()
            if status:
                status.last_error = str(e)

            db.commit()
            raise


registry = SourceRegistry()
