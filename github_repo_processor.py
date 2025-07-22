#!/usr/bin/env python3
"""
GitHub Repository Processor

This script accesses a specified GitHub repository, learns from its content,
and rewrites the project using Python 3. It includes verbose logging of all API interactions.

Usage:
    python github_repo_processor.py --token <github_token> --repo <repo_name>

Example:
    python github_repo_processor.py --token ghp_abc123 --repo testgame1337/vulcan-old
"""

import os
import sys
import argparse
import logging
import json
import base64
import requests
from typing import Dict, List, Any, Optional, Union
import time
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('GithubRepoProcessor')

class VerboseHTTPAdapter(requests.adapters.HTTPAdapter):
    """Custom HTTP adapter that logs request and response details"""
    
    def send(self, request, **kwargs):
        logger.info(f"API REQUEST: {request.method} {request.url}")
        logger.info(f"REQUEST HEADERS: {request.headers}")
        if request.body:
            try:
                logger.info(f"REQUEST BODY: {request.body.decode('utf-8')}")
            except (UnicodeDecodeError, AttributeError):
                logger.info(f"REQUEST BODY: [Binary data of length {len(request.body)}]")
        
        start_time = time.time()
        response = super().send(request, **kwargs)
        elapsed_time = time.time() - start_time
        
        logger.info(f"API RESPONSE: {response.status_code} (took {elapsed_time:.2f}s)")
        logger.info(f"RESPONSE HEADERS: {response.headers}")
        try:
            if response.text:
                if len(response.text) > 1000:
                    logger.info(f"RESPONSE BODY: {response.text[:1000]}... [truncated]")
                else:
                    logger.info(f"RESPONSE BODY: {response.text}")
        except Exception as e:
            logger.warning(f"Could not log response body: {e}")
            
        return response

