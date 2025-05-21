"""Integration tests for the Knowledge agent."""

import json
import logging
import os
import uuid
from unittest.mock import MagicMock, patch, AsyncMock

import pytest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Patch environment variables for testing
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://test-endpoint.openai.azure.com"
os.environ["AZURE_OPENAI_API_KEY"] = "test-key"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-11-20"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "test-deployment"
os.environ["AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"] = "test-connection-string"
os.environ["AZURE_SEARCH_ENABLED"] = "false"
os.environ["FILE_SEARCH_ENABLED"] = "false"
os.environ["AZURE_AI_SUBSCRIPTION_ID"] = "test-subscription"
os.environ["AZURE_AI_RESOURCE_GROUP"] = "test-resource-group"
os.environ["AZURE_AI_PROJECT_NAME"] = "test-project"

# Import after environment variables are set
from context.cosmos_memory_kernel import CosmosMemoryContext
from kernel_agents.knowledge_agent import KnowledgeAgent
from models.messages_kernel import ActionRequest, AgentType

def find_tools_json_file(agent_type_str):
    """Find the appropriate tools JSON file for an agent type."""
    tools_dir = os.path.join(os.path.dirname(__file__), '..', 'tools')
    tools_file = os.path.join(tools_dir, f"{agent_type_str}_tools.json")
    
    if os.path.exists(tools_file):
        return tools_file
    
    # Try alternatives if the direct match isn't found
    alt_file = os.path.join(tools_dir, f"{agent_type_str.replace('_', '')}_tools.json")
    if os.path.exists(alt_file):
        return alt_file
        
    # If nothing is found, log a warning but don't fail
    logger.warning(f"No tools JSON file found for agent type {agent_type_str}")
    return None

@pytest.mark.asyncio
async def test_create_knowledge_agent():
    """Test that we can create a Knowledge agent."""
    # Create test session and user IDs
    session_id = str(uuid.uuid4())
    user_id = "test-user"
    
    # Set up async mock for the agent definition 
    async def mock_create_def(*args, **kwargs):
        return MagicMock()

    # Patch the method with our async mock
    with patch('kernel_agents.knowledge_agent.KnowledgeAgent._create_azure_ai_agent_definition', 
               side_effect=mock_create_def):
        
        # Create a memory store
        memory_store = MagicMock(spec=CosmosMemoryContext)
        
        # Create a Knowledge agent
        agent = await KnowledgeAgent.create(
            session_id=session_id,
            user_id=user_id,
            memory_store=memory_store,
            agent_name=AgentType.KNOWLEDGE.value,
        )
        
        # Verify the agent was created successfully
        assert agent is not None
        assert isinstance(agent, KnowledgeAgent)
        assert agent._agent_name == AgentType.KNOWLEDGE.value
        assert agent._session_id == session_id
        assert agent._user_id == user_id

@pytest.mark.asyncio
async def test_knowledge_agent_has_tools():
    """Test that the Knowledge agent has the expected tools."""
    # Create test session and user IDs
    session_id = str(uuid.uuid4())
    user_id = "test-user"
    
    # Set up async mock for the agent definition
    async def mock_create_def(*args, **kwargs):
        return MagicMock()
        
    # Patch the method with our async mock
    with patch('kernel_agents.knowledge_agent.KnowledgeAgent._create_azure_ai_agent_definition', 
               side_effect=mock_create_def):
        
        # Create a memory store
        memory_store = MagicMock(spec=CosmosMemoryContext)
        
        # Create a Knowledge agent
        agent = await KnowledgeAgent.create(
            session_id=session_id,
            user_id=user_id,
            memory_store=memory_store,
            agent_name=AgentType.KNOWLEDGE.value,
        )
        
        # Verify the agent has tools
        assert agent._tools is not None
        assert len(agent._tools) > 0
        
        # Check for specific knowledge tools
        tools_dict = agent.plugins
        expected_tools = ["search_knowledge_base", "file_search", "get_knowledge_base_info"]
        
        for tool in expected_tools:
            assert tool in tools_dict, f"Missing expected tool: {tool}"

@pytest.mark.asyncio
async def test_knowledge_agent_handle_action_request():
    """Test that the Knowledge agent can handle an action request."""
    # Create test session and user IDs
    session_id = str(uuid.uuid4())
    user_id = "test-user"
    step_id = str(uuid.uuid4())
    plan_id = str(uuid.uuid4())
    
    # Create a memory store with mock
    memory_store = MagicMock(spec=CosmosMemoryContext)
    memory_store.get_step.return_value = MagicMock(
        id=step_id, 
        human_feedback="Please get information about the configured knowledge base",
        plan_id=plan_id,
        session_id=session_id
    )
    
    # Create the action request
    action_request = ActionRequest(
        step_id=step_id,
        plan_id=plan_id,
        session_id=session_id,
        action="Get information about the configured knowledge base",
        agent=AgentType.KNOWLEDGE,
    )
    
    # Set up async mock for the agent definition
    async def mock_create_def(*args, **kwargs):
        return MagicMock()
        
    # Patch the method with our async mock
    with patch('kernel_agents.knowledge_agent.KnowledgeAgent._create_azure_ai_agent_definition', 
               side_effect=mock_create_def):
        
        # Create a Knowledge agent
        agent = await KnowledgeAgent.create(
            session_id=session_id,
            user_id=user_id,
            memory_store=memory_store,
            agent_name=AgentType.KNOWLEDGE.value,
        )
        
        # Replace invoke method with a mock that returns information
        async def mock_invoke(*args, **kwargs):
            yield json.dumps({
                "ai_search": {"enabled": False},
                "file_search": {"enabled": False}
            })
        agent.invoke = mock_invoke
        
        # Mock necessary memory store methods to be async
        memory_store.add_item = AsyncMock()
        memory_store.update_step = AsyncMock()
        
        # Handle the action request
        response_json = await agent.handle_action_request(action_request)
        
        # Verify a response was returned
        assert response_json is not None
        
        # Check that memory store was called the right number of times
        assert memory_store.get_step.call_count == 1
        assert memory_store.add_item.call_count == 1
        assert memory_store.update_step.call_count == 1
