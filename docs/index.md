# GitHub API Package

## Overview

This project is a supporting package for tools which need to access GitHub's APIs. The package includes a function to authenticate with the API using a GitHub App, a class to use GitHub's RESTful API and a class to perform set queries against GitHub's GraphQL API.

This package is primarily used by:

- [GitHub Repository Archive Tool](https://github.com/ONS-Innovation/github-repository-archive-tool)
- [GitHub CoPilot Usage Dashboard](https://github.com/ONS-Innovation/github-copilot-usage-dashboard)
- [GitHub Policy/Audit Dashboard](https://github.com/ONS-Innovation/github-policy-dashboard)

For more information about the package's functionality, see the following pages:

| Name                          | Type     | Description                                                                                                            | Link                                     |
| ----------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------- | :--------------------------------------: |
| `get_token_as_installation()` | Function | A function which gets a GitHub Access Token for a given GitHub App. This allows authenticated API requests to be made. | [:link:](./reference/get_token_as_installation.md) |
| `github_interface()`          | Class    | A class used to interact with GitHub's RESTful API.                                                                    | [:link:](./reference/github_interface.md)          |
| `github_graphql_interface()`  | Class    | A class used to interact with GitHub's GraphQL API.                                                                    | [:link:](./reference/github_graphql_interface.md)  |

## Techstack Overview

This project is written in Python due to its requirement to be used in other Python projects and doesn't use any specific frameworks. The package uses requests to make API calls and JWT to get a GitHub Authentication token.

## Getting Started

To setup and use the project, please refer to the [README](https://github.com/ONS-Innovation/github-api-package/blob/main/README.md).