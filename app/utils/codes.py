from datetime import datetime
from app.config import settings


def build_tracking_code(year: int, seq: int) -> str:
    # Example: PRC-2025-000123

    return f"{settings.TRACKING_CODE_PREFIX}-{year}-{seq:0{settings.TRACKING_CODE_PADDING}d}"


def generate_tracking_code(next_id: int) -> str:
    # Simple and deterministic: use DB auto-increment id as sequence
    year = datetime.utcnow().year
    return build_tracking_code(year, next_id)
