# GitHub API Package

Python module for interacting with the GitHub RESTful and GraphQL APIs.

## Table of Contents

- [GitHub API Package](#github-api-package)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Makefile](#makefile)
  - [Using the Package](#using-the-package)
    - [GitHub App Setup](#github-app-setup)
    - [End User Instructions](#end-user-instructions)
      - [Installation](#installation)
      - [Usage](#usage)
      - [Error Handling](#error-handling)
    - [Developer Instructions](#developer-instructions)
  - [Package Structure](#package-structure)
  - [Deployment](#deployment)
  - [Documentation](#documentation)
    - [GitHub Actions for Documentation](#github-actions-for-documentation)
    - [Local Development of Documentation](#local-development-of-documentation)
  - [Linting and Testing](#linting-and-testing)
    - [GitHub Actions](#github-actions)
    - [Running Tests and Linters Locally](#running-tests-and-linters-locally)
      - [Primary Language](#primary-language)
      - [MegaLinter](#megalinter)
      - [Documentation linting and building](#documentation-linting-and-building)

## Prerequisites

- Python 3.12 or higher
- Poetry for dependency management (>=2.x)
- Node.js and npm for documentation linting (Markdownlint)

## Makefile

This project uses a Makefile to simplify common tasks.
To see the available commands, run:

```bash
make help
```

## Using the Package

### GitHub App Setup

To use the package, you will need to set up a GitHub App in your GitHub organisation. The App is used to authenticate with the GitHub API and perform actions on behalf of the user.

The library requires:

- GitHub App Client ID
- GitHub App Private Key (in PEM format)
- GitHub Organisation name (the organisation where the GitHub App is installed)

to initialise the client instance that makes requests.

Permission management for the GitHub App should be configured according to the actions your application needs to perform. GitHub's API documentation provides detailed guidance on the required permissions for different endpoints.

> **Note:** It is down to the calling application to securely manage and provide these credentials when initializing the client instance.

### End User Instructions

#### Installation

To use the package, you can install it using your preferred method (e.g. pip, Poetry, etc.) and then import the relevant modules and functions in your code.

```bash
# Using pip
pip install git+https://github.com/ONS-Innovation/github-api-package@<version>

# or using Poetry
poetry add git+https://github.com/ONS-Innovation/github-api-package@<version>
```

#### Usage

Then, in your Python code, you can import the relevant modules and functions:

```python
from github_api_toolkit import (
    get_token_as_installation,
    github_graphql_interface, # GraphQL API client
    github_interface, # REST API client
)

# Get credentials for GitHub App
# Note: This is only an example. Do NOT hardcode credentials in your code.

org = "<github_organisation_name>"
client_id = "<github_app_client_id>"
private_key = "<github_app_private_key_in_pem_format>"

# Generate a GitHub App installation token
token_response = get_token_as_installation(org, private_key, client_id)

if isinstance(token_response, Exception):
    raise token_response

token, expires_at = token_response

# Initialise the GitHub API clients
rest = github_interface(token)
ql = github_graphql_interface(token)

# Make API requests

# REST Example
response = rest.get(f"/orgs/{org}/repos")
print(response)

# GraphQL Example
query = """
{
  viewer {
    login
  }
}
"""

variables = {}

response = ql.make_ql_request(
    query=query,
    params=variables,
)
```

A full reference for the toolkit can be found in `/docs`.

#### Error Handling

The REST API client (`github_interface`) uses `raise_for_status()` to raise an exception for any error response from the GitHub API. These error messages are then returned to the calling application for handling.

The GraphQL API client (`github_graphql_interface`) returns the response directly. Any errors from the GitHub API will be included in the response and should be handled by the calling application.

### Developer Instructions

When developing the package, you can use the `tests/manual_testing.py` file for manual testing of the package during development.
This file has a `github_interface` and `github_graphql_interface` instance already setup which can be used to test the API integration.

To use the latest version of the package in the `manual_testing.py` file, you can install the package into your virtual environment:

```bash
pip install .
```

**Note:** This should be done from the root directory of the repository, and you should have your virtual environment activated.

Whenever you make changes to the package, you will need to reinstall it for the changes to be reflected in the `manual_testing.py` file.

To run unit tests, linting, and formatting checks locally, you will need to install the dev dependencies using poetry:

```bash
make install-dev
```

This `make` target will install the development dependencies and the poetry-dynamic-versioning plugin, ensuring that your environment is set up.

## Package Structure

```text
src/
  └── github_api_toolkit/
      ├── __init__.py  # Public package exports
      ├── auth.py      # GitHub App token generation
      ├── graphql.py   # GraphQL API client
      └── rest.py      # REST API client
```

## Deployment

The package can be deployed to GitHub Releases using the GitHub Actions workflow defined in `.github/workflows/publish-release.yml`.

This workflow is triggered on pushes to tags matching the pattern "v\*". The tag must follow the format "v0.0.0" (e.g. "v0.1.0", "v1.0.0", etc.) for the workflow to run successfully.

A production release will be created when a tag is pushed that follows the format "v0.0.0" (e.g. "v0.1.0", "v1.0.0", etc.). A pre-release will be created when a tag is pushed that follows the format "v0.0.0-rc" (e.g. "v0.1.0-rc", "v1.0.0-rc", etc.). This allows for both stable releases and pre-releases to be created and published to GitHub Releases.

Package versioning is derived dynamically from the git tag during the release workflow. To create a new release, create and push a version tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

This triggers the GitHub Actions workflow to build and publish the package to GitHub Releases using version `0.1.0` derived from tag `v0.1.0`.

**Note:** It is important that GitHub Releases are _only_ created via the GitHub Actions workflow, and not manually via the GitHub UI. This is because the workflow ensures that the package is built and published correctly.

## Documentation

This repository uses [MkDocs](https://www.mkdocs.org/) for documentation. The documentation source files are located in the `docs` directory.

### GitHub Actions for Documentation

MkDocs gets deployed to GitHub Pages using GitHub Actions. The workflow for this is located at `.github/workflows/deploy-docs.yml`.
Before deployment, another GitHub Action workflow runs to check that the documentation builds correctly and has no linting or formatting issues.
This workflow is located at `.github/workflows/ci-docs.yml`.

### Local Development of Documentation

To run the documentation locally:

1. Create a Python virtual environment and activate it.

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install the dependencies for MkDocs.

   ```bash
   make docs-install
   ```

3. Run the MkDocs development server.

   ```bash
   make docs-serve
   ```

## Linting and Testing

### GitHub Actions

This repository has GitHub Actions workflows set up for linting and testing. The workflows are located at:

- `.github/workflows/ci-fmt.yml` for linting and formatting checks (primary language).
- `.github/workflows/ci-test.yml` for running automated tests.
- `.github/workflows/ci-docs.yml` for checking that the documentation builds correctly and has no linting or formatting issues.
- `.github/workflows/megalinter.yml` for running MegaLinter, which checks for linting and formatting issues across multiple languages and file types (this is a catch-all linter).
- `.github/workflows/deploy-docs.yml` for deploying documentation to GitHub Pages.

### Running Tests and Linters Locally

#### Primary Language

To run the linters and formatters for the primary language (Python) locally, you can use the following command:

```bash
make lint
```

To apply automatic fixes for any linting or formatting issues found, you can use:

```bash
make fmt
```

To run the tests locally, you can use:

```bash
make test
```

#### MegaLinter

This repository uses MegaLinter for comprehensive linting across multiple languages and file types.
We use this so that all additional assets in the repository (e.g. YAML files, Markdown files, etc.) are also linted and checked for formatting issues, without having to set up specific linters for each file type.

To run MegaLinter locally, you can use the following command:

```bash
make megalinter
```

#### Documentation linting and building

This repository uses Markdownlint for linting the documentation. To run Markdownlint locally, you can use the following:

```bash
make docs-lint
```

**Note:** This will install `markdownlint-cli` globally via npm if it is not already installed.

To apply automatic fixes for any linting issues found by Markdownlint, you can use:

```bash
make docs-fix
```

To test that the documentation builds correctly, you can use the following command:

```bash
make docs-build
```

**Note:** This depends on MkDocs being set up for the repository. Instructions for setting up MkDocs can be found in the [Documentation](#documentation) section of this README.
