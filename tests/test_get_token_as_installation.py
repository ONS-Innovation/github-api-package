from unittest.mock import Mock, patch

import jwt
import pytest
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

import github_api_toolkit


def test_get_token_as_installation_signs_with_pyjwt():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem_contents = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    installation_response = Mock()
    installation_response.json.return_value = {"id": 123}
    access_token_response = Mock()
    access_token_response.json.return_value = {
        "token": "installation-token",
        "expires_at": "2026-09-30T12:00:00Z",
    }

    with (
        patch(
            "github_api_toolkit.auth.requests.get", return_value=installation_response
        ) as get_request,
        patch(
            "github_api_toolkit.auth.requests.post",
            return_value=access_token_response,
        ),
    ):
        result = github_api_toolkit.get_token_as_installation(
            "example-org", pem_contents, "client-id"
        )

    assert result == ("installation-token", "2026-09-30T12:00:00Z")
    authorization = get_request.call_args.kwargs["headers"]["Authorization"]
    encoded_jwt = authorization.removeprefix("Bearer ")
    decoded_jwt = jwt.decode(
        encoded_jwt, private_key.public_key(), algorithms=["RS256"]
    )
    assert decoded_jwt["iss"] == "client-id"


def test_get_token_as_installation_returns_invalid_key_error():
    with (
        patch("github_api_toolkit.auth.requests.get") as get_request,
        patch("github_api_toolkit.auth.requests.post") as post_request,
    ):
        result = github_api_toolkit.get_token_as_installation(
            "example-org", "not a valid PEM key", "client-id"
        )

    assert isinstance(result, jwt.exceptions.InvalidKeyError)
    get_request.assert_not_called()
    post_request.assert_not_called()


@pytest.mark.parametrize(
    "exception_type",
    [
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException,
    ],
)
def test_get_token_as_installation_returns_request_errors(exception_type):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem_contents = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    response = Mock()
    error = exception_type("request failed")
    response.raise_for_status.side_effect = error

    with (
        patch("github_api_toolkit.auth.requests.get", return_value=response),
        patch("github_api_toolkit.auth.requests.post") as post_request,
    ):
        result = github_api_toolkit.get_token_as_installation(
            "example-org", pem_contents, "client-id"
        )

    assert result is error
    post_request.assert_not_called()
