from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./apartment_aggregator.db"
    port: int = 8000
    cors_origins: list[str] = ["*"]

    # Data source API keys (add yours when ready)
    attom_api_key: Optional[str] = None
    reonomy_api_key: Optional[str] = None
    estated_api_token: Optional[str] = None
    propertyshark_api_key: Optional[str] = None

    # Scheduler
    fetch_interval_hours: int = 6

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
