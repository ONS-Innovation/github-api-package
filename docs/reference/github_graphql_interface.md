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

- [`make_ql_request()` :link:](./graphql_methods/make_ql_request.md)
- [`get_domain_email_by_user()` :link:](./graphql_methods/get_domain_email_by_user.md)
- [`get_codeowner_teams()` :link:](./graphql_methods/get_codeowner_teams.md)
- [`get_team_maintainers()` :link:](./graphql_methods/get_team_maintainers.md)