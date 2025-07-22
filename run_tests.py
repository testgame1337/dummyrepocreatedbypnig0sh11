#!/usr/bin/env python3
"""
Script to run tests for Vulcan
"""

import os
import sys
import subprocess


def main():
    """Run tests for Vulcan."""
    print("Running tests for Vulcan...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Run pytest
    try:
        subprocess.run([sys.executable, "-m", "pytest", "-v"], check=True)
        print("\nAll tests passed!")
    except subprocess.CalledProcessError:
        print("\nSome tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()