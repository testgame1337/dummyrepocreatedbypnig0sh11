#!/usr/bin/env python3
"""
Command-line interface for the GitHub Repository Processor.

This script provides a simple interface to run the GitHub Repository Processor.
"""

import os
import sys
import argparse
from github_repo_processor import GitHubRepoProcessor

def main():
    """Main function to parse arguments and run the processor."""
    parser = argparse.ArgumentParser(
        description='Process a GitHub repository and convert it to Python 3'
    )
    
    parser.add_argument(
        '--token', 
        help='GitHub authentication token (can also be set via GITHUB_TOKEN env var)'
    )
    parser.add_argument(
        '--repo', 
        default='testgame1337/vulcan-old',
        help='Repository name in the format owner/repo (default: testgame1337/vulcan-old)'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Check for token in environment if not provided as argument
    token = args.token or os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GitHub token is required. Provide it with --token or set GITHUB_TOKEN environment variable.")
        sys.exit(1)
    
    try:
        processor = GitHubRepoProcessor(token, args.repo)
        processor.process_repository()
        print(f"Repository processing complete. Output directory: {processor.output_dir}")
    except Exception as e:
        print(f"Error processing repository: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()