# `get_domain_email_by_user()`

## Overview

Gets a user's verified domain email within an organisation via their GitHub username.

### GraphQL Query

```graphql
query ($username: String!, $org: String!) {
    user (login: $username) {
        login
        organizationVerifiedDomainEmails(login: $org)
    }
}
```

## Args

### `username`

Type: *String*

The GitHub username for the person.

### `org`

Type: *String*

The GitHub organisation which has the verified domain email.

## Returns

Type: *List* or *Tuple*

A list of verified domain emails for that user in that organisation.

or

A tuple containing a status message and status code (an error).