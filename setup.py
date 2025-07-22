from setuptools import setup, find_packages

setup(
    name="vulcan",
    version="0.1.0",
    description="Python 3 implementation of vulcan-old",
    author="Vulcan Team",
    packages=find_packages(),
    install_requires=[
        "click>=7.0",
        "requests>=2.25.0",
        "pyyaml>=5.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=20.8b1",
            "flake8>=3.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vulcan=vulcan.cli:main",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)