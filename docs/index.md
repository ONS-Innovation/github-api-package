# GitHub API Package

## Overview

This project is a supporting package for tools which need to access GitHub's APIs. The package includes a function to authenticate with the API using a GitHub App, a class to use GitHub's RESTful API and a class to perform set queries against GitHub's GraphQL API.

For more information about the package's functionality, see the following pages:

| Name                          | Type     | Description                                                                                                            |                             Link                             |
|-------------------------------|----------|------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------:|
| `get_token_as_installation()` | Function | A function which gets a GitHub Access Token for a given GitHub App. This allows authenticated API requests to be made. | [Reference :link:](./reference/get_token_as_installation.md) |
| `github_interface()`          | Class    | A class used to interact with GitHub's RESTful API.                                                                    |     [Reference :link:](./reference/github_interface.md)      |
| `github_graphql_interface()`  | Class    | A class used to interact with GitHub's GraphQL API.                                                                    | [Reference :link:](./reference/github_graphql_interface.md)  |

For information about how to use this package, refer to the project README and any example use cases provided.
