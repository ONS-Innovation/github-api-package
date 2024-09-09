# `get_codeowner_teams()`

## Overview

Gets the CODEOWNERS file, at the root directory, for a GitHub repository and returns the teams/users listed in the file.

### GraphQL Query

```graphql
query ($org: String!, $repo: String!) {
    repository(owner: $org, name: $repo) {
        file: object(expression: "main:CODEOWNERS") {
            ... on Blob {
                text
            }
        }
    }
}
```

### Example CODEOWNERS file

```
@ONS-Innovation/team-a
@ONS-Innovation/team-b
@user
```

This would return:

```python
["team-a", "team-b", "user"]
```

## Args

### `org`

Type: *String*

The GitHub organisation the repository is kept within.

### `repo`

Type: *String*

The name of the GitHub repository.

## Returns

Type: *List* or *Tuple*

A list of GitHub Teams.

or

A tuple containing a status message and status code (an error).
