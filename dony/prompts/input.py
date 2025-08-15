from typing import Optional
import questionary
from prompt_toolkit.styles import Style


def input(
    message: str,
    default: str = "",
    allow_empty_string: bool = False,
    provided: Optional[str] = None,
    multiline: bool = False,
):
    # - Return provided answer

    if provided is not None:
        return provided

    # - Run input prompt

    while True:
        # - Ask

        result = questionary.text(
            message,
            default=default,
            qmark="•",
            style=Style(
                [
                    ("question", "fg:ansiblue"),  # the question text
                ]
            ),
            multiline=multiline,
        ).ask()

        # - Raise KeyboardInterrupt if no result

        if result is None:
            raise KeyboardInterrupt

        # - Return result

        if allow_empty_string or result:
            return result


def example():
    print(input(message="What is your name?"))


if __name__ == "__main__":
    example()
