import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from azure.cosmos.partition_key import PartitionKey
from src.backend.context.cosmos_memory import CosmosBufferedChatCompletionContext

# Mock environment variables
@pytest.fixture(autouse=True)
def mock_env_variables(monkeypatch):
    """Mock all required environment variables."""
    env_vars = {
        "COSMOSDB_ENDPOINT": "https://mock-endpoint",
        "COSMOSDB_KEY": "mock-key",
        "COSMOSDB_DATABASE": "mock-database",
        "COSMOSDB_CONTAINER": "mock-container",
        "AZURE_OPENAI_DEPLOYMENT_NAME": "mock-deployment-name",
        "AZURE_OPENAI_API_VERSION": "2023-01-01",
        "AZURE_OPENAI_ENDPOINT": "https://mock-openai-endpoint",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)


@pytest.fixture(autouse=True)
def mock_azure_credentials():
    """Mock Azure DefaultAzureCredential for all tests."""
    with patch("azure.identity.aio.DefaultAzureCredential") as mock_cred:
        mock_cred.return_value.get_token = AsyncMock(return_value={"token": "mock-token"})
        yield


@pytest.fixture
def mock_cosmos_client():
    """Fixture for mocking Cosmos DB client and container."""
    mock_client = AsyncMock()
    mock_container = AsyncMock()
    mock_client.create_container_if_not_exists.return_value = mock_container
    return mock_client, mock_container


@pytest.fixture
def mock_config(mock_cosmos_client):
    """Fixture to patch Config with mock Cosmos DB client."""
    mock_client, _ = mock_cosmos_client
    with patch(
        "src.backend.config.Config.GetCosmosDatabaseClient", return_value=mock_client
    ), patch("src.backend.config.Config.COSMOSDB_CONTAINER", "mock-container"):
        yield


async def async_iterable(mock_items):
    """Helper to create an async iterable."""
    for item in mock_items:
        yield item


@pytest.mark.asyncio(loop_scope="session")
async def test_initialize(mock_config, mock_cosmos_client):
    """Test if the Cosmos DB container is initialized correctly."""
    mock_client, mock_container = mock_cosmos_client
    async with CosmosBufferedChatCompletionContext(
        session_id="test_session", user_id="test_user"
    ) as context:
        await context.initialize()
        mock_client.create_container_if_not_exists.assert_called_once_with(
            id="mock-container", partition_key=PartitionKey(path="/session_id")
        )
        assert context._container == mock_container


@pytest.mark.asyncio(loop_scope="session")
async def test_close_without_initialization(mock_config):
    """Test closing the context without prior initialization."""
    async with CosmosBufferedChatCompletionContext(
        session_id="test_session", user_id="test_user"
    ):
        pass  # Ensure proper cleanup without initialization


@pytest.mark.asyncio(loop_scope="session")
async def test_add_item(mock_config, mock_cosmos_client):
    """Test adding an item to Cosmos DB."""
    _, mock_container = mock_cosmos_client
    mock_item = MagicMock()
    mock_item.model_dump.return_value = {"id": "test-item", "data": "test-data"}

    async with CosmosBufferedChatCompletionContext(
        session_id="test_session", user_id="test_user"
    ) as context:
        await context.initialize()
        await context.add_item(mock_item)
        mock_container.create_item.assert_called_once_with(
            body={"id": "test-item", "data": "test-data"}
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_update_item(mock_config, mock_cosmos_client):
    """Test updating an item in Cosmos DB."""
    _, mock_container = mock_cosmos_client
    mock_item = MagicMock()
    mock_item.model_dump.return_value = {"id": "test-item", "data": "updated-data"}

    async with CosmosBufferedChatCompletionContext(
        session_id="test_session", user_id="test_user"
    ) as context:
        await context.initialize()
        await context.update_item(mock_item)
        mock_container.upsert_item.assert_called_once_with(
            body={"id": "test-item", "data": "updated-data"}
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_item_by_id(mock_config, mock_cosmos_client):
    """Test retrieving an item by ID from Cosmos DB."""
    _, mock_container = mock_cosmos_client
    mock_item = {"id": "test-item", "data": "retrieved-data"}
    mock_container.read_item.return_value = mock_item

    mock_model_class = MagicMock()
    mock_model_class.model_validate.return_value = "validated_item"

    async with CosmosBufferedChatCompletionContext(
        session_id="test_session", user_id="test_user"
    ) as context:
        await context.initialize()
        result = await context.get_item_by_id(
            "test-item", "test-partition", mock_model_class
        )

        assert result == "validated_item"
        mock_container.read_item.assert_called_once_with(
            item="test-item", partition_key="test-partition"
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_item(mock_config, mock_cosmos_client):
    """Test deleting an item from Cosmos DB."""
    _, mock_container = mock_cosmos_client

    async with CosmosBufferedChatCompletionContext(
        session_id="test_session", user_id="test_user"
    ) as context:
        await context.initialize()
        await context.delete_item("test-item", "test-partition")

        mock_container.delete_item.assert_called_once_with(
            item="test-item", partition_key="test-partition"
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_add_plan(mock_config, mock_cosmos_client):
    """Test adding a plan to Cosmos DB."""
    _, mock_container = mock_cosmos_client
    mock_plan = MagicMock()
    mock_plan.model_dump.return_value = {"id": "plan1", "data": "plan-data"}

    async with CosmosBufferedChatCompletionContext(
        session_id="test_session", user_id="test_user"
    ) as context:
        await context.initialize()
        await context.add_plan(mock_plan)

        mock_container.create_item.assert_called_once_with(
            body={"id": "plan1", "data": "plan-data"}
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_update_plan(mock_config, mock_cosmos_client):
    """Test updating a plan in Cosmos DB."""
    _, mock_container = mock_cosmos_client
    mock_plan = MagicMock()
    mock_plan.model_dump.return_value = {
        "id": "plan1",
        "data": "updated-plan-data",
    }

    async with CosmosBufferedChatCompletionContext(
        session_id="test_session", user_id="test_user"
    ) as context:
        await context.initialize()
        await context.update_plan(mock_plan)

        mock_container.upsert_item.assert_called_once_with(
            body={"id": "plan1", "data": "updated-plan-data"}
        )

