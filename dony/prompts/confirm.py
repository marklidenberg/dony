from typing import Optional


def confirm(
    message: str,
    default: bool = True,
    provided: Optional[str] = None,
):
    """
    Prompt the user to confirm a decision.
    """

    # NOTE: typing is worse than using arrows, so we'll just use select instead of `questionary.confirm` with [Y/n]

    # - Return provided answer

    if provided is not None:
        if provided.lower() in ["y", "yes", "true", "1"]:
            return True
        elif provided.lower() in ["n", "no", "false", "0"]:
            return False
        else:
            raise ValueError(
                f"Provided answer '{provided}' is not a valid boolean value. Use one of 'y', 'yes', 'true', '1', 'n', 'no', 'false', '0'."
            )

    # - Run select prompt

    from dony.prompts.select import select  # avoid circular import

    answer = select(
        message=message,
        choices=["[Yes]", "No"] if default else ["[No]", "Yes"],
        multi=False,
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
