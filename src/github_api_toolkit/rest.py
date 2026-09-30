import requests


class github_interface:
    """A class used to interact with the Github API.

    The class can perform authenticated get, patch and post requests to the GitHub API using the requests library.
    """

    def __init__(self, token: str) -> None:
        """Creates the header attribute containing the Personal Access token to make auth'd API requests."""
        self.headers = {"Authorization": "token " + token}

    def handle_response(
        self, response: requests.Response
    ) -> requests.Response | Exception:
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
            return errh
        except requests.exceptions.ConnectionError as errc:
            return errc
        except requests.exceptions.Timeout as errt:
            return errt
        except requests.exceptions.RequestException as err:
            return err

    def get(
        self, url: str, params: dict | None = None, add_prefix: bool = True
    ) -> requests.Response | Exception:
        """Performs a get request using the passed url.

        Args:
            url (str): The url endpoint of the request.
            params (dict | None = None): A Dictionary containing any Query Parameters.
            add_prefix (bool): A Boolean determining whether to add the "https://api.github.com" prefix
            to the beginning of the passed url.

        Returns:
            The response from the API endpoint.
            If an error occurs, an Exception object is returned to be handled by the importing program.
        """
        if add_prefix:
            url = "https://api.github.com" + url
        return self.handle_response(
            requests.get(url=url, headers=self.headers, params=params)
        )

    def patch(
        self, url: str, params: dict | None = None, add_prefix: bool = True
    ) -> requests.Response | Exception:
        """Performs a patch request using the passed url.

        Args:
            url (str): The url endpoint of the request.
            params (dict | None = None): A Dictionary containing any Query Parameters.
            add_prefix (bool): A Boolean determining whether to add the "https://api.github.com" prefix
            to the beginning of the passed url.

        Returns:
            The response from the API endpoint.
            If an error occurs, an Exception object is returned to be handled by the importing program.
        """
        if add_prefix:
            url = "https://api.github.com" + url
        return self.handle_response(
            requests.patch(url=url, headers=self.headers, json=params)
        )

    def post(
        self, url: str, params: dict | None = None, add_prefix: bool = True
    ) -> requests.Response | Exception:
        """Performs a post request using the passed url.

        Args:
            url (str): The url endpoint of the request.
            params (dict | None = None): A Dictionary containing any Query Parameters.
            add_prefix (bool): A Boolean determining whether to add the "https://api.github.com" prefix
            to the beginning of the passed url.

        Returns:
            The response from the API endpoint.
            If an error occurs, an Exception object is returned to be handled by the importing program.
        """
        if add_prefix:
            url = "https://api.github.com" + url
        return self.handle_response(
            requests.post(url=url, headers=self.headers, json=params)
        )
