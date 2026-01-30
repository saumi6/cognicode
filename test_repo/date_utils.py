"""Date and time utilities."""
from datetime import datetime, timedelta

def get_current_timestamp() -> str:
    """Return ISO format timestamp."""
    return datetime.utcnow().isoformat()

def is_expired(expiry_date_str: str) -> bool:
    """Check if a date string is in the past."""
    try:
        exp = datetime.fromisoformat(expiry_date_str)
        return exp < datetime.utcnow()
    except ValueError:
        return True

def add_days(date_str: str, days: int) -> str:
    """Add days to an ISO date string."""
    dt = datetime.fromisoformat(date_str)
    return (dt + timedelta(days=days)).isoformat()