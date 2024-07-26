import jwt
import time
import requests

def get_token_as_installation(org: str, pem_contents: str, app_client_id: str) -> tuple | Exception:
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

    try:
        signing_key = jwt.jwk_from_pem(pem_contents.encode())
    except jwt.exceptions.UnsupportedKeyTypeError as err:
        return(err)

    payload = {
        # Issued at time
        "iat": int(issue_time),
        # Expiration time
        "exp": int(expiration_time),
        # Github App CLient ID
        "iss": app_client_id
    }

    jwt_instance = jwt.JWT()
    encoded_jwt = jwt_instance.encode(payload, signing_key, alg="RS256")

    # Get Installation ID
    header = {"Authorization": f"Bearer {encoded_jwt}"}

    response = requests.get(url=f"https://api.github.com/orgs/{org}/installation", headers=header)
    
    try:
        response = requests.get(url=f"https://api.github.com/orgs/{org}/installation", headers=header)

        response.raise_for_status()

        installation_json = response.json()
        installation_id = installation_json["id"]

        # Get Access Token
        response = requests.post(url=f"https://api.github.com/app/installations/{installation_id}/access_tokens", headers=header)
        access_token = response.json()
        return (access_token["token"], access_token["expires_at"])
    
    except requests.exceptions.HTTPError as errh:
        return(errh)
    except requests.exceptions.ConnectionError as errc:
        return(errc)
    except requests.exceptions.Timeout as errt:
        return(errt)
    except requests.exceptions.RequestException as err:
        return(err)
    

class github_interface():
    """A class used to interact with the Github API.

    The class can perform authenticated get, patch and post requests to the GitHub API using the requests library.
    """

    def __init__(self, token: str) -> None:
        """Creates the header attribute containing the Personal Access token to make auth'd API requests.
        """
        self.headers = {"Authorization": "token " + token}


    def handle_response(self, response: requests.Response) -> requests.Response | Exception:
        """Checks the passed response for errors and returns the response or an Exception object.

        Args:
            response (requests.Response): The response to be checked for errors.

        Returns:
            The response from the API endpoint.
            If an error occurs, an Exception object is returned to be handled by the importing program.
        """

        try:
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as errh:
            return(errh)
        except requests.exceptions.ConnectionError as errc:
            return(errc)
        except requests.exceptions.Timeout as errt:
            return(errt)
        except requests.exceptions.RequestException as err:
            return(err)
        

    def get(self, url: str, params: dict = {}, add_prefix: bool = True) -> requests.Response | Exception:
        """Performs a get request using the passed url.

            Args:
                url (str): The url endpoint of the request.
                params (dict): A Dictionary containing any Query Parameters.
                add_prefix (bool): A Boolean determining whether to add the "https://api.github.com" prefix
                to the beginning of the passed url.

            Returns:
                The response from the API endpoint.
                If an error occurs, an Exception object is returned to be handled by the importing program.
        """
        if add_prefix:
            url = "https://api.github.com" + url
        return self.handle_response(requests.get(url=url, headers=self.headers, params=params))
    
    def patch(self, url: str, params: dict = {}, add_prefix: bool = True) -> requests.Response | Exception:
        """Performs a patch request using the passed url.

            Args:
                url (str): The url endpoint of the request.
                params (dict): A Dictionary containing any Query Parameters.
                add_prefix (bool): A Boolean determining whether to add the "https://api.github.com" prefix
                to the beginning of the passed url.

            Returns:
                The response from the API endpoint.
                If an error occurs, an Exception object is returned to be handled by the importing program.
        """
        if add_prefix:
            url = "https://api.github.com" + url
        return self.handle_response(requests.patch(url=url, headers=self.headers, json=params))
    
    def post(self, url: str, params: dict = {}, add_prefix: bool = True) -> requests.Response | Exception:
        """Performs a post request using the passed url.

            Args:
                url (str): The url endpoint of the request.
                params (dict): A Dictionary containing any Query Parameters.
                add_prefix (bool): A Boolean determining whether to add the "https://api.github.com" prefix
                to the beginning of the passed url.

            Returns:
                The response from the API endpoint.
                If an error occurs, an Exception object is returned to be handled by the importing program.
        """
        if add_prefix:
            url = "https://api.github.com" + url
        return self.handle_response(requests.post(url=url, headers=self.headers, json=params))
