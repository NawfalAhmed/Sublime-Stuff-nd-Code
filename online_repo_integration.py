r"""GitHub integration

To use, run the following:
git config --global alias.open '!f() {
    local action="${1:-branch}"
    local target="${2:-HEAD}"
    local target_other="$3"
    local output="$(python3 "$HOME/Sublime/online_repo_integration.py" "$action" "$target" "$target_other")"
    local exit_code=$?

    if [ "$exit_code" -ne 0 ]; then
        echo "${output#"Error: "}"
    fi
    echo "$output"
}; f'


Inspired by:
https://github.com/oobug/SublimeMergeOobug/blob/master/online_repo_integration.py
"""

import os
import re
import sys
import textwrap
import webbrowser
from string import Template
from types import SimpleNamespace


try:
    import requests
    import pyperclip
    import git as gitPython
    from github import Github
    from github.Repository import Repository
except ImportError:
    print("Installing dependencies...")
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gitpython"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyGithub"])
    import requests
    import pyperclip
    import git as gitPython
    from github import Github
    from github.Repository import Repository

# JIRA
USERNAME = "--DUMMY--"
JIRA_DOMAIN = "--DUMMY--"
JIRA_ACCESS_TOKEN = "--DUMMY--"

# GITHUB
REMOTE = "origin"
GITHUB_ACCESS_TOKEN = "--DUMMY--"
BRANCH_TICKET_REGEX = re.compile(r"(sonic|pon)-(\d+)")
COMMIT_PREFIX = re.compile(
    r"^(build|chore|docs|feat|fix|perf|refactor|revert|style|test|temp)(\(.+\))?!?:\s"
)
DEFAULT_REVIEWERS = ["aht007"]

TEMPLATES = {
    "REVIEW_REQUEST": """
        [Review Request]
        Scope: $TICKET_TITLE
        Pull Request: $PR_LINK
        Ticket: $TICKET_LINK

        CC: $REVIEWERS
    """,
    "PR_TITLE": "$TICKET_KEY: $TICKET_TITLE",
    "PR_BODY": """
        ## Description

        $DESCRIPTION

        ## Supporting Information

        Relevant JIRA Ticket: [$TICKET_KEY]($TICKET_LINK)
    """,
    "PR_BODY_WITHOUT_TICKET_INFO": """
        ## Description

        $DESCRIPTION
    """,
}

# Create a namespace of templates for easy access
TEMPLATES = SimpleNamespace(
    **{
        key: Template(textwrap.dedent(value).strip())
        for key, value in TEMPLATES.items()
    }
)


