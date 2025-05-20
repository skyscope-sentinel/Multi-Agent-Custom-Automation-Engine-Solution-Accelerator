"""Test cases for ProcurementTools class."""
import pytest
from src.backend.kernel_tools.hr_tools import HrTools


@pytest.mark.asyncio
async def test_schedule_orientation_session():
    """Test schedule_orientation_session method."""
    result = await HrTools.schedule_orientation_session("John Doe", "2025-05-20")
    assert "Orientation Session Scheduled" in result
    assert "**Employee Name:** John Doe" in result
    assert "**Date:** 2025-05-20" in result


@pytest.mark.asyncio
async def test_assign_mentor():
    """Test assign_mentor method."""
    result = await HrTools.assign_mentor("Jane Doe")
    assert "Mentor Assigned" in result
    assert "**Employee Name:** Jane Doe" in result


@pytest.mark.asyncio
async def test_register_for_benefits():
    """Test register_for_benefits method."""
    result = await HrTools.register_for_benefits("John Doe")
    assert "Benefits Registration" in result
    assert "**Employee Name:** John Doe" in result


@pytest.mark.asyncio
async def test_enroll_in_training_program():
    """Test enroll_in_training_program method."""
    result = await HrTools.enroll_in_training_program("John Doe", "Leadership Training")
    assert "Training Program Enrollment" in result
    assert "**Employee Name:** John Doe" in result
    assert "**Program Name:** Leadership Training" in result


@pytest.mark.asyncio
async def test_provide_employee_handbook():
    """Test provide_employee_handbook method."""
    result = await HrTools.provide_employee_handbook("Jane Doe")
    assert "Employee Handbook Provided" in result
    assert "**Employee Name:** Jane Doe" in result


@pytest.mark.asyncio
async def test_update_employee_record():
    """Test update_employee_record method."""
    result = await HrTools.update_employee_record("John Doe", "Address", "123 Main St")
    assert "Employee Record Updated" in result
    assert "**Field Updated:** Address" in result
    assert "**New Value:** 123 Main St" in result


@pytest.mark.asyncio
async def test_request_id_card():
    """Test request_id_card method."""
    result = await HrTools.request_id_card("John Doe")
    assert "ID Card Request" in result
    assert "**Employee Name:** John Doe" in result


@pytest.mark.asyncio
async def test_set_up_payroll():
    """Test set_up_payroll method."""
    result = await HrTools.set_up_payroll("Jane Doe")
    assert "Payroll Setup" in result
    assert "**Employee Name:** Jane Doe" in result


@pytest.mark.asyncio
async def test_add_emergency_contact():
    """Test add_emergency_contact method."""
    result = await HrTools.add_emergency_contact("John Doe", "Jane Smith", "555-1234")
    assert "Emergency Contact Added" in result
    assert "**Contact Name:** Jane Smith" in result
    assert "**Contact Phone:** 555-1234" in result


@pytest.mark.asyncio
async def test_process_leave_request():
    """Test process_leave_request method."""
    result = await HrTools.process_leave_request("John Doe", "Vacation", "2025-06-01", "2025-06-10")
    assert "Leave Request Processed" in result
    assert "**Leave Type:** Vacation" in result
    assert "**Start Date:** 2025-06-01" in result
    assert "**End Date:** 2025-06-10" in result


def test_get_all_kernel_functions():
    """Test get_all_kernel_functions method."""
    kernel_functions = HrTools.get_all_kernel_functions()
    assert "schedule_orientation_session" in kernel_functions
    assert "assign_mentor" in kernel_functions
    assert callable(kernel_functions["schedule_orientation_session"])


def test_generate_tools_json_doc():
    """Test generate_tools_json_doc method."""
    tools_json = HrTools.generate_tools_json_doc()
    assert "schedule_orientation_session" in tools_json
    assert "assign_mentor" in tools_json
    assert "arguments" in tools_json
