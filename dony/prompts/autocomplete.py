from typing import Optional, List

import questionary
from prompt_toolkit.styles import Style


def autocomplete(
    message: str,
    choices: List[str],
    default: str = "",
    provided: Optional[str] = None,
) -> str:
    # - Return provided answer

    if provided is not None:
        return provided

    # - Ask

    result = questionary.autocomplete(
        message=message,
        choices=choices,
        default=default,
        qmark="",
        style=Style(
            [
                ("question", "fg:ansiblue"),  # the question text
            ]
        ),
    )
    result = result.ask()

    # - Raise KeyboardInterrupt if no result

    if result is None:
        raise KeyboardInterrupt

    # - Return result

    return result


def example():
    print(
        autocomplete(
            "Give me that path",
            choices=["foo", "bar"],
        )
    )


if __name__ == "__main__":
    example()
