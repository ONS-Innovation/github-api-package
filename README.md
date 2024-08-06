# GitHub API Package
A Python package used to interact with the GitHub RESTful API.

## Installation
This package can be installed using the GitHub repository URL.

### PIP

```bash
pip install git+https://github.com/ONS-Innovation/code-github-api-package.git
```

### Poetry

```bash
poetry add git+https://github.com/ONS-Innovation/code-github-api-package.git
```

## Usage
This package can be imported as a normal Python package.

Import whole module:
```python
import github_api_toolkit
```

Import part of the module:
```python
from github_api_toolkit import github_interface
```

## Development

This project uses pip for package management. Poetry was avoided to keep the package size small.

To develop/test the project locally, clone the repository then navigate to its root directory and run the following:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This will create a virtual environment, activate it and install all the project dependancies into it.

To deactivate the virtual environment, use: 
```bash 
deactivate
```

## Documentation

This project uses MkDocs for documentation which gets deployed to GitHub Pages at a repository level.

For more information about MkDocs, see the below documentation.

[Getting Started with MkDocs](https://www.mkdocs.org/getting-started/)