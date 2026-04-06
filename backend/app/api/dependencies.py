from app.database import get_db

# Re-export for convenience; add auth, rate limiting, etc. here later
__all__ = ["get_db"]
