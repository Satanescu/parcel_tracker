from datetime import datetime
from app.utils.config import Settings


def build_tracking_code(year: int, seq: int) -> str:
    # Example: PRC-2025-000123

    return f"{Settings.TRACKING_CODE_PREFIX}-{year}-{seq:0{Settings.TRACKING_CODE_PADDING}d}"


def generate_tracking_code(next_id: int) -> str:
    # Simple and deterministic: use DB auto-increment id as sequence
    year = datetime.utcnow().year
    return build_tracking_code(year, next_id)
