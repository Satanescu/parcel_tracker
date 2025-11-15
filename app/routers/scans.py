from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.deps import get_db
from app.schemas import ScanOut, ScanCreate
from app.services.parcels import find_parcel_by_code, apply_scan_transition
from customers import parse_sort,apply_sort

from app.models import Scan

router = APIRouter(prefix="/parcels", tags=["scans"])


@router.post("/{tracking_code}/scans", response_model=ScanOut, status_code=201)
def add_scan(
    tracking_code: str, payload: ScanCreate, db: Session = Depends(get_db)
):
    parcel = find_parcel_by_code(db, tracking_code)
    if not parcel:
        raise HTTPException(404, "parcel not found")
    try:
        scan = apply_scan_transition(
            db=db,
            parcel=parcel,
            scan_type=payload.type,
            ts=payload.ts,
            location=payload.location,
            note=payload.note,
        )
        return scan
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.get("/{tracking_code}/scans", response_model=List[ScanOut])
def list_scans(
    tracking_code: str,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    sort: str = "ts,asc",
):
    parcel = find_parcel_by_code(db, tracking_code)
    if not parcel:
        raise HTTPException(404, "parcel not found")

    # scans = list(parcel.scans)
    # # sort simple
    # reverse = False
    # if sort.endswith(",desc"):
    #     reverse = True
    # scans.sort(key=lambda s: s.ts, reverse=reverse)
    #
    # start = (page - 1) * size
    # end = start + size
    # return scans[start:end]

    stmt=select(Scan)

    if parcel:
        stmt=stmt.where(Scan.parcel_id == parcel.id)
    field, order= parse_sort(
        sort,
        {"id","parcel_id","ts","location","type","note"},
        "ts"
    )
    stmt=apply_sort(stmt,Scan,field,order)
    stmt = stmt.offset((page - 1) * size).limit(size)
    rows = db.execute(stmt).scalars().all()
    return rows




