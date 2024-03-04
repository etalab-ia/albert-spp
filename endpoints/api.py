import json
import uuid
from typing import Union, List

from fastapi import Body, HTTPException, Security
from fastapi import APIRouter, Depends
from redis import Redis

import schemas
from deps import get_redis
from subscriptions import encode_experience_key
from security import get_api_key

router = APIRouter()


@router.post("/anonymize", tags=["api"])
def anonymize(
    form_data: Union[schemas.ExpIdWithText, List[schemas.ExpIdWithText]] = Body(...),
    redis: Redis = Depends(get_redis),
    api_key: str = Security(get_api_key),
):
    if not isinstance(form_data, list):
        form_data = [form_data]

    for data in form_data:
        if not data.id:
            # see https://tchap.gouv.fr/#/room/!ZyhOfCwElHmyNMSlcw:agent.dinum.tchap.gouv.fr/$XMeXbIDhGtXBycZu-9Px2frsczn_iU7xiJ5xvjbs-pQ?via=agent.dinum.tchap.gouv.fr&via=agent.externe.tchap.gouv.fr&via=agent.tchap.gouv.fr
            data.id = str(uuid.uuid4())

        data = data.dict()
        redis.publish("spp-exp-channel", json.dumps(data))

    if len(form_data) == 1:
        responseOutput = {"id": form_data[0].id}
    else:
        # The spec is ill-defined !!
        responseOutput = [{"id": x.id} for x in form_data]

    return {"body": responseOutput}


@router.post("/prod/run/ditp-get-data", tags=["api"])
def ditp_get_data(
    form_data: Union[schemas.ExpId, List[schemas.ExpId]] = Body(...),
    redis: Redis = Depends(get_redis),
    api_key: str = Security(get_api_key),
):
    if not isinstance(form_data, list):
        form_data = [form_data]

    answers = []
    for data in form_data:
        data = data.dict()
        anwser = redis.get(encode_experience_key(data))
        answers.append(anwser)

    if len(form_data) == 1:
        if answers[0] is None:
            raise HTTPException(status_code=400, detail="ID not found")
        responseOutput = {"generated_answer": answers[0]}
    else:
        # The spec is ill-defined !!
        responseOutput = [{"generated_answer": x} for x in answers]

    return {"body": responseOutput}
