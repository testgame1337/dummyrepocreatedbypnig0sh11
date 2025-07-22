#!/usr/bin/env python3
"""
Setup script for Vulcan package.
"""

from setuptools import setup, find_packages

setup(
    name="vulcan",
    version="0.1.0",
    description="A Python 3 tool for system analysis and security testing",
    author="Vulcan Team",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vulcan=vulcan.vulcan:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)