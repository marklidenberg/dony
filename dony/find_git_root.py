from pathlib import Path
from typing import Optional, Union


def find_git_root(path: Union[str, Path]) -> Path:
    """Find the git root directory.

    Args:
        path: Where to start searching.

    Raises:
        FileNotFoundError: If no git root directory is found.
    """
    current_dir = Path(path).resolve()
    while not (current_dir / ".git").exists():
        if current_dir.parent == current_dir:
            raise FileNotFoundError(
                f"Git root not found - no .git directory found starting from {path}"
            )
        current_dir = current_dir.parent

    return current_dir


def test():
    assert find_git_root(Path.cwd()).name == "dony"


if __name__ == "__main__":
    test()
