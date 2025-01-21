import os
import pytest
from unittest.mock import MagicMock

# Mock the azure.monitor.events.extension module globally
import sys
sys.modules['azure.monitor.events.extension'] = MagicMock()

# Set environment variables to mock dependencies
os.environ["COSMOSDB_ENDPOINT"] = "https://mock-endpoint"
os.environ["COSMOSDB_KEY"] = "mock-key"
os.environ["COSMOSDB_DATABASE"] = "mock-database"
os.environ["COSMOSDB_CONTAINER"] = "mock-container"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "mock-deployment-name"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-01-01"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://mock-openai-endpoint"

# Import functions directly from product.py for testing
from src.backend.agents.product import (
    add_mobile_extras_pack,
    get_product_info,
    update_inventory,
    schedule_product_launch,
    analyze_sales_data,
    get_customer_feedback,
    manage_promotions,
    set_reorder_level,
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


# Test cases for existing functions
@pytest.mark.asyncio
async def test_add_mobile_extras_pack():
    result = await add_mobile_extras_pack("Roaming Pack", "2025-01-01")
    assert "Roaming Pack" in result
    assert "2025-01-01" in result


@pytest.mark.asyncio
async def test_get_product_info():
    result = await get_product_info()
    assert "Simulated Phone Plans" in result
    assert "Plan A" in result


@pytest.mark.asyncio
async def test_update_inventory():
    result = await update_inventory("Product A", 50)
    assert "Inventory for" in result
    assert "Product A" in result


@pytest.mark.asyncio
async def test_schedule_product_launch():
    result = await schedule_product_launch("New Product", "2025-02-01")
    assert "New Product" in result
    assert "2025-02-01" in result


@pytest.mark.asyncio
async def test_analyze_sales_data():
    result = await analyze_sales_data("Product B", "Last Quarter")
    assert "Sales data for" in result
    assert "Product B" in result


@pytest.mark.asyncio
async def test_get_customer_feedback():
    result = await get_customer_feedback("Product C")
    assert "Customer feedback for" in result
    assert "Product C" in result


@pytest.mark.asyncio
async def test_manage_promotions():
    result = await manage_promotions("Product A", "10% off for summer")
    assert "Promotion for" in result
    assert "Product A" in result


@pytest.mark.asyncio
async def test_handle_product_recall():
    result = await handle_product_recall("Product A", "Defective batch")
    assert "Product recall for" in result
    assert "Defective batch" in result


@pytest.mark.asyncio
async def test_set_product_discount():
    result = await set_product_discount("Product A", 15.0)
    assert "Discount for" in result
    assert "15.0%" in result


@pytest.mark.asyncio
async def test_manage_supply_chain():
    result = await manage_supply_chain("Product A", "Supplier X")
    assert "Supply chain for" in result
    assert "Supplier X" in result


@pytest.mark.asyncio
async def test_check_inventory():
    result = await check_inventory("Product A")
    assert "Inventory status for" in result
    assert "Product A" in result


@pytest.mark.asyncio
async def test_update_product_price():
    result = await update_product_price("Product A", 99.99)
    assert "Price for" in result
    assert "$99.99" in result


@pytest.mark.asyncio
async def test_provide_product_recommendations():
    result = await provide_product_recommendations("High Performance")
    assert "Product recommendations based on preferences" in result
    assert "High Performance" in result


# Additional Test Cases
@pytest.mark.asyncio
async def test_forecast_product_demand():
    result = await forecast_product_demand("Product A", "Next Month")
    assert "Demand for" in result
    assert "Next Month" in result


@pytest.mark.asyncio
async def test_handle_product_complaints():
    result = await handle_product_complaints("Product A", "Complaint about quality")
    assert "Complaint for" in result
    assert "Product A" in result


@pytest.mark.asyncio
async def test_monitor_market_trends():
    result = await monitor_market_trends()
    assert "Market trends monitored" in result


@pytest.mark.asyncio
async def test_generate_product_report():
    result = await generate_product_report("Product A", "Sales")
    assert "Sales report for" in result
    assert "Product A" in result


@pytest.mark.asyncio
async def test_develop_new_product_ideas():
    result = await develop_new_product_ideas("Smartphone X with AI Camera")
    assert "New product idea developed" in result
    assert "Smartphone X" in result


@pytest.mark.asyncio
async def test_optimize_product_page():
    result = await optimize_product_page("Product A", "SEO optimization and faster loading")
    assert "Product page for" in result
    assert "optimized" in result


@pytest.mark.asyncio
async def test_track_product_shipment():
    result = await track_product_shipment("Product A", "1234567890")
    assert "Shipment for" in result
    assert "1234567890" in result


@pytest.mark.asyncio
async def test_evaluate_product_performance():
    result = await evaluate_product_performance("Product A", "Customer reviews and sales data")
    assert "Performance of" in result
    assert "evaluated based on" in result

# Additional Coverage Test
@pytest.mark.asyncio
async def test_manage_supply_chain_edge_case():
    result = await manage_supply_chain("Product B", "New Supplier")
    assert "Supply chain for" in result
    assert "New Supplier" in result

@pytest.mark.asyncio
async def test_optimize_product_page_with_special_chars():
    result = await optimize_product_page("Product A", "Optimize SEO & Speed 🚀")
    assert "Product page for" in result
    assert "Optimize SEO & Speed 🚀" in result

# Tests with valid inputs for uncovered functions
@pytest.mark.asyncio
async def test_set_reorder_level_valid():
    result = await set_reorder_level("Product A", 10)
    assert "Reorder level for" in result
    assert "Product A" in result
    assert "10" in result


@pytest.mark.asyncio
async def test_add_mobile_extras_pack_valid():
    result = await add_mobile_extras_pack("Unlimited Data Pack", "2025-05-01")
    assert "Unlimited Data Pack" in result
    assert "2025-05-01" in result


@pytest.mark.asyncio
async def test_handle_product_recall_valid():
    result = await handle_product_recall("Product B", "Safety concerns")
    assert "Product recall for" in result
    assert "Product B" in result
    assert "Safety concerns" in result    


@pytest.mark.asyncio
async def test_update_inventory_with_zero_quantity():
    result = await update_inventory("Product A", 0)
    assert "Inventory for" in result
    assert "Product A" in result
    assert "0" in result

@pytest.mark.asyncio
async def test_set_reorder_level_with_large_value():
    result = await set_reorder_level("Product B", 100000)
    assert "Reorder level for" in result
    assert "Product B" in result
    assert "100000" in result

@pytest.mark.asyncio
async def test_analyze_sales_data_with_long_period():
    result = await analyze_sales_data("Product C", "Last 5 Years")
    assert "Sales data for" in result
    assert "Last 5 Years" in result

# Test `update_inventory` with negative quantity (boundary case)
@pytest.mark.asyncio
async def test_update_inventory_with_negative_quantity():
    result = await update_inventory("Product D", -10)
    assert "Inventory for" in result
    assert "Product D" in result
    assert "-10" in result

# Test `update_product_price` with maximum valid price
@pytest.mark.asyncio
async def test_update_product_price_maximum():
    result = await update_product_price("Product I", 999999.99)
    assert "Price for" in result
    assert "$999999.99" in result

# Test `add_mobile_extras_pack` with a very long pack name
@pytest.mark.asyncio
async def test_add_mobile_extras_pack_long_name():
    long_pack_name = "Extra Pack" + " with extended features " * 50
    result = await add_mobile_extras_pack(long_pack_name, "2025-12-31")
    assert long_pack_name in result
    assert "2025-12-31" in result

# Test `schedule_product_launch` with invalid date format
@pytest.mark.asyncio
async def test_schedule_product_launch_invalid_date():
    result = await schedule_product_launch("Product J", "31-12-2025")
    assert "launch scheduled on **31-12-2025**" in result

# Test `generate_product_report` with no report type
@pytest.mark.asyncio
async def test_generate_product_report_no_type():
    result = await generate_product_report("Product K", "")
    assert "report for **'Product K'** generated." in result

# Test `forecast_product_demand` with extremely large period
@pytest.mark.asyncio
async def test_forecast_product_demand_large_period():
    result = await forecast_product_demand("Product L", "Next 100 Years")
    assert "Demand for **'Product L'** forecasted for **Next 100 Years**." in result

# Test `evaluate_product_performance` with missing performance metrics
@pytest.mark.asyncio
async def test_evaluate_product_performance_no_metrics():
    result = await evaluate_product_performance("Product M", "")
    assert "Performance of **'Product M'** evaluated" in result

# Test `set_reorder_level` with zero value
@pytest.mark.asyncio
async def test_set_reorder_level_zero():
    result = await set_reorder_level("Product N", 0)
    assert "Reorder level for **'Product N'** set to **0** units." in result

# Test `update_inventory` with very large quantity
@pytest.mark.asyncio
async def test_update_inventory_large_quantity():
    result = await update_inventory("Product O", 100000000)
    assert "Inventory for **'Product O'** updated by **100000000** units." in result

# Test `check_inventory` with product name containing special characters
@pytest.mark.asyncio
async def test_check_inventory_special_name():
    result = await check_inventory("@Product#1!")
    assert "Inventory status for **'@Product#1!'** checked." in result

# Test `handle_product_recall` with empty reason
@pytest.mark.asyncio
async def test_handle_product_recall_no_reason():
    result = await handle_product_recall("Product P", "")
    assert "Product recall for **'Product P'** initiated due to:" in result

# Test `manage_supply_chain` with empty supplier name
@pytest.mark.asyncio
async def test_manage_supply_chain_empty_supplier():
    result = await manage_supply_chain("Product Q", "")
    assert "Supply chain for **'Product Q'** managed with supplier" in result

# Test `analyze_sales_data` with an invalid time period
@pytest.mark.asyncio
async def test_analyze_sales_data_invalid_period():
    result = await analyze_sales_data("Product R", "InvalidPeriod")
    assert "Sales data for **'Product R'** over **InvalidPeriod** analyzed." in result    

# Test `update_product_price` with zero price
@pytest.mark.asyncio
async def test_update_product_price_zero():
    result = await update_product_price("Product S", 0.0)
    assert "Price for **'Product S'** updated to **$0.00**." in result

# Test `monitor_market_trends` with no trends data available
@pytest.mark.asyncio
async def test_monitor_market_trends_no_data():
    result = await monitor_market_trends()
    assert "Market trends monitored and data updated." in result
    
# Test `generate_product_report` with special characters in report type
@pytest.mark.asyncio
async def test_generate_product_report_special_type():
    result = await generate_product_report("Product U", "Sales/Performance")
    assert "report for **'Product U'** generated." in result
    assert "Sales/Performance" in result

# Test `evaluate_product_performance` with multiple metrics
@pytest.mark.asyncio
async def test_evaluate_product_performance_multiple_metrics():
    result = await evaluate_product_performance("Product V", "Customer reviews, sales, and returns")
    assert "Performance of **'Product V'** evaluated" in result
    assert "Customer reviews, sales, and returns" in result

# Test `schedule_product_launch` with no product name
@pytest.mark.asyncio
async def test_schedule_product_launch_no_name():
    result = await schedule_product_launch("", "2025-12-01")
    assert "launch scheduled on **2025-12-01**" in result

# Test `set_product_discount` with an unusually high discount
@pytest.mark.asyncio
async def test_set_product_discount_high_value():
    result = await set_product_discount("Product X", 95.0)
    assert "Discount for **'Product X'**" in result
    assert "95.0%" in result

# Test `monitor_market_trends` for a specific market
@pytest.mark.asyncio
async def test_monitor_market_trends_specific_market():
    result = await monitor_market_trends()
    assert "Market trends monitored and data updated." in result

# Test `provide_product_recommendations` with multiple preferences
@pytest.mark.asyncio
async def test_provide_product_recommendations_multiple_preferences():
    result = await provide_product_recommendations("High Performance, Affordability, Durability")
    assert "Product recommendations based on preferences" in result
    assert "High Performance, Affordability, Durability" in result

# Test `handle_product_complaints` with extensive complaint details
@pytest.mark.asyncio
async def test_handle_product_complaints_detailed():
    detailed_complaint = (
        "The product arrived damaged, the packaging was insufficient, and the user manual was missing."
    )
    result = await handle_product_complaints("Product Y", detailed_complaint)
    assert "Complaint for **'Product Y'**" in result
    assert detailed_complaint in result

# Test `update_product_price` with a very low price
@pytest.mark.asyncio
async def test_update_product_price_low_value():
    result = await update_product_price("Product Z", 0.01)
    assert "Price for **'Product Z'** updated to **$0.01**." in result

# Test `develop_new_product_ideas` with highly detailed input
@pytest.mark.asyncio
async def test_develop_new_product_ideas_detailed():
    detailed_idea = "Smartphone Z with a foldable screen, AI camera, and integrated AR capabilities."
    result = await develop_new_product_ideas(detailed_idea)
    assert "New product idea developed" in result
    assert detailed_idea in result


# Test `forecast_product_demand` with unusual input
@pytest.mark.asyncio
async def test_forecast_product_demand_unusual():
    result = await forecast_product_demand("Product AA", "Next 1000 Days")
    assert "Demand for **'Product AA'** forecasted for **Next 1000 Days**." in result

# Test `set_reorder_level` with extremely high value
@pytest.mark.asyncio
async def test_set_reorder_level_high():
    result = await set_reorder_level("Product AB", 10000000)
    assert "Reorder level for **'Product AB'** set to **10000000** units." in result

# Test `update_inventory` with fractional quantity
@pytest.mark.asyncio
async def test_update_inventory_fractional_quantity():
    result = await update_inventory("Product AD", 5.5)
    assert "Inventory for **'Product AD'** updated by **5.5** units." in result

# Test `analyze_sales_data` with unusual product name
@pytest.mark.asyncio
async def test_analyze_sales_data_unusual_name():
    result = await analyze_sales_data("💡UniqueProduct✨", "Last Month")
    assert "Sales data for **'💡UniqueProduct✨'**" in result

# Test `generate_product_report` with detailed report type
@pytest.mark.asyncio
async def test_generate_product_report_detailed_type():
    detailed_type = "Annual Sales Report with Profit Margin Analysis"
    result = await generate_product_report("Product AE", detailed_type)
    assert f"report for **'Product AE'** generated" in result
    assert detailed_type in result

# Test `update_product_price` with a very high precision value
@pytest.mark.asyncio
async def test_update_product_price_high_precision():
    result = await update_product_price("Product AG", 123.456789)
    assert "Price for **'Product AG'** updated to **$123.46**." in result

