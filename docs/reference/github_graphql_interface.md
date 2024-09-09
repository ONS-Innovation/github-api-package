# `github_graphql_interface()`

Type: *Class*

## Overview

A Class used to interact with GitHub's GraphQL API.

## Args

### `token`

Type: *String*

The GitHub access token the class should use to authenticate its API requests.

## Initialisation

When this class is initialised, it creates a `headers` object and defines the URL endpoint the requests should go to. The `headers` object carries the authorisation token for any API requests.

## Methods

### `make_ql_request()`

#### Overview

Makes a request to the GitHub GraphQL API.

#### Args

##### `query`

Type: *String*

The GraphQL query to be executed.

##### `params`

Type: *Dictionary*

The variables to be passed into the query.

#### Returns

Type: *Response*

The response from the API.

**Please Note:** This response has not been handled for errors and should be managed by the user.

### `get_domain_email_by_user()`

#### Overview

Gets a user's verified domain email within an organisation via their GitHub username.

##### GraphQL Query

```graphql
query ($username: String!, $org: String!) {
    user (login: $username) {
        login
        organizationVerifiedDomainEmails(login: $org)
    }
}
```

#### Args

##### `username`

Type: *String*

The GitHub username for the person.

##### `org`

Type: *String*

The GitHub organisation which has the verified domain email.

#### Returns

Type: *List* or *Tuple*

A list of verified domain emails for that user in that organisation.

or

A tuple containing a status message and status code (an error).

### `get_codeowner_teams()`

#### Overview

Gets the CODEOWNERS file, at the root directory, for a GitHub repository and returns the teams/users listed in the file.

##### GraphQL Query

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

##### Example CODEOWNERS file

```
@ONS-Innovation/team-a
@ONS-Innovation/team-b
@user
```

This would return:

```python
["team-a", "team-b", "user"]
```

#### Args

##### `org`

Type: *String*

The GitHub organisation the repository is kept within.

##### `repo`

Type: *String*

The name of the GitHub repository.

#### Returns

Type: *List* or *Tuple*

A list of GitHub Teams.

or

A tuple containing a status message and status code (an error).

### `get_team_maintainers()`

#### Overview

Gets the users with a maintainer role within a given GitHub team. If a user is passed instead of a team, the method will format the user's name to match the output for the maintainers.

##### GraphQL Query

```graphql
query ($org: String!, $team_name: String!) {
    organization(login: $org) {
        team(slug: $team_name) {
            members(role: MAINTAINER) {
                nodes {
                    login
                }
            }
        }
    }
}
```

#### Args

##### `org`

Type: *String*

The organisation the team is within.

##### `team_name`

Type: *String*

The name of the team to get the maintainers of.

#### Returns

Type: *List* or *Tuple*

A List of maintainers.

or

A tuple containing a status message and status code (an error).