#!/usr/bin/env python3
"""
Basic usage example for Vulcan
"""

import json
import os
import sys
import tempfile

# Add parent directory to path to import vulcan
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vulcan.core import process_data, analyze_system, run_task
from vulcan.config import Config
from vulcan.utils import format_size


def main():
    """Main function demonstrating Vulcan usage."""
    print("Vulcan Basic Usage Example")
    print("=========================\n")
    
    # Create a sample data file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({
            "name": "Example Data",
            "values": [1, 2, 3, 4, 5],
            "metadata": {
                "created": "2023-01-01",
                "version": "1.0"
            }
        }, f)
        sample_file = f.name
    
    try:
        # Process data
        print("Processing data file...")
        result = process_data(sample_file, output_format="json")
        print(f"Result:\n{result}\n")
        
        # Analyze system
        print("Analyzing system...")
        result = analyze_system(detailed=True)
        print(f"System Analysis:\n{result}\n")
        
        # Run a task
        print("Running 'hello' task...")
        result = run_task("hello")
        print(f"Task Result: {result}\n")
        
        # Demonstrate configuration
        print("Loading and using configuration...")
        config = Config()
        config.set("example.key", "example_value")
        config.set("example.number", 42)
        
        print(f"Configuration value: {config.get('example.key')}")
        print(f"Configuration number: {config.get('example.number')}")
        
        # Demonstrate utility functions
        print("\nUtility function examples:")
        print(f"1 KB formatted: {format_size(1024)}")
        print(f"1 MB formatted: {format_size(1024*1024)}")
        print(f"1 GB formatted: {format_size(1024*1024*1024)}")
        
    finally:
        # Clean up
        os.unlink(sample_file)


if __name__ == "__main__":
    main()