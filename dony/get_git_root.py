from pathlib import Path
from typing import Optional, Union


class NotFoundError(Exception):
    """Raised when a resource is not found."""

    pass


def get_git_root(start_path: Optional[Union[str, Path]] = None) -> Path:
    """Get the git root directory.

    Args:
        start_path: Where to start searching. Defaults to current working directory.

    Raises:
        NotFoundError: If no git root directory is found.
    """
    current_dir = Path(start_path or Path.cwd()).resolve()
    while not (current_dir / ".git").exists():
        if current_dir.parent == current_dir:
            raise NotFoundError(
                f"Git root not found - no .git directory found starting from {start_path or Path.cwd()}"
            )
        current_dir = current_dir.parent

    return current_dir


def test():
    assert get_git_root().name == "dony"


if __name__ == "__main__":
    test()
