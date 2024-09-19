from contextlib import asynccontextmanager
import requests

from fastapi import FastAPI
from redis import Redis
from starlette.middleware.cors import CORSMiddleware

from config import (
    ALBERT_API_KEY,
    ALBERT_BASE_URL,
    LANGUAGE_MODEL,
    EMBEDDINGS_MODEL,
    APP_NAME,
    APP_VERSION,
    BACKEND_CORS_ORIGINS,
    ENV,
)
from deps import get_redis
from endpoints import api, misc
from subscriptions import Listener


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
    assert EMBEDDINGS_MODEL in models, f"Model {EMBEDDINGS_MODEL} not found"

    yield

    # Shutdown code
    app.state.listener.stop()


# Init server
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    contact={
        "name": "Etalab",
        "url": "https://www.etalab.gouv.fr/",
        "email": "etalab@modernisation.gouv.fr",
    },
    lifespan=lifespan,
)

if BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(misc.router)
app.include_router(api.router)
