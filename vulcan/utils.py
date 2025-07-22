"""
Utility functions for Vulcan
"""

import os
import json
import yaml
import logging
from datetime import datetime


def setup_logging(level=logging.INFO, log_file=None):
    """
    Set up logging configuration.
    
    Args:
        level (int): Logging level
        log_file (str, optional): Path to log file
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if log_file:
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(
            level=level,
            format=log_format
        )


def load_config(config_file):
    """
    Load configuration from a file.
    
    Args:
        config_file (str): Path to configuration file
        
    Returns:
        dict: Configuration data
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    _, ext = os.path.splitext(config_file)
    
    with open(config_file, "r") as f:
        if ext.lower() in (".yaml", ".yml"):
            return yaml.safe_load(f)
        elif ext.lower() == ".json":
            return json.load(f)
        else:
            # Try to parse as JSON first, then YAML
            content = f.read()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                try:
                    return yaml.safe_load(content)
                except yaml.YAMLError:
                    raise ValueError(f"Unsupported configuration format: {ext}")


def save_config(config, config_file):
    """
    Save configuration to a file.
    
    Args:
        config (dict): Configuration data
        config_file (str): Path to configuration file
    """
    _, ext = os.path.splitext(config_file)
    
    with open(config_file, "w") as f:
        if ext.lower() in (".yaml", ".yml"):
            yaml.dump(config, f, default_flow_style=False)
        elif ext.lower() == ".json":
            json.dump(config, f, indent=2)
        else:
            # Default to JSON
            json.dump(config, f, indent=2)


def format_size(size_bytes):
    """
    Format size in bytes to human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Human-readable size
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.2f}{size_names[i]}"


def get_timestamp():
    """
    Get current timestamp in ISO format.
    
    Returns:
        str: Current timestamp
    """
    return datetime.now().isoformat()


def is_valid_path(path):
    """
    Check if a path is valid.
    
    Args:
        path (str): Path to check
        
    Returns:
        bool: True if path is valid, False otherwise
    """
    return os.path.exists(path)