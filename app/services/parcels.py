from datetime import datetime
from typing import Literal

from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models
from app.utils.codes import generate_tracking_code

Status = Literal[
    "new", "pickup", "in_transit", "out_for_delivery", "delivered", "return"
]

# Allowed transitions
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "new": {"pickup"},
    "pickup": {"in_transit"},
    "in_transit": {"out_for_delivery", "return"},
    "out_for_delivery": {"delivered", "return"},
    "delivered": set(),  # final
    "return": set(),     # final
}


def is_final(status: str) -> bool:
    return status in {"delivered", "return"}


def create_parcel(db: Session, payload: models.Parcel, customer_id: int) -> models.Parcel:
    # Persist once to get auto id, then set tracking_code
    db.add(payload)
    db.flush()  # gets payload.id
    payload.tracking_code = generate_tracking_code(payload.id)
    db.commit()
    db.refresh(payload)
    return payload


def find_parcel_by_code(db: Session, code: str) -> models.Parcel | None:
    stmt = select(models.Parcel).where(models.Parcel.tracking_code == code)
    return db.execute(stmt).scalar_one_or_none()


def apply_scan_transition(
    db: Session,
    parcel: models.Parcel,
    scan_type: Status,
    ts: datetime,
    location: str,
    note: str | None,
) -> models.Scan:
    if is_final(parcel.status):
        raise ValueError("parcel is finalized, scans are not allowed")

    allowed = ALLOWED_TRANSITIONS.get(parcel.status, set())
    if scan_type not in allowed:
        raise ValueError(f"illegal status transition: {parcel.status} -> {scan_type}")

    # Append scan
    scan = models.Scan(
        parcel_id=parcel.id, type=scan_type, location=location, ts=ts, note=note
    )
    db.add(scan)

    # Update parcel status and delivered_at if needed
    parcel.status = scan_type
    if scan_type == "delivered" and parcel.delivered_at is None:
        parcel.delivered_at = ts

    db.commit()
    db.refresh(scan)
    db.refresh(parcel)
    return scan
