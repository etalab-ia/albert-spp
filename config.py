import json
import os

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
API_KEYS = os.environ.get("API_KEYS", "changeme")
API_KEYS = [key.strip() for key in API_KEYS.split(",")]
ENV = os.environ.get("ENV", "dev")
assert ENV in ["unittest", "dev", "staging", "prod"], "wrong ENV value"
BACKEND_CORS_ORIGINS = ["*"]
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
MODEL_NAME = os.getenv("MODEL_NAME", "AgentPublic/llama3-fabrique-texte")
RAG_EMBEDDING_MODEL = os.getenv("RAG_EMBEDDING_MODEL", "BAAI/bge-m3")
