import jwt
import time
import requests
import re

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

    def get_error_message(self, response: requests.Response) -> tuple:
        """Gets the error message and status code from a response.

        Args:
            response (requests.Response): The response from the API endpoint.

        Returns:
            tuple: A tuple containing the error message and status code.
        """

        response_json = response.json()
        return response_json.get("message", "No Error Message"), response_json.get("status", "Unknown status")

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
            return self.get_error_message(response)

    def get_file_contents_from_repo(self, owner: str, repo: str, path: str, branch: str = "main") -> str:
        """Gets the contents of a file from a GitHub Repository.

        Args:
            owner (str): The owner of the repository.
            repo (str): The repository name.
            path (str): The path to the file.
            branch (str, optional): The branch the file is on. Defaults to "main".

        Returns:
            str: The contents of the file.
        """

        self.query = f'''
            query ($owner: String!, $repo: String!) {{
                repository(owner: $owner, name: $repo) {{
                    file: object(expression: "{branch}:{path}") {{
                        ... on Blob {{
                            text
                        }}
                    }}
                }}
            }}
        '''

        self.params = {
            'owner': owner,
            'repo': repo
        }

        response = self.make_ql_request(self.query, self.params)

        if response.status_code == 200:
            try:
                contents = response.json()["data"]["repository"]["file"]["text"]
                return contents
            except TypeError:
                # If there is a type error, ["data"]["repository"]["file"] is None
                # Therefore, the file was not found
                return "File not found."
        else:
            return self.get_error_message(response)

    def check_directory_for_file(self, owner: str, repo: str, path: str, branch: str) -> str | None:
        """Checks if a file exists in a repository.

        Args:
            owner (str): The owner of the repository.
            repo (str): The repository name.
            path (str): The path to the file.
            branch (str): The branch the file is on.

        Returns:
            str | None: The path to the file is found or None if the file is not found.
        """

        response = self.get_file_contents_from_repo(owner, repo, path, branch)

        if response != "File not found.":
            return path

        return

    def locate_codeowners_file(self, owner: str, repo: str, branch: str = "main") -> str | None:
        """Locates the CODEOWNERS file in a repository.

        The CODEOWNERS file can be located in the root of the repository, in the .github/ directory, or in the docs/ directory.

        Args:
            owner (str): The owner of the repository.
            repo (str): The repository name.
            branch (str, optional): The branch the file is on. Defaults to "main".


        Returns:
            str | None: The path to the CODEOWNERS file or None if the file is not found.
        """

        # Check root directory
        response_codeowners = self.check_directory_for_file(owner, repo, "CODEOWNERS", branch)

        # Check .github directory
        response_github = self.check_directory_for_file(owner, repo, ".github/CODEOWNERS", branch)

        # Check docs directory
        response_docs = self.check_directory_for_file(owner, repo, "docs/CODEOWNERS", branch)

        if response_codeowners:
            return response_codeowners
        elif response_github:
            return response_github
        elif response_docs:
            return response_docs

        return

    def get_codeowners_from_text(self, codeowners_content: str) -> list:
        """Gets a list of users and teams from a CODEOWNERS file.

        Args:
            codeowners_content (str): The contents of a CODEOWNERS file.

        Returns:
            list: A list of users and teams from the CODEOWNERS file.
        """

        # Process:
        # 1. Split the CODEOWNERS file into lines.
        # 2. Remove empty lines and comments.
        # 3. Find the index of all instances of @ in the lines.
        # 4. Find the index of when the word after the @ ends (i.e. space, end of line).
        # 5. Get the substring from the @ to the end of the word and add to a list.
        # 6. Remove any emails from the list.
        # 7. Remove duplicates from the list.
        # 8. Return the list.

        codeowner_lines = codeowners_content.split("\n")

        lines_removed = 0

        for i in range(len(codeowner_lines)):
            # If line is empty, remove it

            if codeowner_lines[i-lines_removed] == "":
                codeowner_lines.pop(i-lines_removed)
                lines_removed += 1
            
            # If whole line is a comment, remove it
            elif codeowner_lines[i-lines_removed][0] == "#":
                codeowner_lines.pop(i-lines_removed)
                lines_removed += 1

            # If line has a comment, remove the comment
            elif "#" in codeowner_lines[i-lines_removed]:
                comment_index = codeowner_lines[i-lines_removed].find("#")
                codeowner_lines[i-lines_removed] = codeowner_lines[i-lines_removed][:comment_index]

        codeowner_handles = []

        for line in codeowner_lines:
            for i in range(len(line)):
                if line[i] == "@":
                    next_space = line.find(" ", i)
                    if next_space == -1:
                        codeowner_handles.append(line[i:])
                    else:
                        codeowner_handles.append(line[i:next_space])

        # The function will grab the end of the emails (i.e. @example.com)
        # These emails need to be removed from the list of codeowner_handles

        email_pattern = r'(@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'

        lines_removed = 0

        for i in range(len(codeowner_handles)):
            if len(re.findall(email_pattern, codeowner_handles[i-lines_removed])) > 0:
                codeowner_handles.pop(i-lines_removed)
                lines_removed += 1

        # Remove duplicates
        codeowner_handles = list(dict.fromkeys(codeowner_handles))
        
        return codeowner_handles
    
    def identify_teams_and_users(self, codeowners_list: list) -> list:
        """Iterates through a list of users and teams and identifies the type of each.

        Args:
            codeowners_list (list): A list of users and teams from a CODEOWNERS file to sort.

        Returns:
            list: A list of dictionaries containing the type and name of each user and team.
        """

        team_and_user_list = []

        for i in range(len(codeowners_list)):
            if "/" in codeowners_list[i]:
                # This is a team
                # Need to remove org from team name

                codeowners_list[i] = codeowners_list[i].split("/")[-1]

                team_and_user_list.append({
                    "type": "team",
                    "name": codeowners_list[i]
                })
            else:
                # This is a user

                codeowners_list[i] = codeowners_list[i].replace("@", "")

                team_and_user_list.append({
                    "type": "user",
                    "name": codeowners_list[i]
                })

        return team_and_user_list

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
            return response.json()["data"]["organization"]["team"]["members"]["nodes"]
        else:
            return self.get_error_message(response)
        
    def get_codeowner_users(self, org: str, codeowners: list) -> list:
        """Gets a list of users from a list of users and teams. Will get the maintainers of any teams and add them as a user.

        Args:
            codeowners (list): A list of users and teams from a CODEOWNERS file.

        Returns:
            list: A list of users from the CODEOWNERS file.
        """

        users = []

        for codeowner in codeowners:
            if codeowner["type"] == "team":
                team_maintainers = self.get_team_maintainers(org, codeowner["name"])
                
                for maintainer in team_maintainers:
                    users.append(maintainer["login"])

            elif codeowner["type"] == "user":
                users.append(codeowner["name"])

        # Remove duplicates
        users = list(dict.fromkeys(users))

        return users
    
    def get_codeowner_emails(self, codeowners: list, org: str) -> list:
        """Gets a list of verified domain emails for a list of users.

        Args:
            codeowners (list): A list of users from a CODEOWNERS file.
            org (str): The GitHub organization to get the email for.

        Returns:
            list: A list of verified domain emails for the users.
        """
        
        emails = []

        for codeowner in codeowners:
            user_emails = self.get_domain_email_by_user(codeowner, org)

            for email in user_emails:
                emails.append(email)

        return emails
    
    def get_repository_email_list(self, org: str, repo: str, branch: str = "main") -> list:
        """Gets a list of verified domain emails for the codeowners of a repository.

        Args:
            org (str): The GitHub organization name.
            repo (str): The GitHub repository name.
            branch (str, optional): The branch to check. Defaults to "main".

        Returns:
            list: A list of verified domain emails for the codeowners of the repository.
        """

        codeowners_path = self.locate_codeowners_file(org, repo, branch)

        contents = self.get_file_contents_from_repo(org, repo, codeowners_path)

        codeowners = self.get_codeowners_from_text(contents)

        codeowners = self.identify_teams_and_users(codeowners)

        codeowners = self.get_codeowner_users(org, codeowners)

        emails = self.get_codeowner_emails(codeowners, org)

        return emails
