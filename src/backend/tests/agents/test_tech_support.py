import os
import sys
import pytest
from unittest.mock import MagicMock
from autogen_core.components.tools import FunctionTool

# Import the functions under test
from src.backend.agents.tech_support import (
    send_welcome_email,
    set_up_office_365_account,
    configure_laptop,
    reset_password,
    setup_vpn_access,
    troubleshoot_network_issue,
    install_software,
    update_software,
    manage_data_backup,
    handle_cybersecurity_incident,
    assist_procurement_with_tech_equipment,
    collaborate_with_code_deployment,
    provide_tech_support_for_marketing,
    assist_product_launch,
    implement_it_policy,
    manage_cloud_service,
    configure_server,
    grant_database_access,
    provide_tech_training,
    configure_printer,
    set_up_email_signature,
    configure_mobile_device,
    set_up_remote_desktop,
    troubleshoot_hardware_issue,
    manage_network_security,
    update_firmware,
    assist_with_video_conferencing_setup,
    manage_it_inventory,
    configure_firewall_rules,
    manage_virtual_machines,
    provide_tech_support_for_event,
    configure_network_storage,
    set_up_two_factor_authentication,
    troubleshoot_email_issue,
    manage_it_helpdesk_tickets,
    handle_software_bug_report,
    assist_with_data_recovery,
    manage_system_updates,
    configure_digital_signatures,
    provide_remote_tech_support,
    manage_network_bandwidth,
    assist_with_tech_documentation,
    monitor_system_performance,
    get_tech_support_tools,
)

# Mock the azure.monitor.events.extension module globally
sys.modules["azure.monitor.events.extension"] = MagicMock()

# Set environment variables to mock Config dependencies
os.environ["COSMOSDB_ENDPOINT"] = "https://mock-endpoint"
os.environ["COSMOSDB_KEY"] = "mock-key"
os.environ["COSMOSDB_DATABASE"] = "mock-database"
os.environ["COSMOSDB_CONTAINER"] = "mock-container"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "mock-deployment-name"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-01-01"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://mock-openai-endpoint"


@pytest.mark.asyncio
async def test_collaborate_with_code_deployment():
    result = await collaborate_with_code_deployment("AI Deployment Project")
    assert "Code Deployment Collaboration" in result
    assert "AI Deployment Project" in result


@pytest.mark.asyncio
async def test_send_welcome_email():
    result = await send_welcome_email("John Doe", "john.doe@example.com")
    assert "Welcome Email Sent" in result
    assert "John Doe" in result
    assert "john.doe@example.com" in result


@pytest.mark.asyncio
async def test_set_up_office_365_account():
    result = await set_up_office_365_account("Jane Smith", "jane.smith@example.com")
    assert "Office 365 Account Setup" in result
    assert "Jane Smith" in result
    assert "jane.smith@example.com" in result


@pytest.mark.asyncio
async def test_configure_laptop():
    result = await configure_laptop("John Doe", "Dell XPS 15")
    assert "Laptop Configuration" in result
    assert "Dell XPS 15" in result


@pytest.mark.asyncio
async def test_reset_password():
    result = await reset_password("John Doe")
    assert "Password Reset" in result
    assert "John Doe" in result


@pytest.mark.asyncio
async def test_setup_vpn_access():
    result = await setup_vpn_access("John Doe")
    assert "VPN Access Setup" in result
    assert "John Doe" in result


@pytest.mark.asyncio
async def test_troubleshoot_network_issue():
    result = await troubleshoot_network_issue("Slow internet")
    assert "Network Issue Resolved" in result
    assert "Slow internet" in result


@pytest.mark.asyncio
async def test_install_software():
    result = await install_software("Jane Doe", "Adobe Photoshop")
    assert "Software Installation" in result
    assert "Adobe Photoshop" in result


@pytest.mark.asyncio
async def test_update_software():
    result = await update_software("John Doe", "Microsoft Office")
    assert "Software Update" in result
    assert "Microsoft Office" in result


