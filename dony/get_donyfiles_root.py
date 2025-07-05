import os.path
from pathlib import Path
from typing import Union

from dony.get_donyfiles_path import get_donyfiles_path


def get_donyfiles_root(current_path: Union[str, Path] = ".") -> Path:
    """Find the nearest donyfiles root directory in the path hierarchy."""

    return get_donyfiles_path(current_path).parent


def example():
    print(get_donyfiles_root())


if __name__ == "__main__":
    example()
