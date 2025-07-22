#!/usr/bin/env python3
"""
Test script for the GitHub Repository Processor.

This script tests the functionality of the GitHubRepoProcessor class.
"""

import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from github_repo_processor import GitHubRepoProcessor

class TestGitHubRepoProcessor(unittest.TestCase):
    """Test cases for the GitHubRepoProcessor class."""

    def setUp(self):
        """Set up test environment."""
        self.test_token = "test_token"
        self.test_repo = "testgame1337/vulcan-old"
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock the output directory to use our temp directory
        self.patcher = patch('github_repo_processor.GitHubRepoProcessor.output_dir', 
                            new_callable=unittest.mock.PropertyMock)
        self.mock_output_dir = self.patcher.start()
        self.mock_output_dir.return_value = self.temp_dir

    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir)

    @patch('github_repo_processor.requests.Session')
    def test_initialization(self, mock_session):
        """Test that the processor initializes correctly."""
        # Setup mock
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        # Create processor
        processor = GitHubRepoProcessor(self.test_token, self.test_repo)
        
        # Verify session setup
        self.assertEqual(processor.token, self.test_token)
        self.assertEqual(processor.repo, self.test_repo)
        self.assertEqual(processor.api_base_url, "https://api.github.com")
        
        # Verify headers
        mock_session_instance.headers.update.assert_called_once()
        call_args = mock_session_instance.headers.update.call_args[0][0]
        self.assertEqual(call_args['Authorization'], f'token {self.test_token}')
        self.assertEqual(call_args['Accept'], 'application/vnd.github.v3+json')

    @patch('github_repo_processor.requests.Session')
    def test_get_repo_info(self, mock_session):
        """Test fetching repository information."""
        # Setup mock
        mock_session_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "vulcan-old", "full_name": "testgame1337/vulcan-old"}
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        # Create processor and call method
        processor = GitHubRepoProcessor(self.test_token, self.test_repo)
        result = processor.get_repo_info()
        
        # Verify API call
        expected_url = f"https://api.github.com/repos/{self.test_repo}"
        mock_session_instance.get.assert_called_once_with(expected_url)
        
        # Verify result
        self.assertEqual(result["name"], "vulcan-old")
        self.assertEqual(result["full_name"], "testgame1337/vulcan-old")

    @patch('github_repo_processor.requests.Session')
    def test_get_repo_contents(self, mock_session):
        """Test fetching repository contents."""
        # Setup mock
        mock_session_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"name": "file1.py", "path": "file1.py", "type": "file"},
            {"name": "dir1", "path": "dir1", "type": "dir"}
        ]
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        # Create processor and call method
        processor = GitHubRepoProcessor(self.test_token, self.test_repo)
        result = processor.get_repo_contents()
        
        # Verify API call
        expected_url = f"https://api.github.com/repos/{self.test_repo}/contents/"
        mock_session_instance.get.assert_called_once_with(expected_url)
        
        # Verify result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "file1.py")
        self.assertEqual(result[1]["name"], "dir1")

    def test_convert_to_python3(self):
        """Test Python 2 to Python 3 conversion."""
        processor = GitHubRepoProcessor(self.test_token, self.test_repo)
        
        # Test print statement conversion
        py2_code = 'print "Hello, world!"'
        py3_code = processor.convert_to_python3(py2_code)
        self.assertIn('print("Hello, world!")', py3_code)
        
        # Test xrange conversion
        py2_code = 'for i in xrange(10):'
        py3_code = processor.convert_to_python3(py2_code)
        self.assertIn('for i in range(10):', py3_code)
        
        # Test exception handling
        py2_code = 'try:\n    something()\nexcept Exception, e:\n    print e'
        py3_code = processor.convert_to_python3(py2_code)
        self.assertIn('except Exception as e:', py3_code)

if __name__ == '__main__':
    unittest.main()