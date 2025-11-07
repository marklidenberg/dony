from pathlib import Path


def get_repo_root():
    current_dir = Path(__file__).resolve().parent
    while not (current_dir / ".git").exists():
        if current_dir.parent == current_dir:
            raise ValueError("Repo root not found - no .git directory found")
        current_dir = current_dir.parent

    return current_dir


def test():
    assert get_repo_root().name == "dony"


if __name__ == "__main__":
    test()
