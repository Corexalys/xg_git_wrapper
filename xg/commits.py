"""
Commandes pour créer et gérer des commits.
"""

from subprocess import run

from colorama import Fore, Style

from . import register_command


@register_command("Commits", "c")
def command_commit() -> int:
    """
    Crée un commit avec les fichiers "staged".

    Usage:
    xg c
    """
    commit = run(["git", "commit"])
    return commit.returncode


@register_command("Commits", "cm")
def command_commit_message(*words) -> int:
    """
    Crée un commit avec les fichiers staged en précisant le message.

    Usage:
    xg cm Message du commit
    """
    message = " ".join(words)

    # Show some warnings about commit message styling
    warnings_shown = False
    if len(message) > 50:
        print(
            f"{Fore.YELLOW}Un message de commit ne devrait pas dépasser 50 caractères !"
        )
        warnings_shown = True
    if not message[0].isupper():
        print(
            f"{Fore.YELLOW}Un message de commit devrait commencer par une majuscule !"
        )
        warnings_shown = True
    if warnings_shown:
        print(Style.RESET_ALL)

    commit = run(["git", "commit", "-m", message])
    return commit.returncode


@register_command("Commits", "ca")
def command_commit_amend() -> int:
    """
    Modifie le dernier commit.

    Usage:
    xg ca
    """
    commit = run(["git", "commit", "--amend"])
    return commit.returncode


@register_command("Commits", "uc")
def command_uncommit() -> int:
    """
    Annule un commit.

    Met en unstaged les changements apportés par le dernier commit.

    Usage:
    xg uc
    """
    reset = run(["git", "reset", "HEAD~1"])
    return reset.returncode


@register_command("Commits", "rz")
def command_reset(commit) -> int:
    """
    Revient à un commit précédent.

    Met en unstaged les changements apportés par les commits effacés.

    Usage:
    xg rz [hash commit]
    """
    # TODO allow not specifying a commit and showing a pretty selection tui?
    reset = run(["git", "reset", commit])
    return reset.returncode


@register_command("Commits", "RZ")
def command_reset_hard(commit) -> int:
    """
    Revient à un commit précédent. (mode hard)

    EFFACE les changements apportés par les commits effacés.

    Usage:
    xg RZ [hash commit]
    """
    # TODO allow not specifying a commit and showing a pretty selection tui?
    reset = run(["git", "reset", "--hard", commit])
    return reset.returncode


@register_command("Commits", "cp")
def command_cherry_pick(commit) -> int:
    """
    Copie un commit depuis une autre branche dans la branche courante.

    Usage:
    xg cp [hash commit]
    """
    # TODO allow not specifying a commit and showing a pretty selection tui?
    cherry = run(["git", "cherry-pick", commit])
    return cherry.returncode
