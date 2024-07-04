import os
import subprocess
import time
from typing import Generator
from urllib.parse import urlparse

import pytest
import requests
from fastapi.testclient import TestClient
from pytest import fail

os.environ["ENV"] = "unittest"

from pyalbert import set_llm_table

LLM_TABLE = [{"model": "AgentPublic/llama3-fabrique-texte", "url": "http://127.0.0.1:8899"}]
set_llm_table(LLM_TABLE)


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
def mock_server3():
    if len(LLM_TABLE) > 0:
        LLM_HOST, LLM_PORT = urlparse(LLM_TABLE[0]["url"]).netloc.split(":")

    process = start_mock_server(["uvicorn", "app.tests.mockups.llm:app", "--port", LLM_PORT])
    yield
    process.kill()


class TestApi:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_mockup(self, mock_server3):
        # Start the server
        pass
