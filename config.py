import os
import ast

# app
APP_NAME = "albert-spp"
APP_DESCRIPTION = "Albert for Services Publics Plus."
APP_VERSION = "1.0.0"
CONTACT = {
    "name": "Etalab - Datalab",
    "url": "https://www.etalab.gouv.fr/",
    "email": "etalab@mail.numerique.gouv.fr",
}

# env
ENV = os.environ.get("ENV", "dev")
assert ENV in ["unittest", "dev", "prod"], "Wrong ENV value"

# cors
BACKEND_CORS_ORIGINS = ["*"]

# redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

# llm
LLM_TABLE = ast.literal_eval(os.environ.get("LLM_TABLE", "[]"))
