import os
import subprocess
import time
from typing import Generator
from urllib.parse import urlparse

import fakeredis
import pytest
import requests
from fastapi.testclient import TestClient
from pytest import fail

os.environ["ENV"] = "unittest"

from pyalbert import set_llm_table

LLM_TABLE = [{"model": "AgentPublic/llama3-fabrique-texte", "url": "http://127.0.0.1:8899"}]
set_llm_table(LLM_TABLE)

from app import app, init_redis
from deps import get_redis


def log_and_assert(response, code):
    if code != 200:
        assert response.status_code == code
        return

    if response.status_code != 200:
        fail(
            f"Expected status code 200, but got {response.status_code}.\nError details: {response.text}"
        )


def start_mock_server(command, health_route="/healthcheck", timeout=10, interval=1):
    """Starts a mock server using subprocess.Popen and waits for it to be ready
    by polling a health check endpoint.
    """
    process = subprocess.Popen(command)

    try:
        end_time = time.time() + timeout
        while True:
            try:
                host = "localhost"
                port = command[-1]
                response = requests.get(f"http://{host}:{port}" + health_route)
                if response.status_code == 200:
                    # Server is ready
                    break
            except requests.ConnectionError:
                # Server not ready yet
                pass

            if time.time() > end_time:
                raise RuntimeError("Timeout waiting for server to start")

            time.sleep(interval)
    except Exception as e:
        process.kill()
        raise e

    return process


@pytest.fixture(scope="session")
def mock_llm() -> Generator:
    if len(LLM_TABLE) > 0:
        LLM_HOST, LLM_PORT = urlparse(LLM_TABLE[0]["url"]).netloc.split(":")

    process = start_mock_server(["uvicorn", "tests.mockups.llm:app", "--port", LLM_PORT])
    yield
    process.kill()


@pytest.fixture(scope="session")
def mock_redis() -> Generator:
    # Create a fakeredis server instance
    server = fakeredis.FakeServer()
    client = fakeredis.FakeStrictRedis(server=server)

    # Manually call init_redis with the fakeredis client
    init_redis(client)

    yield server
    # No need for teardown as fakeredis is in-memory and will be cleaned up automatically

    # Stop the listener after the tests
    # if hasattr(app.state, "listener"):
    #    app.state.listener.stop()


@pytest.fixture(scope="module")
def redis_client(mock_redis) -> Generator:
    # Create a fakeredis client connected to the server
    client = fakeredis.FakeStrictRedis(server=mock_redis)
    yield client
    # No need for teardown as fakeredis is in-memory and will be cleaned up automatically


@pytest.fixture(scope="module")
def client(redis_client) -> Generator:
    # Override the get_redis dependency to use fakeredis
    def override_get_redis():
        yield redis_client

    app.dependency_overrides[get_redis] = override_get_redis
    with TestClient(app) as c:
        yield c

    # Remove the dependency override after the tests
    app.dependency_overrides = {}


class TestApi:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_mockup(self, mock_llm, mock_redis):
        # Start the server
        pass
