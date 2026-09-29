"""
This file is for manual testing of the package. This is useful for testing things during development.
Instances of both the REST and GraphQL GitHub API clients are already set up and can be used to test the API integration.

To run this file, you will need to set the following environment variables:
- GITHUB_CLIENT_ID: The client ID of your GitHub App.
- GITHUB_PRIVATE_KEY: The private key of your GitHub App. This should be the contents of the private key file, not the file path.
- GITHUB_ORGANISATION: The name of your GitHub organisation.

Note: Changes to this file should **not** be committed to the repository.
"""

from github_api_toolkit import get_token_as_installation, github_interface, github_graphql_interface

from os import getenv
from pprint import pprint  # noqa: F401 - Unused import, but useful to keep for testing purposes.

# Test Access Token Generation

client_id = getenv("GITHUB_CLIENT_ID")
private_key = getenv("GITHUB_PRIVATE_KEY")
organisation = str(getenv("GITHUB_ORGANISATION"))

token_response = get_token_as_installation(organisation, private_key, client_id)

if isinstance(token_response, tuple):
    token = token_response[0]
else:
    raise ValueError("Failed to obtain GitHub App installation token. Please check your environment variables and GitHub App configuration.")

rest = github_interface(token)
ql = github_graphql_interface(token)

# Space to test any methods during development. Example:

# response = rest.get(f"/orgs/{organisation}/repos")
# pprint(response)

## Reminder: Do not commit any changes to this file, as it is for manual testing purposes only.