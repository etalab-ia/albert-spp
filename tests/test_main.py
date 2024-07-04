import fakeredis
import pytest
from fastapi.testclient import TestClient
from pyalbert import set_llm_table

LLM_TABLE = [{"model": "AgentPublic/llama3-fabrique-texte", "url": "http://127.0.0.1:8899"}]
set_llm_table(LLM_TABLE)

from app import app
from config import APP_VERSION
from deps import get_redis
from tests.conftest import TestApi, log_and_assert


@pytest.fixture
def fake_redis():
    return fakeredis.FakeStrictRedis()


@pytest.fixture
def client(fake_redis):
    def override_get_redis():
        yield fake_redis

    app.dependency_overrides[get_redis] = override_get_redis
    return TestClient(app)


class TestEndpointsStream(TestApi):
    def test_health(self, client: TestClient):
        response = client.get("/healthcheck")
        log_and_assert(response, 200)
        assert response.json()["msg"] == "OK"
        assert response.json()["version"] == APP_VERSION

    def test_crud(self, client: TestClient):
        # Single data
        data = {"id": "user_random_id", "text": "tell me a joke"}
        response = client.post("/anonymize", headers={"Authorization": "Bearer NOOP"}, json=data)
        log_and_assert(response, 200)

        # Batched data
        data = [{"id": "user_random_id", "text": "tell me a joke"}]
        response = client.post("/anonymize", headers={"Authorization": "Bearer NOOP"}, json=data)
        log_and_assert(response, 200)

        # Read data
        # ...
        data = {"id": "user_random_id"}
        response = client.post(
            "/prod/run/ditp-get-data", headers={"Authorization": "Bearer NOOP"}, json=data
        )
        log_and_assert(response, 200)
