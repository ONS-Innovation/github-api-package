from unittest.mock import Mock, call, patch

import pytest

import github_api_toolkit


def test_graphql_interface_error_message_and_request_defaults():
    client = github_api_toolkit.github_graphql_interface("test-token")
    assert client.headers == {"Authorization": "token test-token"}
    assert client.get_error_message(Mock(json=Mock(return_value={}))) == (
        "No Error Message",
        "Unknown status",
    )
    assert client.get_error_message(
        Mock(json=Mock(return_value={"message": "denied", "status": "403"}))
    ) == ("denied", "403")

    response = Mock()
    with patch(
        "github_api_toolkit.graphql.requests.post", return_value=response
    ) as post:
        assert client.make_ql_request("query { viewer { login } }") is response
        assert client.make_ql_request("query", {"login": "octocat"}) is response

    post.assert_has_calls(
        [
            call(
                url="https://api.github.com/graphql",
                json={"query": "query { viewer { login } }", "variables": {}},
                headers=client.headers,
            ),
            call(
                url="https://api.github.com/graphql",
                json={"query": "query", "variables": {"login": "octocat"}},
                headers=client.headers,
            ),
        ]
    )


def test_get_domain_email_by_user_success_and_errors():
    client = github_api_toolkit.github_graphql_interface("test-token")
    response = Mock(status_code=200)
    response.json.return_value = {
        "data": {"user": {"organizationVerifiedDomainEmails": ["a@example.com"]}}
    }

    with patch.object(client, "make_ql_request", return_value=response) as request:
        assert client.get_domain_email_by_user("octocat", "example-org") == [
            "a@example.com"
        ]
    assert request.call_args.args[1] == {"username": "octocat", "org": "example-org"}

    response.status_code = 200
    response.json.return_value = {
        "errors": [{"type": "NOT_FOUND", "message": "missing"}]
    }
    with patch.object(client, "make_ql_request", return_value=response):
        assert client.get_domain_email_by_user("unknown", "example-org") == (
            "NOT_FOUND",
            "missing",
        )

    response.json.return_value = {"errors": [{}]}
    with patch.object(client, "make_ql_request", return_value=response):
        assert client.get_domain_email_by_user("unknown", "example-org") == (
            "No Error Type",
            "No Error Message",
        )

    response.status_code = 403
    response.json.return_value = {"message": "denied", "status": "403"}
    with patch.object(client, "make_ql_request", return_value=response):
        assert client.get_domain_email_by_user("octocat", "example-org") == (
            "denied",
            "403",
        )


def test_get_file_contents_from_repo_result_paths():
    client = github_api_toolkit.github_graphql_interface("test-token")
    success = Mock(status_code=200)
    success.json.return_value = {
        "data": {"repository": {"file": {"text": "* @octocat"}}}
    }
    missing = Mock(status_code=200)
    missing.json.return_value = {"data": {"repository": {"file": None}}}
    denied = Mock(status_code=404)
    denied.json.return_value = {"message": "not found", "status": "404"}

    with patch.object(
        client, "make_ql_request", side_effect=[success, missing, denied]
    ):
        assert client.get_file_contents_from_repo("owner", "repo", "CODEOWNERS") == (
            "* @octocat"
        )
        assert client.get_file_contents_from_repo("owner", "repo", "missing") == (
            "File not found."
        )
        assert client.get_file_contents_from_repo("owner", "repo", "private") == (
            "not found",
            "404",
        )


@pytest.mark.parametrize(
    ("contents", "expected"),
    [
        ("* @octocat", "CODEOWNERS"),
        ("File not found.", None),
        (("Not Found", "404"), None),
    ],
)
def test_check_directory_for_file(contents, expected):
    client = github_api_toolkit.github_graphql_interface("test-token")
    with patch.object(client, "get_file_contents_from_repo", return_value=contents):
        assert (
            client.check_directory_for_file("owner", "repo", "CODEOWNERS", "main")
            == expected
        )


