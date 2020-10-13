"""
Our internal git wrapper.
"""
from typing import Dict, Callable, List, Optional

from wcwidth import wcswidth

COLUMN_SPACING = "    "
COMMANDS: Dict[str, Dict[str, "Command"]] = {}

Command = Callable[[List[str]], int]


def register_command(group, name):
    """Register a command in the command list."""

    def decorator(cmd: Command):
        if group not in COMMANDS:
            COMMANDS[group] = {}
        COMMANDS[group][name] = cmd
        cmd.__cmd_name__ = name
        return cmd

    return decorator


def find_command(name: str) -> Optional[Command]:
    """Return the command matching the given name."""
    for _, commands in COMMANDS.items():
        if name in commands:
            return commands[name]
    return None


def _print_columns(columns: List[List[str]]) -> None:
    """Print columns side by side."""
    column_widths = []
    for col in columns:
        column_widths.append(wcswidth(max(col, key=wcswidth)))

    for row_index in range(len(columns[0])):
        for col_index, col in enumerate(columns):
            value = col[row_index]
            is_last_col = col_index == len(columns) - 1
            padding = " " * (column_widths[col_index] - wcswidth(value))
            if is_last_col:
                print(value)
            else:
                print(f"{value}{padding}", end=COLUMN_SPACING)


def _print_command_list() -> None:
    """Print the registered commands list."""
    print()
    print("Available commands:")
    for group, commands in COMMANDS.items():
        if group:
            print(f"{group}:")
        else:
            print()
        name_column = []
        doc_column = []
        for name, command in commands.items():
            name_column.append(f"  xg {name}")
            doc_column.append(command.__doc__ or "")
        _print_columns([name_column, doc_column])
        print()


def _print_command_help(cmd: Command) -> None:
    """Print the help for a given command."""
    print(cmd.__doc__)


@register_command("", "help")
def command_help(command_name=None) -> int:
    """Print a list of all available commands, or the help for a given one."""
    # No argument given, print list
    if command_name is None:
        _print_command_list()
        return 0
    # Command given as argument, print help if found, otherwise list
    if (command := find_command(command_name)) is not None:
        print()
        print(f"Help for '{command.__cmd_name__}':")
        print()
        _print_command_help(command)
        print()
        return 0
    print(f"Could not find command {command_name}.")
    _print_command_list()
    return 1
