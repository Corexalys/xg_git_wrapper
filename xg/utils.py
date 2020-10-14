"""
Some functions used in xg.
"""

import re
from typing import Optional

from colorama import Fore, Style

RE_REPO_NAME = re.compile(r"^.*?/?(?P<repo>[^:/]+?)(?:.git)?/?$")
"""A regex that extracts the repo name from a git URL."""


def try_get_repo_name(url: str) -> Optional[str]:
    """Try to determine a repo's name from it's url."""
    match = RE_REPO_NAME.match(url)
    if not match:
        print(f"{Fore.RED}Impossible de déterminer le nom du repo.{Style.RESET_ALL}")
        return None
    return match["repo"]
