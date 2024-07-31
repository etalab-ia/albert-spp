from fastapi import APIRouter

from config import APP_VERSION

router = APIRouter(tags=["misc"])


@router.get("/healthcheck")
def get_healthcheck() -> dict[str, str]:
    return {"msg": "OK", "version": APP_VERSION}
