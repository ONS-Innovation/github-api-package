# `make_ql_request()`

## Overview

Makes a request to the GitHub GraphQL API.

## Args

### `query`

Type: *String*

The GraphQL query to be executed.

### `params`

Type: *Dictionary*

The variables to be passed into the query.

## Returns

Type: *Response*

The response from the API.

**Please Note:** This response has not been handled for errors and should be managed by the user.