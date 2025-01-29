# pylint: disable=import-error, wrong-import-position, missing-module-docstring
import asyncio
import json
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from pydantic import ValidationError

# Environment and module setup
sys.modules["azure.monitor.events.extension"] = MagicMock()

os.environ["COSMOSDB_ENDPOINT"] = "https://mock-endpoint"
os.environ["COSMOSDB_KEY"] = "mock-key"
os.environ["COSMOSDB_DATABASE"] = "mock-database"
os.environ["COSMOSDB_CONTAINER"] = "mock-container"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "mock-deployment-name"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-01-01"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://mock-openai-endpoint"

# noqa: F401 is to ignore unused import warnings (if any)
from src.backend.agents.agentutils import extract_and_update_transition_states  # noqa: F401, C0413
from src.backend.models.messages import Step  # noqa: F401, C0413

@pytest.fixture(scope="function")
async def reset_event_loop():
    """Ensure a fresh event loop for each test."""
    yield
    loop = asyncio.get_event_loop()
    if not loop.is_closed():
        loop.close()


def test_step_initialization():
    """Test Step initialization with valid data."""
    step = Step(
        data_type="step",
        plan_id="test_plan",
        action="test_action",
        agent="HumanAgent",
        session_id="test_session",
        user_id="test_user",
        agent_reply="test_reply",
    )

    assert step.data_type == "step"
    assert step.plan_id == "test_plan"
    assert step.action == "test_action"
    assert step.agent == "HumanAgent"
    assert step.session_id == "test_session"
    assert step.user_id == "test_user"
    assert step.agent_reply == "test_reply"
    assert step.status == "planned"
    assert step.human_approval_status == "requested"

def test_step_missing_required_fields():
    """Test Step initialization with missing required fields."""
    with pytest.raises(ValidationError):
        Step(
            data_type="step",
            action="test_action",
            agent="test_agent",
            session_id="test_session",
        )
