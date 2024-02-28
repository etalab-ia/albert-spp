from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.config import APP_VERSION

router = APIRouter()


@router.get("/healthcheck", tags=["misc"])
def get_healthcheck() -> dict[str, str]:
    return {"msg": "OK", "version": APP_VERSION}


