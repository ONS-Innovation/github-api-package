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

### `handle_response()`

#### Overview
Checks the given response for errors and returns an exception if there are.

#### Args

##### `response`

Type: *Response*

The API response to check for errors.

#### Returns

Type: *Response* or *Exception*

The response given if there are no errors.

or

An exception/error message.

### `get()`

#### Overview

Sends a Get request to a given endpoint.

#### Args

##### `url`

Type: *String*

The url endpoint of the request.

##### `params`

Type: *Dictionary*

The parameters for the query.

##### `add_prefix`

Type: *Boolean*

Whether or not the function should add the *"https://api.github.com"* prefix to the beginning of the passed url.

#### Returns

Type: *Response* or *Exception*

The response from the API endpoint.

or

An exception/error message.

### `patch()`

#### Overview

Sends a Patch request to a given endpoint.

#### Args

##### `url`

Type: *String*

The url endpoint of the request.

##### `params`

Type: *Dictionary*

The parameters for the query.

##### `add_prefix`

Type: *Boolean*

Whether or not the function should add the *"https://api.github.com"* prefix to the beginning of the passed url.

#### Returns

Type: *Response* or *Exception*

The response from the API endpoint.

or

An exception/error message.

### `post()`

#### Overview

Sends a Post request to a given endpoint.

#### Args

##### `url`

Type: *String*

The url endpoint of the request.

##### `params`

Type: *Dictionary*

The parameters for the query.

##### `add_prefix`

Type: *Boolean*

Whether or not the function should add the *"https://api.github.com"* prefix to the beginning of the passed url.

#### Returns

Type: *Response* or *Exception*

The response from the API endpoint.

or

An exception/error message.