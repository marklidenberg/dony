from typing import List


from dony.prompts.select import select
from dony.prompts.input import input


def select_or_input(
    message: str,
    choices: List[str],
    allow_empty_string: bool = False,
    reject_choice: str = "✏️ Enter your own",
    provided_answer: str = None,
):
    if provided_answer is not None:
        return provided_answer

    result = select(
        message=message,
        choices=choices + [reject_choice],
    )

    if result != reject_choice:
        return result

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
