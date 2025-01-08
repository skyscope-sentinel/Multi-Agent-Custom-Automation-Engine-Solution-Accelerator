import pytest
from fastapi.testclient import TestClient
from app import app
from unittest.mock import AsyncMock, patch

# Create a test client
client = TestClient(app)

# Mock dependencies
@pytest.fixture
def mock_authenticated_user_details():
    return {"user_principal_id": "test_user_id"}

@pytest.fixture
def mock_runtime_and_context():
    runtime_mock = AsyncMock()
    runtime_mock.send_message = AsyncMock(return_value={"id": "plan123", "summary": "Mocked Plan"})
    return runtime_mock, None

# Test /input_task endpoint
@patch("app.get_authenticated_user_details")
@patch("app.initialize_runtime_and_context")
def test_input_task(mock_initialize_runtime_and_context, mock_get_authenticated_user_details, mock_authenticated_user_details, mock_runtime_and_context):
    mock_get_authenticated_user_details.return_value = mock_authenticated_user_details
    mock_initialize_runtime_and_context.return_value = mock_runtime_and_context

    input_task_data = {
        "session_id": "session123",
        "description": "Test Task",
    }
    response = client.post("/input_task", json=input_task_data)

    assert response.status_code == 200
    assert response.json()["status"] == "Plan created:\n Mocked Plan"

# Test /human_feedback endpoint
@patch("app.get_authenticated_user_details")
@patch("app.initialize_runtime_and_context")
def test_human_feedback(mock_initialize_runtime_and_context, mock_get_authenticated_user_details, mock_authenticated_user_details, mock_runtime_and_context):
    mock_get_authenticated_user_details.return_value = mock_authenticated_user_details
    mock_initialize_runtime_and_context.return_value = mock_runtime_and_context

    human_feedback_data = {
        "step_id": "step123",
        "plan_id": "plan123",
        "session_id": "session123",
        "approved": True,
        "human_feedback": "Looks good",
    }
    response = client.post("/human_feedback", json=human_feedback_data)

    assert response.status_code == 200
    assert response.json()["status"] == "Feedback received"

# Test /plans endpoint
@patch("app.get_authenticated_user_details")
@patch("app.CosmosBufferedChatCompletionContext")
def test_get_plans(mock_cosmos_context, mock_get_authenticated_user_details, mock_authenticated_user_details):
    mock_get_authenticated_user_details.return_value = mock_authenticated_user_details
    cosmos_mock = AsyncMock()
    cosmos_mock.get_all_plans.return_value = [{"id": "plan123", "model_dump": lambda: {"id": "plan123", "summary": "Mock Plan"}}]
    cosmos_mock.get_steps_by_plan.return_value = [{"id": "step123", "description": "Mock Step"}]
    mock_cosmos_context.return_value = cosmos_mock

    response = client.get("/plans")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == "plan123"

# Test /delete_all_messages endpoint
@patch("app.get_authenticated_user_details")
@patch("app.CosmosBufferedChatCompletionContext")
def test_delete_all_messages(mock_cosmos_context, mock_get_authenticated_user_details, mock_authenticated_user_details):
    mock_get_authenticated_user_details.return_value = mock_authenticated_user_details
    cosmos_mock = AsyncMock()
    mock_cosmos_context.return_value = cosmos_mock

    response = client.delete("/messages")

    assert response.status_code == 200
    assert response.json()["status"] == "All messages deleted"

# Test /api/agent-tools endpoint
def test_get_agent_tools():
    response = client.get("/api/agent-tools")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
