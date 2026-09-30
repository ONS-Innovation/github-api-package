from unittest.mock import Mock, patch

import jwt
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
            "github_api_toolkit.requests.get", return_value=installation_response
        ) as get_request,
        patch("github_api_toolkit.requests.post", return_value=access_token_response),
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
