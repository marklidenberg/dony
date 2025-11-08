from pprint import pprint
from textwrap import dedent

import questionary
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


def echo(
    message: str,
    style: questionary.Style = questionary.Style(
        [
            ("question", "fg:ansiwhite"),
        ]
    ),
) -> None:
    return print_formatted_text(
        FormattedText(
            [
                ("class:question", dedent(message).strip()),
            ]
        ),
        style=style,
    )


def example():
    echo(
        message="""echo "{"a": "b"}\nfoobar""",
    )


if __name__ == "__main__":
    example()
