from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends

from app.auth import get_api_key
from app.db import init_db
from app.routers import customers, parcels, scans, reports

app = FastAPI(title="Parcel Tracker API", version="0.1.0",dependencies=[Depends(get_api_key)])
#app_api_key=FastAPI(dependencies=[Depends(get_api_key())])


# CORS for local frontends if needed later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


# include routers
app.include_router(customers.router)
app.include_router(parcels.router)
app.include_router(scans.router)
app.include_router(reports.router)


# create tables on startup (dev only)
@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(customers.router, dependencies=[Depends(get_api_key)])
app.include_router(parcels.router, dependencies=[Depends(get_api_key)])
app.include_router(scans.router, dependencies=[Depends(get_api_key)])
app.include_router(reports.router, dependencies=[Depends(get_api_key)])
