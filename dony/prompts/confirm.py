from typing import Optional

from prompt_toolkit.styles import Style


def confirm(
    message: str,
    default: bool = True,
    provided: Optional[bool] = None,
) -> bool:
    """
    Prompt the user to confirm a decision.
    """

    # NOTE: typing is worse than using arrows, so we'll just use select instead of `questionary.confirm` with [Y/n]

    # - Return provided answer

    if provided is not None:
        return provided

    # - Run select prompt

    from dony.prompts.select import select  # avoid circular import

    answer = select(
        message=message,
        choices=["[Yes]", "No"] if default else ["[No]", "Yes"],
        fuzzy=False,
    )

    # - Raise KeyboardInterrupt if no result

    if answer is None:
        raise KeyboardInterrupt

    # - Return result

    return "Yes" in answer


def example():
    print(confirm("Are you sure?"))


if __name__ == "__main__":
    example()
