import sys
import os
from unittest.mock import MagicMock
import unittest
sys.modules["azure.monitor.events.extension"] = MagicMock()
os.environ["COSMOSDB_ENDPOINT"] = "https://mock-endpoint"
os.environ["COSMOSDB_KEY"] = "mock-key"
os.environ["COSMOSDB_DATABASE"] = "mock-database"
os.environ["COSMOSDB_CONTAINER"] = "mock-container"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "mock-deployment-name"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-01-01"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://mock-openai-endpoint"
from autogen_core.components.models import AzureOpenAIChatCompletionClient
from autogen_core.base import AgentId
from src.backend.context.cosmos_memory import CosmosBufferedChatCompletionContext
from src.backend.agents.generic import get_generic_tools, GenericAgent, dummy_function


class TestGenericAgent(unittest.TestCase):
    def setUp(self):
        self.mock_model_client = MagicMock(spec=AzureOpenAIChatCompletionClient)
        self.mock_session_id = "test_session_id"
        self.mock_user_id = "test_user_id"
        self.mock_memory = MagicMock(spec=CosmosBufferedChatCompletionContext)
        self.mock_tools = get_generic_tools()
        self.mock_agent_id = MagicMock(spec=AgentId)


class TestDummyFunction(unittest.IsolatedAsyncioTestCase):
    async def test_dummy_function(self):
        result = await dummy_function()
        self.assertEqual(result, "This is a placeholder function")


if __name__ == "__main__":
    unittest.main()
