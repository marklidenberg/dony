from typing import Optional
import questionary


def path(
    message: str,
    provided: Optional[str] = None,
):
    # - Return provided answer

    if provided is not None:
        return provided

    # - Run path prompt

    result = questionary.path(
        message=message,
        qmark="•",
    ).ask()

    # - Raise KeyboardInterrupt if no result

    if result is None:
        raise KeyboardInterrupt


def example():
    print(
        path(
            "Give me that path",
        )
    )


if __name__ == "__main__":
    example()
