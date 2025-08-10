from typing import List, Optional


from dony.prompts.select import select
from dony.prompts.input import input


def select_or_input(
    message: str,
    choices: List[str],
    allow_empty_string: bool = False,
    reject_choice: str = "✏️ Enter your own",
    provided: Optional[str] = None,
):
    # - Return provided answer

    if provided is not None:
        return provided

    # - Run select prompt

    result = select(
        message=message,
        choices=choices + [reject_choice],
    )

    # - Return if not rejected

    if result != reject_choice:
        return result

    # - Run input prompt otherwise

    return input(
        message=message,
        allow_empty_string=allow_empty_string,
    )


def example():
    print(
        select_or_input(
            message="What is your name?",
            choices=["Alice", "Bob", "Charlie"],
        )
    )


if __name__ == "__main__":
    example()
