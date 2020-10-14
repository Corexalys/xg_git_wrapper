"""
Commandes pour créer et gérer des submodules.
"""

from subprocess import run

from . import register_command

from .utils import try_get_repo_name


@register_command("Submodules", "ma")
def command_submodule_add(url, repo_name=None) -> int:
    """
    Ajoute un submodule.

    Usage:
    xg ma [url]
    ou
    xg ma [url] [destination]
    """
    if repo_name is None:
        repo_name = try_get_repo_name(url)
        if repo_name is None:
            return 1
    submodule = run(["git", "submodule", "add", "-b", "master", url, repo_name])
    if submodule.returncode != 0:
        return submodule.returncode
    add = run(["git", "add", "--", ".gitmodules", repo_name])
    if add.returncode != 0:
        return add.returncode
    checkout = run(["git", "checkout", "master"], cwd=repo_name)
    return checkout.returncode
