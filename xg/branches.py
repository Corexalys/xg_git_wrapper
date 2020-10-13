from subprocess import run

from . import register_command


@register_command("Branches", "B")
def command_create_branch(branch_name) -> int:
    """
    Crée une branche.

    Usage:
    xg B [nom_de_branche]
    """
    branch = run(["git", "checkout", "-b", branch_name])
    return branch.returncode


@register_command("Branches", "b")
def command_change_branch(branch_name) -> int:
    """
    Change la branche courrante.

    Usage:
    xg b [nom_de_branche]
    """
    checkout = run(["git", "checkout", branch_name])
    return checkout.returncode


@register_command("Branches", "bd")
def command_branch_delete(branch_name) -> int:
    """
    Supprime une branche.

    Usage:
    xg bd [nom_de_branche]
    """
    delete = run(["git", "branch", "-D", branch_name])
    return delete.returncode


@register_command("Branches", "rb")
def command_branch_rebase(branch_target) -> int:
    """
    Rebase la branche courante sur la branche donnée.

    Usage:
    xg rb [nom_de_branche]
    """
    rebase = run(["git", "rebase", branch_target])
    return rebase.returncode
