import questionary
from prompt_toolkit.styles import Style


def input(
    mesdony: str,
    default: str = "",
    allow_empty_string: bool = False,
):
    while True:
        result = questionary.text(
            mesdony,
            default=default,
            qmark="•",
            style=Style(
                [
                    ("question", "fg:ansiblue"),  # the question text
                ]
            ),
        ).ask()

        if allow_empty_string or result:
            return result


def example():
    print(input(mesdony="What is your name?"))


if __name__ == "__main__":
    example()