@pytest.mark.asyncio
async def test_manage_data_backup():
    result = await manage_data_backup("Jane Smith")
    assert "Data Backup Managed" in result
    assert "Jane Smith" in result


@pytest.mark.asyncio
async def test_handle_cybersecurity_incident():
    result = await handle_cybersecurity_incident("Phishing email detected")
    assert "Cybersecurity Incident Handled" in result
    assert "Phishing email detected" in result


@pytest.mark.asyncio
async def test_assist_procurement_with_tech_equipment():
    result = await assist_procurement_with_tech_equipment("Dell Workstation specs")
    assert "Technical Specifications Provided" in result
    assert "Dell Workstation specs" in result


@pytest.mark.asyncio
async def test_provide_tech_support_for_marketing():
    result = await provide_tech_support_for_marketing("Holiday Campaign")
    assert "Tech Support for Marketing Campaign" in result
    assert "Holiday Campaign" in result


@pytest.mark.asyncio
async def test_assist_product_launch():
    result = await assist_product_launch("Smartphone X")
    assert "Tech Support for Product Launch" in result
    assert "Smartphone X" in result


@pytest.mark.asyncio
async def test_implement_it_policy():
    result = await implement_it_policy("Data Retention Policy")
    assert "IT Policy Implemented" in result
    assert "Data Retention Policy" in result


@pytest.mark.asyncio
async def test_manage_cloud_service():
    result = await manage_cloud_service("AWS S3")
    assert "Cloud Service Managed" in result
    assert "AWS S3" in result


@pytest.mark.asyncio
async def test_configure_server():
    result = await configure_server("Database Server")
    assert "Server Configuration" in result
    assert "Database Server" in result


@pytest.mark.asyncio
async def test_grant_database_access():
    result = await grant_database_access("Alice", "SalesDB")
    assert "Database Access Granted" in result
    assert "Alice" in result
    assert "SalesDB" in result


@pytest.mark.asyncio
async def test_provide_tech_training():
    result = await provide_tech_training("Bob", "VPN Tool")
    assert "Tech Training Provided" in result
    assert "Bob" in result
    assert "VPN Tool" in result


@pytest.mark.asyncio
async def test_configure_printer():
    result = await configure_printer("Charlie", "HP LaserJet 123")
    assert "Printer Configuration" in result
    assert "Charlie" in result
    assert "HP LaserJet 123" in result


@pytest.mark.asyncio
async def test_set_up_email_signature():
    result = await set_up_email_signature("Derek", "Best regards, Derek")
    assert "Email Signature Setup" in result
    assert "Derek" in result
    assert "Best regards, Derek" in result


@pytest.mark.asyncio
async def test_configure_mobile_device():
    result = await configure_mobile_device("Emily", "iPhone 13")
    assert "Mobile Device Configuration" in result
    assert "Emily" in result
    assert "iPhone 13" in result


@pytest.mark.asyncio
async def test_set_up_remote_desktop():
    result = await set_up_remote_desktop("Frank")
    assert "Remote Desktop Setup" in result
    assert "Frank" in result


@pytest.mark.asyncio
async def test_troubleshoot_hardware_issue():
    result = await troubleshoot_hardware_issue("Laptop overheating")
    assert "Hardware Issue Resolved" in result
    assert "Laptop overheating" in result


@pytest.mark.asyncio
async def test_manage_network_security():
    result = await manage_network_security()
    assert "Network Security Managed" in result


@pytest.mark.asyncio
async def test_update_firmware():
    result = await update_firmware("Router X", "v1.2.3")
    assert "Firmware Updated" in result
    assert "Router X" in result
    assert "v1.2.3" in result


@pytest.mark.asyncio
async def test_assist_with_video_conferencing_setup():
    result = await assist_with_video_conferencing_setup("Grace", "Zoom")
    assert "Video Conferencing Setup" in result
    assert "Grace" in result
    assert "Zoom" in result


