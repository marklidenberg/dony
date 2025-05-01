import os
from pathlib import Path
from typing import Union


def get_dony_path(path: Union[str, Path] = ".") -> Path:
    # - Convert path to Path object

    if isinstance(path, str):
        path = Path(os.path.abspath(path))

    current_path = path

    while True:
        candidates = [
            (
                current_path / "dony_for_dony"
            ),  # for this exact project, since dony directory is already used
            (current_path / "dony"),
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        current_path = current_path.parent
        if current_path == current_path.parent:
            raise FileNotFoundError("Could not find 'dony' directory")


def example():
    print(get_dony_path(Path.cwd()))


if __name__ == "__main__":
    example()