class GitHubRepoProcessor:
    """Class to process GitHub repositories"""
    
    def __init__(self, token: str, repo: str):
        """
        Initialize the GitHub repository processor.
        
        Args:
            token: GitHub authentication token
            repo: Repository name in the format 'owner/repo'
        """
        self.token = token
        self.repo = repo
        self.api_base_url = "https://api.github.com"
        self.session = requests.Session()
        
        # Add verbose HTTP adapter
        adapter = VerboseHTTPAdapter()
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # Set up headers for GitHub API
        self.session.headers.update({
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Repository-Processor'
        })
        
        # Create output directory
        self.output_dir = os.path.join(os.getcwd(), f"{repo.split('/')[-1]}-python3")
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        
        logger.info(f"Initialized GitHub repository processor for {repo}")
        logger.info(f"Output directory: {self.output_dir}")
    
    def get_repo_info(self) -> Dict[str, Any]:
        """Get repository information"""
        url = f"{self.api_base_url}/repos/{self.repo}"
        logger.info(f"Fetching repository information from {url}")
        
        response = self.session.get(url)
        response.raise_for_status()
        
        repo_info = response.json()
        logger.info(f"Repository information retrieved successfully")
        return repo_info
    
    def get_repo_contents(self, path: str = "") -> List[Dict[str, Any]]:
        """
        Get contents of a repository directory.
        
        Args:
            path: Path within the repository
            
        Returns:
            List of content items
        """
        url = f"{self.api_base_url}/repos/{self.repo}/contents/{path}"
        logger.info(f"Fetching repository contents from {url}")
        
        response = self.session.get(url)
        response.raise_for_status()
        
        contents = response.json()
        if isinstance(contents, dict):
            contents = [contents]
            
        logger.info(f"Retrieved {len(contents)} items from {path or 'root'}")
        return contents
    
    def get_file_content(self, file_path: str) -> str:
        """
        Get the content of a file in the repository.
        
        Args:
            file_path: Path to the file within the repository
            
        Returns:
            Decoded file content
        """
        url = f"{self.api_base_url}/repos/{self.repo}/contents/{file_path}"
        logger.info(f"Fetching file content from {url}")
        
        response = self.session.get(url)
        response.raise_for_status()
        
        content_data = response.json()
        if content_data.get('encoding') == 'base64':
            content = base64.b64decode(content_data['content']).decode('utf-8')
            logger.info(f"File {file_path} content decoded successfully")
            return content
        else:
            logger.warning(f"Unexpected encoding for {file_path}: {content_data.get('encoding')}")
            return ""
    
    def process_directory(self, path: str = ""):
        """
        Process a directory in the repository recursively.
        
        Args:
            path: Path within the repository
        """
        contents = self.get_repo_contents(path)
        
        for item in contents:
            item_path = item['path']
            item_type = item['type']
            
            if item_type == 'dir':
                # Create the directory in the output
                output_path = os.path.join(self.output_dir, item_path)
                os.makedirs(output_path, exist_ok=True)
                logger.info(f"Created directory: {output_path}")
                
                # Process the subdirectory
                self.process_directory(item_path)
            
            elif item_type == 'file':
                self.process_file(item_path)
    
    def process_file(self, file_path: str):
        """
        Process a file from the repository.
        
        Args:
            file_path: Path to the file within the repository
        """
        try:
            content = self.get_file_content(file_path)
            
            # Determine if this is a Python file that needs conversion
            is_python = file_path.endswith('.py')
            
            # Create the output file path
            output_file_path = os.path.join(self.output_dir, file_path)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            
            # If it's a Python file, convert it to Python 3
            if is_python:
                logger.info(f"Converting {file_path} to Python 3")
                content = self.convert_to_python3(content)
            
            # Write the file
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Processed file: {file_path} -> {output_file_path}")
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
    
    def convert_to_python3(self, content: str) -> str:
        """
        Convert Python code to Python 3.
        
        Args:
            content: Python code content
            
        Returns:
            Python 3 compatible code
        """
        # This is a simplified conversion - in a real implementation,
        # you might want to use tools like 2to3 or more sophisticated parsing
        
        # Replace common Python 2 patterns with Python 3 equivalents
        replacements = [
            # Print statement to function
            (r'print ([^(].*)', r'print(\1)'),
            # Unicode literals
            (r'u"', r'"'),
            (r"u'", r"'"),
            # Integer division
            (r'(\d+) / (\d+)', r'\1 // \2'),
            # xrange to range
            (r'xrange\(', r'range('),
            # iteritems to items
            (r'\.iteritems\(\)', r'.items()'),
            # iterkeys to keys
            (r'\.iterkeys\(\)', r'.keys()'),
            # itervalues to values
            (r'\.itervalues\(\)', r'.values()'),
            # Exception handling
            (r'except ([A-Za-z0-9_]+), ([A-Za-z0-9_]+):', r'except \1 as \2:'),
        ]
        
        # Apply replacements
        import re
        result = content
        for pattern, replacement in replacements:
            result = re.sub(pattern, replacement, result)
        
        # Add imports for compatibility
        if 'from __future__ import' not in result:
            result = "from __future__ import absolute_import, division, print_function, unicode_literals\n\n" + result
        
        return result
    
    def process_repository(self):
        """Process the entire repository"""
        try:
            # Get repository information
            repo_info = self.get_repo_info()
            logger.info(f"Processing repository: {repo_info['full_name']}")
            
            # Create README with repository information
            readme_content = f"""# {repo_info['name']} (Python 3 Version)

This is a Python 3 rewrite of the original repository: {repo_info['full_name']}

## Original Description
{repo_info.get('description', 'No description provided.')}

## Original Repository Information
- Stars: {repo_info.get('stargazers_count', 0)}
- Forks: {repo_info.get('forks_count', 0)}
- Created: {repo_info.get('created_at', 'Unknown')}
- Last Updated: {repo_info.get('updated_at', 'Unknown')}

## Python 3 Conversion
This version has been automatically converted to Python 3 compatibility.
"""
            
            with open(os.path.join(self.output_dir, 'README.md'), 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # Process the repository contents
            self.process_directory()
            
            logger.info(f"Repository processing complete. Output directory: {self.output_dir}")
            
        except Exception as e:
            logger.error(f"Error processing repository: {e}")
            raise

def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description='Process a GitHub repository and convert it to Python 3')
    parser.add_argument('--token', required=True, help='GitHub authentication token')
    parser.add_argument('--repo', required=True, help='Repository name in the format owner/repo')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    processor = GitHubRepoProcessor(args.token, args.repo)
    processor.process_repository()

if __name__ == "__main__":
    main()