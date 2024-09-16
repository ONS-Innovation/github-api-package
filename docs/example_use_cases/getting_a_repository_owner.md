# Getting a Repository Owner

## Overview

A major use case for the GraphQL section of the toolkit, is to get a point of contact for a given repository. This can be done using the `github_graphql_interface()` class.

## Prerequisites

1. The GitHub organisation must have verified domain emails. Please see [this](https://docs.github.com/en/organizations/managing-organization-settings/verifying-or-approving-a-domain-for-your-organization) GitHub Doc.

2. The repository must contain a CODEOWNERS file at either the root of the repository, within a `.github` folder at the root of the repository or within a `/docs` folder at the root of the repository.

3. The CODEOWNERS file can contain a mixture of GitHub Teams and Usernames. Emails within a CODEOWNERS file are ignored.

4. The GitHub Team within the CODEOWNERS file must have a member with the maintainer role. This person is identified as a repository owner from the team.

## Python Example

The following code snippet does the following:

1. Get all variables from the environment.

2. Create a GitHub Access Token to make API requests.

3. Create an instance of the GraphQL interface.

4. Run `get_repository_email_list()` to get a list of CODEOWNER emails for that repository.

```python
import github_api_toolkit as gat
from os import getenv

github_org = getenv("GITHUB_ORG")
pem_contents = getenv("SECRET")
github_app_id = getenv("APP_ID")
github_repo = getenv("GITHUB_REPO")

token = gat.get_token_as_installation(github_org, pem_contents, github_app_id)

api = gat.github_graphql_interface(token[0])

emails = api.get_repository_email_list(github_org, github_repo)

print(emails)
```