import os
from pathlib import Path
from typing import Union


def get_donyfiles_path(path: Union[str, Path] = ".") -> Path:
    # - Convert path to Path object

    if isinstance(path, str):
        path = Path(os.path.abspath(path))

    current_path = path

    while True:
        if (current_path / "donyfiles").exists():
            return current_path / "donyfiles"

        current_path = current_path.parent
        if current_path == current_path.parent:
            raise FileNotFoundError("Could not find 'donyfiles' directory")


def example():
    print(get_donyfiles_path(Path.cwd()))


if __name__ == "__main__":
    example()
