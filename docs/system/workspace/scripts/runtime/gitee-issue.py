#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

from freely_user_env import bootstrap_path_hint as freely_bootstrap_env_path_hint
from freely_user_env import checked_paths_hint as freely_checked_paths_hint
from freely_user_env import default_path_hint as freely_default_env_path_hint
from freely_user_env import path_hint as freely_env_path_hint
from freely_user_env import value as freely_env_value


DEFAULT_API_BASE = "https://gitee.com/api/v5"
COMMAND_NAMES = {"list", "get", "create", "update", "comment", "close", "reopen", "delete-branch"}
DEFAULT_API_TIMEOUT_SECS = 15.0


def detect_repo(explicit_repo: str | None) -> str:
    if explicit_repo:
        return explicit_repo
    try:
        output = subprocess.check_output(
            ["git", "remote", "-v"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"failed to read git remotes: {exc}") from exc
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        match = re.search(r"gitee[^:/]*[:/]([^/\s]+/[^/\s]+?)(?:\.git)?$", parts[1])
        if match:
            return match.group(1)
    raise SystemExit("unable to detect Gitee repo; pass --repo owner/name")


def access_token(required: bool) -> str | None:
    token = freely_env_value("GITEE_ACCESS_TOKEN", "GITEE_TOKEN")
    if required and not token:
        raise SystemExit(
            "missing GITEE_ACCESS_TOKEN/GITEE_TOKEN; checked environment plus "
            f"{freely_checked_paths_hint()}. Put the token in {freely_default_env_path_hint()}, "
            f"or point FREELY_ENV_FILE at a custom credentials file via {freely_bootstrap_env_path_hint()}."
        )
    return token


def body_value(inline: str | None, file_path: str | None) -> str | None:
    if inline is not None and file_path is not None:
        raise SystemExit("pass either inline body text or --body-file, not both")
    if file_path is None:
        return inline
    return Path(file_path).read_text(encoding="utf-8")


def normalize_global_repo_arg(argv: list[str]) -> list[str]:
    if "--repo" not in argv:
        return argv
    command_index = None
    for index, token in enumerate(argv):
        if token in COMMAND_NAMES:
            command_index = index
            break
    if command_index is None:
        return argv
    repo_index = argv.index("--repo")
    if repo_index < command_index:
        return argv
    if repo_index + 1 >= len(argv):
        return argv
    repo_pair = argv[repo_index : repo_index + 2]
    remaining = argv[:repo_index] + argv[repo_index + 2 :]
    return repo_pair + remaining


def request_timeout_secs() -> float:
    raw = os.environ.get("GITEE_API_TIMEOUT_SECS")
    if not raw:
        return DEFAULT_API_TIMEOUT_SECS
    try:
        return float(raw)
    except ValueError:
        raise SystemExit(f"invalid GITEE_API_TIMEOUT_SECS: {raw}")


def encode_query(params: dict[str, object], *, include_empty: bool = False) -> str:
    cooked: list[tuple[str, str]] = []
    for key, value in params.items():
        if value is None:
            continue
        if value == "" and not include_empty:
            continue
        if isinstance(value, (list, tuple)):
            for entry in value:
                cooked.append((key, str(entry)))
        else:
            cooked.append((key, str(value)))
    return urllib.parse.urlencode(cooked, doseq=True)


def api_request(
    *,
    method: str,
    path: str,
    query: dict[str, object] | None = None,
    body: dict[str, object] | None = None,
    auth_required: bool,
) -> object:
    api_base = (os.environ.get("GITEE_API_BASE") or DEFAULT_API_BASE).rstrip("/")
    token = access_token(auth_required)
    query = dict(query or {})
    if token:
        query["access_token"] = token
    url = f"{api_base}{path}"
    encoded_query = encode_query(query)
    if encoded_query:
        url = f"{url}?{encoded_query}"
    payload = None
    headers = {"Accept": "application/json"}
    if body:
        payload = encode_query(body, include_empty=True).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=request_timeout_secs()) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        if exc.code in {401, 404} and not token and path.startswith("/repos/"):
            detail = (
                f"{detail} hint: repo may be private or restricted; set GITEE_ACCESS_TOKEN in "
                f"{freely_env_path_hint()}"
            )
        raise SystemExit(f"{method} {path} failed: HTTP {exc.code}: {detail}") from exc


def repo_path(repo: str, suffix: str = "") -> str:
    """Path for GET operations (list/get) - includes repo name in URL."""
    owner, name = repo.split("/", 1)
    base = f"/repos/{owner}/{name}/issues"
    return f"{base}{suffix}"

def repo_path_post(repo: str, suffix: str = "") -> str:
    """Path for POST/PATCH operations - repo name goes in body."""
    owner, name = repo.split("/", 1)
    base = f"/repos/{owner}/issues"
    return f"{base}{suffix}"

def repo_name(repo: str) -> str:
    return repo.split("/", 1)[1]


def repo_path_branch(repo: str, branch: str) -> str:
    """Path for branch ref operations (DELETE)."""
    owner, name = repo.split("/", 1)
    return f"/repos/{owner}/{name}/git/refs/heads/{branch}"


def cmd_delete_branch(args: argparse.Namespace) -> object:
    repo = detect_repo(args.repo)
    return api_request(
        method="DELETE",
        path=repo_path_branch(repo, args.branch),
        auth_required=True,
    )


def cmd_list(args: argparse.Namespace) -> object:
    repo = detect_repo(args.repo)
    query = {
        "state": args.state,
        "page": args.page,
        "per_page": args.per_page,
        "labels": args.labels,
        "sort": args.sort,
        "direction": args.direction,
    }
    return api_request(method="GET", path=repo_path(repo), query=query, auth_required=False)


