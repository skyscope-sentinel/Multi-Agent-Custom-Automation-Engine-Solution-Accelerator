import os
import sys
import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import status

# Mock Azure dependencies
sys.modules['azure.monitor'] = MagicMock()
sys.modules['azure.monitor.events.extension'] = MagicMock()
sys.modules['azure.monitor.opentelemetry'] = MagicMock()

# Mock the configure_azure_monitor function
from azure.monitor.opentelemetry import configure_azure_monitor
configure_azure_monitor = MagicMock()

# Import the app
from src.backend.app import app

# Set environment variables
os.environ["COSMOSDB_ENDPOINT"] = "https://mock-endpoint"
os.environ["COSMOSDB_KEY"] = "mock-key"
os.environ["COSMOSDB_DATABASE"] = "mock-database"
os.environ["COSMOSDB_CONTAINER"] = "mock-container"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "mock-deployment-name"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-01-01"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://mock-openai-endpoint"
os.environ["APPLICATIONINSIGHTS_INSTRUMENTATION_KEY"] = "mock-key"

# Initialize FastAPI test client
client = TestClient(app)

# Mock user authentication
def mock_get_authenticated_user_details(request_headers):
    return {"user_principal_id": "mock-user-id"}


@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    """Patch dependencies used in the app."""
    monkeypatch.setattr(
        "src.backend.auth.auth_utils.get_authenticated_user_details",
        mock_get_authenticated_user_details,
    )
    monkeypatch.setattr(
        "src.backend.context.cosmos_memory.CosmosBufferedChatCompletionContext",
        MagicMock(),
    )
    monkeypatch.setattr(
        "src.backend.utils.initialize_runtime_and_context",
        AsyncMock(return_value=(MagicMock(), None)),
    )
    monkeypatch.setattr(
        "src.backend.utils.retrieve_all_agent_tools",
        MagicMock(return_value=[{"agent": "test_agent", "function": "test_function"}]),
    )
    monkeypatch.setattr(
        "src.backend.app.track_event",
        MagicMock(),
    )

@pytest.mark.asyncio
async def test_human_feedback_endpoint():
    """Test the /human_feedback endpoint."""
    payload = {
        "step_id": "step-1",
        "plan_id": "plan-1",
        "session_id": "session-1",
        "approved": True,
        "human_feedback": "Looks good",
        "updated_action": None,
        "user_id": "mock-user-id",
    }
    response = client.post("/human_feedback", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "Feedback received"


@pytest.mark.asyncio
async def test_get_agent_tools():
    """Test the /api/agent-tools endpoint."""
    response = client.get("/api/agent-tools")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0