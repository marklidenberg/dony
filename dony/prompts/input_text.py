import questionary
from prompt_toolkit.styles import Style


def input_text(
    message: str,
    default: str = "",
    allow_empty: bool = False,
    multiline: bool = False,
) -> str:
    # - Run input prompt

    while True:
        # - Ask

        result = questionary.text(
            message,
            default=default,
            qmark="•",
            style=Style(
                [
                    ("question", "fg:ansiblue"),  # the question text
                ]
            ),
            multiline=multiline,
        ).ask()

        # - Raise KeyboardInterrupt if no result

        if result is None:
            raise KeyboardInterrupt

        # - Return result

        if allow_empty or result:
            return result


def example():
    print(input_text(message="What is your name?"))


if __name__ == "__main__":
    example()
