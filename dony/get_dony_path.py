from pathlib import Path


def get_dony_path(path: Path) -> Path:
    current_path = Path(path)

    while True:
        candidates = [
            (current_path / "dony_twin"),  # for this exact project, since dony directory is already used
            (current_path / "dony"),
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        current_path = current_path.parent
        if current_path == current_path.parent:
            raise FileNotFoundError("Could not find 'dony' folder")


def example():
    print(get_dony_path(Path.cwd()))


if __name__ == "__main__":
    example()