def cmd_get(args: argparse.Namespace) -> object:
    repo = detect_repo(args.repo)
    issue = api_request(
        method="GET",
        path=repo_path(repo, f"/{args.number}"),
        auth_required=False,
    )
    # Gitee reports `comments` as a COUNT on the issue resource, while callers
    # (platform-adapter.fetch_issue) expect the comment bodies. Fetch the list so
    # replica reconciliation can compare comments instead of always seeing none.
    if isinstance(issue, dict) and not isinstance(issue.get("comments"), list):
        try:
            comments = api_request(
                method="GET",
                path=repo_path(repo, f"/{args.number}/comments"),
                auth_required=False,
            )
        except Exception:
            comments = []
        issue["comments"] = comments if isinstance(comments, list) else []
    return issue


def cmd_create(args: argparse.Namespace) -> object:
    repo = detect_repo(args.repo)
    body = {
        "repo": repo_name(repo),
        "title": args.title,
        "body": body_value(args.body, args.body_file),
        "assignee": args.assignee,
        "collaborators": args.collaborators,
        "labels": args.labels,
        "milestone": args.milestone,
        "priority": args.priority,
    }
    return api_request(method="POST", path=repo_path_post(repo), body=body, auth_required=True)


def cmd_update(args: argparse.Namespace) -> object:
    repo = detect_repo(args.repo)
    body = {
        "title": args.title,
        "body": body_value(args.body, args.body_file),
        "state": args.state,
        "assignee": args.assignee,
        "collaborators": args.collaborators,
        "labels": args.labels,
        "priority": args.priority,
    }
    return api_request(
        method="PATCH",
        path=repo_path_post(repo, f"/{args.number}"),
        body={**body, "repo": repo_name(repo)},
        auth_required=True,
    )


def cmd_comment(args: argparse.Namespace) -> object:
    repo = detect_repo(args.repo)
    return api_request(
        method="POST",
        path=repo_path(repo, f"/{args.number}/comments"),
        body={"body": body_value(args.body, args.body_file)},
        auth_required=True,
    )


def cmd_close(args: argparse.Namespace) -> object:
    repo = detect_repo(args.repo)
    if args.comment:
        api_request(
            method="POST",
            path=repo_path(repo, f"/{args.number}/comments"),
            body={"body": args.comment},
            auth_required=True,
        )
    return api_request(
        method="PATCH",
        path=repo_path_post(repo, f"/{args.number}"),
        body={"repo": repo_name(repo), "state": "closed"},
        auth_required=True,
    )


def reopen_request(repo: str, number: str) -> tuple[str, dict]:
    """Gitee reopen uses the same legacy path/body shape as close.

    PATCH /repos/{owner}/{repo}/issues/{number} with bare {"state": "open"}
    answers 404 "project or enterprise"; the working form is
    /repos/{owner}/issues/{number} with the repo name in the body.
    """
    return repo_path_post(repo, f"/{number}"), {"repo": repo_name(repo), "state": "open"}


def cmd_reopen(args: argparse.Namespace) -> object:
    repo = detect_repo(args.repo)
    if args.comment:
        api_request(
            method="POST",
            path=repo_path(repo, f"/{args.number}/comments"),
            body={"body": args.comment},
            auth_required=True,
        )
    path, body = reopen_request(repo, args.number)
    return api_request(
        method="PATCH",
        path=path,
        body=body,
        auth_required=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage Gitee issues with the repository inferred from the current git remote or --repo."
    )
    parser.add_argument("--repo", help="owner/name; defaults to the current repo's Gitee remote")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--state", default="open")
    list_parser.add_argument("--labels")
    list_parser.add_argument("--page", type=str, default=1)
    list_parser.add_argument("--per-page", type=str, default=20)
    list_parser.add_argument("--sort")
    list_parser.add_argument("--direction")
    list_parser.set_defaults(func=cmd_list)

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("number", type=str)
    get_parser.set_defaults(func=cmd_get)

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--title", required=True)
    create_parser.add_argument("--body")
    create_parser.add_argument("--body-file")
    create_parser.add_argument("--assignee")
    create_parser.add_argument("--collaborators")
    create_parser.add_argument("--labels")
    create_parser.add_argument("--milestone")
    create_parser.add_argument("--priority")
    create_parser.set_defaults(func=cmd_create)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("number", type=str)
    update_parser.add_argument("--title")
    update_parser.add_argument("--body")
    update_parser.add_argument("--body-file")
    update_parser.add_argument("--state")
    update_parser.add_argument("--assignee")
    update_parser.add_argument("--collaborators")
    update_parser.add_argument("--labels")
    update_parser.add_argument("--priority")
    update_parser.set_defaults(func=cmd_update)

    comment_parser = subparsers.add_parser("comment")
    comment_parser.add_argument("number", type=str)
    comment_parser.add_argument("--body")
    comment_parser.add_argument("--body-file")
    comment_parser.set_defaults(func=cmd_comment)

    close_parser = subparsers.add_parser("close")
    close_parser.add_argument("number")
    close_parser.add_argument("--comment")
    close_parser.set_defaults(func=cmd_close)

    reopen_parser = subparsers.add_parser("reopen")
    reopen_parser.add_argument("number", type=str)
    reopen_parser.add_argument("--comment")
    reopen_parser.set_defaults(func=cmd_reopen)

    delete_branch_parser = subparsers.add_parser("delete-branch")
    delete_branch_parser.add_argument("branch", help="Branch name to delete (e.g. feature/raw-20260514T103532Z-foo)")
    delete_branch_parser.set_defaults(func=cmd_delete_branch)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args(normalize_global_repo_arg(sys.argv[1:]))
    payload = args.func(args)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
