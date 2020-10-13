import re
from subprocess import run
from typing import List

from . import register_command

RE_REPO_NAME = re.compile(r"^.*?/?(?P<repo>[^:/]+?)(?:.git)?/?$")
"""A regex that extracts the repo name from a git URL."""


@register_command("Base", "clone")
def command_clone(url, repo_name=None) -> int:
    """Clone a repository."""
    if repo_name is None:
        repo_name = RE_REPO_NAME.match(url)["repo"]
    clone = run(["git", "clone", "--recurse-submodules", url, repo_name])
    if clone.returncode != 0:
        return clone.returncode
    checkout = run(
        ["git", "submodule", "foreach", "--recursive", "git", "checkout", "master"],
        cwd=repo_name,
    )
    return checkout.returncode


@register_command("Base", "p")
def command_push() -> int:
    """Push on the remote."""
    push = run(["git", "push"])
    return push.returncode


@register_command("Base", "P")
def command_push_force(args: List[str]) -> int:
    """Push force (with lease) on the remote."""
    push = run(["git", "push", "--force-with-lease"])
    return push.returncode


@register_command("Base", "s")
def command_status() -> int:
    """Affiche le status de la branche courante."""
    status = run(["git", "status"])
    return status.returncode