def get_ticket_title(ticket_key: str):
    """Get the title of the ticket"""

    # Create the basic authentication header
    auth = (USERNAME, JIRA_ACCESS_TOKEN)

    # Send the GET request to fetch the ticket details
    response = requests.get(
        f"{JIRA_DOMAIN}/rest/api/latest/issue/{ticket_key}", auth=auth
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the ticket title from the response JSON
        ticket_data = response.json()
        ticket_title = ticket_data["fields"]["summary"].strip()
        ticket_title = re.sub(r"^\[.*\]\s", "", ticket_title)
        return TEMPLATES.PR_TITLE.substitute(
            TICKET_KEY=ticket_key, TICKET_TITLE=ticket_title
        )

    else:
        raise Exception(
            f"Failed to fetch ticket details for {ticket_key}. Status code: {response.status_code}"
        )


def get_pr_description(repo: Repository, branch_name: str, base_branch_name: str):
    title = body = ticket_key = ""

    base_branch = repo.get_branch(base_branch_name)
    branch = repo.get_branch(branch_name)

    # Set Commits to only the commit that are after the base branch commit message
    commits = repo.compare(base_branch.commit.sha, branch.commit.sha).commits

    matchBranch = re.search(BRANCH_TICKET_REGEX, branch_name)

    if matchBranch:
        # If the branch name starts with the branch prefix, use the ticket title
        ticket_key = matchBranch.group(0).upper()
        title = get_ticket_title(ticket_key)
    else:
        # If the branch name does not start with the branch prefix, use the commit title
        title = commits[0].commit.message.split("\n")[0]

    # Set description to be a bullet list of commit messages
    description = "\n".join(
        "- "
        + re.sub(
            COMMIT_PREFIX,
            "",
            commit.commit.message.split("\n")[0],
        )
        for commit in commits
    )

    if ticket_key:
        body = TEMPLATES.PR_BODY.substitute(
            DESCRIPTION=description,
            TICKET_KEY=ticket_key,
            TICKET_LINK=f"{JIRA_DOMAIN}/browse/{ticket_key}",
        )
        review_request = Template(
            TEMPLATES.REVIEW_REQUEST.safe_substitute(
                TICKET_TITLE=title.partition(": ")[-1].strip(),
                TICKET_LINK=f"{JIRA_DOMAIN}/browse/{ticket_key}",
            )
        )
    else:
        body = TEMPLATES.PR_BODY_WITHOUT_TICKET_INFO.substitute(
            DESCRIPTION=description
        )
        review_request = Template(
            TEMPLATES.REVIEW_REQUEST.safe_substitute(
                TICKET_TITLE=title,
                TICKET_LINK="",
            )
        )

    return title, body, review_request


def open_pull_request(repo_name="", branch_name="", base_branch_name="", dry=False):
    """Open a pull request for the given branch"""

    if not repo_name:
        raise Exception("Please provide a repo name")

    if not branch_name:
        raise Exception("Please provide a branch name")

    github = Github(GITHUB_ACCESS_TOKEN)

    # Get the repository
    repo = github.get_repo(repo_name)

    # Get the head and bas refs for the pull request
    head_ref = branch_name
    base_ref = base_branch_name or repo.default_branch

    # Get the pull request details
    pr_title, pr_body, review_request = get_pr_description(repo, head_ref, base_ref)

    # Iterate through the open pull requests in the repository
    for pr in repo.get_pulls(head=f"{repo.owner.login}:{branch_name}", state="all"):
        # If a pull request is found for the branch, open it
        print(f"Pull request already exists: {pr.html_url}")

        *_, review_request = get_pr_description(repo, head_ref, base_ref)
        reviewers = ", ".join(
            f"@{reviewer.login}" for reviewer in pr.get_review_requests()[0]
        )

        pyperclip.copy(review_request.safe_substitute(PR_LINK=pr.html_url, REVIEWERS=reviewers))

        if not dry:
            webbrowser.open(pr.html_url)

        return
    else:
        # If no pull request is found, create a new one
        print("No pull request found. Opening a new one...")

        if dry:
            return

        pr = repo.create_pull(
            title=pr_title, head=head_ref, base=base_ref, body=pr_body
        )
        # Assign the pr to self i.e current user
        pr.add_to_assignees(github.get_user().login)
        # Request reviews from default reviewers
        pr.create_review_request(reviewers=DEFAULT_REVIEWERS)

        print(f"New pull request created: {pr.html_url}")
        pyperclip.copy(review_request.safe_substitute(PR_LINK=pr.html_url))

        webbrowser.open(pr.html_url)


def get_remote_n_target(target: str, git):
    """Get remote and target branch"""

    initial_target = target

    # Get full name (i.e. refs/heads/*; refs/remotes/*/*);
    # src: https://stackoverflow.com/a/9753364
    target = git.rev_parse(target, symbolic_full_name=True)

    if target.startswith("refs/remotes/"):
        # Extract from remote branch reference
        target = target[13:]
    else:
        # Extract from local branch reference
        # src: https://stackoverflow.com/a/9753364
        target = git.for_each_ref(target, format="%(upstream:short)")

    # Split remote/branch
    try:
        remote, target = target.split("/", maxsplit=1)
    except ValueError:
        raise Exception(
            f"Branch ({initial_target}) does not point to a remote repository."
        )

    return remote, target


def get_pr_hash_from_commit(git, commit_hash: str):
    """Get the PR hash from a commit"""

    # get commit message for the commit
    commit_message = git.log("-n", "1", '--pretty=format:"%s"', commit_hash).strip(
        '"'
    )

    # get PR hash from commit message
    matched = re.search(r"\(#(\d+)\)", commit_message)
    if not matched:
        raise Exception(
            f"Commit{commit_hash}: {commit_message} does not refer to any PR."
        )
    pr_hash = matched.group(1)

    return pr_hash


def get_repo_url(git, remote: str):
    """Get the repository URL from remote"""

    repo_url = git.remote("get-url", REMOTE) or ""
    repo_url = re.sub(r"git@(ssh\.)?", r"https://", repo_url)
    repo_url = re.sub(r"(https://)[^/]+@", r"\1", repo_url)
    repo_url = re.sub(r"(\.(com|org|io|ca))\:v\d", r"\1", repo_url)
    repo_url = re.sub(r"(\.(com|org|io|ca))\:", r"\1/", repo_url)
    repo_url = re.sub(r"\.git$", r"", repo_url)

    if not repo_url:
        raise Exception(
            f"Remote ({remote}) does not point to a valid repository URL."
        )

    if "github" not in repo_url.lower():
        raise Exception(f"Remote ({remote}) does not point to a GitHub repository.")

    return repo_url


def open_github_repo_action(action="branch", target="HEAD", target_other=""):
    """Open a GitHub repository action in the browser"""

    git = gitPython.Repo(os.getcwd()).git
    remote = "origin"

    if ("branch" in action or "pr" in action) and "commit" not in action:
        if target_other:
            remote, target_other = get_remote_n_target(target_other, git)
        remote, target = get_remote_n_target(target, git)

    repo_url = get_repo_url(git, remote)

    commit_hash = commit_pr_hash = ""

    if "commit" in action:
        commit_hash = git.rev_parse(target)
        commit_pr_hash = get_pr_hash_from_commit(git, commit_hash)

    if action in ["open_pr", "review_pr"]:
        repo_name = "/".join(repo_url.split("/")[-2:])
        open_pull_request(
            repo_name,
            branch_name=target,
            base_branch_name=target_other,
            dry=action == "review_pr",
        )
        return

    action_to_path_mapping = {
        "commit_pr": f"/pull/{commit_pr_hash}",
        "commit": f"/commit/{commit_hash}",
        "view_prs": f"/pulls?q=is%3Apr++head%3A{target}",
        "pr": f"/compare/{target_other}...{target}?expand=1",
        "tag": f"/releases/tag/{target}",
        "branch": f"/tree/{target}",
    }

    if action not in action_to_path_mapping:
        raise Exception(f"Action ({action}) is not supported.")

    webbrowser.open(repo_url + action_to_path_mapping[action])


if __name__ == "__main__":
    try:
        open_github_repo_action(*sys.argv[1:])
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(100)
