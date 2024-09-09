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

class github_graphql_interface():
    """A class used to interact with the GitHub GraphQL API. Has a set range of functions.
    """
    
    def __init__(self, token: str) -> None:
        self.headers = { "Authorization": "token " + token }
        self.api_url = "https://api.github.com/graphql"

    def make_ql_request(self, query: str, params: dict) -> requests.Response:
        """Makes a request to the GitHub GraphQL API.

        Args:
            query (str): The GraphQL query to be executed.
            params (dict): A dictionary containing the variables for the query.

        Returns:
            requests.Response: The response from the API endpoint.
        """

        self.json = {
            'query': query,
            'variables': params
        }

        return requests.post(url=self.api_url, json=self.json, headers=self.headers)

    def get_domain_email_by_user(self, username: str, org: str) -> list | tuple:
        """Gets a GitHub user's verified domain email for a specific organization.

        Args:
            username (str): The GitHub username of the user.
            org (str): The GitHub organization name.

        Returns:
            list | tuple: A list of verified domain emails for the user in the organization or a tuple containing an error message and status code.
        """
        
        self.query = '''
            query ($username: String!, $org: String!) {
                user (login: $username) {
                    login
                    organizationVerifiedDomainEmails(login: $org)
                }
            }
        '''

        self.params = {
            'username': username,
            'org': org
        }

        response = self.make_ql_request(self.query, self.params)

        if response.status_code == 200:
            return response.json()["data"]["user"]["organizationVerifiedDomainEmails"]
        else:
            response_json = response.json()
            return response_json["message"], response_json["status"]
        
    def get_codeowner_teams(self, org: str, repo: str) -> list | tuple:
        """Gets the CODEOWNERS file from a GitHub repository and returns the teams listed in the file.

        Args:
            org (str): the GitHub organization name.
            repo (str): the GitHub repository name.

        Returns:
            list | tuple: A list of teams listed in the CODEOWNERS file or a tuple containing an error message and status code.
        """

        self.query = '''
            query ($org: String!, $repo: String!) {
                repository(owner: $org, name: $repo) {
                    file: object(expression: "main:CODEOWNERS") {
                        ... on Blob {
                            text
                        }
                    }
                }
            }
        '''

        self.params = {
            'org': org,
            'repo': repo
        }

        response = self.make_ql_request(self.query, self.params)

        if response.status_code == 200:
            codeowners_contents = response.json()["data"]["repository"]["file"]["text"]

            codeowners = codeowners_contents.split("\n")

            # Remove any empty strings from the list of codeowners

            indexes_removed = 0

            for i in range(0, len(codeowners)):
                if codeowners[i - indexes_removed] == "":
                    codeowners.pop(i - indexes_removed)
                    indexes_removed += 1

            for i in range(len(codeowners)):
                # If the codeowner contains a "/", it is a team and needs to be split from the organisation name.
                # If there is no "/", it is a user and needs to have the @ symbol removed.
                if "/" in codeowners[i]:
                    codeowners[i] = codeowners[i].split("/")[-1]
                else:
                    codeowners[i] = codeowners[i].replace("@", "")

            return codeowners
        else:
            response_json = response.json()
            return response_json["message"], response_json["status"]
        
    def get_team_maintainers(self, org: str, team_name: str) -> list | tuple:
        """Gets the maintainers of a GitHub team.

        Args:
            org (str): the GitHub organization name.
            team_name (str): the GitHub team name.

        Returns:
            list | tuple: A list of maintainers in the team or a tuple containing an error message and status code.
        """

        self.query = '''
            query ($org: String!, $team_name: String!) {
                organization(login: $org) {
                    team(slug: $team_name) {
                        members(role: MAINTAINER) {
                            nodes {
                                login
                            }
                        }
                    }
                }
            }
        '''

        self.params = {
            'org': org,
            'team_name': team_name
        }

        response = self.make_ql_request(self.query, self.params)

        if response.status_code == 200:
            try:
                return response.json()["data"]["organization"]["team"]["members"]["nodes"]
            except TypeError:
                # If the above raises a TypeError, it means that the team_name is not a team, but a user.
                # Therefore we should return the team_name as a list.
                return [{"login": team_name}]
        else:
            response_json = response.json()
            return response_json["message"], response_json["status"]