import pytest
from fastapi.testclient import TestClient
from main import web_server


@pytest.fixture
def client():
    with TestClient(web_server) as client:
        yield client


def test_healthcheck_route(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
