import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings
from app.database import SessionLocal
from app.sources.registry import registry

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def fetch_all_sources():
    db = SessionLocal()
    try:
        for source in registry.list_sources():
            if source.is_configured:
                try:
                    result = await registry.fetch_from_source(source.name, db)
                    logger.info(f"Fetched from {source.name}: {result}")
                except Exception as e:
                    logger.error(f"Error fetching from {source.name}: {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        fetch_all_sources,
        "interval",
        hours=settings.fetch_interval_hours,
        id="fetch_all",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(f"Scheduler started. Fetching every {settings.fetch_interval_hours} hours.")
