from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.config import API_KEY

api_key=APIKeyHeader(name="X-API-KEY") # cu asta obtin header ul API ului

def get_api_key(key: str = Depends(api_key)):  # cu Depends citesc ce am obtinut mai sus
    if not key or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