@pytest.mark.asyncio
async def test_manage_it_inventory():
    result = await manage_it_inventory()
    assert "IT Inventory Managed" in result


@pytest.mark.asyncio
async def test_configure_firewall_rules():
    result = await configure_firewall_rules("Allow traffic on port 8080")
    assert "Firewall Rules Configured" in result
    assert "Allow traffic on port 8080" in result


@pytest.mark.asyncio
async def test_manage_virtual_machines():
    result = await manage_virtual_machines("VM: Ubuntu Server")
    assert "Virtual Machines Managed" in result
    assert "VM: Ubuntu Server" in result


@pytest.mark.asyncio
async def test_provide_tech_support_for_event():
    result = await provide_tech_support_for_event("Annual Tech Summit")
    assert "Tech Support for Event" in result
    assert "Annual Tech Summit" in result


@pytest.mark.asyncio
async def test_configure_network_storage():
    result = await configure_network_storage("John Doe", "500GB NAS")
    assert "Network Storage Configured" in result
    assert "John Doe" in result
    assert "500GB NAS" in result


@pytest.mark.asyncio
async def test_set_up_two_factor_authentication():
    result = await set_up_two_factor_authentication("Jane Smith")
    assert "Two-Factor Authentication Setup" in result
    assert "Jane Smith" in result


@pytest.mark.asyncio
async def test_troubleshoot_email_issue():
    result = await troubleshoot_email_issue("Alice", "Cannot send emails")
    assert "Email Issue Resolved" in result
    assert "Cannot send emails" in result
    assert "Alice" in result


@pytest.mark.asyncio
async def test_manage_it_helpdesk_tickets():
    result = await manage_it_helpdesk_tickets("Ticket #123: Password reset")
    assert "Helpdesk Tickets Managed" in result
    assert "Password reset" in result


@pytest.mark.asyncio
async def test_handle_software_bug_report():
    result = await handle_software_bug_report("Critical bug in payroll module")
    assert "Software Bug Report Handled" in result
    assert "Critical bug in payroll module" in result


@pytest.mark.asyncio
async def test_assist_with_data_recovery():
    result = await assist_with_data_recovery("Jane Doe", "Recover deleted files")
    assert "Data Recovery Assisted" in result
    assert "Jane Doe" in result
    assert "Recover deleted files" in result


@pytest.mark.asyncio
async def test_manage_system_updates():
    result = await manage_system_updates("Patch CVE-2023-1234")
    assert "System Updates Managed" in result
    assert "Patch CVE-2023-1234" in result


@pytest.mark.asyncio
async def test_configure_digital_signatures():
    result = await configure_digital_signatures(
        "John Doe", "Company Approved Signature"
    )
    assert "Digital Signatures Configured" in result
    assert "John Doe" in result
    assert "Company Approved Signature" in result


@pytest.mark.asyncio
async def test_provide_remote_tech_support():
    result = await provide_remote_tech_support("Mark")
    assert "Remote Tech Support Provided" in result
    assert "Mark" in result


@pytest.mark.asyncio
async def test_manage_network_bandwidth():
    result = await manage_network_bandwidth("Allocate more bandwidth for video calls")
    assert "Network Bandwidth Managed" in result
    assert "Allocate more bandwidth for video calls" in result


@pytest.mark.asyncio
async def test_assist_with_tech_documentation():
    result = await assist_with_tech_documentation("Documentation for VPN setup")
    assert "Technical Documentation Created" in result
    assert "VPN setup" in result


@pytest.mark.asyncio
async def test_monitor_system_performance():
    result = await monitor_system_performance()
    assert "System Performance Monitored" in result


@pytest.mark.asyncio
async def test_get_tech_support_tools():
    tools = get_tech_support_tools()
    assert isinstance(tools, list)
    assert len(tools) > 40  # Ensure all tools are included
    assert all(isinstance(tool, FunctionTool) for tool in tools)
