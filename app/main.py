from contextlib import asynccontextmanager
import datetime as dt
import json
import logging
from typing import List, Union
import uuid

from fastapi import Body, Depends, FastAPI, HTTPException, Response, Security
from redis import Redis
import requests
from starlette.middleware.cors import CORSMiddleware

from app.config import (
    ALBERT_API_KEY,
    ALBERT_BASE_URL,
    APP_NAME,
    APP_VERSION,
    ENV,
    LANGUAGE_MODEL,
)
from app.deps import get_redis
from app.schemas import ExpId, ExpIdWithText
from app.security import check_api_key
from app.subscriptions import Listener

logging.basicConfig(level=logging.INFO)


def init_redis(r: Redis):
    app.state.listener = Listener(r, ["spp-exp-channel"])
    app.state.listener.start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    if ENV != "unittest":
        r = next(get_redis(finally_close=False))
        init_redis(r)

    request = requests.get(f"{ALBERT_BASE_URL}/models", headers={"Authorization": f"Bearer {ALBERT_API_KEY}"})
    request.raise_for_status()
    models = [model["id"] for model in request.json()["data"]]
    assert LANGUAGE_MODEL in models, f"Model {LANGUAGE_MODEL} not found"

    yield

    # Shutdown code
    app.state.listener.stop()


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def healt() -> dict[str, str]:
    return Response(status_code=200)


@app.post("/anonymize")
def anonymize(
    form_data: Union[ExpIdWithText, List[ExpIdWithText]] = Body(...),
    redis: Redis = Depends(get_redis),
    api_key: str = Security(check_api_key),
):
    if not isinstance(form_data, list):
        form_data = [form_data]

    for data in form_data:
        if not data.id:
            # see https://tchap.gouv.fr/#/room/!ZyhOfCwElHmyNMSlcw:agent.dinum.tchap.gouv.fr/$XMeXbIDhGtXBycZu-9Px2frsczn_iU7xiJ5xvjbs-pQ?via=agent.dinum.tchap.gouv.fr&via=agent.externe.tchap.gouv.fr&via=agent.tchap.gouv.fr
            data.id = str(uuid.uuid4())

        data = data.model_dump()

        data["time"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f%z")
        print(f"anonymize - {data['id']}: {data['time']}")  # TODO: replace with logger later
        redis.publish("spp-exp-channel", json.dumps(data))

    if len(form_data) == 1:
        responseOutput = {"id": form_data[0].id}
    else:
        # The spec is ill-defined !!
        responseOutput = [{"id": x.id} for x in form_data]

    return {"body": responseOutput}


@app.post("/prod/run/ditp-get-data")
def ditp_get_data(form_data: Union[ExpId, List[ExpId]] = Body(...), redis: Redis = Depends(get_redis), api_key: str = Security(check_api_key)):
    if not isinstance(form_data, list):
        form_data = [form_data]

    answers = []
    for data in form_data:
        data = data.model_dump()
        answer = redis.get(data["id"])
        answers.append(answer)

    if len(form_data) == 1:
        if answers[0] is None:
            raise HTTPException(status_code=400, detail="ID not found")
        responseOutput = {"generated_answer": answers[0]}
    else:
        # The spec is ill-defined !!
        responseOutput = [{"generated_answer": x} for x in answers]

    return {"body": responseOutput}
