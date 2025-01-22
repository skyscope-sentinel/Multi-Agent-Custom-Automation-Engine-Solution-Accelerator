import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import sys

# Import functions under test
from src.backend.agents.product import (
    add_mobile_extras_pack,
    get_product_info,
    update_inventory,
    schedule_product_launch,
    analyze_sales_data,
    get_customer_feedback,
    manage_promotions,
    check_inventory,
    update_product_price,
    provide_product_recommendations,
    handle_product_recall,
    set_product_discount,
    manage_supply_chain,
    forecast_product_demand,
    handle_product_complaints,
    monitor_market_trends,
    generate_product_report,
    develop_new_product_ideas,
    optimize_product_page,
    track_product_shipment,
    evaluate_product_performance,
)

# Mock Azure dependencies
sys.modules["azure.monitor.events.extension"] = MagicMock()

# Mock environment variables for external dependencies
os.environ["COSMOSDB_ENDPOINT"] = "https://mock-endpoint"
os.environ["COSMOSDB_KEY"] = "mock-key"
os.environ["COSMOSDB_DATABASE"] = "mock-database"
os.environ["COSMOSDB_CONTAINER"] = "mock-container"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "mock-deployment-name"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-01-01"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://mock-openai-endpoint"


# Fixture to mock Azure credentials globally
@pytest.fixture(autouse=True)
def mock_azure_credentials():
    """Mock Azure DefaultAzureCredential for all tests."""
    with patch("azure.identity.aio.DefaultAzureCredential") as mock_cred:
        mock_cred.return_value.get_token = AsyncMock(return_value={"token": "mock-token"})
        yield


# Test cases for all product functions

@pytest.mark.asyncio
async def test_add_mobile_extras_pack():
    try:
        result = await add_mobile_extras_pack("Roaming Pack", "2025-01-01")
        assert "Roaming Pack" in result
        assert "2025-01-01" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_get_product_info():
    try:
        result = await get_product_info()
        assert "Simulated Phone Plans" in result
        assert "Plan A" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_update_inventory():
    try:
        result = await update_inventory("Product A", 50)
        assert "Inventory for" in result
        assert "Product A" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_schedule_product_launch():
    try:
        result = await schedule_product_launch("New Product", "2025-02-01")
        assert "New Product" in result
        assert "2025-02-01" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_analyze_sales_data():
    try:
        result = await analyze_sales_data("Product B", "Last Quarter")
        assert "Sales data for" in result
        assert "Product B" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_get_customer_feedback():
    try:
        result = await get_customer_feedback("Product C")
        assert "Customer feedback for" in result
        assert "Product C" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_manage_promotions():
    try:
        result = await manage_promotions("Product A", "10% off for summer")
        assert "Promotion for" in result
        assert "Product A" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_handle_product_recall():
    try:
        result = await handle_product_recall("Product A", "Defective batch")
        assert "Product recall for" in result
        assert "Defective batch" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_set_product_discount():
    try:
        result = await set_product_discount("Product A", 15.0)
        assert "Discount for" in result
        assert "15.0%" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_manage_supply_chain():
    try:
        result = await manage_supply_chain("Product A", "Supplier X")
        assert "Supply chain for" in result
        assert "Supplier X" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_check_inventory():
    try:
        result = await check_inventory("Product A")
        assert "Inventory status for" in result
        assert "Product A" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_update_product_price():
    try:
        result = await update_product_price("Product A", 99.99)
        assert "Price for" in result
        assert "$99.99" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_provide_product_recommendations():
    try:
        result = await provide_product_recommendations("High Performance")
        assert "Product recommendations based on preferences" in result
        assert "High Performance" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_forecast_product_demand():
    try:
        result = await forecast_product_demand("Product A", "Next Month")
        assert "Demand for" in result
        assert "Next Month" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_handle_product_complaints():
    try:
        result = await handle_product_complaints("Product A", "Complaint about quality")
        assert "Complaint for" in result
        assert "Product A" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_monitor_market_trends():
    try:
        result = await monitor_market_trends()
        assert "Market trends monitored" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_generate_product_report():
    try:
        result = await generate_product_report("Product A", "Sales")
        assert "Sales report for" in result
        assert "Product A" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_develop_new_product_ideas():
    try:
        result = await develop_new_product_ideas("Smartphone X with AI Camera")
        assert "New product idea developed" in result
        assert "Smartphone X" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_optimize_product_page():
    try:
        result = await optimize_product_page("Product A", "SEO optimization and faster loading")
        assert "Product page for" in result
        assert "optimized" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_track_product_shipment():
    try:
        result = await track_product_shipment("Product A", "1234567890")
        assert "Shipment for" in result
        assert "1234567890" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_evaluate_product_performance():
    try:
        result = await evaluate_product_performance("Product A", "Customer reviews and sales data")
        assert "Performance of" in result
        assert "evaluated based on" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_update_product_price_maximum():
    try:
        result = await update_product_price("Product I", 999999.99)
        assert "Price for" in result
        assert "$999999.99" in result
    finally:
        pass


@pytest.mark.asyncio
async def test_update_product_price_high_precision():
    try:
        result = await update_product_price("Product AG", 123.456789)
        assert "Price for **'Product AG'** updated to **$123.46**." in result
    finally:
        pass
