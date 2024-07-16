import time

from fastapi.testclient import TestClient

from config import APP_VERSION
from tests.conftest import TestApi, log_and_assert


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
        time.sleep(2)
        data = {"id": "user_random_id"}
        response = client.post(
            "/prod/run/ditp-get-data", headers={"Authorization": "Bearer NOOP"}, json=data
        )
        log_and_assert(response, 200)
