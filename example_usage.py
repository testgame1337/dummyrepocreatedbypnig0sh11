#!/usr/bin/env python3
"""
Example usage of the GitHub Repository Processor.

This script demonstrates how to use the GitHubRepoProcessor class programmatically.
"""

import os
import logging
from github_repo_processor import GitHubRepoProcessor

# Configure logging to show all messages
logging.basicConfig(level=logging.INFO)

def main():
    """Example function demonstrating how to use the GitHubRepoProcessor."""
    
    # Get GitHub token from environment variable
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Please set the GITHUB_TOKEN environment variable")
        print("Example: export GITHUB_TOKEN=your_github_token")
        return
    
    # Create an instance of the processor
    repo = "testgame1337/vulcan-old"
    print(f"Processing repository: {repo}")
    processor = GitHubRepoProcessor(token=token, repo=repo)
    
    # Process the repository
    processor.process_repository()
    
    print(f"\nProcessing complete!")
    print(f"The Python 3 version of the repository is available at: {processor.output_dir}")

if __name__ == "__main__":
    main()