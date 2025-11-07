from typing import Sequence, Union, Optional

from dony.prompts.choice import Choice
from dony.prompts.select import select
from dony.prompts.input import input


def select_or_input(
    message: str,
    choices: Sequence[Union[str, Choice]],
    default: Optional[str] = None,
    fuzzy: bool = True,
    allow_empty: bool = False,
    reject_choice: str = "Custom",
) -> str:
    """
    Prompt the user to select from a list of choices or enter their own value.

    If the user selects the reject_choice option, they will be prompted to enter
    their own value using the input prompt.
    """

    # - Run select prompt

    result = select(
        message=message,
        choices=list(choices) + [reject_choice],
        default=default,
        fuzzy=fuzzy,
    )

    # - Return if not rejected

    if result != reject_choice:
        return result

    # - Run input prompt otherwise

    return input(
        message=message,
        allow_empty=allow_empty,
    )


def example():
    # Example with strings
    result1 = select_or_input(
        message="What is your name?",
        choices=["Alice", "Bob", "Charlie"],
    )
    print(result1)

    # Example with Choice objects
    result2 = select_or_input(
        message="Select a framework",
        choices=[
            Choice(
                "react", "React", "A JavaScript library for building user interfaces"
            ),
            Choice("vue", "Vue.js", "The Progressive JavaScript Framework"),
            Choice(
                "angular",
                "Angular",
                "Platform for building mobile and desktop web applications",
            ),
        ],
        fuzzy=False,
    )
    print(result2)


if __name__ == "__main__":
    example()
