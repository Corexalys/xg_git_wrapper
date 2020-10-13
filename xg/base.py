from typing import List

from . import register_command


@register_command("Base", "clone")
def command_clone(args: List[str]) -> int:
    """Clone a repository."""
    # TODO
    return -1

@register_command("Base", "p")
def command_push(args: List[str]) -> int:
    """Push on the remote."""
    # TODO
    return -1

@register_command("Base", "P")
def command_push_force(args: List[str]) -> int:
    """Push force (with lease) on the remote."""
    # TODO
    return -1
