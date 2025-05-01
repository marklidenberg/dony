import questionary
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


def error(
    text: str,
):
    return print_formatted_text(
        FormattedText(
            [
                ("class:qmark", "• "),
                ("class:question", text + "\n"),
            ]
        ),
        style=questionary.Style(
            [
                ("question", "fg:ansired"),  # the question text
                ("question", "bold"),  # the question text
            ]
        ),
    )


def example():
    error("Are you sure?")


if __name__ == "__main__":
    example()
