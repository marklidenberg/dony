import questionary
from prompt_toolkit.styles import Style


def confirm(
    message: str,
    default: bool = True,
):
    result = questionary.confirm(
        message=message,
        default=default,
        qmark="",
        auto_enter=False,
        style=Style(
            [
                ("question", "fg:ansiblue"),  # the question text
            ]
        ),
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    return result


def example():
    print(confirm("Are you sure?"))


if __name__ == "__main__":
    example()
