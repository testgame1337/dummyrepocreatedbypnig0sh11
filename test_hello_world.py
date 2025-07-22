#!/usr/bin/env python3
"""
Test module for hello_world.py
"""

import unittest
import io
import sys
from hello_world import print_hello_world

class TestHelloWorld(unittest.TestCase):
    """Test cases for the hello_world module"""
    
    def test_print_hello_world_output(self):
        """Test that print_hello_world prints 'hello world' to stdout"""
        # Redirect stdout to capture the printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the function
        print_hello_world()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the captured output
        self.assertEqual(captured_output.getvalue().strip(), "hello world")
    
    def test_print_hello_world_return(self):
        """Test that print_hello_world returns the 'hello world' string"""
        result = print_hello_world()
        self.assertEqual(result, "hello world")

if __name__ == "__main__":
    unittest.main()