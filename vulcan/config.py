"""
Configuration handling for Vulcan
"""

import os
import yaml
import json
from pathlib import Path


class Config:
    """Configuration manager for Vulcan."""
    
    def __init__(self, config_file=None):
        """
        Initialize configuration.
        
        Args:
            config_file (str, optional): Path to configuration file
        """
        self.config_file = config_file
        self.config = {}
        
        # Default configuration
        self.config = {
            "log_level": "INFO",
            "output_format": "json",
            "data_dir": str(Path.home() / ".vulcan"),
            "tasks": {
                "system_check": {
                    "detailed": False
                },
                "disk_usage": {
                    "path": "/"
                }
            }
        }
        
        # Load configuration from file if provided
        if config_file and os.path.exists(config_file):
            self.load()
    
    def load(self):
        """Load configuration from file."""
        if not self.config_file:
            return
        
        _, ext = os.path.splitext(self.config_file)
        
        with open(self.config_file, "r") as f:
            if ext.lower() in (".yaml", ".yml"):
                loaded_config = yaml.safe_load(f)
            elif ext.lower() == ".json":
                loaded_config = json.load(f)
            else:
                # Try to parse as JSON first, then YAML
                content = f.read()
                try:
                    loaded_config = json.loads(content)
                except json.JSONDecodeError:
                    try:
                        loaded_config = yaml.safe_load(content)
                    except yaml.YAMLError:
                        raise ValueError(f"Unsupported configuration format: {ext}")
        
        # Update configuration with loaded values
        self._update_recursive(self.config, loaded_config)
    
    def save(self, config_file=None):
        """
        Save configuration to file.
        
        Args:
            config_file (str, optional): Path to configuration file
        """
        save_path = config_file or self.config_file
        if not save_path:
            raise ValueError("No configuration file specified")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        
        _, ext = os.path.splitext(save_path)
        
        with open(save_path, "w") as f:
            if ext.lower() in (".yaml", ".yml"):
                yaml.dump(self.config, f, default_flow_style=False)
            else:
                # Default to JSON
                json.dump(self.config, f, indent=2)
    
    def get(self, key, default=None):
        """
        Get configuration value.
        
        Args:
            key (str): Configuration key
            default: Default value if key is not found
            
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """
        Set configuration value.
        
        Args:
            key (str): Configuration key
            value: Configuration value
        """
        keys = key.split(".")
        config = self.config
        
        for i, k in enumerate(keys[:-1]):
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def _update_recursive(self, target, source):
        """
        Update target dictionary recursively with values from source.
        
        Args:
            target (dict): Target dictionary
            source (dict): Source dictionary
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._update_recursive(target[key], value)
            else:
                target[key] = value


# Global configuration instance
config = Config()


def load_config(config_file):
    """
    Load configuration from file.
    
    Args:
        config_file (str): Path to configuration file
    """
    global config
    config = Config(config_file)
    return config


def get_config():
    """
    Get global configuration instance.
    
    Returns:
        Config: Global configuration instance
    """
    return config