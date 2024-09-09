# `github_interface()`

Type: *Class*

## Overview

A Class used to interact with GitHub's RESTful API. Allows the user to send Get, Patch and Post requests.

## Args

### `token`

Type: *String*

The GitHub access token the class should use to authenticate its API requests.

## Initialisation

When this class is initialised, it creates a `headers` object which carries the authorisation token for any API requests.

## Methods

- [`handle_response()` :link:](./rest_methods/handle_response.md)
- [`get()` :link:](./rest_methods/get.md)
- [`patch()` :link:](./rest_methods/patch.md)
- [`post()` :link:](./rest_methods/post.md)