from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

API_KEY = "supersecret123"   # change this to your own key
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
