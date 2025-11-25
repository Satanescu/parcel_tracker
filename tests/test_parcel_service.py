from datetime import datetime

import pytest

from app.db import SessionLocal
from app.services.parcels import apply_scan_transition


class FakeSession:
    """Minimal fake SQLAlchemy Session for unit testing."""

    def __init__(self):
        self.added = []
        self.committed = False
        self.refreshed = []

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        # we don't need real DB behaviour here
        self.refreshed.append(obj)


class DummyParcel:
    """Simple stand-in for the real  model."""

    def __init__(self, id: int, status: str, delivered_at=None):
        self.id = id
        self.status = status
        self.delivered_at = delivered_at


@pytest.fixture
def db_session():
    return FakeSession()

def test_parcel_new_to_pickup(db_session):
    parcel = DummyParcel(status="new",id=1)
    apply_scan_transition(db_session,parcel,ts=datetime.now(),location="Timisoara", scan_type="pickup", note=None)
    assert parcel.status == "pickup"

def test_parcel_pickup_to_in_transit(db_session):
    parcel = DummyParcel(id=1, status="pickup")
    apply_scan_transition(db_session, parcel,ts=datetime.now(),location="Timisoara", scan_type="in_transit",note=None)
    assert parcel.status == "in_transit"

def test_parcel_in_transit_out_for_delivery(db_session):
    parcel = DummyParcel(id=1, status="in_transit")
    apply_scan_transition(db_session, parcel,ts=datetime.now(),location="Timisoara", scan_type="out_for_delivery",note=None)
    assert parcel.status == "out_for_delivery" #or parcel.status == "return"

def test_parcel_in_transit_return(db_session):
    parcel = DummyParcel(id=1, status="in_transit")
    apply_scan_transition(db_session, parcel,ts=datetime.now(),location="Timisoara", scan_type="return",note=None)
    assert parcel.status == "return"

def test_parcel_out_for_delivery_return(db_session):
    parcel = DummyParcel(id=1, status="out_for_delivery")
    apply_scan_transition(db_session, parcel,ts=datetime.now(),location="Timisoara", scan_type="return",note=None)
    assert parcel.status == "return"

def test_parcel_delivered(db_session):
    parcel = DummyParcel(id=1, status="out_for_delivery")
    apply_scan_transition(db_session, parcel,ts=datetime.now(),location="Timisoara", scan_type="delivered",note=None)
    assert parcel.status == "delivered"

def test_parcel_return(db_session):
    parcel = DummyParcel(id=1, status="in_transit")
    apply_scan_transition(db_session, parcel,ts=datetime.now(),location="Timisoara", scan_type="return",note=None)
    assert parcel.status == "return"

def test_ilegal_transition_no_1():
    parcel = DummyParcel(id=1,status="new")
    with pytest.raises(ValueError):
        apply_scan_transition(db_session, parcel,ts=datetime.now(),location="Timisoara", scan_type="delivered",note=None)


def test_ilegal_transition_no_2(db_session):
    parcel = DummyParcel(id=1, status="delivered")
    with pytest.raises(ValueError):
        apply_scan_transition(db_session, parcel,ts=datetime.now(),location="Timisoara", scan_type="return",note=None)


