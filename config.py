import os

from pyalbert.config import LLM_TABLE

# App
APP_NAME = "albert-spp"
APP_DESCRIPTION = """Albert for Services Publics Plus.

Les requêtes aux différents endpoints doivent contenir un header au format `Authorization: Bearer <token>` avec une clé API valide. Pour obtenir une clé API, veuillez contacter l'équipe Etalab.
"""
APP_VERSION = os.environ.get("APP_VERSION", "0.0.0")
CONTACT = {
    "name": "Etalab - Datalab",
    "url": "https://www.etalab.gouv.fr/",
    "email": "etalab@modernisation.gouv.fr",
}
API_KEYS_FILE = os.environ.get("API_KEYS_FILE", "api_keys.example.json")

# Env
ENV = os.environ.get("ENV", "dev")
assert ENV in [
    "unittest",
    "dev",
    "staging",
    "prod",
], "wrong ENV value. Should be 'unittest', 'dev', 'staging' or 'prod'"

# CORS
BACKEND_CORS_ORIGINS = ["*"]

# Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

# LLM
# The model is not customizable for this API
LLM_DEFAULT_MODEL = "AgentPublic/llama3-fabrique-texte"

assert LLM_DEFAULT_MODEL in [
    m["model"] for m in LLM_TABLE
], f"{LLM_DEFAULT_MODEL} should be in LLM_TABLE"
