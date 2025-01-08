import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Awaitable

from health_check import HealthCheckMiddleware, HealthCheckResult

# A sample health check function
async def sample_check() -> HealthCheckResult:
    return HealthCheckResult(True, "Sample check passed")

# A failing health check function
async def failing_check() -> HealthCheckResult:
    return HealthCheckResult(False, "Sample check failed")

def create_app():
    app = FastAPI()

    checks = {
        "SampleCheck": sample_check,
        "FailingCheck": failing_check,
    }

    app.add_middleware(HealthCheckMiddleware, checks=checks, password="testpassword")

    @app.get("/")
    async def read_root():
        return {"message": "Hello World"}

    return app

@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)

def test_healthcheck_default(client):
    response = client.get("/healthz")
    assert response.status_code == 503  # Failing check should result in 503
    assert response.text == "Service Unavailable"


def test_non_healthz_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
