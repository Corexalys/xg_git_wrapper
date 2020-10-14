"""
Commandes de "base" git: clone, pull, push...
"""

import re
from subprocess import run

from . import register_command

RE_REPO_NAME = re.compile(r"^.*?/?(?P<repo>[^:/]+?)(?:.git)?/?$")
"""A regex that extracts the repo name from a git URL."""


@register_command("Base", "clone")
def command_clone(url, repo_name=None) -> int:
    """
    Clone un repo.

    Usage:
    xg clone [url]
    ou
    xg clone [url] [destination]
    """
    if repo_name is None:
        match = RE_REPO_NAME.match(url)
        if not match:
            print("Impossible de déterminer le nom du repo.")
            return 1
        repo_name = match["repo"]
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
    """Pousse le contenu du repo local sur le serveur."""
    push = run(["git", "push"])
    return push.returncode


@register_command("Base", "P")
def command_push_force() -> int:
    """Pousse le contenu du repo local sur le serveur. (mode force)"""
    push = run(["git", "push", "--force-with-lease"])
    return push.returncode


@register_command("Base", "s")
def command_status() -> int:
    """Affiche le status de la branche courante."""
    status = run(["git", "status"])
    return status.returncode


@register_command("Base", "a")
def command_add(*fichiers) -> int:
    """
    Ajoute un ou plusieurs fichier aux fichiers "staged".

    Usage:
    xg a [nom_fichier] [nom_fichier] ...
    """
    add = run(["git", "add", "--"] + list(fichiers))
    return add.returncode


@register_command("Base", "A")
def command_add_force(*fichiers) -> int:
    """
    Ajoute un ou plusieurs fichiers aux fichiers "staged". (mode force)

    Usage:
    xg A [nom_fichier] [nom_fichier] ...
    """
    add = run(["git", "add", "--force", "--"] + list(fichiers))
    return add.returncode


@register_command("Base", "d")
def command_diff() -> int:
    """
    Affiche les changements non "staged".

    Usage:
    xg d
    """
    diff = run(["git", "diff"])
    return diff.returncode


@register_command("Base", "ds")
def command_diff_staged() -> int:
    """
    Affiche les changements "staged".

    Usage:
    xg ds
    """
    diff = run(["git", "diff", "--staged"])
    return diff.returncode
