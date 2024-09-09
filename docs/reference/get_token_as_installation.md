# `get_token_as_installation()`

Type: *Function*

## Overview
Gets an access token for a GitHub App installed into an organisation. This access token will allow users to make authenticated requests to any GitHub API.

The function follows the process outlined in [GitHub's documentation](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation).

## Args

### `org`

Type: *String*

The GitHub organisation the GitHub App is installed in.

### `pem_contents`

Type: *String*

The contents of the private key file for the GitHub App.

### `app_client_id`

Type: *String*

The GitHub App's Client ID.

## Returns

Type: *Tuple* or *Exception*

A tuple containing the GitHub access token and its expiry time.

or

An exception/error message.

## Process Flow Chart
``` mermaid
graph
  A[Start] --> B[Create a signing key using pem_contents];
  B --> C[Define the JSON web token's payload];
  C --> D[Encode the payload using the signing key and the RS256 algorithm];
  D --> E[Send a Get request to /orgs/*ORG*/installation with the encoded JSON web token];
  E --> F{Did the API return a success status?};
  F -->|Yes| G[Get the GitHub App's installation ID from the request's response];
  G --> H[Send a Post request to /app/installations/*INSTALLATION_ID*/access_tokens];
  H --> I[Return the access token and expiry from the request's response];
  F ---->|No| J[Return Exception];
```