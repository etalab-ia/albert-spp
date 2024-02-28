from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    BACKEND_CORS_ORIGINS,
    CONTACT,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)
from endpoints import api, misc
from redis import Redis
from subscriptions import Listener


# Init Redis
r = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
listener = Listener(r, ["spp-exp-channel"])
listener.start()

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
