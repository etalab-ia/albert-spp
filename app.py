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

# Init server
app = FastAPI(title=APP_NAME, description=APP_DESCRIPTION, version=APP_VERSION, contact=CONTACT)

if BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api_router = APIRouter()
api_router.include_router(misc.router)
api_router.include_router(api.router)
app.include_router(api_router)


def init_redis(r: Redis):
    app.state.listener = Listener(r, ["spp-exp-channel"])
    app.state.listener.start()


@app.on_event("startup")
async def startup_event():
    if ENV != "unittest":
        r = next(get_redis(finally_close=False))
        init_redis(r)


@app.on_event("shutdown")
async def shutdown_event():
    app.state.listener.stop()
