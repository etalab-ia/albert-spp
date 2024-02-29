import os
import ast

# App
APP_NAME = "albert-spp"
APP_DESCRIPTION = "Albert for Services Publics Plus."
APP_VERSION = "1.0.0"
CONTACT = {
    "name": "Etalab - Datalab",
    "url": "https://www.etalab.gouv.fr/",
    "email": "etalab@mail.numerique.gouv.fr",
}

# Env
ENV = os.environ.get("ENV", "dev")
assert ENV in ["unittest", "dev", "prod"], "Wrong ENV value"

# CORS
BACKEND_CORS_ORIGINS = ["*"]

# Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

# LLM
LLM_DEFAULT_MODEL = "AgentPuclic/fabrique-reference-2"  # The model is not customizable for this API
LLM_TABLE = os.getenv("LLM_TABLE")
if LLM_TABLE:
    try:
        LLM_TABLE = ast.literal_eval(LLM_TABLE)
    except Exception as e:
        raise ValueError("LLM_TABLE is not valid: %s" % e)
else:  # default
    LLM_TABLE = [
        # model_name/api URL
        ("AgentPuclic/fabrique-reference-2", "http://127.0.0.1:8081")
    ]
