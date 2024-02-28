import os
from dotenv import load_dotenv

# App metadata
# TODO load metadata from pyproject.toml using tomlib instead of this
APP_NAME = "albert-spp"
APP_DESCRIPTION = "Albert, also known as LIA: the **L**egal **I**nformation **A**ssistant, is a conversational agent that uses official French data sources to answer administrative agent questions."
APP_VERSION = "1.0.0"
CONTACT = {
    "name": "Etalab - Datalab",
    "url": "https://www.etalab.gouv.fr/",
    "email": "etalab@mail.numerique.gouv.fr",
}

# Root directory:
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Environment:
load_dotenv(os.path.join(ROOT_DIR, ".env"))

ENV = os.getenv("ENV", "dev")
if ENV not in ("unittest", "dev", "prod"):
    raise EnvironmentError("Wrong ENV value")

# CORS
BACKEND_CORS_ORIGINS = [
    "http://localhost:4173",
    "http://localhost:8080",
    "http://ia.etalab.gouv.fr",
    "http://albert.etalab.gouv.fr",
    "http://albert.staging.etalab.gouv.fr",
    "http://franceservices.etalab.gouv.fr",
    "http://franceservices.staging.etalab.gouv.fr",
    "https://ia.etalab.gouv.fr",
    "https://albert.etalab.gouv.fr",
    "https://albert.staging.etalab.gouv.fr",
    "https://franceservices.etalab.gouv.fr",
    "https://franceservices.staging.etalab.gouv.fr",
]


# Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
