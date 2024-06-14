from redis import Redis

from config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


def get_redis() -> Redis:
    client = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
    try:
        yield client
    finally:
        # Ensure the connection is cleaned up
        if client:
            client.close()
