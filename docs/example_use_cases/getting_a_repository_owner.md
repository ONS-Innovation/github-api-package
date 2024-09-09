# Getting a Repository Owner

## Overview

A major use case for the GraphQL section of the toolkit, is to get a point of contact for a given repository. This can be done using a combination of methods from the the `github_graphql_interface()` class.

## Prerequisites

1. The GitHub organisation must have verified domain emails. Please see [this](https://docs.github.com/en/organizations/managing-organization-settings/verifying-or-approving-a-domain-for-your-organization) GitHub Doc.

2. The repository must contain a CODEOWNERS file at the **root** of the repository.

3. The CODEOWNERS file can contain either an individual's username or a GitHub Team name and should be formatted as follows:

    ```
    @organisation/team-name     # This is a GitHub Team
    @username                   # This is a GitHub User
    ```

    Each CODEOWNER should be on a new line and no line should be left blank.

4. The GitHub Team within the CODEOWNERS file must have a member with the maintainer role. This person is identified as a repository owner from the team.

## Python Example

The following code snippet does the following:

1. Get all variables from the environment.

2. Create a GitHub Access Token to make API requests.

3. Create an instance of the GraphQL interface.

4. Get the Teams/Users kept within the CODEOWNERS file of a given repository

5. Get the maintainers for each team. If the team is a user, it will format the user to match.

6. Iterate through the maintainers and print their username followed by their verified domain email.

```python
import github_api_toolkit as gat
from os import getenv

github_org = getenv("GITHUB_ORG")
pem_contents = getenv("SECRET")
github_app_id = getenv("APP_ID")
github_repo = getenv("GITHUB_REPO")

token = gat.get_token_as_installation(github_org, pem_contents, github_app_id)

api = gat.github_graphql_interface(token[0])

teams = api.get_codeowner_teams(github_org, github_repo)

for team in teams:
    maintainers = api.get_team_maintainers(github_org, team)
    print(f"Team: {team}")
    print("Maintainers:")
    for maintainer in maintainers:
        print(f"{maintainer["login"]} - {api.get_domain_email_by_user(maintainer["login"], getenv("GITHUB_ORG"))}")
```