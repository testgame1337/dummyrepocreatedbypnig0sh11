# GitHub Repository Python3 Converter

This tool accesses a GitHub repository, learns from its content, and rewrites the project using Python 3. It includes verbose logging of all API interactions to help with debugging.

## Features

- Authenticates to GitHub using a personal access token
- Accesses specified repositories with proper authentication
- Fetches repository content and structure
- Converts Python 2 code to Python 3
- Provides verbose logging of all API requests and responses
- Creates a new directory with the Python 3 version of the repository

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Using the command-line interface

```bash
python run_processor.py --token YOUR_GITHUB_TOKEN --repo testgame1337/vulcan-old --verbose
```

Or set the token as an environment variable:

```bash
export GITHUB_TOKEN=YOUR_GITHUB_TOKEN
python run_processor.py --repo testgame1337/vulcan-old --verbose
```

### Using the Python module directly

```python
from github_repo_processor import GitHubRepoProcessor

processor = GitHubRepoProcessor(token="YOUR_GITHUB_TOKEN", repo="testgame1337/vulcan-old")
processor.process_repository()
```

## Testing

Run the unit tests:

```bash
python -m unittest test_github_repo_processor.py
```

## Security Note

- Never commit your GitHub token to version control
- Use environment variables or secure secret management for tokens
- The token should have appropriate permissions to access the repository

## Output

The processed repository will be created in a new directory named after the repository with "-python3" suffix.
