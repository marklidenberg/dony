from typing import Sequence, Union, Optional, List

import questionary
from prompt_toolkit.styles import Style


def autocomplete(
    message: str,
    choices: List[str],
    default: Optional[str] = "",
    provided_answer: str = None,
):
    if provided_answer is not None:
        return provided_answer

    result = questionary.autocomplete(
        message=message,
        choices=choices,
        default=default,
        qmark="•",
        style=Style(
            [
                ("question", "fg:ansiblue"),  # the question text
            ]
        ),
    )

    if result is None:
        raise KeyboardInterrupt


def example():
    print(
        autocomplete(
            "Give me that path",
            choices=["foo", "bar"],
        ).ask()
    )


if __name__ == "__main__":
    example()
