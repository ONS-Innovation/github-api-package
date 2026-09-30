import re

import requests


class github_graphql_interface:
    """A class used to interact with the GitHub GraphQL API. Has a set range of functions."""

    def __init__(self, token: str) -> None:
        self.headers = {"Authorization": "token " + token}
        self.api_url = "https://api.github.com/graphql"

    def get_error_message(self, response: requests.Response) -> tuple:
        """Gets the error message and status code from a response.

        Args:
            response (requests.Response): The response from the API endpoint.

        Returns:
            tuple: A tuple containing the error message and status code.
        """

        response_json = response.json()
        return response_json.get("message", "No Error Message"), response_json.get(
            "status", "Unknown status"
        )

    def make_ql_request(
        self, query: str, params: dict | None = None
    ) -> requests.Response:
        """Makes a request to the GitHub GraphQL API.

        Args:
            query (str): The GraphQL query to be executed.
            params (dict | None = None): A dictionary containing the variables for the query.

        Returns:
            requests.Response: The response from the API endpoint.
        """

        return requests.post(
            url=self.api_url,
            json={"query": query, "variables": params or {}},
            headers=self.headers,
        )

    def get_domain_email_by_user(self, username: str, org: str) -> list | tuple:
        """Gets a GitHub user's verified domain email for a specific organization.

        Args:
            username (str): The GitHub username of the user.
            org (str): The GitHub organization name.

        Returns:
            list | tuple: A list of verified domain emails for the user in the organization or a tuple containing an error message and status code.
        """

        self.query = """
            query ($username: String!, $org: String!) {
                user (login: $username) {
                    login
                    organizationVerifiedDomainEmails(login: $org)
                }
            }
        """

        self.params = {"username": username, "org": org}

        response = self.make_ql_request(self.query, self.params)

        if response.status_code != 200:
            return self.get_error_message(response)

        response_json = response.json()

        if "errors" in response_json:
            return response_json["errors"][0].get(
                "type", "No Error Type"
            ), response_json["errors"][0].get("message", "No Error Message")

        return response.json()["data"]["user"]["organizationVerifiedDomainEmails"]

    def get_file_contents_from_repo(
        self, owner: str, repo: str, path: str, branch: str = "main"
    ) -> str | tuple:
        """Gets the contents of a file from a GitHub Repository.

        Args:
            owner (str): The owner of the repository.
            repo (str): The repository name.
            path (str): The path to the file.
            branch (str, optional): The branch the file is on. Defaults to "main".

        Returns:
            str | tuple: The contents of the file, or an error message and status code.
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

        self.params = {"owner": owner, "repo": repo}

        response = self.make_ql_request(self.query, self.params)

        if response.status_code != 200:
            return self.get_error_message(response)

        try:
            return response.json()["data"]["repository"]["file"]["text"]
        except TypeError:
            # If there is a type error, ["data"]["repository"]["file"] is None
            # Therefore, the file was not found
            return "File not found."

    def check_directory_for_file(
        self, owner: str, repo: str, path: str, branch: str
    ) -> str | None:
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

        if isinstance(response, str) and response != "File not found.":
            return path

        return None

    def locate_codeowners_file(
        self, owner: str, repo: str, branch: str = "main"
    ) -> str | None:
        """Locates the CODEOWNERS file in a repository.

        The CODEOWNERS file can be located in the root of the repository, in the .github/ directory, or in the docs/ directory.

        Args:
            owner (str): The owner of the repository.
            repo (str): The repository name.
            branch (str, optional): The branch the file is on. Defaults to "main".


        Returns:
            str | None: The path to the file is found or None if the file is not found.
        """

        # Check root directory
        response_codeowners = self.check_directory_for_file(
            owner, repo, "CODEOWNERS", branch
        )

        # Check .github directory
        response_github = self.check_directory_for_file(
            owner, repo, ".github/CODEOWNERS", branch
        )

        # Check docs directory
        response_docs = self.check_directory_for_file(
            owner, repo, "docs/CODEOWNERS", branch
        )

        if response_codeowners:
            return response_codeowners
        elif response_github:
            return response_github
        elif response_docs:
            return response_docs

        return None

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

            if (
                codeowner_lines[i - lines_removed] == ""
                or codeowner_lines[i - lines_removed][0] == "#"
            ):
                codeowner_lines.pop(i - lines_removed)
                lines_removed += 1

            # If line has a comment, remove the comment
            elif "#" in codeowner_lines[i - lines_removed]:
                comment_index = codeowner_lines[i - lines_removed].find("#")
                codeowner_lines[i - lines_removed] = codeowner_lines[i - lines_removed][
                    :comment_index
                ]

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

        email_pattern = r"(@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
        lines_removed = 0

        for i in range(len(codeowner_handles)):
            if len(re.findall(email_pattern, codeowner_handles[i - lines_removed])) > 0:
                codeowner_handles.pop(i - lines_removed)
                lines_removed += 1

        # Remove duplicates
        codeowner_handles = list(dict.fromkeys(codeowner_handles))

        return codeowner_handles

    def identify_teams_and_users(self, codeowners_list: list) -> list:
        """Iterates through a list of users and teams and identifies the type of each.

        Args:
            codeowners_list (list): A list of users and teams from a CODEOWNERS file.

        Returns:
            list: A list of dictionaries containing the type and name of each user and team.
        """

        team_and_user_list = []

        for i in range(len(codeowners_list)):
            if "/" in codeowners_list[i]:
                # This is a team
                # Need to remove org from team name

                codeowners_list[i] = codeowners_list[i].split("/")[-1]
                team_and_user_list.append({"type": "team", "name": codeowners_list[i]})
            else:
                # This is a user

                codeowners_list[i] = codeowners_list[i].replace("@", "")
                team_and_user_list.append({"type": "user", "name": codeowners_list[i]})

        return team_and_user_list

    def get_team_maintainers(self, org: str, team_name: str) -> list | tuple:
        """Gets the maintainers of a GitHub team.

        Args:
            org (str): the GitHub organization name.
            team_name (str): the GitHub team name.

        Returns:
            list | tuple: A list of maintainers in the team or a tuple containing an error message and status code.
        """

        self.query = """
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
        """

        self.params = {"org": org, "team_name": team_name}

        response = self.make_ql_request(self.query, self.params)

        if response.status_code != 200:
            return self.get_error_message(response)

        try:
            return response.json()["data"]["organization"]["team"]["members"]["nodes"]
        except TypeError:
            # If there is a type error, ["data"]["organization"]["team"]["members"]["nodes"] is None
            # Therefore, the team was not found
            # Return an empty list
            return []

    def get_codeowner_users(self, org: str, codeowners: list) -> list:
        """Gets a list of users from a list of users and teams. Will get the maintainers of any teams and add them as a user.

        Args:
            org (str): The GitHub organization name.
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

        emails: list[str] = []

        for codeowner in codeowners:
            user_emails = self.get_domain_email_by_user(codeowner, org)
            emails.extend(user_emails)

        return emails

    def get_repository_email_list(
        self, org: str, repo: str, branch: str = "main"
    ) -> list:
        """Gets a list of verified domain emails for the codeowners of a repository.

        Args:
            org (str): The GitHub organization name.
            repo (str): The GitHub repository name.
            branch (str, optional): The branch to check. Defaults to "main".

        Returns:
            list: A list of verified domain emails for the codeowners of the repository.
        """

        codeowners_path = self.locate_codeowners_file(org, repo, branch)
        if codeowners_path is None:
            return []

        contents = self.get_file_contents_from_repo(org, repo, codeowners_path, branch)
        if isinstance(contents, tuple):
            raise TypeError(f"Expected CODEOWNERS text, got API error: {contents}")

        codeowners = self.get_codeowners_from_text(contents)
        codeowners = self.identify_teams_and_users(codeowners)
        codeowners = self.get_codeowner_users(org, codeowners)
        emails = self.get_codeowner_emails(codeowners, org)

        return emails
