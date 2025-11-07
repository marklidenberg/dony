from pathlib import Path
from typing import Optional


def get_git_root(start_path: Optional[Path] = None) -> Path:
    """Get the git root directory.

    Args:
        start_path: Where to start searching. Defaults to current working directory.
    """
    current_dir = start_path.resolve() if start_path else Path.cwd()
    while not (current_dir / ".git").exists():
        if current_dir.parent == current_dir:
            raise ValueError(
                f"Git root not found - no .git directory found starting from {start_path or Path.cwd()}"
            )
        current_dir = current_dir.parent

    return current_dir


def test():
    assert get_git_root().name == "dony"


if __name__ == "__main__":
    test()
