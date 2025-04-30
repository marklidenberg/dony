from typing import Sequence, Union, Optional, List

import questionary
from prompt_toolkit.styles import Style


def autocomplete(
    mesdony: str,
    choices: List[str],
    default: Optional[str] = "",
):
    return questionary.autocomplete(
        mesdony=mesdony,
        choices=choices,
        default=default,
        qmark="•",
        style=Style(
            [
                ("question", "fg:ansiblue"),  # the question text
            ]
        ),
    )


def example():
    print(
        autocomplete(
            "Give me that path",
            choices=["foo", "bar"],
        ).ask()
    )


if __name__ == "__main__":
    example()
