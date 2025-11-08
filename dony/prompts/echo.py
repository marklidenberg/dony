from pprint import pprint
from textwrap import dedent

import questionary
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


def echo(
    text: str,
    style: questionary.Style = questionary.Style(
        [
            ("question", "fg:ansiwhite"),
        ]
    ),
) -> None:
    return print_formatted_text(
        FormattedText(
            [
                ("class:question", dedent(text).strip()),
            ]
        ),
        style=style,
    )


def example():
    echo(
        """echo "{"a": "b"}\nfoobar""",
    )


if __name__ == "__main__":
    example()
