import pickle
import sys
from functools import lru_cache
from typing import Dict

import pkg_resources  # type: ignore


def get_python_version() -> str:
    """Get current Python version."""
    v = sys.version_info
    return f'{v.major}.{v.minor}.{v.micro}'


def get_pickle_version() -> str:
    """Get ``pickle`` package version."""
    return str(pickle.format_version)


def get_self_version() -> str:
    """Get self package version."""
    from scikit_cache import __version__
    return __version__


def get_installed_packages(exclude_self: bool = True) -> Dict[str, str]:
    """Get dict with installed packages.

    :param exclude_self: exclude current package itself from result dict or not
    :return: dict with packages and their versions
    """
    from scikit_cache import __package_name__
    return {
        d.project_name: d.version for d in pkg_resources.working_set
        if not exclude_self or d.project_name != __package_name__
    }


@lru_cache(maxsize=128)
def compare_versions(version_a: str, version_b: str, level: int) -> bool:
    """Compare two string versions with specified level.

    Levels are counted from left to right. Version "12.4.37" means:
        - "12" is level 1
        - "4" is level 2
        - "37" is level 3 and so on

    For example:
        >>> compare_versions('0.2.1', '0.7.1', level=1)
        True
        >>> compare_versions('0.1.2', '0.1.3', level=2)
        True
        >>> compare_versions('0.1.2', '0.1.3', level=3)
        False
    """
    if version_a == version_b:
        return True

    return version_a.split('.')[:level] == version_b.split('.')[:level]  # type: ignore
