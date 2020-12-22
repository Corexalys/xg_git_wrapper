"""
Commandes de "base" git: clone, pull, push...
"""

from subprocess import run

from . import register_command
from .utils import try_get_repo_name


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
        repo_name = try_get_repo_name(url)
        if repo_name is None:
            return 1
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


@register_command("Base", "pu")
def command_push(remote, branch) -> int:
    """
    Pousse le contenu d'une nouvelle branche sur le serveur.

    Equivalent à `git push -u [remote] [branch]`
    """
    push = run(["git", "push", "-u", remote, branch])
    return push.returncode


@register_command("Base", "s")
def command_status() -> int:
    """Affiche le status de la branche courante."""
    status = run(["git", "status"])
    return status.returncode


@register_command("Base", "pr")
def command_pull_rebase() -> int:
    """
    Met à jour le repo ainsi que tout les submodules.

    Usage:
    xg pr
    """
    pull_rebase = run(["git", "pull", "--rebase"])
    if pull_rebase.returncode != 0:
        return pull_rebase.returncode
    sub_init = run(["git", "submodule", "update", "--init", "--recursive"])
    if sub_init.returncode != 0:
        return sub_init.returncode
    sub_checkout = run(
        ["git", "submodule", "foreach", "--recursive", "git", "checkout", "master"]
    )
    if sub_checkout.returncode != 0:
        return sub_checkout.returncode
    sub_rebase = run(
        ["git", "submodule", "foreach", "--recursive", "git", "pull", "--rebase"]
    )
    return sub_rebase.returncode


@register_command("Base", "a")
def command_add(*fichiers) -> int:
    """
    Ajoute un ou plusieurs fichier aux fichiers "staged".

    Usage:
    xg a [nom_fichier] [nom_fichier] ...
    """
    add = run(["git", "add", "--"] + list(fichiers))
    return add.returncode


@register_command("Base", "ap")
def command_add(*fichiers) -> int:
    """
    Ajoute un ou plusieurs fichier aux fichiers "staged" en mode "patch".

    Cette commande permet de n'ajouter qu'une partie d'un fichier.

    Usage:
    xg ap [nom_fichier] [nom_fichier] ...
    """
    add = run(["git", "add", "--patch", "--"] + list(fichiers))
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


@register_command("Base", "l")
def command_log() -> int:
    """
    Affiche un historique des commits.

    Usage:
    xg l
    """
    log = run(
        ["git", "log", r"--format=%C(auto)%h %Cred%aN %Cblue%ar %C(auto)%d%n    %s%n"]
    )
    return log.returncode


@register_command("Base", "d")
def command_diff(*args) -> int:
    """
    Affiche les changements non "staged".

    Usage:
    xg d
    ou
    xg d [fichier] [fichier] ...
    """
    diff = run(["git", "diff", "--"] + list(args))
    return diff.returncode


@register_command("Base", "ds")
def command_diff_staged(*args) -> int:
    """
    Affiche les changements "staged".

    Usage:
    xg ds
    ou
    xg d [fichier] [fichier] ...
    """
    diff = run(["git", "diff", "--staged", "--"] + list(args))
    return diff.returncode
