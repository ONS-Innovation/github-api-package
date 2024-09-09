# `post()`

## Overview

Sends a Post request to a given endpoint.

## Args

### `url`

Type: *String*

The url endpoint of the request.

### `params`

Type: *Dictionary*

The parameters for the query.

### `add_prefix`

Type: *Boolean*

Whether or not the function should add the *"https://api.github.com"* prefix to the beginning of the passed url.

## Returns

Type: *Response* or *Exception*

The response from the API endpoint.

or

An exception/error message.