import os
import json

from pyalbert.config import LLM_TABLE

# App
APP_NAME = "albert-spp"
APP_DESCRIPTION = """Albert for Services Publics Plus.

Les requêtes aux différents endpoints doivent contenir un header au format `Authorization: Bearer <token>` avec une clé API valide. Pour obtenir une clé API, veuillez contacter l'équipe Etalab.
"""
APP_VERSION = os.environ.get("APP_VERSION", "0.0.0")
CONTACT = {
    "name": "Etalab",
    "url": "https://www.etalab.gouv.fr/",
    "email": "etalab@modernisation.gouv.fr",
}
API_KEYS_FILE = os.environ.get("API_KEYS_FILE", "api_keys.example.json")
API_KEYS_FILE = json.load(open(API_KEYS_FILE, "r"))
API_KEYS = [key for title, key in API_KEYS_FILE.items()]
ENV = os.environ.get("ENV", "dev")
assert ENV in ["unittest", "dev", "staging", "prod"], "wrong ENV value"
BACKEND_CORS_ORIGINS = ["*"]
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
MODEL_NAME = os.getenv("MODEL_NAME", "AgentPublic/llama3-fabrique-texte")
