"""
Tests for utility functions
"""

import os
import json
import tempfile
import pytest
from vulcan.utils import (
    load_config,
    save_config,
    format_size,
    get_timestamp,
    is_valid_path
)


def test_load_config():
    """Test loading configuration from file."""
    # Create a temporary JSON config file
    config_data = {
        "test": "value",
        "nested": {
            "key": "value"
        },
        "list": [1, 2, 3]
    }
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_data, f)
        temp_file = f.name
    
    try:
        # Load the config
        loaded_config = load_config(temp_file)
        
        # Check the loaded config
        assert loaded_config["test"] == "value"
        assert loaded_config["nested"]["key"] == "value"
        assert loaded_config["list"] == [1, 2, 3]
    finally:
        # Clean up
        os.unlink(temp_file)


def test_save_config():
    """Test saving configuration to file."""
    config_data = {
        "test": "value",
        "nested": {
            "key": "value"
        },
        "list": [1, 2, 3]
    }
    
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        temp_file = f.name
    
    try:
        # Save the config
        save_config(config_data, temp_file)
        
        # Load it back and check
        with open(temp_file, "r") as f:
            loaded_data = json.load(f)
        
        assert loaded_data["test"] == "value"
        assert loaded_data["nested"]["key"] == "value"
        assert loaded_data["list"] == [1, 2, 3]
    finally:
        # Clean up
        os.unlink(temp_file)


def test_format_size():
    """Test formatting size in bytes to human-readable format."""
    assert format_size(0) == "0B"
    assert format_size(1024) == "1.00KB"
    assert format_size(1024 * 1024) == "1.00MB"
    assert format_size(1024 * 1024 * 1024) == "1.00GB"
    assert format_size(1024 * 1024 * 1024 * 1024) == "1.00TB"


def test_get_timestamp():
    """Test getting current timestamp."""
    timestamp = get_timestamp()
    assert isinstance(timestamp, str)
    assert "T" in timestamp  # ISO format contains T between date and time
    assert ":" in timestamp  # Time part contains colons


def test_is_valid_path():
    """Test checking if a path is valid."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_file = f.name
    
    try:
        # Check valid path
        assert is_valid_path(temp_file) is True
        
        # Check invalid path
        assert is_valid_path("/path/that/does/not/exist") is False
    finally:
        # Clean up
        os.unlink(temp_file)