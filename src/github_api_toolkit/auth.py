import time

import jwt
import requests


def get_token_as_installation(
    org: str, pem_contents: str, app_client_id: str
) -> tuple | Exception:
    """Get an access token for a GitHub App installed in an organization.

    Generates an encoded JSON Web Token (JWT) using the GitHub app client ID and the private key (pem_contents).
    The JWT is used to get the installation ID of the GitHub App in the organization.
    The installation ID is then used to get an access token for the GitHub App.
    The access token is returned along with the expiration time.

    Args:
        org (str): The GitHub organization name which the GitHub App is installed in.
        pem_contents (str): The contents of the private key file for the GitHub App.
        app_client_id (str): The GitHub App Client ID.

    Returns:
        A tuple containing the access token and the expiration time.
        If an error occurs, an Exception object is returned to be handled by the importing program.
    """

    # Generate JSON Web Token
    issue_time = time.time()
    expiration_time = issue_time + 600

    payload = {
        # Issued at time
        "iat": int(issue_time),
        # Expiration time
        "exp": int(expiration_time),
        # Github App CLient ID
        "iss": app_client_id,
    }

    try:
        encoded_jwt = jwt.encode(payload, pem_contents, algorithm="RS256")
    except jwt.exceptions.InvalidKeyError as err:
        return err

    # Get Installation ID
    header = {"Authorization": f"Bearer {encoded_jwt}"}

    try:
        response = requests.get(
            url=f"https://api.github.com/orgs/{org}/installation", headers=header
        )

        response.raise_for_status()

        installation_json = response.json()
        installation_id = installation_json["id"]

        # Get Access Token
        response = requests.post(
            url=f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers=header,
        )
        response.raise_for_status()
        access_token = response.json()
        return (access_token["token"], access_token["expires_at"])

    except requests.exceptions.HTTPError as errh:
        return errh
    except requests.exceptions.ConnectionError as errc:
        return errc
    except requests.exceptions.Timeout as errt:
        return errt
    except requests.exceptions.RequestException as err:
        return err