@pytest.mark.parametrize(
    ("paths", "expected"),
    [
        (["CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS"], "CODEOWNERS"),
        ([None, ".github/CODEOWNERS", "docs/CODEOWNERS"], ".github/CODEOWNERS"),
        ([None, None, "docs/CODEOWNERS"], "docs/CODEOWNERS"),
        ([None, None, None], None),
    ],
)
def test_locate_codeowners_file(paths, expected):
    client = github_api_toolkit.github_graphql_interface("test-token")
    with patch.object(client, "check_directory_for_file", side_effect=paths):
        assert client.locate_codeowners_file("owner", "repo") == expected


def test_identify_teams_and_users():
    client = github_api_toolkit.github_graphql_interface("test-token")
    assert client.identify_teams_and_users(["@example-org/platform", "@octocat"]) == [
        {"type": "team", "name": "platform"},
        {"type": "user", "name": "octocat"},
    ]


def test_get_team_maintainers_result_paths():
    client = github_api_toolkit.github_graphql_interface("test-token")
    success = Mock(status_code=200)
    success.json.return_value = {
        "data": {
            "organization": {"team": {"members": {"nodes": [{"login": "octocat"}]}}}
        }
    }
    missing = Mock(status_code=200)
    missing.json.return_value = {"data": {"organization": {"team": None}}}
    denied = Mock(status_code=403)
    denied.json.return_value = {"message": "denied", "status": "403"}

    with patch.object(
        client, "make_ql_request", side_effect=[success, missing, denied]
    ):
        assert client.get_team_maintainers("example-org", "platform") == [
            {"login": "octocat"}
        ]
        assert client.get_team_maintainers("example-org", "missing") == []
        assert client.get_team_maintainers("example-org", "private") == (
            "denied",
            "403",
        )


def test_get_codeowner_users_and_emails():
    client = github_api_toolkit.github_graphql_interface("test-token")
    with patch.object(
        client, "get_team_maintainers", return_value=[{"login": "octocat"}]
    ) as maintainers:
        users = client.get_codeowner_users(
            "example-org",
            [
                {"type": "team", "name": "platform"},
                {"type": "user", "name": "octocat"},
                {"type": "user", "name": "hubot"},
            ],
        )
    assert users == ["octocat", "hubot"]
    maintainers.assert_called_once_with("example-org", "platform")

    with patch.object(
        client,
        "get_domain_email_by_user",
        side_effect=[["octocat@example.com"], ["hubot@example.com"]],
    ):
        assert client.get_codeowner_emails(["octocat", "hubot"], "example-org") == [
            "octocat@example.com",
            "hubot@example.com",
        ]


def test_get_repository_email_list_paths():
    client = github_api_toolkit.github_graphql_interface("test-token")
    with patch.object(client, "locate_codeowners_file", return_value=None):
        assert client.get_repository_email_list("owner", "repo") == []

    with (
        patch.object(client, "locate_codeowners_file", return_value="CODEOWNERS"),
        patch.object(
            client, "get_file_contents_from_repo", return_value=("error", 404)
        ),
        pytest.raises(TypeError, match="Expected CODEOWNERS text"),
    ):
        client.get_repository_email_list("owner", "repo")

    with (
        patch.object(client, "locate_codeowners_file", return_value="CODEOWNERS"),
        patch.object(client, "get_file_contents_from_repo", return_value="* @octocat"),
        patch.object(client, "get_codeowners_from_text", return_value=["@octocat"]),
        patch.object(
            client,
            "identify_teams_and_users",
            return_value=[{"type": "user", "name": "octocat"}],
        ),
        patch.object(client, "get_codeowner_users", return_value=["octocat"]),
        patch.object(
            client, "get_codeowner_emails", return_value=["octocat@example.com"]
        ),
    ):
        assert client.get_repository_email_list("owner", "repo") == [
            "octocat@example.com"
        ]
