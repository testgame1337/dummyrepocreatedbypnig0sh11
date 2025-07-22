"""
Tests for configuration handling
"""

import os
import json
import tempfile
import pytest
from vulcan.config import Config, load_config, get_config


def test_config_init():
    """Test configuration initialization."""
    # Initialize with default values
    config = Config()
    
    # Check default values
    assert config.get("log_level") == "INFO"
    assert config.get("output_format") == "json"
    assert "tasks" in config.config


def test_config_get_set():
    """Test getting and setting configuration values."""
    config = Config()
    
    # Set a value
    config.set("test.key", "value")
    
    # Get the value
    assert config.get("test.key") == "value"
    
    # Get a nested value
    assert config.get("tasks.system_check.detailed") is False
    
    # Get a non-existent value
    assert config.get("non.existent.key") is None
    assert config.get("non.existent.key", "default") == "default"


def test_config_load_save():
    """Test loading and saving configuration."""
    # Create a temporary config file
    config_data = {
        "log_level": "DEBUG",
        "custom": {
            "key": "value"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_data, f)
        temp_file = f.name
    
    try:
        # Load the config
        config = Config(temp_file)
        
        # Check loaded values
        assert config.get("log_level") == "DEBUG"
        assert config.get("custom.key") == "value"
        
        # Default values should still be present
        assert config.get("output_format") == "json"
        
        # Modify and save
        config.set("custom.key", "new_value")
        config.set("new_key", "new_value")
        
        new_temp_file = temp_file + ".new"
        config.save(new_temp_file)
        
        # Load the saved config
        new_config = Config(new_temp_file)
        assert new_config.get("custom.key") == "new_value"
        assert new_config.get("new_key") == "new_value"
        assert new_config.get("log_level") == "DEBUG"
    finally:
        # Clean up
        os.unlink(temp_file)
        if os.path.exists(temp_file + ".new"):
            os.unlink(temp_file + ".new")


def test_global_config():
    """Test global configuration instance."""
    # Get default global config
    config = get_config()
    assert config.get("log_level") == "INFO"
    
    # Create a temporary config file
    config_data = {
        "log_level": "DEBUG",
        "custom": {
            "key": "value"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_data, f)
        temp_file = f.name
    
    try:
        # Load the config
        loaded_config = load_config(temp_file)
        
        # Check loaded values
        assert loaded_config.get("log_level") == "DEBUG"
        assert loaded_config.get("custom.key") == "value"
        
        # Global config should be updated
        global_config = get_config()
        assert global_config.get("log_level") == "DEBUG"
        assert global_config.get("custom.key") == "value"
    finally:
        # Clean up
        os.unlink(temp_file)