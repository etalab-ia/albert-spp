import subprocess
import time
from pathlib import Path
from typing import Generator


import fakeredis
import pytest
import requests
from fastapi.testclient import TestClient
from pytest import fail

from app import init_redis, main
from app.deps import get_redis


def log_and_assert(response, code):
    if code != 200:
        assert response.status_code == code
        return

    if response.status_code != 200:
        fail(f"Expected status code 200, but got {response.status_code}.\nError details: {response.text}")


def start_mock_server(command, timeout=10, interval=1, cwd=None):
    """Starts a mock server using subprocess.Popen and waits for it to be ready
    by polling a health check endpoint.
    """
    process = subprocess.Popen(command, cwd=cwd)

    try:
        end_time = time.time() + timeout
        while True:
            try:
                response = requests.get("http://localhost:8000/health")
                if response.status_code == 200:
                    # Server is ready
                    break
            except requests.ConnectionError:
                # Server not ready yet
                pass

            if time.time() > end_time:
                raise RuntimeError("Timeout waiting for server to start.")

            time.sleep(interval)
    except Exception as e:
        process.kill()
        raise e

    return process


#
# Albert API mockup
#

APP_FOLDER = Path(__file__).parents[1]


@pytest.fixture(scope="session")
def mock_llm() -> Generator:
    process = start_mock_server(["uvicorn", "tests.mockups:app", "--port", 8080], cwd=APP_FOLDER)
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

    main.dependency_overrides[get_redis] = override_get_redis
    with TestClient(main) as c:
        yield c

    # Remove the dependency override after the tests
    main.dependency_overrides = {}


class TestApi:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_mockup(self, mock_llm, mock_redis):
        # Start the server
        pass
