import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database import init_db, SessionLocal
from app.api.routes import router
from app.sources.registry import registry
from app.sources.mock_source import MockSource
from app.sources.attom_source import AttomSource
from app.sources.reonomy_source import ReonomySource
from app.sources.estated_source import EstatedSource
from app.sources.toronto_source import TorontoSource
from app.sources.calgary_source import CalgarySource
from app.sources.edmonton_source import EdmontonSource
from app.sources.vancouver_source import VancouverSource
from app.sources.montreal_source import MontrealSource
from app.sources.cmhc_source import CmhcSource
from app.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()

    # Register data sources
    registry.register(MockSource(count=300))
    registry.register(AttomSource())
    registry.register(ReonomySource())
    registry.register(EstatedSource())
    # Canadian sources (free, no API key needed)
    registry.register(TorontoSource())
    registry.register(CalgarySource())
    registry.register(EdmontonSource())
    registry.register(VancouverSource())
    registry.register(MontrealSource())
    registry.register(CmhcSource())

    # Seed mock data on first run
    db = SessionLocal()
    try:
        from app.models import Listing
        if db.query(Listing).count() == 0:
            logger.info("No listings found. Seeding mock data...")
            await registry.fetch_from_source("mock", db)
            logger.info("Mock data seeded.")
    finally:
        db.close()

    start_scheduler()

    yield

    # Shutdown
    from app.scheduler import scheduler
    scheduler.shutdown(wait=False)


app = FastAPI(
    title="Apartment Building Aggregator",
    description="Aggregates apartment building for-sale listings from multiple CRE data sources",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Serve React frontend static files in production
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the React SPA for all non-API routes."""
        file_path = STATIC_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")
