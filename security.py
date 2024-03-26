import json

from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException

from config import API_KEYS_FILE, ENV

api_key_header = APIKeyHeader(name="Authorization")


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    # ignore api key validation in development
    if ENV == "dev":
        return api_key_header
    
    # check if api key is in the correct format
    if not api_key_header.startswith("Bearer "):
        
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key",
        )
    
    api_key_header = api_key_header.replace("Bearer ", "")

    # open api_keys json file
    with open(API_KEYS_FILE, "r") as file:
        api_keys = json.load(file)

    available_keys = [key.replace("Bearer ", "") for title, key in api_keys.items()]

    if api_key_header in available_keys:
        return api_key_header
    
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key",
    )
