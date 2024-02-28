from fastapi import APIRouter, Depends, HTTPException
import schemas
from redis import Redis
from deps import get_redis

router = APIRouter()

@router.post("/anonymize", tags=["api"])
def anonimyze(
    form_data: schemas.ExpIdWithText | list[schemas.ExpIdWithText],
    redis: Redis = Depends(get_redis),
) -> dict:
    print(redis)
    return {"body": "User created. An admin must confirm the user."}

@router.post("/prod/run/ditp-get-data", tags=["api"])
def ditp_get_data(
    form_data: schemas.ExpId | list[schemas.ExpId],
    redis: Redis = Depends(get_redis),
) -> dict:
    print(redis)
    return {"body": "User created. An admin must confirm the user."}
