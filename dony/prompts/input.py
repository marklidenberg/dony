import questionary
from prompt_toolkit.styles import Style


def input(
    message: str,
    default: str = "",
    allow_empty_string: bool = False,
    provided_answer: str = None,
):
    if provided_answer is not None:
        return provided_answer

    while True:
        result = questionary.text(
            message,
            default=default,
            qmark="•",
            style=Style(
                [
                    ("question", "fg:ansiblue"),  # the question text
                ]
            ),
        ).ask()

        if result is None:
            raise KeyboardInterrupt

        if allow_empty_string or result:
            return result


def example():
    print(input(message="What is your name?"))


if __name__ == "__main__":
    example()
