#!/usr/bin/env python3
"""
GitHub Issue Manager - stdlib only implementation
Manages GitHub issues and comments using only Python standard library.
"""

import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from typing import Any


def get_github_token() -> str:
    """Get GitHub token from gh CLI or environment variable."""
    # Try gh CLI first
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True
        )
        token = result.stdout.strip()
        if token:
            return token
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fall back to environment variable
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("Error: No GitHub token found.", file=sys.stderr)
        print("Either install gh CLI and run 'gh auth login', or set GITHUB_TOKEN env var.", file=sys.stderr)
        sys.exit(1)

    return token


def get_repo_info() -> tuple[str, str]:
    """Get repository owner and name from git remote."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()

        # Parse various GitHub URL formats
        # https://github.com/owner/repo.git
        # git@github.com:owner/repo.git
        # https://github.com/owner/repo
        # http://local_proxy@127.0.0.1:54190/git/owner/repo (Claude Code Web)

        if remote_url.startswith("http://local_proxy@127.0.0.1:"):
            # Claude Code Web proxy URL format
            # Extract path after /git/
            if "/git/" in remote_url:
                path = remote_url.split("/git/", 1)[1]
                parts = path.replace(".git", "").split("/")
            else:
                print(f"Error: Unable to parse Claude Code Web proxy URL: {remote_url}", file=sys.stderr)
                sys.exit(1)
        elif remote_url.startswith("https://github.com/"):
            parts = remote_url.replace("https://github.com/", "").replace(".git", "").split("/")
        elif remote_url.startswith("git@github.com:"):
            parts = remote_url.replace("git@github.com:", "").replace(".git", "").split("/")
        else:
            print(f"Error: Unable to parse GitHub remote URL: {remote_url}", file=sys.stderr)
            sys.exit(1)

        if len(parts) != 2:
            print(f"Error: Invalid GitHub remote URL format: {remote_url}", file=sys.stderr)
            sys.exit(1)

        return parts[0], parts[1]

    except subprocess.CalledProcessError as e:
        print(f"Error: Could not get git remote: {e}", file=sys.stderr)
        sys.exit(1)


def github_api_request(
    token: str,
    endpoint: str,
    method: str = "GET",
    data: dict[str, Any] | None = None
) -> Any:
    """Make a request to GitHub API."""
    url = f"https://api.github.com{endpoint}"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    request_data = None
    if data:
        request_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=request_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Error: GitHub API request failed: {e.code} {e.reason}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        sys.exit(1)


def get_issue(token: str, owner: str, repo: str, issue_number: int) -> dict[str, Any]:
    """Get issue details from GitHub."""
    endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}"
    return github_api_request(token, endpoint)


def add_comment(token: str, owner: str, repo: str, issue_number: int, comment: str) -> dict[str, Any]:
    """Add a comment to a GitHub issue."""
    endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/comments"
    data = {"body": comment}
    return github_api_request(token, endpoint, method="POST", data=data)


def list_comments(token: str, owner: str, repo: str, issue_number: int) -> list[dict[str, Any]]:
    """List comments on a GitHub issue."""
    endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/comments"
    return github_api_request(token, endpoint)


def format_issue(issue: dict[str, Any]) -> str:
    """Format issue details for display."""
    output = []
    output.append(f"Issue #{issue['number']}: {issue['title']}")
    output.append(f"State: {issue['state']}")
    output.append(f"Author: {issue['user']['login']}")
    output.append(f"Created: {issue['created_at']}")
    output.append(f"URL: {issue['html_url']}")

    if issue.get("labels"):
        labels = ", ".join(label["name"] for label in issue["labels"])
        output.append(f"Labels: {labels}")

    if issue.get("assignees"):
        assignees = ", ".join(assignee["login"] for assignee in issue["assignees"])
        output.append(f"Assignees: {assignees}")

    output.append("")
    output.append("Description:")
    output.append(issue["body"] or "(No description)")

    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage:", file=sys.stderr)
        print("  gh_issue.py get <issue_number>           - Get issue details", file=sys.stderr)
        print("  gh_issue.py comment <issue_number> <msg> - Add comment to issue", file=sys.stderr)
        print("  gh_issue.py comments <issue_number>      - List issue comments", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    # Get authentication and repo info
    token = get_github_token()
    owner, repo = get_repo_info()

    if command == "get":
        if len(sys.argv) != 3:
            print("Error: get command requires issue number", file=sys.stderr)
            sys.exit(1)

        issue_number = int(sys.argv[2])
        issue = get_issue(token, owner, repo, issue_number)
        print(format_issue(issue))

    elif command == "comment":
        if len(sys.argv) != 4:
            print("Error: comment command requires issue number and message", file=sys.stderr)
            sys.exit(1)

        issue_number = int(sys.argv[2])
        comment_body = sys.argv[3]

        result = add_comment(token, owner, repo, issue_number, comment_body)
        print(f"Comment added: {result['html_url']}")

    elif command == "comments":
        if len(sys.argv) != 3:
            print("Error: comments command requires issue number", file=sys.stderr)
            sys.exit(1)

        issue_number = int(sys.argv[2])
        comments = list_comments(token, owner, repo, issue_number)

        if not comments:
            print("No comments found.")
        else:
            for i, comment in enumerate(comments, 1):
                print(f"\n--- Comment {i} ---")
                print(f"Author: {comment['user']['login']}")
                print(f"Created: {comment['created_at']}")
                print(f"URL: {comment['html_url']}")
                print(f"\n{comment['body']}")

    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
