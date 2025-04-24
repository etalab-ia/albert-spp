import os

APP_NAME = "Albert SPP"
APP_VERSION = os.environ.get("APP_VERSION", "0.0.0")
API_KEYS = os.environ.get("API_KEYS", "changeme")
API_KEYS = [key.strip() for key in API_KEYS.split(",")]
ENV = os.environ.get("ENV", "dev")
assert ENV in ["unittest", "dev", "staging", "prod"], "wrong ENV value"
BACKEND_CORS_ORIGINS = ["*"]
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

LANGUAGE_MODEL = os.environ["LANGUAGE_MODEL"]
ALBERT_BASE_URL = os.environ["ALBERT_BASE_URL"]
ALBERT_API_KEY = os.environ["ALBERT_API_KEY"]
COLLECTION_ID = int(os.environ["COLLECTION_ID"])
