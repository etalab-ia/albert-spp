from redis import Redis

from config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


def get_redis(finally_close=True) -> Redis:
    client = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
    assert client.ping(), "Redis connection failed"
    try:
        yield client
    finally:
        # Ensure the connection is cleaned up
        if client and finally_close:
            client.close()
