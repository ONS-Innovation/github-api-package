import github_api_toolkit

# This script tests the get_codeowners_from_text function in the github_graphql_interface class.
# The function is used to extract the codeowners from a CODEOWNERS file on GitHub.
# The tests below are used to test the function with different CODEOWNERS file formats.

ql = github_api_toolkit.github_graphql_interface("test_token")

def test_codeowners_format_a():
    codeowners = """
    schemas/* @organisation/team-a @organisation/team-b @organisation/team-c @organisation/team-d
    examples/* @organisation/team-a @organisation/team-b @organisation/team-c @organisation/team-d
    docs/* @organisation/team-a @organisation/team-b @organisation/team-c @organisation/team-d
    mapping/* @organisation/team-a @organisation/team-b @organisation/team-c @organisation/team-d
    """

    excepted_output = [
        "@organisation/team-a",
        "@organisation/team-b",
        "@organisation/team-c",
        "@organisation/team-d"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output

def test_codeowners_format_b():
    codeowners = """
    # EQ API documentation
    docs/electronic_questionnaire_to_data_exchange.rst @organisation/team-a
    docs/jwt_profile.rst @organisation/team-a
    docs/respondent_management_to_electronic_questionnaire.rst @organisation/team-a
    docs/survey_data_exchange_to_respondent_account_services.rst @organisation/team-a
    """

    excepted_output = [
        "@organisation/team-a"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output

def test_codeowners_format_c():
    codeowners = """
    # global owners
    * @organisation/team-a

    # deployment related files
    **app.yaml 
    proxy.config.json @organisation/team-b
    proxy.config.*.json @organisation/team-b
    """

    excepted_output = [
        "@organisation/team-a",
        "@organisation/team-b"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output

def test_codeowners_format_d():
    codeowners = """
    *   @organisation/team-a @organisation/team-b
    """

    excepted_output = [
        "@organisation/team-a",
        "@organisation/team-b"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output

def test_codeowners_format_e():
    codeowners = """
    * @organisation/team-a

    users.yml @organisation/team-a @organisation/team-b
    """

    excepted_output = [
        "@organisation/team-a",
        "@organisation/team-b"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output

def test_codeowners_format_f():
    codeowners = """
    # Global owners - will be requested for review unless a later match takes precedence
    # Keeping terraform files as globally owned - all terraform should be reviewed
    * @organisation/team-a
    """

    excepted_output = [
        "@organisation/team-a"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output

def test_codeowners_format_g():
    codeowners = """
    # You can use a CODEOWNERS file to define individuals or teams that are responsible for code in a repository.
    * @user-a @user-b
    """

    excepted_output = [
        "@user-a",
        "@user-b"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output

def test_codeowners_format_h():
    codeowners = """
    # review when someone opens a pull request.
    *       @organisation/team-a
    """

    excepted_output = [
        "@organisation/team-a"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output

def test_codeowners_format_i():
    codeowners = """
    # review when someone opens a pull request.
    *       @user-a
    *       @user-b
    """

    excepted_output = [
        "@user-a",
        "@user-b"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output

def test_codeowners_format_j():
    codeowners = """
    # This is a comment.
    # Each line is a file pattern followed by one or more owners.

    # These owners will be the default owners for everything in
    # the repo. Unless a later match takes precedence,
    # @global-owner1 and @global-owner2 will be requested for
    # review when someone opens a pull request.
    *       @global-owner1 @global-owner2

    # Order is important; the last matching pattern takes the most
    # precedence. When someone opens a pull request that only
    # modifies JS files, only @js-owner and not the global
    # owner(s) will be requested for a review.
    *.js    @js-owner #This is an inline comment.

    # You can also use email addresses if you prefer. They'll be
    # used to look up users just like we do for commit author
    # emails.
    *.go docs@example.com

    # Teams can be specified as code owners as well. Teams should
    # be identified in the format @org/team-name. Teams must have
    # explicit write access to the repository. In this example,
    # the octocats team in the octo-org organization owns all .txt files.
    *.txt @octo-org/octocats

    # In this example, @doctocat owns any files in the build/logs
    # directory at the root of the repository and any of its
    # subdirectories.
    /build/logs/ @doctocat

    # The `docs/*` pattern will match files like
    # `docs/getting-started.md` but not further nested files like
    # `docs/build-app/troubleshooting.md`.
    docs/*  docs@example.com

    # In this example, @octocat owns any file in an apps directory
    # anywhere in your repository.
    apps/ @octocat

    # In this example, @doctocat owns any file in the `/docs`
    # directory in the root of your repository and any of its
    # subdirectories.
    /docs/ @doctocat

    # In this example, any change inside the `/scripts` directory
    # will require approval from @doctocat or @octocat.
    /scripts/ @doctocat @octocat

    # In this example, @octocat owns any file in a `/logs` directory such as
    # `/build/logs`, `/scripts/logs`, and `/deeply/nested/logs`. Any changes
    # in a `/logs` directory will require approval from @octocat.
    **/logs @octocat

    # In this example, @octocat owns any file in the `/apps`
    # directory in the root of your repository except for the `/apps/github`
    # subdirectory, as its owners are left empty.
    /apps/ @octocat
    /apps/github

    # In this example, @octocat owns any file in the `/apps`
    # directory in the root of your repository except for the `/apps/github`
    # subdirectory, as this subdirectory has its own owner @doctocat
    /apps/ @octocat
    /apps/github @doctocat
    """

    excepted_output = [
        "@global-owner1",
        "@global-owner2",
        "@js-owner",
        "@octo-org/octocats",
        "@doctocat",
        "@octocat"
    ]

    assert ql.get_codeowners_from_text(codeowners) == excepted_output