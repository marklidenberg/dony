import os.path
from pathlib import Path
from typing import Union

from dony.get_dony_path import get_donyfiles_path


def get_dony_root(current_path: Union[str, Path] = ".") -> Path:
    return get_donyfiles_path(current_path).parent


def example():
    print(get_dony_root())


if __name__ == "__main__":
    example()
