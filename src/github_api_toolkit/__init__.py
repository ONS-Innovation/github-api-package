from .auth import get_token_as_installation
from .graphql import github_graphql_interface
from .rest import github_interface

__all__ = [
    "get_token_as_installation",
    "github_graphql_interface",
    "github_interface",
]
