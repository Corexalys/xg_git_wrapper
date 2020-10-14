"""
Commandes pour créer et gérer des submodules.
"""

from subprocess import run

from . import register_command

from .base import RE_REPO_NAME


@register_command("Submodules", "ma")
def command_submodule_add(url, repo_name=None) -> int:
    """
    Ajoute un submodule.

    Usage:
    xg ma [url]
    ou
    xg ma [url] [destination]
    """
    # TODO create an helper function to determine the URL.
    if repo_name is None:
        match = RE_REPO_NAME.match(url)
        if not match:
            print("Impossible de déterminer le nom du repo.")
            return 1
        repo_name = match["repo"]
    submodule = run(["git", "submodule", "add", "-b", "master", url, repo_name])
    if submodule.returncode != 0:
        return submodule.returncode
    add = run(["git", "add", "--", ".gitmodules", repo_name])
    if add.returncode != 0:
        return add.returncode
    checkout = run(["git", "checkout", "master"], cwd=repo_name)
    return checkout.returncode
