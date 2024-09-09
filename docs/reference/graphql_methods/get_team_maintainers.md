# `get_team_maintainers()`

## Overview

Gets the users with a maintainer role within a given GitHub team. If a user is passed instead of a team, the method will format the user's name to match the output for the maintainers.

### GraphQL Query

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

## Args

### `org`

Type: *String*

The organisation the team is within.

### `team_name`

Type: *String*

The name of the team to get the maintainers of.

## Returns

Type: *List* or *Tuple*

A List of maintainers.

or

A tuple containing a status message and status code (an error).