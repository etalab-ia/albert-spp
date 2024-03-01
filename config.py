import os
import ast

# App
APP_NAME = "albert-spp"
APP_DESCRIPTION = """Albert for Services Publics Plus.

Les requêtes aux différents doivent contenir un header au format `Authorization: Bearer <token>` avec une clé API valide. Pour obtenir une clé API, veuillez contacter l'équipe Etalab.
"""
APP_VERSION = os.environ.get("APP_VERSION", "0.0.0")
CONTACT = {
    "name": "Etalab - Datalab",
    "url": "https://www.etalab.gouv.fr/",
    "email": "etalab@modernisation.gouv.fr",
}
API_KEYS_FILE = os.environ("API_KEYS_FILE", "api_keys.example.json")

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
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

# LLM
# The model is not customizable for this API
LLM_DEFAULT_MODEL = "AgentPublic/fabrique-reference-2"

LLM_TABLE = os.getenv("LLM_TABLE")
if LLM_TABLE:
    LLM_TABLE = ast.literal_eval(LLM_TABLE)
    models = [model for model, url in LLM_TABLE]
    assert LLM_DEFAULT_MODEL in models, f"{LLM_DEFAULT_MODEL} should be in LLM_TABLE"

# only for local deployment, to use a local LLM server on port 8081
elif ENV == "dev":
    LLM_TABLE = [(LLM_DEFAULT_MODEL, "http://127.0.0.1:8081")]
