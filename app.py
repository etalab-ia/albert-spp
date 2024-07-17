from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from redis import Redis
from starlette.middleware.cors import CORSMiddleware

from config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    BACKEND_CORS_ORIGINS,
    CONTACT,
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

    yield

    # Shutdown code
    app.state.listener.stop()


# Init server
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    contact=CONTACT,
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
