import pytest
from fastapi import status
from fastapi.testclient import TestClient
from template_api.main import app


@pytest.fixture(scope="session")
def client():
    """Create TestClient with full app for E2E tests."""
    return TestClient(app)


@pytest.mark.e2e
def test_healthcheck_endpoint(client: TestClient):
    """E2E test: verify healthcheck endpoint returns 200."""
    response = client.get("/v1/public/test/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "ok"
