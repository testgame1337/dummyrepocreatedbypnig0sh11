"""
Tests for the core functionality
"""

import json
import os
import tempfile
import pytest
from vulcan.core import process_data, analyze_system, run_task


def test_process_data_json():
    """Test processing data with JSON output."""
    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"test": "data", "value": 123}, f)
        temp_file = f.name
    
    try:
        # Process the file
        result = process_data(temp_file, output_format="json")
        
        # Parse the result and check
        data = json.loads(result)
        assert "test" in data
        assert data["test"] == "data"
        assert "value" in data
        assert data["value"] == 123
        assert "processed_at" in data
        assert "processed_by" in data
        assert data["processed_by"] == "vulcan"
    finally:
        # Clean up
        os.unlink(temp_file)


def test_process_data_yaml():
    """Test processing data with YAML output."""
    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"test": "data", "value": 123}, f)
        temp_file = f.name
    
    try:
        # Process the file
        result = process_data(temp_file, output_format="yaml")
        
        # Check that the result is a YAML string
        assert "test: data" in result
        assert "value: 123" in result
        assert "processed_at:" in result
        assert "processed_by: vulcan" in result
    finally:
        # Clean up
        os.unlink(temp_file)


def test_process_data_csv():
    """Test processing data with CSV output."""
    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"test": "data", "value": 123}, f)
        temp_file = f.name
    
    try:
        # Process the file
        result = process_data(temp_file, output_format="csv")
        
        # Check that the result is a CSV string
        lines = result.strip().split("\n")
        assert len(lines) == 2  # Header and data
        
        # Check headers
        headers = lines[0].split(",")
        assert "test" in headers
        assert "value" in headers
        assert "processed_at" in headers
        assert "processed_by" in headers
        
        # Check data
        data = lines[1].split(",")
        assert "data" in data
        assert "123" in data
        assert "vulcan" in data
    finally:
        # Clean up
        os.unlink(temp_file)


def test_analyze_system():
    """Test system analysis."""
    # Basic analysis
    result = analyze_system(detailed=False)
    data = json.loads(result)
    
    # Check basic fields
    assert "platform" in data
    assert "python_version" in data
    assert "timestamp" in data
    
    # Detailed analysis
    result = analyze_system(detailed=True)
    data = json.loads(result)
    
    # Check detailed fields
    assert "platform" in data
    assert "python_version" in data
    assert "timestamp" in data
    assert "platform_details" in data
    assert "python_build" in data
    assert "environment_variables" in data


def test_run_task():
    """Test running tasks."""
    # Test hello task
    result = run_task("hello")
    assert "Hello from Vulcan" in result
    
    # Test system_check task
    result = run_task("system_check")
    data = json.loads(result)
    assert "platform" in data
    
    # Test invalid task
    with pytest.raises(ValueError):
        run_task("invalid_task")