from typing import Optional
import questionary
from prompt_toolkit.styles import Style


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
        style=Style(
            [
                ("question", "fg:ansiblue"),  # the question text
            ]
        ),
    ).ask()

    # - Raise KeyboardInterrupt if no result

    if result is None:
        raise KeyboardInterrupt

    # - Return result

    return result


def example():
    print(
        path(
            "Give me that path",
        )
    )


if __name__ == "__main__":
    example()
