from unittest.mock import Mock, call, patch

import pytest
import requests

import github_api_toolkit


def test_github_interface_requests_and_prefix_options():
    client = github_api_toolkit.github_interface("test-token")
    response = Mock()

    with (
        patch("github_api_toolkit.requests.get", return_value=response) as get,
        patch(
            "github_api_toolkit.requests.patch", return_value=response
        ) as patch_request,
        patch("github_api_toolkit.requests.post", return_value=response) as post,
    ):
        assert client.get("/repos", {"page": 1}) is response
        assert client.get("https://example.test/repos", add_prefix=False) is response
        assert client.patch("/repos/1", {"name": "updated"}) is response
        assert client.patch("/repos/1", add_prefix=False) is response
        assert client.post("/repos", {"name": "new"}) is response
        assert client.post("/repos", add_prefix=False) is response

    assert client.headers == {"Authorization": "token test-token"}
    get.assert_has_calls(
        [
            call(
                url="https://api.github.com/repos",
                headers=client.headers,
                params={"page": 1},
            ),
            call(url="https://example.test/repos", headers=client.headers, params=None),
        ]
    )
    patch_request.assert_has_calls(
        [
            call(
                url="https://api.github.com/repos/1",
                headers=client.headers,
                json={"name": "updated"},
            ),
            call(url="/repos/1", headers=client.headers, json=None),
        ]
    )
    post.assert_has_calls(
        [
            call(
                url="https://api.github.com/repos",
                headers=client.headers,
                json={"name": "new"},
            ),
            call(url="/repos", headers=client.headers, json=None),
        ]
    )


@pytest.mark.parametrize(
    "exception_type",
    [
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException,
    ],
)
def test_github_interface_returns_request_errors(exception_type):
    client = github_api_toolkit.github_interface("test-token")
    response = Mock()
    error = exception_type("request failed")
    response.raise_for_status.side_effect = error

    assert client.handle_response(response) is error
