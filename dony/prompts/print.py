from textwrap import dedent

import questionary
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


def print(
    text: str,
    color_style: str = "ansiblue",  # take colors from prompt_toolkit
):
    return print_formatted_text(
        FormattedText(
            [
                ("class:question", dedent(text).strip()),
            ]
        ),
        style=questionary.Style(
            [
                ("question", f"fg:{color_style}"),  # the question text
            ]
        ),
    )


def example():
    print("Are you sure?")


if __name__ == "__main__":
    example()
