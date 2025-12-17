import pytest
from fastapi import status
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def test_api(client: TestClient):
    response = client.get("/v1/public/test/healthcheck")
    assert response.status_code == status.HTTP_200_OK
