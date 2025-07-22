# Vulcan

A Python 3 tool for system analysis and security testing. Vulcan provides functionality for scanning networks, analyzing systems, and identifying potential security vulnerabilities.

## Features

- Port scanning with customizable ranges and timeouts
- System information gathering
- Security vulnerability checks
- JSON output for further analysis
- Multi-threaded scanning for improved performance

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/vulcan.git
cd vulcan

# Install the package
pip install -e .
```

## Usage

### Basic Usage

```bash
# Scan a specific host
vulcan --target example.com

# Scan a specific IP address with custom port range
vulcan --target 192.168.1.1 --ports 1-1000

# Save results to a file
vulcan --target example.com --output results.json

# Enable verbose output
vulcan --target example.com --verbose
```

### Command Line Options

- `-t, --target`: Target IP address or hostname (use 'localhost' for local system)
- `-p, --ports`: Port range to scan (format: start-end, default: 1-1024)
- `-o, --output`: Output file for scan results
- `-v, --verbose`: Enable verbose output
- `--timeout`: Timeout for connection attempts in seconds (default: 1.0)

## Running Tests

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
