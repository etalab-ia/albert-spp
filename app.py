from fastapi import APIRouter, FastAPI
from redis import Redis
from starlette.middleware.cors import CORSMiddleware

from config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    BACKEND_CORS_ORIGINS,
    CONTACT,
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
)
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


# startup init redis
@app.on_event("startup")
async def init_redis():
    r = Redis(host=REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PASSWORD, db=0)
    app.state.listener = Listener(r, ["spp-exp-channel"])
    app.state.listener.start()
