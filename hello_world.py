#!/usr/bin/env python3
"""
A simple module that prints "hello world"
"""

def print_hello_world():
    """
    Function that prints "hello world" to the console.
    
    Returns:
        str: The "hello world" message
    """
    message = "hello world"
    print(message)
    return message

if __name__ == "__main__":
    # Execute the function when the script is run directly
    print_hello_world()