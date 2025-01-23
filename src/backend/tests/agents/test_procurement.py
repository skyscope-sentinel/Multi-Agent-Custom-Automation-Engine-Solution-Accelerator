import os
import sys
import asyncio
import pytest
from unittest.mock import MagicMock

# Import the procurement tools for testing
from src.backend.agents.procurement import (
    order_hardware,
    order_software_license,
    check_inventory,
    process_purchase_order,
    initiate_contract_negotiation,
    approve_invoice,
    track_order,
    manage_vendor_relationship,
    update_procurement_policy,
    generate_procurement_report,
    evaluate_supplier_performance,
    handle_return,
    process_payment,
    request_quote,
    recommend_sourcing_options,
    update_asset_register,
    conduct_market_research,
    audit_inventory,
    approve_budget,
    manage_import_licenses,
    allocate_budget,
    track_procurement_metrics,
)

# Mock dependencies
sys.modules["azure.monitor.events.extension"] = MagicMock()

os.environ["COSMOSDB_ENDPOINT"] = "https://mock-endpoint"
os.environ["COSMOSDB_KEY"] = "mock-key"
os.environ["COSMOSDB_DATABASE"] = "mock-database"
os.environ["COSMOSDB_CONTAINER"] = "mock-container"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "mock-deployment-name"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-01-01"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://mock-openai-endpoint"


# Test cases for async functions with loop_scope
@pytest.mark.asyncio(loop_scope="session")
async def test_order_hardware():
    result = await order_hardware("laptop", 10)
    assert "Ordered 10 units of laptop." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_order_software_license():
    result = await order_software_license("Photoshop", "team", 5)
    assert "Ordered 5 team licenses of Photoshop." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_check_inventory():
    result = await check_inventory("printer")
    assert "Inventory status of printer: In Stock." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_process_purchase_order():
    result = await process_purchase_order("PO12345")
    assert "Purchase Order PO12345 has been processed." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_initiate_contract_negotiation():
    result = await initiate_contract_negotiation("VendorX", "Exclusive deal for 2025")
    assert (
        "Contract negotiation initiated with VendorX: Exclusive deal for 2025" in result
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_approve_invoice():
    result = await approve_invoice("INV001")
    assert "Invoice INV001 approved for payment." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_track_order():
    result = await track_order("ORDER123")
    assert "Order ORDER123 is currently in transit." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_manage_vendor_relationship():
    result = await manage_vendor_relationship("VendorY", "renewed")
    assert "Vendor relationship with VendorY has been renewed." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_update_procurement_policy():
    result = await update_procurement_policy(
        "Policy2025", "Updated terms and conditions"
    )
    assert "Procurement policy 'Policy2025' updated." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_generate_procurement_report():
    result = await generate_procurement_report("Annual")
    assert "Generated Annual procurement report." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_evaluate_supplier_performance():
    result = await evaluate_supplier_performance("SupplierZ")
    assert "Performance evaluation for supplier SupplierZ completed." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_handle_return():
    result = await handle_return("Laptop", 3, "Defective screens")
    assert "Processed return of 3 units of Laptop due to Defective screens." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_process_payment():
    result = await process_payment("VendorA", 5000.00)
    assert "Processed payment of $5000.00 to VendorA." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_request_quote():
    result = await request_quote("Tablet", 20)
    assert "Requested quote for 20 units of Tablet." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_recommend_sourcing_options():
    result = await recommend_sourcing_options("Projector")
    assert "Sourcing options for Projector have been provided." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_update_asset_register():
    result = await update_asset_register("ServerX", "Deployed in Data Center")
    assert "Asset register updated for ServerX: Deployed in Data Center" in result


@pytest.mark.asyncio(loop_scope="session")
async def test_conduct_market_research():
    result = await conduct_market_research("Electronics")
    assert "Market research conducted for category: Electronics" in result


@pytest.mark.asyncio(loop_scope="session")
async def test_audit_inventory():
    result = await audit_inventory()
    assert "Inventory audit has been conducted." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_approve_budget():
    result = await approve_budget("BUD001", 25000.00)
    assert "Approved budget ID BUD001 for amount $25000.00." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_manage_import_licenses():
    result = await manage_import_licenses("Smartphones", "License12345")
    assert "Import license for Smartphones managed: License12345." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_allocate_budget():
    result = await allocate_budget("IT Department", 150000.00)
    assert "Allocated budget of $150000.00 to IT Department." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_track_procurement_metrics():
    result = await track_procurement_metrics("Cost Savings")
    assert "Procurement metric 'Cost Savings' tracked." in result


@pytest.mark.asyncio(loop_scope="session")
async def test_edge_cases():
    result_handle_return_negative = await handle_return("Monitor", -5, "Damaged")
    result_handle_return_zero = await handle_return("Monitor", 0, "Packaging Issue")
    result_order_hardware_large = await order_hardware("Monitor", 1000000)
    result_order_hardware_missing = await order_hardware("", 5)
    result_payment_large = await process_payment("VendorX", 1e7)
    result_payment_no_vendor = await process_payment("", 500.00)

    assert "Processed return of -5 units of Monitor due to Damaged." in result_handle_return_negative
    assert "Processed return of 0 units of Monitor due to Packaging Issue." in result_handle_return_zero
    assert "Ordered 1000000 units of Monitor." in result_order_hardware_large
    assert "Ordered 5 units of ." in result_order_hardware_missing
    assert "Processed payment of $10000000.00 to VendorX." in result_payment_large
    assert "Processed payment of $500.00 to ." in result_payment_no_vendor
