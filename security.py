from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import API_KEYS

if API_KEYS:

    def check_api_key(api_key: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(scheme_name="API key"))]):
        if api_key.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
        if api_key.credentials not in API_KEYS:
            raise HTTPException(status_code=403, detail="Invalid API key")
else:

    def check_api_key():
        pass


