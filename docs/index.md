# GitHub API Package

## Overview

This project is a supporting package for tools which need to access the GitHub RESTful API. It includes a function to authenticate requests as a GitHub App installation and a class which allows Get, Patch and Post requests to be made easily.

This package is primarily used by:

- [GitHub Repository Archive Tool](https://github.com/ONS-Innovation/github-repository-archive-tool)
- [GitHub CoPilot Usage Dashboard](https://github.com/ONS-Innovation/github-copilot-usage-dashboard)
- [GitHub Policy/Audit Dashboard](https://github.com/ONS-Innovation/github-policy-dashboard)

## Techstack Overview

This project is written in Python due to its requirement to be used in other Python projects and doesn't use any specific frameworks. The package uses requests to make API calls and JWT to get a GitHub Authentication token.

## Getting Started

To setup and use the project, please refer to the [README](https://github.com/ONS-Innovation/github-api-package/blob/main/README.md).