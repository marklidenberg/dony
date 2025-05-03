import questionary
from prompt_toolkit.styles import Style


def confirm(
    message: str,
    default: bool = True,
    provided_answer: str = None,
):
    if provided_answer is not None:
        if provided_answer.lower() in ["y", "yes", "true", "1"]:
            return True
        elif provided_answer.lower() in ["n", "no", "false", "0"]:
            return False
        else:
            raise ValueError(
                f"Provided answer '{provided_answer}' is not a valid boolean value. Use one of 'y', 'yes', 'true', '1', 'n', 'no', 'false', '0'."
            )

    # typing is worse than using arrows, use select instead for now
    # result = questionary.confirm(
    #     message=message,
    #     default=default,
    #     qmark="",
    #     auto_enter=False,
    #     style=Style(
    #         [
    #             ("question", "fg:ansiblue"),  # the question text
    #         ]
    #     ),
    # ).ask()
    from dony.prompts.select import select  # avoid circular import

    result = (
        select(
            message=message,
            choices=["Yes", "No"] if default else ["No", "Yes"],
            multi=False,
            fuzzy=False,
        )
        == "Yes"
    )

    if result is None:
        raise KeyboardInterrupt

    return result


def example():
    print(confirm("Are you sure?"))


if __name__ == "__main__":
    example()
