"""
Commandes pour créer et gérer des commits.
"""

import re
from subprocess import run
from typing import Callable, List, Optional

from colorama import Fore, Style

from . import register_command

MessageChecker = Callable[[str], "CheckerResult"]

MESSAGE_CHECKERS: List[MessageChecker] = []

MESSAGE_MIN_LENGTH = 10
MESSAGE_MAX_LENGTH = 50

RE_MESSAGE_SPLIT = re.compile(r"^(?P<prefix>(?:\[.*?\]|.*?:)\s*)?(?P<body>.*)$")


def _register_checker(checker):
    """Register a commit message checker."""
    if checker not in MESSAGE_CHECKERS:
        MESSAGE_CHECKERS.append(checker)
    return checker


class CheckerResult:
    """The result of a message checker."""

    def __init__(self, shown_error: bool, suggestions: Optional[List[str]] = None):
        self.shown_error: bool = shown_error
        self.suggestions: List[str] = suggestions if suggestions is not None else []


def _merge_checker_results(results: List[CheckerResult]) -> CheckerResult:
    """Merge multiple CheckerResults into a single one."""
    shown_error = False
    suggestions = []

    for result in results:
        shown_error = shown_error or result.shown_error
        suggestions.extend(result.suggestions)

    return CheckerResult(shown_error, suggestions)


############
# Commands #
############


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
    print(end=Fore.YELLOW)
    result = _merge_checker_results([checker(message) for checker in MESSAGE_CHECKERS])
    if result.shown_error:
        print(Style.RESET_ALL)

    if result.suggestions:
        print(end=Fore.CYAN)
        print("Voici des suggestions pour améliorer votre commit :")
        for suggestion in result.suggestions:
            print(">", suggestion)
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


############
# Checkers #
############


@_register_checker
def _check_min_length(msg: str) -> bool:
    """Check if the message is at least a certain length."""
    if len(msg) < MESSAGE_MIN_LENGTH:
        print(
            f"Le message de commit semble trop court ({len(msg)}/{MESSAGE_MIN_LENGTH} caractères) !"
        )
        return CheckerResult(True)
    return CheckerResult(False)


@_register_checker
def _check_max_length(msg: str) -> bool:
    """Check if the message is at bellow a certain length."""
    if len(msg) > MESSAGE_MAX_LENGTH:
        print(
            f"Le message de commit est trop long ({len(msg)}/{MESSAGE_MAX_LENGTH} caractères) !"
        )
        return CheckerResult(True)
    return CheckerResult(False)


@_register_checker
def _check_first_letter_uppercase(msg: str) -> bool:
    """Check if the first letter of the message is uppercase."""
    match = RE_MESSAGE_SPLIT.match(msg)
    prefix = match["prefix"] or ""
    body = match["body"] or ""
    if not body[0].isupper():
        print("Le message de commit devrait commencer par une majuscule !")
        suggestion = prefix + body[0].upper() + body[1:]
        return CheckerResult(True, [suggestion])
    return CheckerResult(False)


@_register_checker
def _check_trailing_period(msg: str) -> bool:
    """Check if the last character is a period."""
    if msg[-1] == ".":
        print("Le message de commit ne devrait pas se terminer par un point !")
        return CheckerResult(True, [msg.rstrip(".")])
    return CheckerResult(False)
